import json
import os
from pathlib import Path
from typing import Dict

_SUPPORTED = {"en", "ru"}

def _find_locale_path(lang: str) -> Path:
    """
    Ищем файл локали в двух местах:
    1) корневой репозиторий:   /locales/<lang>.json
    2) внутри пакета:          src/aip_runner/locales/<lang>.json   (fallback)
    """
    # /repo/locales/<lang>.json
    root_locales = Path(__file__).resolve().parents[2] / "locales" / f"{lang}.json"
    if root_locales.exists():
        return root_locales

    # /package/locales/<lang>.json
    pkg_locales = Path(__file__).resolve().parent / "locales" / f"{lang}.json"
    if pkg_locales.exists():
        return pkg_locales

    raise FileNotFoundError(f"Locale file not found for lang={lang}")

class I18n:
    def __init__(self, lang: str | None = None):
        # берём из аргумента, иначе из переменной окружения, иначе en
        selected = (lang or os.getenv("AIP_LANG", "en")).lower()
        if selected not in _SUPPORTED:
            selected = "en"
        self.lang = selected

        try:
            path = _find_locale_path(self.lang)
            self._dict: Dict[str, str] = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            # надёжный фоллбек на en
            self.lang = "en"
            path = _find_locale_path("en")
            self._dict = json.loads(path.read_text(encoding="utf-8"))

    def t(self, key: str, **kwargs) -> str:
        s = self._dict.get(key, key)
        if kwargs:
            try:
                s = s.format(**kwargs)
            except Exception:
                # не роняем CLI, если подстановка не удалась
                pass
        return s
