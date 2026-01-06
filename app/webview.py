from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl

from app.webpage import BrowserPage
from app.settings_bridge import SettingsBridge


class WebView(QWebEngineView):
    def __init__(self, profile, window):
        super().__init__()

        page = BrowserPage(profile, self)
        self.setPage(page)

        channel = QWebChannel(self)
        channel.registerObject("settings", SettingsBridge(window))
        self.page().setWebChannel(channel)

        self.setUrl(QUrl("https://www.google.com"))
