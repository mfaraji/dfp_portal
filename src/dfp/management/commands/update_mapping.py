import csv
from django.core.management.base import BaseCommand, CommandError

from dfp.models import Community, Topic


class Command(BaseCommand):
    help = 'Updating list of Communities and topics'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs=1, type=file)

    def handle(self, *args, **options):
        reader = csv.reader(options['csv_file'][0])
        reader.next()

        item = reader.next()
        while item:
            community_name = item[2]
            community = Community.objects.filter(name=community_name).first()

            if community:
                self.stdout.write('Community Exist: %s' % community_name)
            else:
                self.stdout.write('Creating community: %s' % community_name)
                community = Community.objects.create(name=community_name, code=item[0])

            while item:
                if item[2] != community_name:
                    break
                topic = Topic.objects.filter(code=item[3])
                if not topic:
                    self.std.write('Creating Topic: %s' % item[4])
                    Topic.objects.create(name=item[4], code=item[3], community=community)
                item = reader.next()