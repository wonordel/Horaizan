from PySide6.QtCore import QSettings


class Settings:
    def __init__(self):
        self.settings = QSettings("Horaizan", "Browser")

    def search_engine(self):
        return self.settings.value(
            "search_engine",
            "https://www.google.com/search?q=",
            type=str
        )

    def set_search_engine(self, url):
        self.settings.setValue("search_engine", url)
    def is_dark(self):
        return self.settings.value("dark_theme", True, bool)

    def set_dark(self, value):
        self.settings.setValue("dark_theme", value)

    def toggle_theme(self, state):
        self.settings.set_dark(bool(state))
        self.apply_theme()
    
    def apply_theme(self):
        theme = "dark.qss" if self.settings.is_dark() else "light.qss"
        path = Path(__file__).parent / "themes" / theme
        with open(path) as f:
            self.setStyleSheet(f.read())
