from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PortfolioSite, User

admin.site.register(User, UserAdmin)
admin.site.register(PortfolioSite)
