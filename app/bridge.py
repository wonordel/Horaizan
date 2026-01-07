from PySide6.QtCore import QObject, Slot


class SettingsBridge(QObject):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser

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
