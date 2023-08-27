from django.urls import path

from ..abstract.urls import development_media_files
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("experience", views.ExpView.as_view(), name="experience"),
    path("awards", views.AwardsView.as_view(), name="awards"),
    path("contact", views.ContactView.as_view(), name="contact"),
] + development_media_files()
