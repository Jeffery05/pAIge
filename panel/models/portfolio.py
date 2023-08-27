import random
import secrets

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import models

from page.themes import themes

from .. import utils
from .abstract import (
    PortfolioItem,
    PortfolioItemAuthor,
    PortfolioItemDate,
    PortfolioItemDescription,
    PortfolioItemDuration,
    PortfolioItemImage,
    PortfolioItemLogo,
    PortfolioItemNumber,
    PortfolioItemOrganization,
    PortfolioItemTitle,
    PortfolioItemTitleDescription,
    PortfolioItemURL,
)
from .user import User


def pfp_upload_path(instance, filename):
    return utils.file_upload_path_generator("pfp")(instance, filename)


class Portfolio(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    site = models.OneToOneField(
        Site, related_name="portfolio", on_delete=models.RESTRICT
    )
    theme = models.CharField(max_length=16)

    linkedin_id = models.CharField(max_length=64)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    occupation = models.CharField(max_length=256, blank=True)
    headline = models.CharField(max_length=256, blank=True)

    country = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)

    gender = models.CharField(max_length=32, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    industry = models.CharField(max_length=64, blank=True)

    summary = models.TextField(blank=True)

    profile_pic = models.ImageField(upload_to=pfp_upload_path, blank=True)
    background_cover_image = models.ImageField(upload_to=pfp_upload_path, blank=True)
    source_url = models.URLField()

    @classmethod
    def create_from_profile(
        cls,
        linkedin_url,
        owner=None,
        domain=None,
        theme=None,
    ):
        if domain is None:
            domain = settings.PORTFOLIO_DOMAIN.format(secrets.token_hex(4))

        site = Site.objects.create(domain=domain, name=f"Portfolio {domain}")

        portfolio_data = utils.fetch_linkedin_profile(linkedin_url)
        profile_pic_url = portfolio_data["header"].pop("profile_pic_url")
        background_cover_url = portfolio_data["header"].pop("background_cover_url")

        if theme is None:
            theme = random.choice(list(themes.keys()))

        portfolio = cls.objects.create(
            owner=owner,
            source_url=linkedin_url,
            site=site,
            theme=theme,
            **portfolio_data["header"],
        )

        if profile_pic_url is not None:
            portfolio.profile_pic = utils.download_file(profile_pic_url)

        if background_cover_url is not None:
            portfolio.background_cover_image = utils.download_file(background_cover_url)

        portfolio.save()

        portfolio_logo_items = {
            "experiences": PortfolioExperience,
            "education": PortfolioEducation,
            "volunteer_work": PortfolioVolunteerWork,
        }

        portfolio_image_items = {
            "articles": PortfolioArticle,
        }

        portfolio_logoless_items = {
            "languages": PortfolioLanguage,
            "organizations": PortfolioOrganization,
            "publications": PortfolioPublication,
            "honors_awards": PortfolioHonorAward,
            "patents": PortfolioPatent,
            "courses": PortfolioCourse,
            "projects": PortfolioProject,
            "test_scores": PortfolioTestScore,
            "certifications": PortfolioCertification,
            "recommendations": PortfolioRecommendation,
            "interests": PortfolioInterest,
            "skills": PortfolioSkill,
        }

        for itemtype_name, itemtype_model in portfolio_logo_items.items():
            for item_data in portfolio_data[itemtype_name]:
                logo_url = item_data.pop("logo_url")

                item = itemtype_model.objects.create(portfolio=portfolio, **item_data)

                if logo_url is not None:
                    item.logo = utils.download_file(logo_url)

                item.save()

        for itemtype_name, itemtype_model in portfolio_image_items.items():
            for item_data in portfolio_data[itemtype_name]:
                image_url = item_data.pop("image_url")

                item = itemtype_model.objects.create(portfolio=portfolio, **item_data)

                if logo_url is not None:
                    item.image = utils.download_file(image_url)

                item.save()

        for itemtype_name, itemtype_model in portfolio_logoless_items.items():
            for item_data in portfolio_data[itemtype_name]:
                item = itemtype_model.objects.create(portfolio=portfolio, **item_data)

                item.save()

        return portfolio


class PortfolioExperience(
    PortfolioItem,
    PortfolioItemDuration,
    PortfolioItemOrganization,
    PortfolioItemTitleDescription,
    PortfolioItemURL,
    PortfolioItemLogo,
):
    location = models.CharField(max_length=256, blank=True)


class PortfolioEducation(
    PortfolioItem,
    PortfolioItemDuration,
    PortfolioItemOrganization,
    PortfolioItemTitleDescription,
    PortfolioItemURL,
    PortfolioItemLogo,
):
    field = models.CharField(max_length=256, blank=True)
    grade = models.CharField(max_length=256, blank=True)
    activities_societies = models.TextField()

    @property
    def school(self):
        return self.organization

    @property
    def degree(self):
        return self.title


class PortfolioLanguage(PortfolioItem, PortfolioItemTitle):
    pass


class PortfolioOrganization(
    PortfolioItem,
    PortfolioItemDuration,
    PortfolioItemOrganization,
    PortfolioItemTitleDescription,
):
    pass


class PortfolioPublication(
    PortfolioItemDate,
    PortfolioItemOrganization,
    PortfolioItem,
    PortfolioItemTitleDescription,
    PortfolioItemURL,
):
    pass


class PortfolioHonorAward(
    PortfolioItemDate,
    PortfolioItemOrganization,
    PortfolioItem,
    PortfolioItemTitleDescription,
):
    pass


class PortfolioPatent(
    PortfolioItemDate,
    PortfolioItemOrganization,
    PortfolioItem,
    PortfolioItemTitleDescription,
    PortfolioItemURL,
    PortfolioItemNumber,
):
    application_number = models.CharField(max_length=128, blank=True)


class PortfolioCourse(PortfolioItem, PortfolioItemTitle, PortfolioItemNumber):
    pass


class PortfolioProject(
    PortfolioItem,
    PortfolioItemDuration,
    PortfolioItemTitleDescription,
    PortfolioItemURL,
):
    pass


class PortfolioTestScore(
    PortfolioItem, PortfolioItemTitleDescription, PortfolioItemDate, PortfolioItemNumber
):
    pass


class PortfolioVolunteerWork(
    PortfolioItemOrganization,
    PortfolioItem,
    PortfolioItemDuration,
    PortfolioItemTitleDescription,
    PortfolioItemURL,
    PortfolioItemLogo,
):
    cause = models.CharField(max_length=256, blank=True)


class PortfolioCertification(
    PortfolioItemOrganization,
    PortfolioItem,
    PortfolioItemDuration,
    PortfolioItemTitle,
    PortfolioItemURL,
    PortfolioItemNumber,
):
    pass


class PortfolioRecommendation(
    PortfolioItem, PortfolioItemDescription, PortfolioItemAuthor
):
    pass


class PortfolioArticle(
    PortfolioItem,
    PortfolioItemDate,
    PortfolioItemTitle,
    PortfolioItemAuthor,
    PortfolioItemURL,
    PortfolioItemImage,
):
    pass


class PortfolioInterest(PortfolioItem, PortfolioItemTitle):
    pass


class PortfolioSkill(PortfolioItem, PortfolioItemTitle):
    pass
