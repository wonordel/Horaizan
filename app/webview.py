from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl

from app.webpage import BrowserPage
from app.bridge import SettingsBridge


class WebView(QWebEngineView):
    def __init__(self, profile, window):
        super().__init__()

        self.channel = QWebChannel(self)
        self.bridge = SettingsBridge(window)
        self.channel.registerObject("bridge", self.bridge)

        page = BrowserPage(profile, self)
        page.setWebChannel(self.channel)
        self.setPage(page)

        self.setUrl(QUrl("https://www.google.com"))
