SETTINGS_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Settings</title>

<script src="qrc:///qtwebchannel/qwebchannel.js"></script>

<style>
:root {
    --bg: #1c1b22;
    --panel: #2b2a33;
    --text: #ffffff;
    --accent: #00c2ff;
}

body {
    margin: 0;
    font-family: system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
}

.container {
    display: flex;
    height: 100vh;
}

.sidebar {
    width: 220px;
    background: var(--panel);
    padding: 20px;
}

.content {
    flex: 1;
    padding: 30px;
}

.option {
    margin-bottom: 20px;
}
</style>
</head>

<body>
<div class="container">

<div class="sidebar">
    <h3>Настройки</h3>
</div>

<div class="content">
    <div class="option">
        <label>
            <input type="checkbox" id="themeToggle">
            Тёмная тема
        </label>
    </div>

    <div class="option">
        <label>Поисковая система</label><br><br>
        <select id="search">
            <option>Google</option>
            <option>Yandex</option>
            <option>Bing</option>
            <option>DuckDuckGo</option>
        </select>
    </div>

    <div class="option">
        <button onclick="settings.clearData()">
            Очистить cookies и кеш
        </button>
    </div>
</div>

</div>

<script>
new QWebChannel(qt.webChannelTransport, function(channel) {
    window.settings = channel.objects.settings;

    document.getElementById("themeToggle").onchange = function() {
        settings.setDarkTheme(this.checked);
    };

    document.getElementById("search").onchange = function() {
        settings.setSearchEngine(this.value);
    };
});
</script>
</body>
</html>
"""
