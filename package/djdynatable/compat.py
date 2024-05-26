import os
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS
from django.db import connections
import subprocess
from typing import NoReturn, List

BASE_SCHEMA_NAME = "public"
DJANGO_PROJECT_NAME = None


def compatability_check():
    try:
        global DJANGO_PROJECT_NAME
        DJANGO_PROJECT_NAME = os.environ.get("DJANGO_SETTINGS_MODULE").split(".")[0]
        global BASE_SCHEMA_NAME
    except Exception as e:
        raise ImproperlyConfigured(
            "DJANGO_SETTINGS_MODULE environment variable is not set."
        ) from e


# def set_schema_name(self):
#     connection = connections[DEFAULT_DB_ALIAS]
#     with connection.cursor() as cursor:
#         cursor.execute(f"CREATE SCHEMA IF NOT EXISTS sample")
#         cursor.execute(f"SET search_path = sample, public")
#         cursor.execute(f"SET SCHEMA = sample")


def drop_schema_name(schema_name) -> NoReturn:
    connection = connections[DEFAULT_DB_ALIAS]
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name}")
        cursor.execute(f"SET search_path = {BASE_SCHEMA_NAME}, public")
        cursor.execute(f"SET SCHEMA = {BASE_SCHEMA_NAME}")


def drop_schema(schema_name: str) -> NoReturn:
    connection = connections["default"]

    with connection.cursor() as cursor:
        cursor.execute(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE;')
        cursor.execute("SET search_path = public, public")


def base(command: str, input_args: List[str]):
    process = subprocess.Popen(
        ["python", "manage.py", f"{command}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for data in input_args:
        process.stdin.write(data)
        process.stdin.flush()
    stdout, stderr = process.communicate()


def create_tenant(schema_name, user_id):
    base(
        command="create_tenant",
        input_args=[
            f"{schema_name}\n".encode(),
            f"{user_id}\n".encode(),
            f"{user_id}\n".encode(),
            b"True",
        ],
    )


def delete_tenant(schema_name) -> NoReturn:
    base(
        command="delete_tenant",
        input_args=[f"{schema_name}\n".encode(), b"\n", b"yes\n"],
    )
