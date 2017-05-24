from __future__ import unicode_literals
import json

from django.db import models
from authtools.models import User

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = 'countries'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def as_json(self):
        return {
            'name': self.name,
            'id': self.code
        }

class Community(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    ad_unit_code = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'communities'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def as_json(self):
        return {
            'name': self.name,
            'code': self.code,
            'ad_unit_code': self.ad_unit_code
        }

class Topic(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def as_json(self):
        return {
            'name': self.name,
            'code': self.code,
            'community': self.community.name
        }

class ReportType(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Report(models.Model):
    name = models.CharField(max_length=256)
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=256, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    r_type = models.ForeignKey(ReportType, on_delete=models.CASCADE, blank=True, null=True)

    def as_json(self, full=False):
        if not full:
            return {
                'id': self.id,
                'name': self.name,
                'created_at': self.created_at.date(),
                'creator': self.user.email,
                'status': self.status
            }
        else:
             return {
                'id': self.id,
                'name': self.name,
                'status': self.status,
                'job': self.query
            }

    def __unicode__(self):
        return self.name

    @property
    def dimensions(self):
        params = json.loads(self.query)
        result = []
        for dim in params['dimensions']:
            result.append(Dimension.objects.get(pk=dim['id']))
        return result

    @property
    def metrics(self):
        params = json.loads(self.query)
        result = []
        for metric in params['metrics']:
            result.append(Metric.objects.get(pk=metric['id']))
        return result

    def has_dimension(self, code):
        dim = Dimension.objects.get(code=code)
        return dim in self.dimensions


class DimesionCategory(models.Model):
    name =  models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    def as_json(self):
        return sorted([dimesion.as_json() for dimesion in self.dimension_set.all()], key=lambda k: k['name'])

class Dimension(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    category = models.ForeignKey(DimesionCategory, on_delete=models.CASCADE, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    def as_json(self):
        return {
            'name': self.name,
            'id': self.id,
            'category': self.category.name,
        }

    @property
    def column_name(self):
        return 'Dimension.%s' % self.code

class Metric(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    is_default = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

    def as_json(self):
        return {
            'name': self.name,
            'id': self.id,
        }

    @property
    def column_name(self):
        return 'Column.%s' % self.code