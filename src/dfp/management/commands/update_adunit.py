from django.core.management.base import BaseCommand, CommandError

from dfp.models import AdUnit
from dfp.apis.inventory import AdUnitService


class Command(BaseCommand):
    help = 'Updating list of adunits'

    def handle(self, *args, **options):
        AdUnit.objects.all().delete()
        result = AdUnitService().get()
        for entry in result:
            AdUnit.objects.create(**entry)