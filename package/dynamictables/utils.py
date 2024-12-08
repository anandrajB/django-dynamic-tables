from functools import wraps

from rest_framework.authtoken.models import Token

import importlib.util
import contextlib


with contextlib.suppress(Exception):
    from django_tenants.utils import schema_context


def check_dependencies():
    """checks for django-tenants else keeps in public schema"""
    return bool(importlib.util.find_spec("django-tenants"))


def schema_aware(schema_name_getter):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            schema_name = schema_name_getter(self)
            if schema_name and check_dependencies():
                with schema_context(schema_name):
                    return func(self, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)

        return wrapper

    return decorator


class BaseDispath:
    def dispatch(self, request, *args, **kwargs):
        with contextlib.suppress(Exception):
            self.schema_name = str(
                Token.objects.get(
                    key=request.headers["Authorization"].split(" ")[1]
                ).user.id
            )
        self.schema_name = self.request.user.id
        return super().dispatch(request, *args, **kwargs)
