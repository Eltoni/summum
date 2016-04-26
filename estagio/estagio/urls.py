#-*- coding: UTF-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import javascript_catalog
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

from app_global.views import checa_foreignkey_habilitada
from dashboard.sites import DashboardSite

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('estagio',),
}

admin.site = DashboardSite()
admin.sites.site = admin.site
admin.autodiscover()

urlpatterns = [
    # django
    url(r'^doc/', include('django.contrib.admindocs.urls')),
    url(r'', include(admin.site.urls)),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict),

    # bibliotecas
    url(r'^admin/salmonella/', include('salmonella.urls')),         # url necessária para o funcionamento da biblioteca django-salmonella
    url(r'^selectable/', include('selectable.urls')),               # url necessária para o funcionamento da biblioteca django-selectable
    url(r'^schedule/', include('schedule.urls')),                   # url necessária para o funcionamento da biblioteca django-scheduler
    url(r'^diagrama_sistema/', include('django_spaghetti.urls')),   # url necessária para o funcionamento da biblioteca django-spaghetti-and-meatballs
    url(r'^wiki-site/notifications/', get_nyt_pattern()),           # url necessária para o funcionamento da biblioteca django-wiki (sistema de notificações)
    url(r'^wiki-site/', get_wiki_pattern()),                        # url necessária para o funcionamento da biblioteca django-wiki
    url(r'^su/', include('django_su.urls')),                        # url necessária para o funcionamento da biblioteca django-su

    # urls das aplicações
    url(r'^admin/salmonella/(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<id>\d+)/$', checa_foreignkey_habilitada),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
