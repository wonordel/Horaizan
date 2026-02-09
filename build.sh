#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"
PIP_EXTRA_ARGS=()
APPIMAGE_COMP="${APPIMAGE_COMP:-zstd}"

log() {
  echo "[build] $*"
}

warn() {
  echo "[warn] $*" >&2
}

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    warn "Команда '$1' не найдена"
    return 1
  fi
}

setup_pip_args() {
  case "$(uname -s)" in
    Linux*)
      PIP_EXTRA_ARGS=(--break-system-packages)
      ;;
    *)
      PIP_EXTRA_ARGS=()
      ;;
  esac
}

ensure_appimagetool() {
  if command -v appimagetool >/dev/null 2>&1; then
    return 0
  fi

  if [[ "$(uname -s)" != "Linux" ]]; then
    warn "appimagetool поддерживается только на Linux"
    return 1
  fi

  log "appimagetool не найден, пытаюсь установить appimagetool-bin"

  if command -v yay >/dev/null 2>&1; then
    yay -S --needed --noconfirm appimagetool-bin || true
  elif command -v paru >/dev/null 2>&1; then
    paru -S --needed --noconfirm appimagetool-bin || true
  else
    warn "Не найден ни yay, ни paru. Установи appimagetool-bin вручную."
    return 1
  fi

  if ! command -v appimagetool >/dev/null 2>&1; then
    warn "Не удалось установить appimagetool-bin через AUR helper"
    return 1
  fi
}

venv_python() {
  if [[ -x "$VENV_DIR/bin/python" ]]; then
    echo "$VENV_DIR/bin/python"
  elif [[ -x "$VENV_DIR/Scripts/python.exe" ]]; then
    echo "$VENV_DIR/Scripts/python.exe"
  else
    return 1
  fi
}

ensure_venv() {
  if [[ ! -d "$VENV_DIR" ]]; then
    log "Создаю virtualenv в $VENV_DIR"
    "$PYTHON_BIN" -m venv "$VENV_DIR"
  fi

  local py
  py="$(venv_python)"
  "$py" -m pip install "${PIP_EXTRA_ARGS[@]}" --upgrade pip wheel setuptools >/dev/null
}

install_python_deps() {
  local py
  py="$(venv_python)"

  "$py" -m pip install "${PIP_EXTRA_ARGS[@]}" --upgrade -r "$ROOT_DIR/requirements.txt"

  if [[ -f "$ROOT_DIR/requirements-build.txt" ]]; then
    "$py" -m pip install "${PIP_EXTRA_ARGS[@]}" --upgrade -r "$ROOT_DIR/requirements-build.txt"
  fi
}

install_os_deps_linux() {
  if command -v pacman >/dev/null 2>&1; then
    log "Устанавливаю системные пакеты через pacman"
    sudo pacman -Syu --noconfirm --needed \
      base-devel python python-pip python-virtualenv pyinstaller \
      appstream desktop-file-utils patchelf fuse2 nsis
  elif command -v apt-get >/dev/null 2>&1; then
    log "Устанавливаю системные пакеты через apt"
    sudo apt-get update
    sudo apt-get install -y \
      python3 python3-venv python3-pip build-essential \
      desktop-file-utils appstream patchelf libfuse2 nsis
  elif command -v dnf >/dev/null 2>&1; then
    log "Устанавливаю системные пакеты через dnf"
    sudo dnf install -y \
      python3 python3-pip python3-virtualenv gcc \
      desktop-file-utils appstream patchelf fuse nsis
  else
    warn "Неизвестный пакетный менеджер Linux. Системные пакеты установи вручную."
  fi
}

install_os_deps_windows() {
  if command -v choco >/dev/null 2>&1; then
    log "Пробую установить инструменты через Chocolatey"
    choco install -y python nsis
  else
    warn "Chocolatey не найден. Установи Python и NSIS вручную."
  fi
}

reinstall_dependencies() {
  log "Переустанавливаю зависимости"

  case "$(uname -s)" in
    Linux*) install_os_deps_linux ;;
    MINGW*|MSYS*|CYGWIN*) install_os_deps_windows ;;
    *) warn "Неподдерживаемая ОС для автоустановки системных зависимостей" ;;
  esac

  ensure_venv
  install_python_deps

  log "Зависимости установлены"
}

build_appimage() {
  need_cmd cp
  need_cmd tar

  ensure_venv
  install_python_deps
  local py
  py="$(venv_python)"

  log "Собираю Linux onedir через PyInstaller"
  rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist" "$ROOT_DIR/AppDir"

  "$py" -m PyInstaller \
    --noconfirm \
    --clean \
    --onedir \
    --windowed \
    --name Horaizan \
    --icon "$ROOT_DIR/app/themes/icon.png" \
    --collect-all PySide6 \
    --collect-submodules PySide6.QtWebEngineCore \
    --collect-submodules PySide6.QtWebEngineWidgets \
    --add-data "$ROOT_DIR/app/themes:app/themes" \
    "$ROOT_DIR/app/__main__.py"

  log "Формирую AppDir"
  mkdir -p \
    "$ROOT_DIR/AppDir/usr/bin" \
    "$ROOT_DIR/AppDir/usr/lib" \
    "$ROOT_DIR/AppDir/usr/share/applications" \
    "$ROOT_DIR/AppDir/usr/share/icons/hicolor/256x256/apps" \
    "$ROOT_DIR/AppDir/usr/share/pixmaps"

  cp -r "$ROOT_DIR/dist/Horaizan" "$ROOT_DIR/AppDir/usr/lib/horaizan"
  cp "$ROOT_DIR/app/themes/icon.png" "$ROOT_DIR/AppDir/usr/share/icons/hicolor/256x256/apps/horaizan.png"
  cp "$ROOT_DIR/app/themes/icon.png" "$ROOT_DIR/AppDir/usr/share/pixmaps/horaizan.png"
  cp "$ROOT_DIR/app/themes/icon.png" "$ROOT_DIR/AppDir/horaizan.png"
  cp "$ROOT_DIR/app/themes/icon.png" "$ROOT_DIR/AppDir/.DirIcon"

  cat > "$ROOT_DIR/AppDir/usr/bin/horaizan" <<'LAUNCH'
#!/usr/bin/env bash
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# QtWebEngine в AppImage часто падает из-за sandbox helper прав.
export QTWEBENGINE_DISABLE_SANDBOX=1
export QTWEBENGINE_CHROMIUM_FLAGS="${QTWEBENGINE_CHROMIUM_FLAGS:-} --no-sandbox"
exec "$HERE/../lib/horaizan/Horaizan" "$@"
LAUNCH
  chmod +x "$ROOT_DIR/AppDir/usr/bin/horaizan"

  cat > "$ROOT_DIR/AppDir/AppRun" <<'APPRUN'
#!/usr/bin/env bash
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$HERE/usr/bin/horaizan" "$@"
APPRUN
  chmod +x "$ROOT_DIR/AppDir/AppRun"

  cat > "$ROOT_DIR/AppDir/horaizan.desktop" <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=Horaizan
Comment=Chromium-based Python browser
Exec=horaizan
Icon=horaizan
Categories=Network;WebBrowser;
Terminal=false
StartupWMClass=Horaizan
DESKTOP
  cp "$ROOT_DIR/AppDir/horaizan.desktop" "$ROOT_DIR/AppDir/usr/share/applications/horaizan.desktop"

  if command -v desktop-file-validate >/dev/null 2>&1; then
    desktop-file-validate "$ROOT_DIR/AppDir/horaizan.desktop" || true
  fi

  if ensure_appimagetool; then
    log "Собираю AppImage"
    ARCH="$(uname -m)" appimagetool --comp "$APPIMAGE_COMP" "$ROOT_DIR/AppDir" "$ROOT_DIR/dist/Horaizan-$(uname -m).AppImage"
    chmod +x "$ROOT_DIR/dist/Horaizan-$(uname -m).AppImage" || true
    log "Готово: dist/Horaizan-$(uname -m).AppImage"
    log "Compression: $APPIMAGE_COMP"
    log "Иконка в AppImage вшита через .DirIcon и desktop metadata"
    log "Если система без FUSE: ./dist/Horaizan-$(uname -m).AppImage --appimage-extract-and-run"
  else
    warn "appimagetool не найден. AppDir готов в ./AppDir"
    warn "Установи appimagetool и запусти: ARCH=$(uname -m) appimagetool AppDir dist/Horaizan-$(uname -m).AppImage"
  fi
}

build_windows_installer_nsis() {
  if ! command -v makensis >/dev/null 2>&1; then
    warn "NSIS (makensis) не найден. Инсталлятор пропущен."
    return 0
  fi

  mkdir -p "$ROOT_DIR/build/windows"
  cat > "$ROOT_DIR/build/windows/horaizan-installer.nsi" <<'NSI'
!define APPNAME "Horaizan"
!define COMPANY "Horaizan"
!define VERSION "1.0.0"
!define EXEFILE "Horaizan.exe"

OutFile "..\\..\\dist\\Horaizan-Setup.exe"
InstallDir "$PROGRAMFILES\\${APPNAME}"
RequestExecutionLevel admin

Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File "..\\..\\dist\\${EXEFILE}"
  CreateDirectory "$SMPROGRAMS\\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk" "$INSTDIR\\${EXEFILE}"
  CreateShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\${EXEFILE}"
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\\${APPNAME}\\${APPNAME}.lnk"
  RMDir "$SMPROGRAMS\\${APPNAME}"
  Delete "$INSTDIR\\${EXEFILE}"
  Delete "$INSTDIR\\Uninstall.exe"
  RMDir "$INSTDIR"
SectionEnd
NSI

  (cd "$ROOT_DIR/build/windows" && makensis horaizan-installer.nsi)
  log "Инсталлятор: dist/Horaizan-Setup.exe"
}

build_windows_exe() {
  ensure_venv
  install_python_deps
  local py
  py="$(venv_python)"

  rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist"

  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*)
      log "Собираю .exe на Windows"
      "$py" -m PyInstaller \
        --noconfirm \
        --clean \
        --onefile \
        --windowed \
        --name Horaizan \
        --icon "$ROOT_DIR/app/themes/icon.png" \
        --add-data "$ROOT_DIR/app/themes;app/themes" \
        "$ROOT_DIR/app/__main__.py"
      build_windows_installer_nsis
      ;;
    Linux*)
      warn "Нативная сборка .exe на Linux не поддерживается PyInstaller напрямую."
      warn "Рекомендуется запускать пункт 2 на Windows, либо настроить Wine+Windows Python вручную."
      if command -v wine >/dev/null 2>&1; then
        warn "Wine найден, но автоматический кросс-билд не включён из-за нестабильности окружений."
      fi
      return 1
      ;;
    *)
      warn "Неподдерживаемая ОС для .exe сборки"
      return 1
      ;;
  esac

  log "Готово: dist/Horaizan.exe"
}

build_aur_package() {
  need_cmd tar
  mkdir -p "$ROOT_DIR/packaging/aur"

  local pkgver sha tarball
  pkgver="$(date +%Y.%m.%d)"
  tarball="horaizan-${pkgver}.tar.gz"

  log "Генерирую source tarball для PKGBUILD"
  tar --exclude-vcs --exclude='*.pyc' --exclude='__pycache__' \
    -czf "$ROOT_DIR/packaging/aur/$tarball" \
    -C "$ROOT_DIR" app requirements.txt README.md README.en.md

  sha="$(sha256sum "$ROOT_DIR/packaging/aur/$tarball" | awk '{print $1}')"

  cat > "$ROOT_DIR/packaging/aur/horaizan" <<'LAUNCH'
#!/usr/bin/env bash
exec python /usr/share/horaizan/app/__main__.py "$@"
LAUNCH
  chmod +x "$ROOT_DIR/packaging/aur/horaizan"

  cat > "$ROOT_DIR/packaging/aur/horaizan.desktop" <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=Horaizan
Comment=Chromium-based Python browser
Exec=horaizan
Icon=horaizan
Categories=Network;WebBrowser;
Terminal=false
DESKTOP

  cat > "$ROOT_DIR/packaging/aur/PKGBUILD" <<PKG
pkgname=horaizan
pkgver=${pkgver}
pkgrel=1
pkgdesc="Chromium-based Python browser"
arch=('x86_64')
url="https://example.com/horaizan"
license=('MIT')
depends=('python' 'pyside6')
source=('${tarball}' 'horaizan' 'horaizan.desktop' 'icon.png')
sha256sums=('${sha}' 'SKIP' 'SKIP' 'SKIP')

package() {
  install -dm755 "\$pkgdir/usr/share/horaizan"
  cp -r "\$srcdir/app" "\$pkgdir/usr/share/horaizan/app"
  install -Dm644 "\$srcdir/requirements.txt" "\$pkgdir/usr/share/horaizan/requirements.txt"

  install -Dm755 "\$srcdir/horaizan" "\$pkgdir/usr/bin/horaizan"
  install -Dm644 "\$srcdir/horaizan.desktop" "\$pkgdir/usr/share/applications/horaizan.desktop"
  install -Dm644 "\$srcdir/icon.png" "\$pkgdir/usr/share/icons/hicolor/256x256/apps/horaizan.png"
}
PKG

  cp "$ROOT_DIR/app/themes/icon.png" "$ROOT_DIR/packaging/aur/icon.png"

  if command -v makepkg >/dev/null 2>&1; then
    log "Запускаю makepkg"
    (cd "$ROOT_DIR/packaging/aur" && makepkg -f)
    log "Готово: packaging/aur/*.pkg.tar.*"
  else
    warn "makepkg не найден. Файлы AUR-шаблона подготовлены в packaging/aur"
  fi
}

show_menu() {
  cat <<'MENU'

Выбери действие:
  1) Компилировать браузер в AppImage
  2) Компилировать браузер в .exe (и попытка сделать инсталлер)
  5) Сборка для AUR (Arch Linux)
  4) Заново скачать/переустановить зависимости (Linux/Windows)
  0) Выход
MENU
}

main() {
  cd "$ROOT_DIR"
  setup_pip_args
  show_menu
  read -rp "Номер действия: " choice

  case "$choice" in
    1) build_appimage ;;
    2) build_windows_exe ;;
    5) build_aur_package ;;
    4) reinstall_dependencies ;;
    0) log "Выход" ;;
    *) warn "Неизвестный пункт: $choice"; exit 1 ;;
  esac
}

main "$@"
