from django.core.management.base import BaseCommand, CommandError

from dfp.apis.target import CustomTargetService


class Command(BaseCommand):
    help = 'Updating list of key values'

    def handle(self, *args, **options):
        result = CustomTargetService().get()