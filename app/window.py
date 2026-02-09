from pathlib import Path
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QToolButton, QApplication

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
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.settings = Settings()
        self.profile = create_profile()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

        add = QToolButton()
        add.setText("+")
        add.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(add, Qt.TopRightCorner)

        self._shortcuts: dict[str, QShortcut] = {}

        self.add_tab()
        self.set_theme(self.settings.theme())
        self.apply_shortcuts()
        self._bind_system_theme_change()

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

    def add_tab(self):
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

        index = self.tabs.addTab(container, "New Tab")
        self.tabs.setCurrentIndex(index)

        mode = self.settings.new_tab_mode()
        if mode == "blank":
            view.setUrl(QUrl("about:blank"))
        else:
            home_url = self.settings.search_engine_home_url()
            view.setUrl(QUrl(home_url))

    def close_current_tab(self):
        index = self.tabs.currentIndex()
        if index < 0:
            return

        if self.tabs.count() <= 1:
            self.close()
            return

        self.tabs.removeTab(index)

    def open_settings(self):
        view = self.current_webview()
        if not view:
            return

        view.open_settings_page()
        toolbar = self.current_toolbar()
        if toolbar:
            toolbar.address_bar.setText("Настройки")

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

    def clear_browser_data(self):
        self.profile.clearHttpCache()
        self.profile.cookieStore().deleteAllCookies()

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
            "close_tab": self.close_current_tab,
            "reload": self.reload_current_page,
            "focus_address": self.focus_address_bar,
            "open_settings": self.open_settings,
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
