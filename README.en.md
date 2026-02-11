# Horaizan Browser

# Языки/Languages
[Русский](README.md)
[English](README.en.md)

Horaizan is an open source browser built with PySide6 (Chromium/WebEngine). The project includes a custom UI, built-in settings, incognito mode, configurable shortcuts, and build tooling for Linux/Windows 🌐.
 
## Features

- **Updated UI**: Top bar and tabs were redesigned (Firefox-inspired style, compact controls, cleaner address bar).
- **Tabs with site icon and title**: Displays `favicon`, page title, movable tabs, and close controls.
- **Built-in settings page**: `horaizan://settings` with sections:
  - General (theme, search engine, new tab behavior)
  - Privacy (cache/cookies cleanup, confirmation toggle, incognito, download manager)
  - Hotkeys (edit keyboard shortcuts)
- **Themes**: `dark`, `light`, and `system` (follows OS theme).
- **Incognito mode**: Separate window with non-persistent cookies/cache (default shortcut `Ctrl+Shift+N`).
- **DevTools and context menu**: Developer tools are available from right click ("Inspect element") and via `F12`.
- **File downloads**: Built-in download flow with a downloads manager and progress tracking.
- **Custom hotkeys**: Standard shortcuts are supported (`Ctrl+T`, `Ctrl+W`, `Ctrl+R`, `Ctrl+L`, `Ctrl+,`, `F12`, `Ctrl+J`, `Alt+Left`, `Alt+Right`) and can be changed in settings.
- **App icon support**: Uses `app/themes/icon.png` for windows and builds.

## Installation

1. Make sure you have Python 3.9 or later installed 🐍.
2. Clone the repository:

   ```bash
   git clone --depth 1 https://github.com/wonordel/Horaizan.git
   cd horaizan
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Install via AUR

You can also install the package from AUR as `horaizan-git`:

```bash
yay -S horaizan-git
```

or

```bash
paru -S horaizan-git
```
[URL to AUR:](https://aur.archlinux.org/packages/horaizan-git)

### Install from local AUR files (without GitHub)

If you already have the project directory with `packaging/aur`, you can install the browser directly from these files:

1. Open the AUR files directory:

   ```bash
   cd /path/to/Horaizan/packaging/aur
   ```

2. Build and install the package:

   ```bash
   makepkg -Csi
   ```

3. (Optional) Set it as default browser:

   ```bash
   xdg-settings set default-web-browser horaizan.desktop
   xdg-mime default horaizan.desktop x-scheme-handler/http
   xdg-mime default horaizan.desktop x-scheme-handler/https
   xdg-mime default horaizan.desktop application/pdf
   ```

## Launching

To launch the browser, run the following command (Linux 🐧):

```bash
python3 -m app.main
```
(if it throws an error, restart it several times)

To launch the browser on Windows 🪟:

```batch
python -m app.main
```

## Usage

- **Home page**: At startup, the browser opens the home page of the selected search engine.
- **New tab**: Click the "+" button next to the tabs to open a new tab.
- **Navigation**: Use the "Back", "Forward", and "Reload" buttons to navigate through the pages.
- **Address bar**: Enter a URL or search query in the address bar and press Enter.
- **Settings**: The `☰` button opens the internal settings page.
- **Incognito**: Available from settings or via `Ctrl+Shift+N`.
- **System theme**: When `system` is selected, the browser follows light/dark OS changes automatically.

## Build and automation (`build.sh`)

This repository includes an interactive build script:

```bash
./build.sh
```

Available options:

- `1` - build `AppImage` (portable one-file)
- `2` - build `.exe` (on Windows) + attempt NSIS installer
- `5` - prepare/build `AUR` package
- `4` - reinstall system and Python dependencies

AppImage build notes:

- The script checks for `appimagetool`; if missing, it tries to install `appimagetool-bin` via `yay` or `paru`.
- AppImage icon is embedded from `app/themes/icon.png`.
- Compression is set to `zstd` for wider runtime compatibility.
- If your system has FUSE issues, run:

```bash
./dist/Horaizan-x86_64.AppImage --appimage-extract-and-run
```

## Project structure
```
├── app
│   ├── bridge.py
│   ├── cookies.py
│   ├── downloads.py
│   ├── history.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   ├── profile.py
│   ├── __pycache__
│   │   ├── bridge.cpython-314.pyc
│   │   ├── cookies.cpython-314.pyc
│   │   ├── downloads.cpython-314.pyc
│   │   ├── history.cpython-314.pyc
│   │   ├── __init__.cpython-314.pyc
│   │   ├── __main__.cpython-314.pyc
│   │   ├── main.cpython-314.pyc
│   │   ├── profile.cpython-314.pyc
│   │   ├── settings.cpython-314.pyc
│   │   ├── webpage.cpython-314.pyc
│   │   ├── webview.cpython-314.pyc
│   │   └── window.cpython-314.pyc
│   ├── settings.py
│   ├── themes
│   │   ├── dark.qss
│   │   ├── icon.png
│   │   └── light.qss
│   ├── ui
│   │   ├── __init__.py
│   │   ├── menu.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-314.pyc
│   │   │   ├── menu.cpython-314.pyc
│   │   │   ├── settings_html.cpython-314.pyc
│   │   │   └── toolbar.cpython-314.pyc
│   │   ├── settings_html.py
│   │   └── toolbar.py
│   ├── webpage.py
│   ├── webview.py
│   └── window.py
├── build.sh
├── packaging
│   └── aur
│       ├── app-main-argv.patch
│       ├── horaizan
│       ├── horaizan.desktop
│       ├── horaizan.install
│       ├── PKGBUILD
│       └── session-and-pdf.patch
├── README.en.md
├── README.md
├── requirements-build.txt
└── requirements.txt

```

- **requirements.txt**: Runtime dependencies.
- **requirements-build.txt**: Python build dependencies.
- **build.sh**: Interactive script for dependency install and builds.

## Authors

- 1. Creator and main developer: **Xarays** (who gave up on this project) - Discord: `xarays.gg`
- 2. Secondary developer: **Wonordel** (who continued to develop the project) - Discord: `egorchik6767`
- 3. Third developer: **Kidknightik** (who completely redesigned the project) - Discord: `kidknightik`

## Acknowledgements

Thanks to the PySide6 community, ChatGPT, DeepSeek and everyone who has contributed to the development of this project ❤️.

---

**Note**: This project is in an inactive development stage and various bugs may appear(they will be here, I made it myself). If you find errors or have suggestions for improvement, please create an issue or submit a pull request ❤️.
