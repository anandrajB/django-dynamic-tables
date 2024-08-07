from django.contrib import admin

# Register your models here.
from ....djdynatable.models import SchemaModel

admin.site.register(SchemaModel)