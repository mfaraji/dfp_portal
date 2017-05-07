from django.contrib import admin

# Register your models here.

from dfp.models import Country, Report, Dimension, Metric, DimesionCategory, ReportType, Community, Topic


class ReportAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')



admin.site.register(Country)
admin.site.register(Report, ReportAdmin)
admin.site.register(Dimension)
admin.site.register(Metric)
admin.site.register(DimesionCategory)
admin.site.register(ReportType)
admin.site.register(Community)
admin.site.register(Topic)
