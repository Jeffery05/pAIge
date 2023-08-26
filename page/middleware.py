from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import DisallowedHost

from page.themes import themes
from panel.models import Portfolio, User


class PortfolioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            site = get_current_site(request)

            try:
                page_theme_name = site.portfolio.theme

                request.urlconf = f'{themes[page_theme_name]["module_name"]}.urls'

                request.portfolio = site.portfolio
            except Site.portfolio.RelatedObjectDoesNotExist:
                if settings.DEBUG_PORTFOLIO_ID is not None:
                    request.portfolio = Portfolio.objects.get(
                        pk=settings.DEBUG_PORTFOLIO_ID
                    )

                    request.urlconf = (
                        f'{themes[request.portfolio.theme]["module_name"]}.urls'
                    )

        except Site.DoesNotExist:
            raise DisallowedHost("Unknown host")

        return self.get_response(request)

    def process_template_response(self, request, response):
        if hasattr(request, "portfolio"):
            response.context_data["portfolio"] = request.portfolio

        return response
