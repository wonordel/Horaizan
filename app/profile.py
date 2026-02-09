from PySide6.QtWebEngineCore import QWebEngineProfile
from pathlib import Path


def create_profile(incognito: bool = False, parent=None):
    if incognito:
        profile = QWebEngineProfile(parent)
        profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
        profile.setPersistentCookiesPolicy(
            QWebEngineProfile.NoPersistentCookies
        )
        return profile

    data_path = Path.home() / ".config" / "horaizan"
    data_path.mkdir(parents=True, exist_ok=True)

    profile = QWebEngineProfile("Horaizan", parent)
    profile.setPersistentStoragePath(str(data_path))
    profile.setCachePath(str(data_path / "cache"))
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.ForcePersistentCookies
    )

    return profile
