#-*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # dashboard
    url(r'^dashboard/$', 'movimento.views.index'),

    # django
    url(r'^doc/', include('django.contrib.admindocs.urls')),
    url(r'', include(admin.site.urls)),

    # bibliotecas
    url(r'^chaining/', include('smart_selects.urls')),      # url necessária para o funcionamento da biblioteca django-smart-selects
    url(r'^admin/salmonella/', include('salmonella.urls')), # url necessária para o funcionamento da biblioteca django-salmonella

    # urls das aplicações
    url(r'^admin/salmonella/(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<id>\d+)/$', 'app_global.views.checa_foreignkey_habilitada'),
    (r'^checa_pedido_compra_habilitado/(?P<id>\d+)/$', 'compra.views.checa_pedido_compra_habilitado'),
    (r'^get_valor_unitario/(?P<id>\d+)/$', 'compra.views.get_valor_unitario'),
    (r'^checa_pedido_venda_habilitado/(?P<id>\d+)/$', 'venda.views.checa_pedido_venda_habilitado'),
    (r'^get_valor_unitario/(?P<id>\d+)/$', 'venda.views.get_valor_unitario'),
    (r'^get_dados_usuario/(?P<id>\d+)/$', 'pessoal.views.get_dados_usuario'),
)
