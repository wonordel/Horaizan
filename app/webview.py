from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl


class WebView(QWebEngineView):
    def __init__(self, profile):
        super().__init__()

        page = QWebEnginePage(profile, self)
        self.setPage(page)

        self.setUrl(QUrl("https://www.google.com"))
