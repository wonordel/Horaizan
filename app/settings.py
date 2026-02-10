from PySide6.QtCore import QSettings


class Settings:
    ORGANIZATION = "Horaizan"
    APPLICATION = "Browser"

    DEFAULT_SEARCH_ENGINE = "Google"
    DEFAULT_THEME = "dark"
    DEFAULT_NEW_TAB_MODE = "home"
    DEFAULT_CONFIRM_CLEAR_DATA = True
    DEFAULT_SHORTCUTS = {
        "new_tab": "Ctrl+T",
        "open_incognito": "Ctrl+Shift+N",
        "close_tab": "Ctrl+W",
        "reload": "Ctrl+R",
        "focus_address": "Ctrl+L",
        "open_settings": "Ctrl+,",
        "toggle_devtools": "F12",
        "open_downloads": "Ctrl+J",
        "open_history": "Ctrl+H",
        "open_cookies": "Ctrl+Shift+J",
        "back": "Alt+Left",
        "forward": "Alt+Right",
    }

    SEARCH_ENGINES = {
        "Google": "https://www.google.com/search?q=",
        "Yandex": "https://yandex.ru/search/?text=",
        "Bing": "https://www.bing.com/search?q=",
        "DuckDuckGo": "https://duckduckgo.com/?q=",
    }

    SEARCH_ENGINE_HOME = {
        "Google": "https://www.google.com/",
        "Yandex": "https://ya.ru/",
        "Bing": "https://www.bing.com/",
        "DuckDuckGo": "https://duckduckgo.com/",
    }

    def __init__(self):
        self._settings = QSettings(
            self.ORGANIZATION,
            self.APPLICATION
        )

    # ======================
    # THEME
    # ======================

    def theme(self) -> str:
        return self._settings.value(
            "theme",
            self.DEFAULT_THEME,
            type=str
        )

    def set_theme(self, theme: str):
        if theme in ("dark", "light", "system"):
            self._settings.setValue("theme", theme)

    def is_dark(self) -> bool:
        return self.theme() == "dark"

    # ======================
    # NEW TAB
    # ======================

    def new_tab_mode(self) -> str:
        return self._settings.value(
            "new_tab_mode",
            self.DEFAULT_NEW_TAB_MODE,
            type=str
        )

    def set_new_tab_mode(self, mode: str):
        if mode in ("home", "blank"):
            self._settings.setValue("new_tab_mode", mode)

    # ======================
    # PRIVACY
    # ======================

    def confirm_clear_data(self) -> bool:
        return self._settings.value(
            "confirm_clear_data",
            self.DEFAULT_CONFIRM_CLEAR_DATA,
            type=bool
        )

    def set_confirm_clear_data(self, value: bool):
        self._settings.setValue("confirm_clear_data", bool(value))

    # ======================
    # SHORTCUTS
    # ======================

    def shortcut(self, action: str) -> str:
        default = self.DEFAULT_SHORTCUTS.get(action, "")
        return self._settings.value(
            f"shortcut/{action}",
            default,
            type=str
        )

    def set_shortcut(self, action: str, sequence: str):
        if action not in self.DEFAULT_SHORTCUTS:
            return
        self._settings.setValue(f"shortcut/{action}", sequence)

    def shortcuts(self) -> dict:
        return {
            action: self.shortcut(action)
            for action in self.DEFAULT_SHORTCUTS
        }

    def reset_shortcuts(self):
        for action, sequence in self.DEFAULT_SHORTCUTS.items():
            self._settings.setValue(f"shortcut/{action}", sequence)

    # ======================
    # SEARCH ENGINE
    # ======================

    def search_engine_name(self) -> str:
        return self._settings.value(
            "search_engine",
            self.DEFAULT_SEARCH_ENGINE,
            type=str
        )

    def set_search_engine_name(self, name: str):
        if name in self.SEARCH_ENGINES:
            self._settings.setValue("search_engine", name)

    def search_engine_url(self) -> str:
        name = self.search_engine_name()
        return self.SEARCH_ENGINES.get(
            name,
            self.SEARCH_ENGINES[self.DEFAULT_SEARCH_ENGINE]
        )

    def search_engine_home_url(self) -> str:
        name = self.search_engine_name()
        return self.SEARCH_ENGINE_HOME.get(
            name,
            self.SEARCH_ENGINE_HOME[self.DEFAULT_SEARCH_ENGINE]
        )

    # ======================
    # RESET
    # ======================

    def reset_to_defaults(self):
        self._settings.setValue("theme", self.DEFAULT_THEME)
        self._settings.setValue("search_engine", self.DEFAULT_SEARCH_ENGINE)
        self._settings.setValue("new_tab_mode", self.DEFAULT_NEW_TAB_MODE)
        self._settings.setValue(
            "confirm_clear_data",
            self.DEFAULT_CONFIRM_CLEAR_DATA
        )
        self.reset_shortcuts()
