from django.views.generic.base import TemplateView

# Create your views here.


class IndexView(TemplateView):
    template_name = "themes;josh;index.html"


class ExpView(TemplateView):
    template_name = "themes;josh;experience.html"


class AwardsView(TemplateView):
    template_name = "themes;josh;awards.html"


class ContactView(TemplateView):
    template_name = "themes;josh;contact.html"
