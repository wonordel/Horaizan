from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Qt, QUrl
from app.webview import WebView
from app.ui.toolbar import BrowserToolbar
from app.profile import create_profile
from app.settings import Settings
from pathlib import Path
import os



class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Horaizan")
        self.resize(1200, 800)

        self.profile = create_profile()
        self.settings = Settings()

        self.tabs = QTabWidget()
        self.tabs.setCornerWidget(
            self.create_window_controls(),
            Qt.TopRightCorner
        )

        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)

        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.tabs.setCornerWidget(self.create_add_tab_button())

        self.setCentralWidget(self.tabs)

        self.add_tab()
        self.apply_theme()
        
    def create_add_tab_button(self):
        button = QToolButton()
        button.setText("+")
        button.setAutoRaise(True)
        button.clicked.connect(lambda: self.add_tab())
        return button

    def add_tab(self, url: str | None = None):
        if not isinstance(url, str):
            url = "https://www.google.com"

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        webview = WebView(self.profile, self)
        toolbar = BrowserToolbar(webview)

        layout.addWidget(toolbar)
        layout.addWidget(webview)

        index = self.tabs.addTab(container, "New Tab")
        self.tabs.setCurrentIndex(index)

        def on_title_changed(title: str):
            if isinstance(url, str) and url.startswith("horaizan://"):
                self.tabs.setTabText(index, "Настройки")
            else:
                self.tabs.setTabText(index, title if title else "New Tab")

        webview.titleChanged.connect(on_title_changed)

        if url == "horaizan://settings":
            container.is_settings_tab = True
            self.tabs.setTabText(index, "Настройки")

        webview.setUrl(QUrl(url))


    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_settings(self):
        print("OPEN SETTINGS CALLED")
        self.webview.setUrl(QUrl("horaizan://settings"))


 
    def create_window_controls(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(4)

        minimize = QToolButton()
        minimize.setText("—")
        minimize.clicked.connect(self.showMinimized)

        maximize = QToolButton()
        maximize.setText("⬜")
        maximize.clicked.connect(
            lambda: self.showNormal()
            if self.isMaximized()
            else self.showMaximized()
        )

        close = QToolButton()
        close.setText("✕")
        close.clicked.connect(self.close)

        layout.addWidget(minimize)
        layout.addWidget(maximize)
        layout.addWidget(close)

        return widget

    def clear_browser_data(self):
        self.profile.clearHttpCache()
        self.profile.cookieStore().deleteAllCookies()

    def toggle_theme(self, state):
        """
        state приходит от QCheckBox:
        0 = выкл, 2 = вкл
        """
        self.settings.set_dark(bool(state))
        self.apply_theme()

    def apply_theme(self):
        from pathlib import Path

        theme_file = "dark.qss" if self.settings.is_dark() else "light.qss"
        theme_path = Path(__file__).parent / "themes" / theme_file

        try:
            with open(theme_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            pass

    def set_theme(self, theme: str):
        if theme not in ("dark", "light"):
            return

        self.settings.set_theme(theme)

        theme_path = (
            Path(__file__).parent
            / "themes"
            / f"{theme}.qss"
        )

        if not theme_path.exists():
            print("Theme not found:", theme_path)
            return

        with open(theme_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def apply_theme_from_settings(self):
        self.set_theme(self.settings.theme())
