new QWebChannel(qt.webChannelTransport, channel => {
    window.bridge = channel.objects.bridge;

    bridge.getTheme(theme => {
        document.body.classList.toggle("light", theme === "light");
        document.getElementById("theme").value = theme;
    });

    bridge.getSearchEngine(engine => {
        document.getElementById("search").value = engine;
    });
});

document.getElementById("theme").onchange = e =>
    bridge.setTheme(e.target.value);

document.getElementById("search").onchange = e =>
    bridge.setSearchEngine(e.target.value);

document.getElementById("clear").onclick = () =>
    bridge.clearData();
