# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from dfp.models import Community
from dfp.models import Country
from dfp.models import Dimension
from dfp.models import DimesionCategory
from dfp.models import Metric
from dfp.models import Report
from dfp.models import ReportType
from dfp.models import Topic
from django.contrib import admin
# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


class CommunityAdmin(admin.ModelAdmin):
    ordering = ('name',)


admin.site.register(Country)
admin.site.register(Report, ReportAdmin)
admin.site.register(Dimension)
admin.site.register(Metric)
admin.site.register(DimesionCategory)
admin.site.register(ReportType)
admin.site.register(Community, CommunityAdmin)
admin.site.register(Topic)
