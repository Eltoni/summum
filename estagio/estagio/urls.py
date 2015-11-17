#-*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import javascript_catalog

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('estagio',),
}

admin.autodiscover()

urlpatterns = patterns('',
    # django
    url(r'^doc/', include('django.contrib.admindocs.urls')),
    url(r'', include(admin.site.urls)),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # bibliotecas
    url(r'^admin/salmonella/', include('salmonella.urls')),         # url necessária para o funcionamento da biblioteca django-salmonella
    url(r'^selectable/', include('selectable.urls')),               # url necessária para o funcionamento da biblioteca django-selectable
    url(r'^schedule/', include('schedule.urls')),                   # url necessária para o funcionamento da biblioteca django-scheduler
    url(r'^diagrama_sistema/', include('django_spaghetti.urls')),    # url necessária para o funcionamento da biblioteca django-spaghetti-and-meatballs

    # dashboard
    url(r'^dashboard/$', 'movimento.views.index'),
    # urls das aplicações
    url(r'^admin/salmonella/(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<id>\d+)/$', 'app_global.views.checa_foreignkey_habilitada'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
