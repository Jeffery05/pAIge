from django.urls import path

from ..abstract.urls import development_media_files
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
] + development_media_files()
