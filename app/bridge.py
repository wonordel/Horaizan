from PySide6.QtCore import QObject, Slot


class SettingsBridge(QObject):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser

    @Slot(result=str)
    def getTheme(self):
        return "dark" if self.browser.settings.is_dark() else "light"

    @Slot(str)
    def setTheme(self, value):
        self.browser.settings.set_dark(value == "dark")
        self.browser.apply_theme()

    @Slot(result=str)
    def getSearchEngine(self):
        return self.browser.settings.search_engine_name()

    @Slot(str)
    def setSearchEngine(self, value):
        self.browser.settings.set_search_engine_name(value)

    @Slot()
    def clearData(self):
        self.browser.clear_browser_data()
