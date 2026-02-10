from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl
from PySide6.QtGui import QContextMenuEvent

from app.webpage import BrowserPage
from app.bridge import SettingsBridge

class WebView(QWebEngineView):
    def __init__(self, profile, window):
        super().__init__()
        self.browser_window = window

        self.channel = QWebChannel(self)
        self.bridge = SettingsBridge(window)

        # регистрируем как "bridge"
        self.channel.registerObject("bridge", self.bridge)

        page = BrowserPage(profile, self)
        page.setWebChannel(self.channel)
        self.setPage(page)

    def open_settings_page(self):
        self.setHtml(self.page().settings_html(), QUrl("horaizan://settings"))

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = self.createStandardContextMenu()
        menu.addSeparator()

        inspect_action = menu.addAction("Проверить элемент")
        inspect_action.triggered.connect(lambda: self.browser_window.inspect_element_for_view(self))

        devtools_opened = self.page().devToolsPage() is not None
        devtools_text = "Закрыть DevTools" if devtools_opened else "Открыть DevTools"
        devtools_action = menu.addAction(devtools_text)
        devtools_action.triggered.connect(lambda: self.browser_window.toggle_devtools_for_view(self))

        menu.exec(event.globalPos())
