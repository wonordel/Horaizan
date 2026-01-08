from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl

from app.webpage import BrowserPage
from app.bridge import SettingsBridge
from app.settings import Settings

class WebView(QWebEngineView):
    def __init__(self, profile, window):
        super().__init__()

        self.channel = QWebChannel(self)
        self.bridge = SettingsBridge(window)

        # регистрируем как "bridge"
        self.channel.registerObject("bridge", self.bridge)

        page = BrowserPage(profile, self)
        page.setWebChannel(self.channel)
        self.setPage(page)
        settings = Settings()
        self.setUrl(QUrl(settings.search_engine_url()))
