import sys
from PySide6.QtWidgets import QApplication
from app.window import BrowserWindow
from pathlib import Path
from app.window import resource_path

def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    theme_path = resource_path("app/themes/dark.qss")
    with open(theme_path, "r") as f:
        app.setStyleSheet(f.read())
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

