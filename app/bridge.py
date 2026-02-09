import json
from PySide6.QtCore import QObject, Slot


class SettingsBridge(QObject):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser

    # ===== THEME =====
    @Slot(str)
    def setTheme(self, theme: str):
        """
        theme: 'dark' | 'light' | 'system'
        """
        print("SET THEME:", theme)
        self.browser.set_theme(theme)

    @Slot(result=str)
    def getTheme(self):
        return self.browser.settings.theme()

    @Slot(result=str)
    def getEffectiveTheme(self):
        return self.browser.effective_theme()

    # ===== SEARCH ENGINE =====
    @Slot(str)
    def setSearchEngine(self, value):
        self.browser.settings.set_search_engine_name(value)

    @Slot(result=str)
    def getSearchEngine(self):
        return self.browser.settings.search_engine_name()

    # ===== NEW TAB =====
    @Slot(str)
    def setNewTabMode(self, mode: str):
        self.browser.settings.set_new_tab_mode(mode)

    @Slot(result=str)
    def getNewTabMode(self):
        return self.browser.settings.new_tab_mode()

    # ===== PRIVACY =====
    @Slot(bool)
    def setConfirmClearData(self, enabled: bool):
        self.browser.settings.set_confirm_clear_data(enabled)

    @Slot(result=bool)
    def getConfirmClearData(self):
        return self.browser.settings.confirm_clear_data()

    # ===== SHORTCUTS =====
    @Slot(result=str)
    def getShortcuts(self):
        return json.dumps(self.browser.settings.shortcuts())

    @Slot(str, str, result=bool)
    def setShortcut(self, action: str, sequence: str):
        return self.browser.set_shortcut(action, sequence)

    @Slot()
    def resetShortcuts(self):
        self.browser.settings.reset_shortcuts()
        self.browser.apply_shortcuts()

    # ===== CLEAR DATA =====
    @Slot()
    def clearData(self):
        print("CLEAR COOKIES + CACHE")

        profile = self.browser.profile
        profile.cookieStore().deleteAllCookies()
        profile.clearHttpCache()

        print("DONE")

    # ===== WINDOW ACTIONS =====
    @Slot()
    def openIncognitoWindow(self):
        self.browser.open_incognito_window()

    # ===== RESET =====
    @Slot()
    def resetSettings(self):
        self.browser.settings.reset_to_defaults()
        self.browser.set_theme(self.browser.settings.theme())
        self.browser.apply_shortcuts()
