from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("generate/", views.GenerateView.as_view(), name="generate"),
    path("preview/", views.PreviewView.as_view(), name="preview"),
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "portfolio/<int:pk>/edit",
        views.PortfolioEditView.as_view(),
        name="portfolio_edit",
    ),
]
