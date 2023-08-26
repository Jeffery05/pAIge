import json

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Add a site object"

    def add_arguments(self, parser):
        parser.add_argument(
            "fqdn", type=str, help="Fully qualified domain name of the site"
        )

    def handle(self, *args, **options):
        try:
            Site.objects.create(domain=options["fqdn"], name=f'Panel {options["fqdn"]}')

            self.stdout.write(
                self.style.SUCCESS(f'Added site object for {options["fqdn"]}!')
            )
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(f"Site object for {options['fqdn']} already exists!")
            )
        except:
            raise CommandError("Something went wrong!")
