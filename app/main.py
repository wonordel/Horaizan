import sys
import os
import locale
from PySide6.QtWidgets import QApplication
from app.window import BrowserWindow
from pathlib import Path

def main():
    # Устанавливаем локаль UTF-8
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    
    # Устанавливаем платформу (попробуйте разные варианты)
    os.environ["QT_QPA_PLATFORM"] = "xcb"  # или "wayland"
    
    app = QApplication(sys.argv)
    window = BrowserWindow()
    
    # Правильный путь к теме
    current_dir = Path(__file__).resolve().parent
    theme_path = current_dir / "themes" / "dark.qss"
    
    if theme_path.exists():
        with open(theme_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Theme file not found at {theme_path}")
        # Альтернативный путь
        theme_path = Path(__file__).resolve().parent.parent / "app" / "themes" / "dark.qss"
        if theme_path.exists():
            with open(theme_path, "r") as f:
                app.setStyleSheet(f.read())
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()