from pathlib import Path

from django.core.exceptions import SuspiciousFileOperation
from django.template import Origin, TemplateDoesNotExist
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django.utils._os import safe_join

from . import themes


class Loader(FilesystemLoader):
    def get_template_sources(self, template_name):
        template_path = template_name.split(";")
        if (
            len(template_path) == 3
            and template_path[0] == "themes"
            and template_path[1] in themes
        ):
            theme_info = themes[template_path[1]]
            try:
                name = safe_join(theme_info["path"] / "templates", template_path[2])
            except SuspiciousFileOperation:
                return

            yield Origin(
                name=name,
                template_name=template_name,
                loader=self,
            )
