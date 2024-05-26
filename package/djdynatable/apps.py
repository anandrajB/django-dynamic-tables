from django.apps import AppConfig

from .compat import compatability_check


class TablesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tables"

    def ready(self) -> None:
        return compatability_check()
