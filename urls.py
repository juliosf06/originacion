# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_reports, name='login_reports'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    #url(r'^$', views.campana_ofertas, name='campana_ofertas'),
    # URLS para reportes de campaña
    url(r'^campanas/$', views.campana_ofertas, name='campana_ofertas'),
    url(r'^campanas/ofertas/$', views.campana_ofertas, name='campana_ofertas'),
    url(r'^campanas/json_ofertas/$', views.json_ofertas, name='json_ofertas'),
    url(r'^campanas/detalles/$', views.campana_detalles, name='campana_detalles'),
    url(r'^campanas/json_detalles/$', views.json_detalles, name='json_detalles'),
    url(r'^campanas/caidas/$', views.campana_caidas, name='campana_caidas'),
    url(r'^campanas/json_caidas/$', views.json_caidas, name='json_caidas'),
    url(r'^campanas/exoneraciones/$', views.campana_exoneraciones, name='campana_exoneraciones'),
    url(r'^campanas/altas_sf/$', views.dummy, name='dummy'),
    url(r'^campanas/altas_buro/$', views.dummy, name='dummy'),
    url(r'^campanas/altas_personas/$', views.dummy, name='dummy'),
    url(r'^campanas/otros/$', views.dummy, name='dummy'),

    # URLS para reportes de RVGL
    url(r'^rvgl/$', views.rvgl_banca, name='rvgl_banca'),
    url(r'^rvgl/banca/$', views.rvgl_banca, name='rvgl_banca'),
    url(r'^rvgl/json_banca/$', views.json_banca, name='json_banca'),
    url(r'^rvgl/dictamen/$', views.rvgl_dictamen, name='rvgl_dictamen'),
    url(r'^rvgl/json_dictamen/$', views.json_dictamen, name='json_dictamen'),
    url(r'^rvgl/producto/$', views.rvgl_producto, name='rvgl_producto'),
    url(r'^rvgl/json_producto/$', views.json_producto, name='json_producto'),
    url(r'^rvgl/importexprod/$', views.rvgl_importexprod, name='rvgl_importexprod'),
    url(r'^rvgl/json_importexprod/$', views.json_importexprod, name='json_importexprod'),
    url(r'^rvgl/buro/$', views.rvgl_buro, name='rvgl_buro'),
    url(r'^rvgl/json_buro/$', views.json_buro, name='json_buro'),
    url(r'^rvgl/tiempo/$', views.rvgl_tiempo, name='rvgl_tiempo'),
    url(r'^rvgl/json_tiempo/$', views.json_tiempo, name='json_tiempo'),
    url(r'^rvgl/importexdict/$', views.rvgl_importexdict, name='rvgl_importexdict'),
    url(r'^rvgl/json_importexdict/$', views.json_importexdict, name='json_importexdict'),
    url(r'^rvgl/dictamenxsco/$', views.rvgl_dictamenxsco, name='rvgl_dictamenxsco'),
    url(r'^rvgl/json_dictamenxsco/$', views.json_dictamenxsco, name='json_dictamenxsco'),
    url(r'^rvgl/scoxllenado/$', views.rvgl_scoxllenado, name='rvgl_scoxllenado'),
    url(r'^rvgl/json_scoxllenado/$', views.json_scoxllenado, name='json_scoxllenado'),
    url(r'^rvgl/scoxforzaje/$', views.rvgl_scoxforzaje, name='rvgl_scoxforzaje'),
    url(r'^rvgl/json_scoxforzaje/$', views.json_scoxforzaje, name='json_scoxforzaje'),
    url(r'^rvgl/scoxdictamen/$', views.rvgl_scoxdictamen, name='rvgl_scoxdictamen'),
    url(r'^rvgl/json_scoxdictamen/$', views.json_scoxdictamen, name='json_scoxdictamen'),
    url(r'^rvgl/top20terr/$', views.rvgl_top20terr, name='rvgl_top20terr'),
    url(r'^rvgl/json_top20terr/$', views.json_top20terr, name='json_top20terr'),
    url(r'^rvgl/top20gest/$', views.rvgl_top20gest, name='rvgl_top20gest'),
    #url(r'^rvgl/json_top20gest/$', views.json_top20gest, name='json_top20gest'),
    url(r'^rvgl/top20clie/$', views.rvgl_top20clie, name='rvgl_top20clie'),
    #url(r'^rvgl/json_top20clie/$', views.json_top20clie, name='json_top20clie'),
    url(r'^rvgl/top20ofic/$', views.rvgl_top20ofic, name='rvgl_top20ofic'),
    #url(r'^rvgl/json_top20ofic/$', views.json_top20ofic, name='json_top20ofic'),


    # URLS para carga de archivos
    url(r'^load_data/carga_rvgl/$', views.carga_rvgl, name='carga_rvgl'),
    url(r'^load_data/carga_campana/$', views.carga_campana, name='carga_campana'),
    url(r'^load_data/carga_caidas/$', views.carga_caidas, name='carga_caidas'),
    url(r'^load_data/carga_verificaciones/$', views.carga_verificaciones, name='carga_verificaciones'),
    url(r'^load_data/$', views.load, name='load'),
    url(r'^mapa/$', views.mapa, name='mapa'),
]
