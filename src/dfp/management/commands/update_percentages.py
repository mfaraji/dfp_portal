# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from aurora.query import update_us_users_ratio
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = 'Updating US only percentages'

    def handle(self, *args, **options):
        update_us_users_ratio()
