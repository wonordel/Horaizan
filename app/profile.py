from PySide6.QtWebEngineCore import QWebEngineProfile
from pathlib import Path


def create_profile():
    data_path = Path.home() / ".config" / "horaizan"
    data_path.mkdir(parents=True, exist_ok=True)

    profile = QWebEngineProfile("Horaizan", None)
    profile.setPersistentStoragePath(str(data_path))
    profile.setCachePath(str(data_path / "cache"))
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.ForcePersistentCookies
    )

    return profile

