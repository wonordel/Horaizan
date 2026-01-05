from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolButton
)
from PySide6.QtCore import Qt

from app.webview import WebView
from app.ui.toolbar import BrowserToolbar
from app.profile import create_profile
from app.settings import Settings
from app.ui.settings_page import SettingsPage


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

        menu = self.menuBar().addMenu("Меню")
        settings_action = menu.addAction("Настройки")
        settings_action.triggered.connect(self.open_settings)

        self.add_tab()

    def create_add_tab_button(self):
        button = QToolButton()
        button.setText("+")
        button.setAutoRaise(True)
        button.clicked.connect(self.add_tab)
        return button

    def add_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        webview = WebView(self.profile)
        toolbar = BrowserToolbar(webview)

        layout.addWidget(toolbar)
        layout.addWidget(webview)

        index = self.tabs.addTab(container, "New Tab")
        self.tabs.setCurrentIndex(index)

        webview.titleChanged.connect(
            lambda title: self.tabs.setTabText(index, title[:30])
        )

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self)
        dialog.exec()
 
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
