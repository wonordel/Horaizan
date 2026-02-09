SETTINGS_HTML = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Настройки</title>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>

<style>
:root {
    --bg-1: #0f172a;
    --bg-2: #16213e;
    --surface: rgba(255, 255, 255, 0.08);
    --surface-strong: rgba(255, 255, 255, 0.14);
    --text: #ecf2ff;
    --muted: #b9c4e8;
    --accent: #4ade80;
    --accent-2: #38bdf8;
    --danger: #fb7185;
    --border: rgba(255, 255, 255, 0.16);
    --shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
}

body.light {
    --bg-1: #f4f7fb;
    --bg-2: #dce7f8;
    --surface: rgba(255, 255, 255, 0.72);
    --surface-strong: rgba(255, 255, 255, 0.94);
    --text: #0f172a;
    --muted: #4b5563;
    --accent: #0ea5e9;
    --accent-2: #14b8a6;
    --danger: #e11d48;
    --border: rgba(15, 23, 42, 0.14);
    --shadow: 0 16px 38px rgba(15, 23, 42, 0.16);
}

* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    font-family: "Segoe UI", "Noto Sans", sans-serif;
    color: var(--text);
    background: radial-gradient(circle at 15% 20%, var(--bg-2), transparent 50%),
                linear-gradient(135deg, var(--bg-1), #0b1225);
}

.layout {
    display: grid;
    grid-template-columns: 260px 1fr;
    min-height: 100vh;
}

.sidebar {
    padding: 28px 20px;
    border-right: 1px solid var(--border);
    background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
}

.brand {
    font-size: 18px;
    font-weight: 700;
    margin: 0 0 6px;
}

.subtitle {
    margin: 0 0 24px;
    color: var(--muted);
    font-size: 13px;
}

.navitem {
    display: block;
    width: 100%;
    border: 1px solid transparent;
    color: var(--text);
    text-align: left;
    font-size: 14px;
    padding: 10px 12px;
    margin-bottom: 8px;
    border-radius: 10px;
    background: transparent;
    cursor: pointer;
}

.navitem:hover,
.navitem.active {
    background: var(--surface);
    border-color: var(--border);
}

.content {
    padding: 28px;
}

.card {
    display: none;
    max-width: 860px;
    background: var(--surface-strong);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px;
    backdrop-filter: blur(8px);
    box-shadow: var(--shadow);
    animation: rise .22s ease;
}

.card.active { display: block; }

@keyframes rise {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}

h2 {
    margin: 0 0 8px;
    font-size: 24px;
}

p.lead {
    margin: 0 0 20px;
    color: var(--muted);
}

.row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 14px;
    align-items: center;
    padding: 14px 0;
    border-top: 1px solid var(--border);
}

.row:first-of-type { border-top: 0; }

.label {
    font-size: 14px;
    font-weight: 600;
}

.help {
    font-size: 13px;
    color: var(--muted);
    margin-top: 4px;
}

.controls {
    display: flex;
    gap: 8px;
    align-items: center;
}

button,
select,
input.shortcut {
    height: 36px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    font-size: 14px;
    padding: 0 12px;
}

input.shortcut {
    width: 170px;
}

button {
    cursor: pointer;
}

button:hover,
select:hover,
input.shortcut:hover,
input.shortcut:focus {
    background: rgba(255, 255, 255, 0.18);
}

button.primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    border-color: transparent;
    color: #001017;
    font-weight: 700;
}

button.danger {
    border-color: rgba(251, 113, 133, 0.55);
    color: #ffe3e7;
    background: rgba(251, 113, 133, 0.16);
}

.toggle {
    position: relative;
    width: 52px;
    height: 30px;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--surface);
    cursor: pointer;
}

.toggle::after {
    content: "";
    position: absolute;
    top: 3px;
    left: 3px;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #ffffff;
    transition: transform .18s ease;
}

.toggle.on {
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
}

.toggle.on::after {
    transform: translateX(22px);
}

.toast {
    position: fixed;
    right: 16px;
    bottom: 16px;
    padding: 10px 14px;
    border-radius: 10px;
    background: #0f172a;
    color: #eff6ff;
    border: 1px solid rgba(255,255,255,0.2);
    opacity: 0;
    transform: translateY(6px);
    pointer-events: none;
    transition: .2s;
}

.toast.show {
    opacity: 1;
    transform: translateY(0);
}

@media (max-width: 860px) {
    .layout {
        grid-template-columns: 1fr;
    }

    .sidebar {
        border-right: 0;
        border-bottom: 1px solid var(--border);
    }

    .content {
        padding: 18px;
    }

    .row {
        grid-template-columns: 1fr;
    }

    .controls {
        flex-wrap: wrap;
    }
}
</style>
</head>

<body>
<div class="layout">
    <aside class="sidebar">
        <h1 class="brand">Настройки Horaizan</h1>
        <p class="subtitle">Персонализация, приватность и управление</p>

        <button class="navitem active" onclick="openSection('general', this)">Общие</button>
        <button class="navitem" onclick="openSection('privacy', this)">Приватность</button>
        <button class="navitem" onclick="openSection('shortcuts', this)">Горячие клавиши</button>
    </aside>

    <main class="content">
        <section id="general" class="card active">
            <h2>Общие</h2>
            <p class="lead">Внешний вид, поиск и старт новой вкладки.</p>

            <div class="row">
                <div>
                    <div class="label">Тема</div>
                    <div class="help">Системная тема подстраивается под тему ОС.</div>
                </div>
                <div class="controls">
                    <button id="theme-system" onclick="setTheme('system')">Системная</button>
                    <button id="theme-dark" onclick="setTheme('dark')">Тёмная</button>
                    <button id="theme-light" onclick="setTheme('light')">Светлая</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Поисковая система</div>
                    <div class="help">Используется для поисковых запросов из адресной строки.</div>
                </div>
                <div class="controls">
                    <select id="search" onchange="setSearchEngine(this.value)">
                        <option value="Google">Google</option>
                        <option value="Yandex">Yandex</option>
                        <option value="Bing">Bing</option>
                        <option value="DuckDuckGo">DuckDuckGo</option>
                    </select>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Новая вкладка</div>
                    <div class="help">Выберите, что открывать при создании вкладки.</div>
                </div>
                <div class="controls">
                    <select id="new-tab" onchange="setNewTabMode(this.value)">
                        <option value="home">Домашняя страница</option>
                        <option value="blank">Пустая страница</option>
                    </select>
                </div>
            </div>
        </section>

        <section id="privacy" class="card">
            <h2>Приватность</h2>
            <p class="lead">Управление очисткой данных и восстановлением параметров.</p>

            <div class="row">
                <div>
                    <div class="label">Подтверждать очистку данных</div>
                    <div class="help">Перед очисткой cookies и кеша выводить диалог подтверждения.</div>
                </div>
                <div class="controls">
                    <button id="confirm-toggle" class="toggle" onclick="toggleConfirmClear()" aria-label="Подтверждение очистки"></button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Очистить данные браузера</div>
                    <div class="help">Удаляет cookies и HTTP кеш.</div>
                </div>
                <div class="controls">
                    <button class="danger" onclick="clearData()">Очистить данные</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Окно инкогнито</div>
                    <div class="help">Открывает отдельное приватное окно без сохранения истории и cookies на диск.</div>
                </div>
                <div class="controls">
                    <button onclick="openIncognito()">Открыть инкогнито</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Сброс настроек</div>
                    <div class="help">Вернуть все настройки (включая горячие клавиши) к значениям по умолчанию.</div>
                </div>
                <div class="controls">
                    <button class="primary" onclick="resetSettings()">Сбросить всё</button>
                </div>
            </div>
        </section>

        <section id="shortcuts" class="card">
            <h2>Горячие клавиши</h2>
            <p class="lead">Нажмите в поле и введите комбинацию. Потом нажмите «Сохранить».</p>

            <div class="row">
                <div>
                    <div class="label">Новая вкладка</div>
                    <div class="help">Действие: создать новую вкладку.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-new_tab" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('new_tab')">Сохранить</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Новое окно инкогнито</div>
                    <div class="help">Действие: открыть отдельное приватное окно.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-open_incognito" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('open_incognito')">Сохранить</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Закрыть вкладку</div>
                    <div class="help">Действие: закрыть текущую вкладку.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-close_tab" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('close_tab')">Сохранить</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Перезагрузка страницы</div>
                    <div class="help">Действие: перезагрузить текущую страницу.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-reload" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('reload')">Сохранить</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Фокус адресной строки</div>
                    <div class="help">Действие: перейти в адресную строку.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-focus_address" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('focus_address')">Сохранить</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Открыть настройки</div>
                    <div class="help">Действие: открыть страницу настроек.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-open_settings" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('open_settings')">Сохранить</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Назад</div>
                    <div class="help">Действие: перейти назад по истории.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-back" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('back')">Сохранить</button>
                </div>
            </div>

            <div class="row">
                <div>
                    <div class="label">Вперёд</div>
                    <div class="help">Действие: перейти вперёд по истории.</div>
                </div>
                <div class="controls">
                    <input id="shortcut-forward" class="shortcut" type="text" value="" onkeydown="captureShortcut(event, this)">
                    <button onclick="saveShortcut('forward')">Сохранить</button>
                    <button class="primary" onclick="resetShortcuts()">Сбросить клавиши</button>
                </div>
            </div>
        </section>
    </main>
</div>

<div id="toast" class="toast"></div>

<script>
let bridge = null;
let currentThemeMode = 'dark';
let confirmClearDataEnabled = true;

const shortcutActions = [
    'new_tab',
    'open_incognito',
    'close_tab',
    'reload',
    'focus_address',
    'open_settings',
    'back',
    'forward',
];

function toast(message) {
    const el = document.getElementById('toast');
    el.textContent = message;
    el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 1700);
}

function openSection(id, trigger) {
    document.querySelectorAll('.card').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.navitem').forEach(el => el.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    if (trigger) trigger.classList.add('active');
}

function applyThemeVisual(mode, effectiveTheme) {
    currentThemeMode = mode;
    document.body.classList.toggle('light', effectiveTheme === 'light');

    document.getElementById('theme-system').classList.toggle('primary', mode === 'system');
    document.getElementById('theme-dark').classList.toggle('primary', mode === 'dark');
    document.getElementById('theme-light').classList.toggle('primary', mode === 'light');
}

function updateConfirmToggle() {
    const btn = document.getElementById('confirm-toggle');
    btn.classList.toggle('on', confirmClearDataEnabled);
}

function loadShortcuts() {
    if (!bridge) return;
    bridge.getShortcuts(function(raw) {
        let shortcuts = {};
        try {
            shortcuts = JSON.parse(raw || '{}');
        } catch (e) {
            shortcuts = {};
        }

        shortcutActions.forEach(action => {
            const el = document.getElementById('shortcut-' + action);
            if (el) el.value = shortcuts[action] || '';
        });
    });
}

new QWebChannel(qt.webChannelTransport, function(channel) {
    bridge = channel.objects.bridge;

    bridge.getTheme(function(mode) {
        bridge.getEffectiveTheme(function(effectiveTheme) {
            applyThemeVisual(mode, effectiveTheme);
        });
    });

    bridge.getSearchEngine(function(engine) {
        const select = document.getElementById('search');
        if (select) select.value = engine;
    });

    bridge.getNewTabMode(function(mode) {
        const select = document.getElementById('new-tab');
        if (select) select.value = mode;
    });

    bridge.getConfirmClearData(function(enabled) {
        confirmClearDataEnabled = !!enabled;
        updateConfirmToggle();
    });

    loadShortcuts();
});

function setTheme(value) {
    if (!bridge) return;
    bridge.setTheme(value);
    bridge.getEffectiveTheme(function(effectiveTheme) {
        applyThemeVisual(value, effectiveTheme);
    });
    toast('Тема изменена');
}

function setSearchEngine(value) {
    if (!bridge) return;
    bridge.setSearchEngine(value);
    toast('Поисковая система сохранена');
}

function setNewTabMode(value) {
    if (!bridge) return;
    bridge.setNewTabMode(value);
    toast('Параметр новой вкладки сохранён');
}

function toggleConfirmClear() {
    if (!bridge) return;
    confirmClearDataEnabled = !confirmClearDataEnabled;
    bridge.setConfirmClearData(confirmClearDataEnabled);
    updateConfirmToggle();
    toast(confirmClearDataEnabled ? 'Подтверждение включено' : 'Подтверждение выключено');
}

function clearData() {
    if (!bridge) return;
    if (confirmClearDataEnabled && !confirm('Очистить cookies и кеш?')) {
        return;
    }

    bridge.clearData();
    toast('Cookies и кеш очищены');
}

function openIncognito() {
    if (!bridge) return;
    bridge.openIncognitoWindow();
    toast('Окно инкогнито открыто');
}

function captureShortcut(event, input) {
    event.preventDefault();

    if (event.key === 'Escape') {
        input.blur();
        return;
    }

    const sequence = eventToShortcut(event);
    if (sequence) {
        input.value = sequence;
    }
}

function eventToShortcut(event) {
    const key = normalizeKey(event.key);
    const isModifier = ['Ctrl', 'Alt', 'Shift', 'Meta'].includes(key);
    if (isModifier) return '';

    const parts = [];
    if (event.ctrlKey) parts.push('Ctrl');
    if (event.altKey) parts.push('Alt');
    if (event.shiftKey) parts.push('Shift');
    if (event.metaKey) parts.push('Meta');

    if (!key) return '';
    parts.push(key);

    return parts.join('+');
}

function normalizeKey(key) {
    if (!key) return '';

    const aliases = {
        Control: 'Ctrl',
        Alt: 'Alt',
        Shift: 'Shift',
        Meta: 'Meta',
        ArrowLeft: 'Left',
        ArrowRight: 'Right',
        ArrowUp: 'Up',
        ArrowDown: 'Down',
        ' ': 'Space',
        Escape: 'Esc',
        Enter: 'Enter',
        Tab: 'Tab',
        Backspace: 'Backspace',
        Delete: 'Delete',
        Home: 'Home',
        End: 'End',
        PageUp: 'PgUp',
        PageDown: 'PgDown',
    };

    if (aliases[key]) return aliases[key];
    if (key.length === 1) return key.toUpperCase();
    return key;
}

function saveShortcut(action) {
    if (!bridge) return;

    const input = document.getElementById('shortcut-' + action);
    if (!input) return;

    const value = input.value.trim();
    if (!value) {
        toast('Комбинация не может быть пустой');
        return;
    }

    bridge.setShortcut(action, value, function(ok) {
        if (!ok) {
            toast('Не удалось сохранить сочетание');
            return;
        }

        loadShortcuts();
        toast('Горячая клавиша сохранена');
    });
}

function resetShortcuts() {
    if (!bridge) return;
    if (!confirm('Сбросить горячие клавиши к значениям по умолчанию?')) {
        return;
    }

    bridge.resetShortcuts();
    loadShortcuts();
    toast('Горячие клавиши сброшены');
}

function resetSettings() {
    if (!bridge) return;
    if (!confirm('Сбросить все настройки к значениям по умолчанию?')) {
        return;
    }

    bridge.resetSettings();

    bridge.getTheme(function(mode) {
        bridge.getEffectiveTheme(function(effectiveTheme) {
            applyThemeVisual(mode, effectiveTheme);
        });
    });

    bridge.getSearchEngine(function(engine) {
        document.getElementById('search').value = engine;
    });

    bridge.getNewTabMode(function(mode) {
        document.getElementById('new-tab').value = mode;
    });

    bridge.getConfirmClearData(function(enabled) {
        confirmClearDataEnabled = !!enabled;
        updateConfirmToggle();
    });

    loadShortcuts();
    toast('Настройки сброшены');
}
</script>
</body>
</html>
"""
