# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from dfp.apis.target import CustomTargetService
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = 'Updating list of key values'

    def handle(self, *args, **options):
        result = CustomTargetService().get()
