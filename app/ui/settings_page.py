from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QCheckBox
)


class SettingsPage(QWidget):
    def __init__(self, settings, browser):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<h2>Настройки</h2>"))

        # === ТЕМА ===
        self.theme_toggle = QCheckBox("Тёмная тема")
        self.theme_toggle.setChecked(settings.is_dark())
        self.theme_toggle.stateChanged.connect(browser.toggle_theme)

        layout.addWidget(self.theme_toggle)

        # === ПОИСКОВИК ===
        layout.addWidget(QLabel("Поисковая система"))

        self.search_combo = QComboBox()
        self.search_combo.addItems(
            ["Google", "Yandex", "Bing", "DuckDuckGo"]
        )
        self.search_combo.setCurrentText(settings.search_engine_name())
        self.search_combo.currentTextChanged.connect(
            settings.set_search_engine_name
        )

        layout.addWidget(self.search_combo)

        # === ОЧИСТКА ===
        clear_btn = QPushButton("Очистить кэш и cookies")
        clear_btn.clicked.connect(browser.clear_browser_data)

        layout.addWidget(clear_btn)

        layout.addStretch()
