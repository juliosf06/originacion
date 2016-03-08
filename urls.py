# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.campana_ofertas, name='campana_ofertas'),
    # URLS para reportes de campaña
    url(r'^campanas/$', views.campana_ofertas, name='campana_ofertas'),
    url(r'^campanas/ofertas/$', views.campana_ofertas, name='campana_ofertas'),
    url(r'^campanas/efectividad/$', views.dummy, name='dummy'),
    url(r'^campanas/competitividad/$', views.dummy, name='dummy'),
    url(r'^campanas/altas_oa/$', views.dummy, name='dummy'),
    url(r'^campanas/altas_sf/$', views.dummy, name='dummy'),
    url(r'^campanas/altas_buro/$', views.dummy, name='dummy'),
    url(r'^campanas/altas_personas/$', views.dummy, name='dummy'),
    url(r'^campanas/otros/$', views.dummy, name='dummy'),

    # URLS para reportes de RVGL
    url(r'^rvgl/$', views.rvgl_banca, name='rvgl_banca'),
    url(r'^rvgl/banca/$', views.rvgl_banca, name='rvgl_banca'),
    url(r'^rvgl/dictamen/$', views.rvgl_dictamen, name='rvgl_dictamen'),
    url(r'^rvgl/json_dictamen/$', views.json_dictamen, name='json_dictamen'),
    url(r'^rvgl/producto/$', views.rvgl_producto, name='rvgl_producto'),
    url(r'^rvgl/importexprod/$', views.rvgl_importexprod, name='rvgl_importexprod'),

    # URLS para carga de archivos
    url(r'^load_data/carga_rvgl/$', views.carga_rvgl, name='carga_rvgl'),
    url(r'^load_data/$', views.load, name='load'),
    url(r'^mapa/$', views.mapa, name='mapa'),
]
