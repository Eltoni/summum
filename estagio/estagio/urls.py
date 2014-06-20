#-*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^doc/', include('django.contrib.admindocs.urls')),
    url(r'', include(admin.site.urls)),

    url(r'^chaining/', include('smart_selects.urls')),      # url necessária para o funcionamento da biblioteca django-smart-selects
)
