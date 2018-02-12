# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^acs/$', views.acs, name="acs"),
    url(r'^welcome/$', views.welcome, name="welcome"),
    url(r'^denied/$', views.denied, name="denied"),
    url(r'^saml_auth/', views.signin, name="signin")
]
