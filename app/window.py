from pathlib import Path
import sys

from PySide6.QtCore import Qt, QUrl, QSize, QStandardPaths
from PySide6.QtGui import QKeySequence, QShortcut, QIcon, QCloseEvent
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QToolButton, QApplication
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView

from app.cookies import CookieManagerDialog
from app.downloads import DownloadManagerDialog
from app.history import HistoryManagerDialog
from app.profile import create_profile
from app.settings import Settings
from app.ui.toolbar import BrowserToolbar
from app.webview import WebView


def resolve_theme_path(theme: str) -> Path | None:
    candidates = []
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
        candidates.extend([
            base / "themes" / f"{theme}.qss",
            base / "app" / "themes" / f"{theme}.qss",
        ])
    else:
        base = Path(__file__).resolve().parent
        candidates.extend([
            base / "themes" / f"{theme}.qss",
            base / "app" / "themes" / f"{theme}.qss",
        ])

    for path in candidates:
        if path.exists():
            return path
    return None


class BrowserWindow(QMainWindow):
    _spawned_windows = []

    def __init__(self, incognito: bool = False):
        super().__init__()
        self.incognito = incognito

        app = QApplication.instance()
        if app and not app.windowIcon().isNull():
            self.setWindowIcon(app.windowIcon())

        self.resize(1240, 840)
        self.settings = Settings()
        self.profile = create_profile(incognito=self.incognito, parent=self)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setIconSize(QSize(18, 18))
        self.tabs.tabCloseRequested.connect(self.on_tab_close_requested)
        self.tabs.currentChanged.connect(self._update_window_title)
        self.tabs.currentChanged.connect(lambda _index: self._save_session_tabs())

        tab_bar = self.tabs.tabBar()
        tab_bar.setExpanding(False)
        tab_bar.setElideMode(Qt.ElideRight)

        self.setCentralWidget(self.tabs)

        add = QToolButton()
        add.setObjectName("AddTabButton")
        add.setText("+")
        add.setToolTip("Новая вкладка")
        add.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(add, Qt.TopRightCorner)

        self._shortcuts: dict[str, QShortcut] = {}
        self._reopen_tab_shortcut = QShortcut(QKeySequence("Ctrl+Shift+T"), self)
        self._reopen_tab_shortcut.setContext(Qt.WindowShortcut)
        self._reopen_tab_shortcut.activated.connect(self.reopen_last_closed_tab)
        self._devtools_windows: dict[WebView, QMainWindow] = {}
        self._closed_tabs_stack: list[QUrl] = []
        self.download_manager = DownloadManagerDialog(self)
        self.history_manager = HistoryManagerDialog(self)
        self.cookie_manager = CookieManagerDialog(self.profile.cookieStore(), self)

        self.history_manager.set_open_url_handler(self.open_url_in_current_tab)

        self.profile.downloadRequested.connect(self._on_download_requested)

        if self.incognito or not self._restore_session_tabs():
            self.add_tab()
        self.set_theme(self.settings.theme())
        self.apply_shortcuts()
        self._bind_system_theme_change()
        self._update_window_title()

    def _bind_system_theme_change(self):
        app = QApplication.instance()
        if not app:
            return

        hints = app.styleHints()
        if hasattr(hints, "colorSchemeChanged"):
            hints.colorSchemeChanged.connect(self._on_system_color_scheme_changed)

    def _on_system_color_scheme_changed(self, _scheme):
        if self.settings.theme() == "system":
            self._apply_theme_stylesheet(self.effective_theme())

    def system_theme(self) -> str:
        app = QApplication.instance()
        if not app:
            return "light"

        hints = app.styleHints()
        if not hasattr(hints, "colorScheme") or not hasattr(Qt, "ColorScheme"):
            return "light"

        try:
            scheme = hints.colorScheme()
            if scheme == Qt.ColorScheme.Dark:
                return "dark"
        except Exception:
            return "light"

        return "light"

    def effective_theme(self) -> str:
        theme = self.settings.theme()
        if theme == "system":
            return self.system_theme()
        if theme in ("dark", "light"):
            return theme
        return "dark"

    def _apply_theme_stylesheet(self, theme: str) -> bool:
        theme_path = resolve_theme_path(theme)
        if theme_path is None:
            print(f"Theme not found for '{theme}'")
            return False

        with open(theme_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        return True

    def set_theme(self, theme: str):
        if theme not in ("dark", "light", "system"):
            return False

        self.settings.set_theme(theme)
        return self._apply_theme_stylesheet(self.effective_theme())

    def current_tab_container(self):
        return self.tabs.currentWidget()

    def current_webview(self):
        container = self.current_tab_container()
        if container is None:
            return None
        return getattr(container, "webview", None)

    def current_toolbar(self):
        container = self.current_tab_container()
        if container is None:
            return None
        return getattr(container, "toolbar", None)

    def _tab_index_for_view(self, webview):
        for idx in range(self.tabs.count()):
            container = self.tabs.widget(idx)
            if getattr(container, "webview", None) is webview:
                return idx
        return -1

    def _format_tab_title(self, webview, title: str) -> str:
        clean = (title or "").strip()
        if not clean:
            url = webview.url()
            if url.scheme() == "horaizan":
                clean = "Настройки"
            else:
                clean = url.host() or url.toString() or "Новая вкладка"

        clean = clean.replace("\n", " ").strip()
        if len(clean) > 32:
            return clean[:31] + "…"
        return clean or "Новая вкладка"

    def _update_tab_title(self, webview, title: str = ""):
        idx = self._tab_index_for_view(webview)
        if idx < 0:
            return

        tab_title = self._format_tab_title(webview, title)
        self.tabs.setTabText(idx, tab_title)
        self._update_window_title()

    def _update_tab_icon(self, webview, icon: QIcon):
        idx = self._tab_index_for_view(webview)
        if idx < 0:
            return
        self.tabs.setTabIcon(idx, icon if not icon.isNull() else QIcon())

    def _update_window_title(self, _index: int = -1):
        title = "Horaizan"
        view = self.current_webview()
        if view:
            current_title = self.tabs.tabText(self.tabs.currentIndex())
            if current_title:
                title = f"{current_title} - Horaizan"

        if self.incognito:
            title += " [Инкогнито]"
        self.setWindowTitle(title)

    def add_tab(self, url: QUrl | None = None):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        view = WebView(self.profile, self)
        toolbar = BrowserToolbar(view, self)

        container.webview = view
        container.toolbar = toolbar

        layout.addWidget(toolbar)
        layout.addWidget(view)

        index = self.tabs.addTab(container, "Новая вкладка")
        self.tabs.setCurrentIndex(index)

        view.titleChanged.connect(lambda text, v=view: self._update_tab_title(v, text))
        view.iconChanged.connect(lambda icon, v=view: self._update_tab_icon(v, icon))
        view.urlChanged.connect(lambda _url, v=view: self._update_tab_title(v))
        view.urlChanged.connect(lambda _url: self._save_session_tabs())
        view.loadFinished.connect(lambda ok, v=view: self._record_history_for_view(v, ok))

        if url is not None and url.isValid() and not url.isEmpty():
            view.setUrl(url)
        else:
            mode = self.settings.new_tab_mode()
            if mode == "blank":
                view.setUrl(QUrl("about:blank"))
            else:
                home_url = self.settings.search_engine_home_url()
                view.setUrl(QUrl(home_url))
        self._save_session_tabs()

    def on_tab_close_requested(self, index: int):
        if index < 0:
            return

        container = self.tabs.widget(index)
        if container is not None:
            webview = getattr(container, "webview", None)
            if webview:
                closed_url = webview.url()
                if (
                    closed_url.isValid()
                    and not closed_url.isEmpty()
                    and closed_url.scheme() not in ("about", "horaizan")
                ):
                    self._closed_tabs_stack.append(closed_url)
                self._close_devtools_for_view(webview)

        if self.tabs.count() <= 1:
            self._save_session_tabs()
            self.close()
            return

        self.tabs.removeTab(index)
        self._save_session_tabs()
        self._update_window_title()

    def close_current_tab(self):
        self.on_tab_close_requested(self.tabs.currentIndex())

    def open_settings(self):
        view = self.current_webview()
        if not view:
            return

        view.open_settings_page()
        toolbar = self.current_toolbar()
        if toolbar:
            toolbar.address_bar.setText("Настройки")

    def open_url_in_current_tab(self, url: QUrl):
        view = self.current_webview()
        if not view:
            self.add_tab()
            view = self.current_webview()
        if view:
            view.setUrl(url)
            self._save_session_tabs()

    def reopen_last_closed_tab(self):
        while self._closed_tabs_stack:
            url = self._closed_tabs_stack.pop()
            if not url.isValid() or url.isEmpty():
                continue
            self.add_tab(url=url)
            return

    def _session_urls(self) -> list[str]:
        urls: list[str] = []
        for idx in range(self.tabs.count()):
            container = self.tabs.widget(idx)
            view = getattr(container, "webview", None)
            if view is None:
                continue
            url = view.url()
            if not url.isValid() or url.isEmpty():
                continue
            if url.scheme() in ("about", "horaizan"):
                continue
            urls.append(url.toString())
        return urls

    def _restore_session_tabs(self) -> bool:
        session_tabs = self.settings.session_tabs()
        if not session_tabs:
            return False

        restored = 0
        for tab_url in session_tabs:
            url = QUrl.fromUserInput(tab_url)
            if not url.isValid() or url.isEmpty():
                continue
            self.add_tab(url=url)
            restored += 1
        return restored > 0

    def _save_session_tabs(self):
        if self.incognito:
            return
        self.settings.set_session_tabs(self._session_urls())

    def open_incognito_window(self):
        window = BrowserWindow(incognito=True)
        window.show()
        self.__class__._spawned_windows.append(window)

        def _cleanup(_obj=None, ref=window):
            if ref in self.__class__._spawned_windows:
                self.__class__._spawned_windows.remove(ref)

        window.destroyed.connect(_cleanup)

    def reload_current_page(self):
        view = self.current_webview()
        if view:
            view.reload()

    def go_back(self):
        view = self.current_webview()
        if view:
            view.back()

    def go_forward(self):
        view = self.current_webview()
        if view:
            view.forward()

    def focus_address_bar(self):
        toolbar = self.current_toolbar()
        if not toolbar:
            return
        toolbar.address_bar.setFocus()
        toolbar.address_bar.selectAll()

    def toggle_devtools_for_current(self):
        view = self.current_webview()
        if view:
            self.toggle_devtools_for_view(view)

    def inspect_element_for_view(self, view):
        if not view:
            return
        self.toggle_devtools_for_view(view)
        view.page().triggerAction(QWebEnginePage.WebAction.InspectElement)

    def toggle_devtools_for_view(self, view):
        if not view:
            return

        existing = self._devtools_windows.get(view)
        if existing is not None:
            self._close_devtools_for_view(view)
            return

        devtools_window = QMainWindow(self)
        devtools_window.resize(960, 620)
        devtools_window.setWindowTitle("DevTools - Horaizan")

        devtools_view = QWebEngineView(devtools_window)
        devtools_window.setCentralWidget(devtools_view)

        view.page().setDevToolsPage(devtools_view.page())
        devtools_window.show()

        self._devtools_windows[view] = devtools_window

        def _cleanup(_obj=None, current=view):
            self._close_devtools_for_view(current, silent=True)

        devtools_window.destroyed.connect(_cleanup)

    def _close_devtools_for_view(self, view, silent: bool = False):
        window = self._devtools_windows.pop(view, None)
        if view:
            try:
                view.page().setDevToolsPage(None)
            except RuntimeError:
                pass
        if window and not silent:
            window.close()

    def open_downloads_manager(self):
        self.download_manager.show()
        self.download_manager.raise_()
        self.download_manager.activateWindow()

    def open_history_manager(self):
        self.history_manager.show()
        self.history_manager.raise_()
        self.history_manager.activateWindow()

    def open_cookie_manager(self):
        self.cookie_manager.show()
        self.cookie_manager.raise_()
        self.cookie_manager.activateWindow()

    def _default_download_directory(self) -> str:
        location = QStandardPaths.DownloadLocation
        if hasattr(QStandardPaths, "StandardLocation"):
            location = QStandardPaths.StandardLocation.DownloadLocation
        directory = QStandardPaths.writableLocation(location)
        if directory:
            return directory
        return str(Path.home() / "Downloads")

    def _on_download_requested(self, request):
        directory = self._default_download_directory()
        file_name = request.suggestedFileName() or "download.bin"

        if hasattr(request, "setDownloadDirectory"):
            request.setDownloadDirectory(directory)
        if hasattr(request, "setDownloadFileName"):
            request.setDownloadFileName(file_name)
        if hasattr(request, "setPath"):
            request.setPath(str(Path(directory) / file_name))

        request.accept()
        self.download_manager.register_download(request)
        self.open_downloads_manager()

    def _record_history_for_view(self, view, ok: bool):
        if not ok or self.incognito:
            return
        url = view.url()
        if not url.isValid():
            return
        if url.scheme() in ("about", "horaizan"):
            return
        self.history_manager.add_entry(view.title() or url.toString(), url.toString())

    def clear_browser_data(self):
        self.profile.clearHttpCache()
        self.profile.cookieStore().deleteAllCookies()

    def closeEvent(self, event: QCloseEvent):
        self._save_session_tabs()
        super().closeEvent(event)

    def set_shortcut(self, action: str, sequence: str) -> bool:
        if action not in self.settings.DEFAULT_SHORTCUTS:
            return False

        normalized = QKeySequence(sequence).toString(QKeySequence.PortableText)
        if not normalized:
            return False

        self.settings.set_shortcut(action, normalized)
        self.apply_shortcuts()
        return True

    def apply_shortcuts(self):
        for shortcut in self._shortcuts.values():
            shortcut.setParent(None)
            shortcut.deleteLater()
        self._shortcuts.clear()

        actions = {
            "new_tab": self.add_tab,
            "reopen_closed_tab": self.reopen_last_closed_tab,
            "open_incognito": self.open_incognito_window,
            "close_tab": self.close_current_tab,
            "reload": self.reload_current_page,
            "focus_address": self.focus_address_bar,
            "open_settings": self.open_settings,
            "toggle_devtools": self.toggle_devtools_for_current,
            "open_downloads": self.open_downloads_manager,
            "open_history": self.open_history_manager,
            "open_cookies": self.open_cookie_manager,
            "back": self.go_back,
            "forward": self.go_forward,
        }

        for action, handler in actions.items():
            sequence = self.settings.shortcut(action)
            if not sequence:
                continue

            shortcut = QShortcut(QKeySequence(sequence), self)
            shortcut.setContext(Qt.WindowShortcut)
            shortcut.activated.connect(handler)
            self._shortcuts[action] = shortcut
