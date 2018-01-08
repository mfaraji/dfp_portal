# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^countries/$', views.list_countries, name='countries_list'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^report/download/(?P<pk>\d+)', views.download_report, name='download'),
    url(r'^report/config/(?P<pk>\d+)', views.report_config, name='report_config'),
    url(r'^report/(?P<pk>\d+)', views.report, name='report'),
    url(r'^dimensions/$', views.dimensions, name='dimensions'),
    url(r'^metrics/$', views.metrics, name='metrics'),
    url(r'^communities/$', views.communities, name='communities'),
    url(r'^topics/$', views.topics, name='topics'),
    url(r'^search/$', views.search, name='search')
]
