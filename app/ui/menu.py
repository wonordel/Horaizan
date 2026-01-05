from PySide6.QtWidgets import QMenu


class BrowserMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.setTitle("☰")

        self.settings_action = self.addAction("Настройки")
        self.addSeparator()
        self.exit_action = self.addAction("Выход")
