import csv
from django.core.management.base import BaseCommand, CommandError

from dfp.models import Community


class Command(BaseCommand):
    help = 'Updating list of adunits'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=file)

    def handle(self, *args, **options):
        reader = csv.reader(options['csv_file'][0])
        # 0 -> Id
        # 1 -> parent id
        # 3 -> name
        reader.next()
        for item in reader:
            if item[1] == '64299533' and item[3] != 'sidebar':
                community = Community.objects.filter(name=item[3]).first()
                if not community:
                    self.stderr.write('Community not found: %s' % item[3])
                    continue
                community.ad_unit_code = item[0]
                community.save()
                self.stdout.write('Community updated: %s' % community)
