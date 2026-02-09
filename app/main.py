import sys
import os
import locale
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from app.window import BrowserWindow


def resolve_icon_path() -> Path | None:
    candidates = []

    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
        candidates.extend([
            base / "themes" / "icon.png",
            base / "app" / "themes" / "icon.png",
        ])
    else:
        base = Path(__file__).resolve().parent
        candidates.extend([
            base / "themes" / "icon.png",
            base / "app" / "themes" / "icon.png",
        ])

    for path in candidates:
        if path.exists():
            return path
    return None


def main():
    # Устанавливаем локаль UTF-8
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    
    # Устанавливаем платформу в зависимости от ОС
    if sys.platform == "linux":
        os.environ["QT_QPA_PLATFORM"] = "xcb"  # или "wayland"
    elif sys.platform == "win32":
        # На Windows Qt сам выберет правильную платформу
        # Можно удалить эту строку или оставить как есть
        pass
    elif sys.platform == "darwin":
        os.environ["QT_QPA_PLATFORM"] = "cocoa"
    
    app = QApplication(sys.argv)
    icon_path = resolve_icon_path()
    if icon_path is not None:
        app.setWindowIcon(QIcon(str(icon_path)))

    window = BrowserWindow()
    if icon_path is not None:
        window.setWindowIcon(QIcon(str(icon_path)))

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
