from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    occupation = models.CharField(max_length=256, blank=True)
    headline = models.CharField(max_length=256, blank=True)

    country = models.CharField(max_length=2, blank=True)

    description = models.TextField(blank=True)

    pfp = models.ImageField(upload_to='portfolio_site_images', blank=True)
    source_url = models.URLField()

class PortfolioExperience(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    starts_at = models.DateField()
    ends_at = models.DateField(blank=True)

    organization = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    
    description = models.TextField(blank=True)

class PortfolioEducation(PortfolioExperience):
    school = models.CharField(max_length=256)
    degree = models.CharField(max_length=256, blank=True)
    field = models.CharField(max_length=256, blank=True)

    activities_societies = models.TextField()

    logo = models.ImageField(upload_to='portfolio_site_images', blank=True)

from django.db import models


class PortfolioAccomplishment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    class Meta:
        abstract = True

class PortfolioAccomplishmentIssuer(models.Model):
    issuer = models.CharField(max_length=256)
    issued_at = models.DateField(blank=True)

    class Meta:
        abstract = True

class PortfolioHonorsAwards(PortfolioAccomplishmentIssuer):
    pass
class PortfolioTestScore(PortfolioAccomplishmentIssuer):
    score = models.IntegerField()