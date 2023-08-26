from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.base import ContextMixin

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

class GenerateView(TemplateView, TitleMixin):
    template_name = "generator.html"
    title = "Generate"