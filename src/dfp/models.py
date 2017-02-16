from __future__ import unicode_literals

from django.db import models

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
			'code': self.code
		}


class Report(models.Model):
	name = models.CharField(max_length=256)
	query = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=256, null=True)

	def as_json(self):
		return {
			'id': self.id,
			'name': self.name,
			'created_at': self.created_at.date(),
			'status': self.status
		}

	def __unicode__(self):
		return self.name


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
			'category': self.category.name
		}

class Metric(models.Model):
	name = models.CharField(max_length=256)
	code = models.CharField(max_length=256)

	def __unicode__(self):
		return self.name

	def as_json(self):
		return {
			'name': self.name,
			'code': self.code
		}