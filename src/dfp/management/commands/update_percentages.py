from django.core.management.base import BaseCommand, CommandError

from dfp.aws_db import update_us_users_ratio


class Command(BaseCommand):
    help = 'Updating US only percentages'

    def handle(self, *args, **options):
        update_us_users_ratio()