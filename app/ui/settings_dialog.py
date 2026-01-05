from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton
)


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)

        self.settings = settings
        self.setWindowTitle("Настройки")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Поисковая система"))

        self.combo = QComboBox()
        self.engines = {
            "Google": "https://www.google.com/search?q=",
            "DuckDuckGo": "https://duckduckgo.com/?q=",
            "Bing": "https://www.bing.com/search?q="
        }

        self.combo.addItems(self.engines.keys())

        current = self.settings.search_engine()
        for name, url in self.engines.items():
            if url == current:
                self.combo.setCurrentText(name)

        layout.addWidget(self.combo)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save)

        layout.addWidget(save_btn)

    def save(self):
        engine_url = self.engines[self.combo.currentText()]
        self.settings.set_search_engine(engine_url)
        self.accept()
