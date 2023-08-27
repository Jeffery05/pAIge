from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.filter
def pfpfb(fieldfile):
    if fieldfile:
        return fieldfile.url
    else:
        return static(settings.PORTFOLIO_PFP_FALLBACK)
