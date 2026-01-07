# Horaizan Browser

# Языки/Languages
[Русский](README.md)
[English](README.en.md)

Horaizan - is a minimalistic open source web browser developed using PySide6. The browser provides basic features for navigating web pages, managing tabs, customizing the appearance, and selecting a search engine 🌐.
 
## Features

- **Minimalistic interface**: A simple and intuitive interface that doesn't distract from the main content.
- **Tab management**: The ability to open and close tabs.
- **Search engine customization**: Choose from popular search engines such as Google, Yandex, DuckDuckGo, and Bing.
- **Privacy**: Our browser will *never* be monitored by anyone (we don't talk about websites), we promise 🤫.
- **Change the theme to your liking**: The browser allows you to change the theme in the settings, from black to white!

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

- **Home page**: When you launch the browser, it opens google.com
- **New tab**: Click the "+" button next to the tabs to open a new tab.
- **Navigation**: Use the "Back", "Forward", and "Reload" buttons to navigate through the pages.
- **Address bar**: Enter a URL or search query in the address bar and press Enter.
- **Settings**: In the "Menu" menu, you can change the search engine and appearance settings.

## Project structure
```
.
├── app
│   ├── bridge.py
│   ├── __init__.py
│   ├── main.py
│   ├── profile.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── main.cpython-313.pyc
│   │   ├── profile.cpython-313.pyc
│   │   ├── settings.cpython-313.pyc
│   │   ├── webview.cpython-313.pyc
│   │   └── window.cpython-313.pyc
│   ├── settings_bridge.py
│   ├── settings.py
│   ├── themes
│   │   ├── dark.qss
│   │   └── light.qss
│   ├── ui
│   │   ├── __init__.py
│   │   ├── menu.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── menu.cpython-313.pyc
│   │   │   ├── settings_page.cpython-313.pyc
│   │   │   └── toolbar.cpython-313.pyc
│   │   ├── settings_dialog.py
│   │   ├── settings_html.py
│   │   ├── settings_page.py
│   │   └── toolbar.py
│   ├── web
│   │   ├── settings.css
│   │   ├── settings.html
│   │   └── settings.js
│   ├── webpage.py
│   ├── webview.py
│   └── window.py
├── README.en.md
├── README.md
└── requirements.txt
```

- **requirements.txt**: List of dependencies to install.

## Authors

- 1. Creator and main developer: **Xarays** (who gave up on this project) - Discord: `xarays.gg`
- 2. Secondary developer: **Wonordel** (who continued to develop the project) - Discord: `egorchik6767`
- 3. Third developer: **Kidknightik** (who completely redesigned the project) - Discord: `kidknightik`

## Acknowledgements

Thanks to the PySide6 community, ChatGPT, DeepSeek and everyone who has contributed to the development of this project ❤️.

---

**Note**: This project is in an inactive development stage and various bugs may appear(they will be here, I made it myself). If you find errors or have suggestions for improvement, please do not create an issue or submit a pull request ❤️.