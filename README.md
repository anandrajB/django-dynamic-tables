# Django Dynamic Table

### Dynamic table creation in django app

##### **refer** : https://docs.djangoproject.com/en/5.0/ref/schema-editor/

## Authors

- [@anandrajB](https://github.com/anandrajB)

## Prerequisite

- python
- Django
- Django-rest-framework

## 1. Installation

### 1.1 Initial setup

- Install finflo using [pip](https://pypi.org/project/finflo/)

```bash

pip install finflo

```

- In your django application , browse to installed_apps section in settings.py and add this ,

```bash

INSTALLED_APPS = [

    'djdynatable',

    'rest_framework'

]

```

- Now add urls in urls.py

```

urlpatterns = [

    path('', include('djdynatable.urls'))

]

```

### 1.2 Migrations

- once all the steps done from the above section 1.1 .
- now we can apply the migrations for the database using ,

```

- python manage.py makemigrations

```

```

- python manage.py migrate 

```
