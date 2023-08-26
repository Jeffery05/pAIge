import importlib
from pathlib import Path

from django.conf import settings

themes = {}

for theme in settings.INSTALLED_THEMES:
    theme_module = importlib.import_module(theme)
    theme_name = theme.split(".")[-1]

    themes[theme_name] = {
        "module_name": theme,
        "theme_name": theme_name,
        "path": Path(theme_module.__file__).resolve().parent,
        "module": theme_module,
    }
