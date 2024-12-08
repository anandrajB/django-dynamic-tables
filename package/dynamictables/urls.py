from django.urls import path

# from rest_framework import routers
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/table/", views.TableListCreateApiView.as_view()),
    path("api/table/<str:table_name>/", views.TableUpdateDeleteApiView.as_view()),
    path("api/row/<str:table_name>/", views.RowListCreateUpdateDeleteApiView.as_view()),
    path("api/fields/", views.FieldListApiview.as_view()),
]
