from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
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


class DownloadManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Менеджер загрузок")
        self.resize(920, 420)

        self._downloads: list = []
        self._rows: dict[object, int] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        self.summary = QLabel("Нет загрузок")
        root.addWidget(self.summary)

        self.table = QTableWidget(0, 5, self)
        self.table.setHorizontalHeaderLabels(
            ["Файл", "Статус", "Прогресс", "Источник", "Путь"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setMinimumSectionSize(80)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 220)
        root.addWidget(self.table, stretch=1)

        actions = QWidget(self)
        actions_layout = QHBoxLayout(actions)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(8)

        self.open_file_btn = QPushButton("Открыть файл")
        self.open_file_btn.clicked.connect(self.open_selected_file)
        actions_layout.addWidget(self.open_file_btn)

        self.open_folder_btn = QPushButton("Открыть папку")
        self.open_folder_btn.clicked.connect(self.open_selected_folder)
        actions_layout.addWidget(self.open_folder_btn)

        self.cancel_btn = QPushButton("Отменить")
        self.cancel_btn.clicked.connect(self.cancel_selected)
        actions_layout.addWidget(self.cancel_btn)

        self.clear_btn = QPushButton("Очистить завершённые")
        self.clear_btn.clicked.connect(self.clear_finished)
        actions_layout.addWidget(self.clear_btn)

        actions_layout.addStretch(1)
        root.addWidget(actions)

    def register_download(self, request):
        if request in self._rows:
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        self._downloads.append(request)
        self._rows[request] = row

        file_name = self._download_file_name(request)
        source = request.url().toString()
        path = self._download_path(request)

        self.table.setItem(row, 0, QTableWidgetItem(file_name))
        self.table.setItem(row, 1, QTableWidgetItem(self._state_label(request)))
        self.table.setItem(row, 2, QTableWidgetItem(self._progress_label(request)))
        self.table.setItem(row, 3, QTableWidgetItem(source))
        self.table.setItem(row, 4, QTableWidgetItem(path))

        self._bind_updates(request)
        self._update_summary()

    def _bind_updates(self, request):
        if hasattr(request, "receivedBytesChanged"):
            request.receivedBytesChanged.connect(
                lambda req=request: self._refresh_request(req)
            )
        if hasattr(request, "totalBytesChanged"):
            request.totalBytesChanged.connect(
                lambda req=request: self._refresh_request(req)
            )
        if hasattr(request, "stateChanged"):
            request.stateChanged.connect(
                lambda _state, req=request: self._refresh_request(req)
            )
        if hasattr(request, "isFinishedChanged"):
            request.isFinishedChanged.connect(
                lambda req=request: self._refresh_request(req)
            )

    def _refresh_request(self, request):
        row = self._rows.get(request)
        if row is None:
            return

        self.table.item(row, 1).setText(self._state_label(request))
        self.table.item(row, 2).setText(self._progress_label(request))
        self.table.item(row, 4).setText(self._download_path(request))
        self._update_summary()

    def _progress_label(self, request) -> str:
        total = int(getattr(request, "totalBytes", lambda: 0)())
        received = int(getattr(request, "receivedBytes", lambda: 0)())
        if total <= 0:
            if received <= 0:
                return "0%"
            return f"{received} B"
        percent = max(0, min(100, int((received / total) * 100)))
        return f"{percent}%"

    def _state_label(self, request) -> str:
        state = getattr(request, "state", lambda: None)()
        enum = request.DownloadState if hasattr(request, "DownloadState") else None
        if enum is None:
            return "Неизвестно"

        if state == enum.DownloadRequested:
            return "Ожидание"
        if state == enum.DownloadInProgress:
            return "Скачивается"
        if state == enum.DownloadCompleted:
            return "Завершено"
        if state == enum.DownloadCancelled:
            return "Отменено"
        if state == enum.DownloadInterrupted:
            reason = ""
            if hasattr(request, "interruptReasonString"):
                reason = request.interruptReasonString()
            return f"Ошибка: {reason}" if reason else "Ошибка"
        return "Неизвестно"

    def _selected_request(self):
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return None
        row = indexes[0].row()
        if row < 0 or row >= len(self._downloads):
            return None
        return self._downloads[row]

    def _download_file_name(self, request) -> str:
        if hasattr(request, "downloadFileName"):
            return request.downloadFileName() or "download.bin"
        if hasattr(request, "suggestedFileName"):
            return request.suggestedFileName() or "download.bin"
        return "download.bin"

    def _download_path(self, request) -> str:
        if hasattr(request, "path"):
            return request.path() or ""

        directory = request.downloadDirectory() if hasattr(request, "downloadDirectory") else ""
        file_name = self._download_file_name(request)
        return str(Path(directory) / file_name) if directory else file_name

    def open_selected_file(self):
        request = self._selected_request()
        if not request:
            return
        path = self._download_path(request)
        if path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def open_selected_folder(self):
        request = self._selected_request()
        if not request:
            return
        path = self._download_path(request)
        if not path:
            return
        folder = str(Path(path).expanduser().resolve().parent)
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    def cancel_selected(self):
        request = self._selected_request()
        if not request:
            return
        if hasattr(request, "cancel"):
            request.cancel()
            self._refresh_request(request)

    def clear_finished(self):
        to_remove = []
        for request in self._downloads:
            state = getattr(request, "state", lambda: None)()
            if hasattr(request, "DownloadState"):
                finished = {
                    request.DownloadState.DownloadCompleted,
                    request.DownloadState.DownloadCancelled,
                    request.DownloadState.DownloadInterrupted,
                }
                if state in finished:
                    to_remove.append(request)

        if not to_remove:
            return

        rows = sorted(
            (self._rows[req] for req in to_remove if req in self._rows),
            reverse=True,
        )
        for row in rows:
            self.table.removeRow(row)
            self._downloads.pop(row)

        self._rows.clear()
        for idx, req in enumerate(self._downloads):
            self._rows[req] = idx

        self._update_summary()

    def _update_summary(self):
        total = len(self._downloads)
        in_progress = 0
        for request in self._downloads:
            state = getattr(request, "state", lambda: None)()
            if hasattr(request, "DownloadState"):
                if state in (
                    request.DownloadState.DownloadRequested,
                    request.DownloadState.DownloadInProgress,
                ):
                    in_progress += 1
        self.summary.setText(f"Всего: {total} | Активные: {in_progress}")
