import re
import csv
from dfp.models import Report

from dfp.utils import ReportFormatter



from django.core.management.base import BaseCommand, CommandError


FILE = "/tmp/tmpsz8Whl.csv"

class Command(BaseCommand):
    help = 'Updating list of adunits'

    def handle(self, *args, **options):
        report = Report.objects.all()[0]
        with open(FILE, 'r') as f:
			reader = csv.DictReader(f)
			print ReportFormatter(reader, report).format()
