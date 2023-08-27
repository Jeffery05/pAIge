from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import FormView

from . import forms, models, utils
from .models import Portfolio


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
    success_url = "/preview"

    def form_valid(self, form):
        portfolio = Portfolio.create_from_profile(form.cleaned_data["profile_url"])
        self.request.session["anonymous_site_generated"] = portfolio.pk

        return super().form_valid(form)


class PreviewView(TemplateView, TitleMixin):
    template_name = "preview.html"
    title = "Preview your website!"

    def dispatch(self, request, *args, **kwargs):
        portfolio_pk = request.session.get("anonymous_site_generated")

        if not portfolio_pk:
            return redirect('generate')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio_pk = self.request.session.get("anonymous_site_generated")
        if portfolio_pk:
            context["portfolio"] = Portfolio.objects.get(pk=portfolio_pk)
        return context

class ProfileView(LoginRequiredMixin, ListView):
    context_object_name = "portfolios"
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        portfolio_pk = request.session.get("anonymous_site_generated")
        if portfolio_pk:
            del request.session["anonymous_site_generated"]

            portfolio = Portfolio.objects.get(pk=portfolio_pk)
            portfolio.assign_owner(request.user)
            
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return models.Portfolio.objects.filter(owner=self.request.user)