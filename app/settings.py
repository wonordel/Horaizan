from PySide6.QtCore import QSettings


class Settings:
    ORGANIZATION = "Horaizan"
    APPLICATION = "Browser"

    DEFAULT_SEARCH_ENGINE = "Google"
    DEFAULT_THEME = "dark"

    SEARCH_ENGINES = {
        "Google": "https://www.google.com/search?q=",
        "Yandex": "https://yandex.ru/search/?text=",
        "Bing": "https://www.bing.com/search?q=",
        "DuckDuckGo": "https://duckduckgo.com/?q=",
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
        if theme in ("dark", "light"):
            self._settings.setValue("theme", theme)

    def is_dark(self) -> bool:
        return self.theme() == "dark"

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
