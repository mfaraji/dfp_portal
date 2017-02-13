from django.contrib import admin

# Register your models here.

from dfp.models import Country, Report

admin.site.register(Country)
admin.site.register(Report)
