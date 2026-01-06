from PySide6.QtWebEngineCore import QWebEnginePage
from app.ui.settings_html import SETTINGS_HTML


class BrowserPage(QWebEnginePage):
    def __init__(self, profile, webview):
        super().__init__(profile, webview)
        self.webview = webview

    def acceptNavigationRequest(self, url, nav_type, is_main):
        url_str = url.toString()
        print("NAVIGATION:", url_str)

        if url_str == "horaizan://settings":
            self.webview.setHtml(SETTINGS_HTML)
            return False

        return super().acceptNavigationRequest(url, nav_type, is_main)
