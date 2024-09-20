from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^api/v1/persons$', views.person_api),
    re_path(r'^api/v1/persons/([0-9]+)$', views.person_api),
]
