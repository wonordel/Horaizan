from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtNetwork import QNetworkCookie
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CookieManagerDialog(QDialog):
    def __init__(self, cookie_store, parent=None):
        super().__init__(parent)
        self.cookie_store = cookie_store
        self.setWindowTitle("Управление cookies")
        self.resize(1050, 440)

        self._cookies: list[QNetworkCookie] = []
        self._cookie_keys: set[str] = set()
        self._rows: dict[str, int] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        self.summary = QLabel("Cookies: 0")
        root.addWidget(self.summary)

        self.table = QTableWidget(0, 7, self)
        self.table.setHorizontalHeaderLabels(
            ["Домен", "Имя", "Значение", "Путь", "Secure", "HttpOnly", "Expires"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 220)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 70)
        self.table.setColumnWidth(5, 80)
        root.addWidget(self.table, stretch=1)

        actions = QWidget(self)
        actions_layout = QHBoxLayout(actions)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)

        self.delete_btn = QPushButton("Удалить выбранный")
        self.delete_btn.clicked.connect(self.delete_selected)
        actions_layout.addWidget(self.delete_btn)

        self.reload_btn = QPushButton("Обновить список")
        self.reload_btn.clicked.connect(self.reload_cookies)
        actions_layout.addWidget(self.reload_btn)

        self.clear_btn = QPushButton("Удалить все cookies")
        self.clear_btn.clicked.connect(self.clear_all)
        actions_layout.addWidget(self.clear_btn)

        actions_layout.addStretch(1)
        root.addWidget(actions)

        self.cookie_store.cookieAdded.connect(self._on_cookie_added)
        self.cookie_store.cookieRemoved.connect(self._on_cookie_removed)
        self.reload_cookies()

    def _cookie_key(self, cookie: QNetworkCookie) -> str:
        name = bytes(cookie.name()).decode("utf-8", errors="ignore")
        domain = cookie.domain() or ""
        path = cookie.path() or ""
        return f"{domain}\t{path}\t{name}"

    def _safe_value(self, value: bytes, max_len: int = 140) -> str:
        text = value.decode("utf-8", errors="replace")
        if len(text) > max_len:
            return text[: max_len - 1] + "…"
        return text

    def _on_cookie_added(self, cookie: QNetworkCookie):
        key = self._cookie_key(cookie)
        if key in self._cookie_keys:
            row = self._rows.get(key)
            if row is None:
                return
            self._cookies[row] = cookie
            self.table.item(row, 2).setText(self._safe_value(bytes(cookie.value())))
            if cookie.expirationDate().isValid():
                expires = cookie.expirationDate().toString(Qt.DateFormat.ISODate)
            else:
                expires = "Session"
            self.table.item(row, 6).setText(expires)
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        self._cookies.append(cookie)
        self._cookie_keys.add(key)
        self._rows[key] = row

        self.table.setItem(row, 0, QTableWidgetItem(cookie.domain() or ""))
        self.table.setItem(row, 1, QTableWidgetItem(self._safe_value(bytes(cookie.name()))))
        self.table.setItem(row, 2, QTableWidgetItem(self._safe_value(bytes(cookie.value()))))
        self.table.setItem(row, 3, QTableWidgetItem(cookie.path() or "/"))
        self.table.setItem(row, 4, QTableWidgetItem("Да" if cookie.isSecure() else "Нет"))
        self.table.setItem(row, 5, QTableWidgetItem("Да" if cookie.isHttpOnly() else "Нет"))

        if cookie.expirationDate().isValid():
            expires = cookie.expirationDate().toString(Qt.DateFormat.ISODate)
        else:
            expires = "Session"
        self.table.setItem(row, 6, QTableWidgetItem(expires))

        self._update_summary()

    def _on_cookie_removed(self, cookie: QNetworkCookie):
        key = self._cookie_key(cookie)
        row = self._rows.get(key)
        if row is None:
            return

        self.table.removeRow(row)
        self._cookies.pop(row)
        self._cookie_keys.discard(key)

        self._rows.clear()
        for idx, current in enumerate(self._cookies):
            self._rows[self._cookie_key(current)] = idx

        self._update_summary()

    def reload_cookies(self):
        self.table.setRowCount(0)
        self._cookies.clear()
        self._cookie_keys.clear()
        self._rows.clear()
        self._update_summary()
        self.cookie_store.loadAllCookies()

    def _selected_cookie(self):
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return None
        row = indexes[0].row()
        if row < 0 or row >= len(self._cookies):
            return None
        return self._cookies[row]

    def delete_selected(self):
        cookie = self._selected_cookie()
        if not cookie:
            return
        self.cookie_store.deleteCookie(cookie)

    def clear_all(self):
        self.cookie_store.deleteAllCookies()
        self.table.setRowCount(0)
        self._cookies.clear()
        self._cookie_keys.clear()
        self._rows.clear()
        self._update_summary()

    def _update_summary(self):
        self.summary.setText(f"Cookies: {len(self._cookies)}")
