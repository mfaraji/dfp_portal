from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Country(models.Model):
	name = models.CharField(max_length=256)
	code = models.CharField(max_length=30)
    