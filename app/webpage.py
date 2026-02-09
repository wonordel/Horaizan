from PySide6.QtWebEngineCore import QWebEnginePage
from app.ui.settings_html import SETTINGS_HTML


class BrowserPage(QWebEnginePage):
    def __init__(self, profile, webview):
        super().__init__(profile, webview)
        self.webview = webview

    def acceptNavigationRequest(self, url, nav_type, is_main):
        if url.toString() == "horaizan://settings":
            self.webview.open_settings_page()
            return False

        return super().acceptNavigationRequest(url, nav_type, is_main)

    def settings_html(self) -> str:
        return SETTINGS_HTML
