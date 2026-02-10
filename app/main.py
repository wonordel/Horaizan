import sys
import os
import locale
from pathlib import Path
from PySide6.QtCore import QUrl
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


def _to_startup_url(value: str) -> QUrl | None:
    if not value:
        return None

    value = value.strip().strip('"').strip("'")
    if not value or value in ("%u", "%U"):
        return None

    expanded = os.path.expanduser(value)
    if os.path.exists(expanded):
        return QUrl.fromLocalFile(os.path.abspath(expanded))

    if value.startswith(("/", "./", "../", "~/")):
        abs_path = os.path.abspath(os.path.expanduser(value))
        return QUrl.fromLocalFile(abs_path)

    if value.startswith(("http://", "https://", "ftp://", "file://")):
        direct = QUrl(value)
        if direct.isValid() and not direct.isEmpty():
            return direct

    candidate = QUrl.fromUserInput(value)
    if candidate.isValid() and not candidate.isEmpty():
        return candidate

    return None


def collect_startup_urls(args: list[str]) -> list[QUrl]:
    urls: list[QUrl] = []
    seen: set[str] = set()
    parse_all = False

    for arg in args:
        if not arg:
            continue

        value = arg
        if arg == "--":
            parse_all = True
            continue

        if not parse_all and arg.startswith("-"):
            # Ignore CLI switches from launchers/desktop environments.
            continue

        url = _to_startup_url(value)
        if url is None:
            continue

        key = url.toString()
        if key in seen:
            continue
        seen.add(key)
        urls.append(url)

    return urls


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

    startup_urls = collect_startup_urls(sys.argv[1:])
    if startup_urls:
        window.open_url_in_current_tab(startup_urls[0])
        for extra_url in startup_urls[1:]:
            window.add_tab()
            window.open_url_in_current_tab(extra_url)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
