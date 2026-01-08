SETTINGS_HTML = r"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Настройки</title>

<!-- Qt WebChannel -->
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>

<style>
:root {
    --bg: #1c1b22;
    --panel: #2b2a33;
    --text: #ffffff;
    --accent: #00c2ff;
    --border: #3a3944;
}

body {
    margin: 0;
    height: 100vh;
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
}

.container {
    display: flex;
    height: 100%;
}

/* ===== SIDEBAR ===== */
.sidebar {
    width: 240px;
    background: var(--panel);
    padding: 20px;
    box-sizing: border-box;
}

.sidebar h1 {
    font-size: 18px;
    margin: 0 0 20px 0;
}

/* ===== CONTENT ===== */
.content {
    flex: 1;
    padding: 30px;
    box-sizing: border-box;
}

.section {
    max-width: 640px;
}

.section h2 {
    margin-top: 0;
    font-size: 22px;
}

.option {
    margin-bottom: 24px;
}

label {
    display: block;
    margin-bottom: 8px;
    opacity: 0.9;
}

/* ===== CONTROLS ===== */
button {
    background: var(--panel);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 14px;
    cursor: pointer;
    margin-right: 8px;
}

button:hover {
    background: #3a3944;
}

button.primary {
    background: var(--accent);
    color: #000;
    border: none;
}

select {
    background: var(--panel);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 14px;
}
</style>
</head>

<body>

<div class="container">

    <!-- SIDEBAR -->
    <div class="sidebar">
        <h1>Настройки</h1>
    </div>

    <!-- CONTENT -->
    <div class="content">
        <div class="section">

            <h2>Основные</h2>

            <!-- THEME -->
            <div class="option">
                <label>Тема</label>
                <button onclick="setTheme('dark')">Тёмная</button>
                <button onclick="setTheme('light')">Светлая</button>

            </div>

            <!-- SEARCH ENGINE -->
            <div class="option">
                <label>Поисковая система</label>
                <select onchange="setSearchEngine(this.value)" id="search">
                    <option value="Google">Google</option>
                    <option value="Yandex">Yandex</option>
                    <option value="Bing">Bing</option>
                    <option value="DuckDuckGo">DuckDuckGo</option>
                </select>

            </div>

            <!-- CLEAR DATA -->
            <div class="option">
                <label>Данные браузера</label>
               <button onclick="clearData()">Очистить cookies и кеш</button>
                </button>
            </div>

        </div>
    </div>

</div>

<script>
let bridge = null;

new QWebChannel(qt.webChannelTransport, function (channel) {
    bridge = channel.objects.bridge;
    console.log("Bridge ready:", bridge);

    bridge.getTheme(function (theme) {
        console.log("Current theme:", theme);
    });

    bridge.getSearchEngine(function (engine) {
        console.log("Current search engine:", engine);
        const select = document.getElementById("search");
        if (select) select.value = engine;
    });
});

/* ===== THEME ===== */
function setTheme(value) {
    if (!bridge) return;
    bridge.setTheme(value);
}

/* ===== SEARCH ENGINE ===== */
function setSearchEngine(value) {
    if (!bridge) return;
    bridge.setSearchEngine(value);
}

/* ===== CLEAR DATA ===== */
function clearData() {
    if (!bridge) return;
    bridge.clearData();
    alert("Cookies и кеш очищены");
}

</script>

</body>
</html>
"""
