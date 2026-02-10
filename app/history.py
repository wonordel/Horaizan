from __future__ import annotations

import json
from datetime import datetime

from PySide6.QtCore import Qt, QUrl, QSettings
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


class HistoryManagerDialog(QDialog):
    SETTINGS_KEY = "history/items"
    MAX_ITEMS = 1000

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("История браузера")
        self.resize(980, 430)

        self._settings = QSettings("Horaizan", "Browser")
        self._items: list[dict] = []
        self._open_url_handler = None

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        self.summary = QLabel("История пуста")
        root.addWidget(self.summary)

        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(["Название", "URL", "Время"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        self.table.setColumnWidth(0, 280)
        self.table.setColumnWidth(1, 470)
        root.addWidget(self.table, stretch=1)

        actions = QWidget(self)
        actions_layout = QHBoxLayout(actions)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)

        self.open_btn = QPushButton("Открыть")
        self.open_btn.clicked.connect(self.open_selected)
        actions_layout.addWidget(self.open_btn)

        self.remove_btn = QPushButton("Удалить запись")
        self.remove_btn.clicked.connect(self.remove_selected)
        actions_layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("Очистить историю")
        self.clear_btn.clicked.connect(self.clear_history)
        actions_layout.addWidget(self.clear_btn)

        actions_layout.addStretch(1)
        root.addWidget(actions)

        self.table.doubleClicked.connect(lambda _index: self.open_selected())
        self._load_history()
        self._refresh_table()

    def set_open_url_handler(self, handler):
        self._open_url_handler = handler

    def add_entry(self, title: str, url: str):
        if not url:
            return

        item = {
            "title": (title or "").strip() or url,
            "url": url,
            "visited_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._items.insert(0, item)
        if len(self._items) > self.MAX_ITEMS:
            self._items = self._items[: self.MAX_ITEMS]

        self._save_history()
        self._refresh_table()

    def _load_history(self):
        raw = self._settings.value(self.SETTINGS_KEY, "[]", type=str)
        try:
            items = json.loads(raw)
            if isinstance(items, list):
                self._items = [x for x in items if isinstance(x, dict)]
            else:
                self._items = []
        except Exception:
            self._items = []

    def _save_history(self):
        self._settings.setValue(self.SETTINGS_KEY, json.dumps(self._items, ensure_ascii=False))

    def _refresh_table(self):
        self.table.setRowCount(0)
        for item in self._items:
            row = self.table.rowCount()
            self.table.insertRow(row)

            title_item = QTableWidgetItem(item.get("title", ""))
            title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, QTableWidgetItem(item.get("url", "")))
            self.table.setItem(row, 2, QTableWidgetItem(item.get("visited_at", "")))

        total = len(self._items)
        self.summary.setText(f"Записей: {total}")

    def _selected_row(self) -> int:
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return -1
        return indexes[0].row()

    def open_selected(self):
        row = self._selected_row()
        if row < 0 or row >= len(self._items):
            return
        url = self._items[row].get("url", "")
        if not url:
            return
        if self._open_url_handler:
            self._open_url_handler(QUrl(url))

    def remove_selected(self):
        row = self._selected_row()
        if row < 0 or row >= len(self._items):
            return
        self._items.pop(row)
        self._save_history()
        self._refresh_table()

    def clear_history(self):
        self._items = []
        self._save_history()
        self._refresh_table()
