import json

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from ...models import Portfolio


class Command(BaseCommand):
    help = "Change theme of a portfolio site"

    def add_arguments(self, parser):
        parser.add_argument(
            "portfolio_id", type=int, help="Portfolio Site ID to change the theme of"
        )
        parser.add_argument(
            "theme", type=str, help="Name of the theme to change to"
        )

    def handle(self, *args, **options):
        try:
            portfolio = Portfolio.objects.get(pk=options["portfolio_id"])
            portfolio.theme = options["theme"]
            portfolio.save()

            self.stdout.write(
                self.style.SUCCESS(f'Changed theme of portfolio site {options["portfolio_id"]} to {options["theme"]}!')
            )
        except Portfolio.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Portfolio site {options["portfolio_id"]} does not exist!')
            )
        # except:
        #     raise CommandError("Something went wrong!")