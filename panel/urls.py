from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about", views.AboutView.as_view(), name="about"),
    path("generate", views.GenerateView.as_view(), name="generate"),
    path("submitted", views.SubmittedView.as_view(), name="submitted"),
]
