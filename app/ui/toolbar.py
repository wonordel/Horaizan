import re
from PySide6.QtWidgets import (
    QWidget,
    QToolButton,
    QHBoxLayout,
    QLineEdit,
    QApplication
)
from PySide6.QtCore import QUrl
from app.settings import Settings
from app.ui.menu import BrowserMenu


class BrowserToolbar(QWidget):
    def __init__(self, webview, browser):
        super().__init__()

        self.setObjectName("BrowserToolbar")

        self.webview = webview
        self.settings = Settings()
        self.browser = browser
        self.settings = browser.settings


        self.setFixedHeight(44)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        self.back_btn = QToolButton()
        self.back_btn.setText("◀")
        self.back_btn.clicked.connect(self.webview.back)

        self.forward_btn = QToolButton()
        self.forward_btn.setText("▶")
        self.forward_btn.clicked.connect(self.webview.forward)

        self.reload_btn = QToolButton()
        self.reload_btn.setText("⟳")
        self.reload_btn.clicked.connect(self.webview.reload)

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Введите адрес или поисковый запрос")
        self.address_bar.setMinimumHeight(30)
        self.address_bar.setClearButtonEnabled(True)
        self.address_bar.returnPressed.connect(self.load_url)

        self.minimize_btn = QToolButton()
        self.minimize_btn.setText("—")
        self.minimize_btn.clicked.connect(self.window().showMinimized)

        self.close_btn = QToolButton()
        self.close_btn.setText("✕")
        self.close_btn.clicked.connect(QApplication.quit)
        self.menu_button = QToolButton()
        self.menu_button.setText("☰")
        self.menu_button.setToolTip("Настройки")
        self.menu_button.clicked.connect(self.open_settings)

        layout.addWidget(self.menu_button)



        layout.addWidget(self.back_btn)
        layout.addWidget(self.forward_btn)
        layout.addWidget(self.reload_btn)
        layout.addWidget(self.address_bar, stretch=1)
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.close_btn)

        self.webview.urlChanged.connect(self.update_url)

    def load_url(self):
        text = self.address_bar.text().strip()

        if not text:
            return

        if text.startswith(("http://", "https://")):
            self.webview.setUrl(QUrl(text))
            return

        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", text):
            self.webview.setUrl(QUrl(f"http://{text}"))
            return

        if "." in text and " " not in text:
            self.webview.setUrl(QUrl(f"https://{text}"))
            return

        search_url = self.settings.search_engine_url()
        self.webview.setUrl(QUrl(f"{search_url}{text}"))


    def update_url(self, url: QUrl):
        if url.scheme() == "horaizan":
            self.address_bar.setText("Настройки")
        else:
            self.address_bar.setText(url.toString())

    def open_settings(self):
        print("OPEN SETTINGS CALLED")

        # напрямую говорим webview загрузить URL
        # и НЕ ТРОГАЕМ address_bar
        self.webview.page().acceptNavigationRequest(
            QUrl("horaizan://settings"),
            None,
            True
        )





    def navigate(self):
        text = self.address_bar.text().strip()

        # 🔴 ВАЖНО: не трогать horaizan://
        if text.startswith("horaizan://"):
            self.webview.setUrl(QUrl(text))
            return

        if "://" not in text:
            text = "https://" + text

        self.webview.setUrl(QUrl(text))

