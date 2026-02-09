import sys
import os
import locale
from PySide6.QtWidgets import QApplication
from app.window import BrowserWindow

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
    window = BrowserWindow()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
