from PySide6.QtWidgets import QMainWindow,QTabWidget,QWidget,QVBoxLayout,QToolButton
from PySide6.QtCore import Qt,QUrl
from pathlib import Path

from app.webview import WebView
from app.ui.toolbar import BrowserToolbar
from app.profile import create_profile
from app.settings import Settings


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200,800)
        self.settings = Settings()
        self.profile = create_profile()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

        add=QToolButton();add.setText("+")
        add.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(add,Qt.TopRightCorner)

        self.add_tab()
        self.set_theme(self.settings.theme())


    def add_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        view = WebView(self.profile, self)
        toolbar = BrowserToolbar(view, self)

        layout.addWidget(toolbar)
        layout.addWidget(view)

        index = self.tabs.addTab(container, "New Tab")
        self.tabs.setCurrentIndex(index)

        # ✅ ВАЖНО: открываем стартовую страницу выбранного поисковика
        home_url = self.settings.search_engine_home_url()
        view.setUrl(QUrl(home_url))


    def clear_browser_data(self):
        self.profile.clearHttpCache()
        self.profile.cookieStore().deleteAllCookies()

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
