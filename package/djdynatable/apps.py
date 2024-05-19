from django.apps import AppConfig


class TablesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tables"

    # def ready(self) -> None:
    #     return self.set_schema_name()

    # def set_schema_name(self):
    #     connection = connections[DEFAULT_DB_ALIAS]
    #     with connection.cursor() as cursor:
    #         cursor.execute(f"CREATE SCHEMA IF NOT EXISTS sample")
    #         cursor.execute(f"SET search_path = sample, public")
    #         cursor.execute(f"SET SCHEMA = sample")
