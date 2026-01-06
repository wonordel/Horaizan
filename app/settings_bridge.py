from PySide6.QtCore import QObject, Slot


class SettingsBridge(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    @Slot(bool)
    def setDarkTheme(self, enabled):
        self.window.set_theme("dark" if enabled else "light")

    @Slot(str)
    def setSearchEngine(self, engine):
        self.window.settings["search_engine"] = engine

    @Slot()
    def clearData(self):
        profile = self.window.profile
        profile.cookieStore().deleteAllCookies()
        profile.clearHttpCache()
