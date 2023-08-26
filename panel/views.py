from django.shortcuts import render
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import FormView

from . import forms, utils
from .models import PortfolioSite


class TitleMixin(ContextMixin):
    title = ""

    def get_title(self):
        return self.title

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context


class IndexView(TemplateView, TitleMixin):
    template_name = "index.html"
    title = "Home"


class AboutView(TemplateView, TitleMixin):
    template_name = "about.html"
    title = "About"


class GenerateView(FormView, TitleMixin):
    template_name = "generate.html"
    form_class = forms.CreateSiteForm
    title = "Generate"
    success_url = "/submitted"

    def form_valid(self, form):
        PortfolioSite.create_from_profile(form.cleaned_data["profile_url"])

        return super().form_valid(form)


class SubmittedView(TemplateView, TitleMixin):
    template_name = "submitted.html"
    title = "Submitted"
