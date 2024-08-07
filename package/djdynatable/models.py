from django.db import models
from django.utils import timezone
import datetime
import uuid
from rest_framework import serializers
import contextlib
from django.conf import settings

Generated_model_objects = {}

DJANGO_FIELD_MAP = {
    "boolean": ("django.db.models", "BooleanField"),
    "chat": ("django.db.models", "CharField"),
    "datefiel": ("django.db.models", "DateField"),
    "datetimefield": ("django.db.models", "DatetimeField"),
    "integer": ("django.db.models", "IntegerField"),
    "positiveinteger": ("django.db.models", "PositiveIntegerField"),
    "text": ("django.db.models", "TextField"),
    "timefield": ("django.db.models", "TimeField"),
    "urlfield": ("django.db.models", "UrlField"),
    "foreignkey": ("django.db.models", "ForeignKey"),
    "onetoonefield": ("django.db.models", "OneToOneField"),
    "manytomanyfield": ("django.db.models", "ManyToManyField"),
}


DEFAULT_FIELD_TYPES = {
    "string": models.CharField,
    "number": models.IntegerField,
    "boolean": models.BooleanField,
    "date": models.DateField,
    "datetime": models.DateTimeField,
    "positiveinteger": models.PositiveIntegerField,
    "text": models.TextField,
    "time": models.TimeField,
    "email": models.EmailField,
    "url": models.URLField,
    "uuid": models.UUIDField,
    "foreignkey": models.ForeignKey,
    "onetoonefield": models.OneToOneField,
    "manytomanyfield": models.ManyToManyField,
}


DEFAULT_SERIALIZER_FIELD_TYPES = {
    "string": serializers.CharField,
    "number": serializers.IntegerField,
    "boolean": serializers.BooleanField,
    "date": serializers.DateField,
    "datetime": serializers.DateTimeField,
    "positiveinteger": serializers.IntegerField,
    "text": serializers.CharField,
    "time": serializers.TimeField,
    "email": serializers.EmailField,
    "url": serializers.URLField,
    "uuid": serializers.UUIDField,
    "foreignkey": serializers.PrimaryKeyRelatedField,
}


RELATIONSHIP_FIELD_OPTIONS = {
    "to": "self",
    "on_delete": models.DO_NOTHING,
    "blank": True,
    "null": True,
}

DEFAULT_BLANK_FIELD_OPTIONS = {
    "default": "",
    "blank": True,
}

DEFAULT_SERIALIZER_OPTIONS = {"allow_null": True}

RELATIONSHIP_FIELD = ["foreignkey", "onetoonefield", "manytomanyfield"]


EXTRA_MODEL_ATTRS = {
    "string": {"editable": bool, "unique": bool},
    "integer": {"editable": bool, "unique": bool, "db_index": bool},
    "text": {"editable": bool, "unique": bool, "db_index": bool},
}


DEFAULT_MODEL_ATTRS = {
    "string": {"max_length": 1024, "blank": True, "null": True},
    "number": {"blank": True, "null": True},
    "boolean": {"default": False, "blank": True, "null": True},
    "date": {"default": datetime.date.today},
    "datetime": {"default": datetime.datetime.now},
    "positiveinteger": {"default": 0},
    "text": DEFAULT_BLANK_FIELD_OPTIONS,
    "time": {"default": timezone.now},
    "email": DEFAULT_BLANK_FIELD_OPTIONS,
    "url": DEFAULT_BLANK_FIELD_OPTIONS,
    "uuid": {"default": uuid.uuid4},
    "foreignkey": RELATIONSHIP_FIELD_OPTIONS,
    "onetoonefield": RELATIONSHIP_FIELD_OPTIONS,
    "manytomanyfield": RELATIONSHIP_FIELD_OPTIONS,
}


DEFAULT_SERIALIZER_ATTRS = {
    "string": DEFAULT_SERIALIZER_OPTIONS,
    "number": DEFAULT_SERIALIZER_OPTIONS,
    "boolean": DEFAULT_SERIALIZER_OPTIONS,
    "date": {
        "default": datetime.date.today,
        **DEFAULT_SERIALIZER_OPTIONS,
    },
    "datetime": {
        "default": datetime.datetime.now,
        **DEFAULT_SERIALIZER_OPTIONS,
    },
    "positiveinteger": {"default": 0, "allow_null": True},
    "text": DEFAULT_SERIALIZER_OPTIONS,
    "time": {"default": timezone.now},
    "email": DEFAULT_SERIALIZER_OPTIONS,
    "url": DEFAULT_SERIALIZER_OPTIONS,
    "uuid": {"default": uuid.uuid4},
    "foreignkey": RELATIONSHIP_FIELD_OPTIONS,
    "onetoonefield": RELATIONSHIP_FIELD_OPTIONS,
    "manytomanyfield": RELATIONSHIP_FIELD_OPTIONS,
}


DJANGO_FIELD_CHOICES = [
    ("Basic Fields", [(key, value[1]) for key, value in DJANGO_FIELD_MAP.items()])
]

from django.db import models


class SchemaModel(models.Model):
    table_name = models.CharField(max_length=1024, unique=True)
    columns = models.JSONField(help_text="column schema")

    @property
    def chunk_size(self):
        return SchemaModel.objects.all().count()


class Fields(models.Model):
    field_type = models.CharField(max_length=1024, unique=True)
