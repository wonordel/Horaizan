from PySide6.QtCore import QObject, Slot


class SettingsBridge(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    @Slot()
    def setDarkTheme(self):
        print("DARK THEME")
        self.window.settings.set_theme("dark")
        self.window.set_theme("dark")

    @Slot()
    def setLightTheme(self):
        print("LIGHT THEME")
        self.window.settings.set_theme("light")
        self.window.set_theme("light")


    @Slot(str)
    def setSearchEngine(self, engine):
        print("SEARCH ENGINE:", engine)
        self.window.settings.set_search_engine(engine)


    @Slot()
    def clearData(self):
        print("CLEAR DATA")
        profile = self.window.profile
        profile.cookieStore().deleteAllCookies()
        profile.clearHttpCache()
