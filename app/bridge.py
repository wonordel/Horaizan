from PySide6.QtCore import QObject, Slot


class SettingsBridge(QObject):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser

    # ===== THEME =====
    @Slot(str)
    def setTheme(self, theme: str):
        """
        theme: 'dark' | 'light'
        """
        print("SET THEME:", theme)
        self.browser.set_theme(theme)

    @Slot(result=str)
    def getTheme(self):
        return self.browser.settings.theme()

    # ===== SEARCH ENGINE =====
    @Slot(str)
    def setSearchEngine(self, value):
        self.browser.settings.set_search_engine_name(value)

    @Slot(result=str)
    def getSearchEngine(self):
        return self.browser.settings.search_engine_name()

    # ===== CLEAR DATA =====
    @Slot()
    def clearData(self):
        print("CLEAR COOKIES + CACHE")

        profile = self.browser.profile
        profile.cookieStore().deleteAllCookies()
        profile.clearHttpCache()

        print("DONE")
