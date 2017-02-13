from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^countries/$', views.list_countries, name='countries_list'),
	url(r'^reports/$', views.list_reports, name='reports_list'),
	url(r'^report/(?P<pk>\d+)', views.report, name='report'),
]