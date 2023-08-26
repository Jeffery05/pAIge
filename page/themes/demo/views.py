from django.views.generic.base import TemplateView

# Create your views here.


class IndexView(TemplateView):
    template_name = "themes:demo:index.html"
    title = "Home"
