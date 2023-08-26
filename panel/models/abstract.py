from django.db import models

from .. import utils


class PortfolioItem(models.Model):
    portfolio = models.ForeignKey("PortfolioSite", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PortfolioItemAuthor(models.Model):
    author = models.CharField(max_length=256)

    class Meta:
        abstract = True


class PortfolioItemTitle(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        abstract = True


class PortfolioItemDescription(models.Model):
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class PortfolioItemTitleDescription(PortfolioItemTitle, PortfolioItemDescription):
    class Meta:
        abstract = True


class PortfolioItemOrganization(models.Model):
    organization = models.CharField(max_length=256)

    class Meta:
        abstract = True


class PortfolioItemDuration(models.Model):
    starts_at = models.DateField()
    ends_at = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class PortfolioItemDate(models.Model):
    date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class PortfolioItemURL(models.Model):
    url = models.URLField()

    class Meta:
        abstract = True


class PortfolioItemNumber(models.Model):
    number = models.CharField(max_length=128, blank=True)

    class Meta:
        abstract = True


def logo_upload_path(instance, filename):
    return utils.file_upload_path_generator("logo")(instance, filename)


class PortfolioItemLogo(models.Model):
    logo = models.ImageField(upload_to=logo_upload_path, blank=True)

    class Meta:
        abstract = True


def image_upload_path(instance, filename):
    return utils.file_upload_path_generator("image")(instance, filename)


class PortfolioItemImage(models.Model):
    image = models.ImageField(upload_to=image_upload_path, blank=True)

    class Meta:
        abstract = True
