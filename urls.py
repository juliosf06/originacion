# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_reports, name='login_reports'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    #url(r'^$', views.campana_ofertas, name='campana_ofertas'),

    # URLS para reportes de campaña
    url(r'^campanas/$', views.campana_resumen, name='campana_resumen'),
    url(r'^campanas/resumen/$', views.campana_resumen, name='campana_resumen'),
    url(r'^campanas/resumen/(?P<fecha>[0-9]{6})/$', views.campana_resumen, name='campana_resumen'),
    url(r'^campanas/ofertas/$', views.campana_ofertas, name='campana_ofertas'),
    url(r'^campanas/ofertas/(?P<fecha>[0-9]{6})/$', views.campana_ofertas, name='campana_ofertas'),
    url(r'^campanas/detalles/$', views.campana_detalles, name='campana_detalles'),
    url(r'^campanas/detalles/(?P<segmento>[\w|\W]+)/(?P<fecha>[0-9]{6})/$', views.campana_detalles, name='campana_detalles'),
    url(r'^campanas/caidas/$', views.campana_caidas, name='campana_caidas'),
    url(r'^campanas/caidas/(?P<fecha>[0-9]{6})/$', views.campana_caidas, name='campana_caidas'),
    url(r'^campanas/exoneraciones/$', views.campana_exoneraciones, name='campana_exoneraciones'),
    url(r'^campanas/exoneraciones/(?P<segmento>[\w|\W]+)/$', views.campana_exoneraciones, name='campana_exoneraciones'),
    url(r'^campanas/flujo/$', views.campana_flujo, name='campana_flujo'),
    url(r'^campanas/flujo/(?P<fecha>[0-9]{6})/$', views.campana_flujo, name='campana_flujo'),
    url(r'^campanas/altasempresa/$', views.campana_altasempresa, name='campana_altasempresa'),
    url(r'^campanas/prestinmediato/$', views.campana_prestinmediato, name='campana_prestinmediato'),
    url(r'^campanas/prueba/$', views.campana_prueba, name='campana_prueba'),

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
    url(r'^rvgl/dictamenxsco/(?P<fecha>[0-9]{6})/(?P<analista>[\w|\W]+)/$', views.rvgl2_dictamenxsco, name='rvgl2_dictamenxsco'),
    url(r'^rvgl/scoxllenado/$', views.rvgl_scoxllenado, name='rvgl_scoxllenado'),
    url(r'^rvgl/json_scoxllenado/$', views.json_scoxllenado, name='json_scoxllenado'),
    url(r'^rvgl/scoxforzaje/$', views.rvgl_scoxforzaje, name='rvgl_scoxforzaje'),
    url(r'^rvgl/json_scoxforzaje/$', views.json_scoxforzaje, name='json_scoxforzaje'),
    url(r'^rvgl/scoxdictamen/$', views.rvgl_scoxdictamen, name='rvgl_scoxdictamen'),
    url(r'^rvgl/json_scoxdictamen/$', views.json_scoxdictamen, name='json_scoxdictamen'),
    url(r'^rvgl/top20terr/$', views.rvgl_top20terr, name='rvgl_top20terr'),
    url(r'^rvgl/top20terr/(?P<fecha>[0-9]{6})/(?P<analista>[\w|\W]+)/$', views.rvgl2_top20terr, name='rvgl2_top20terr'),
    url(r'^rvgl/top20gest/$', views.rvgl_top20gest, name='rvgl_top20gest'),
    url(r'^rvgl/top20gest/(?P<fecha>[0-9]{6})/(?P<analista>[\w|\W]+)/$', views.rvgl2_top20gest, name='rvgl2_top20gest'),
    url(r'^rvgl/top20clie/$', views.rvgl_top20clie, name='rvgl_top20clie'),
    url(r'^rvgl/top20clie/(?P<fecha>[0-9]{6})/(?P<analista>[\w|\W]+)/$', views.rvgl2_top20clie, name='rvgl2_top20clie'),
    url(r'^rvgl/top20ofic/$', views.rvgl_top20ofic, name='rvgl_top20ofic'),
    url(r'^rvgl/top20ofic/(?P<fecha>[0-9]{6})/(?P<analista>[\w|\W]+)/$', views.rvgl2_top20ofic, name='rvgl2_top20ofic'),


    # URLS para reportes de Evaluacion
    url(r'^evaluacion/$', views.evaluacion_evaluaciontc, name='evaluacion_evaluaciontc'),
    url(r'^evaluacion/evaluaciontc/$', views.evaluacion_evaluaciontc, name='evaluacion_evaluaciontc'),
    url(r'^evaluacion/evaluacionpld/$', views.evaluacion_evaluacionpld, name='evaluacion_evaluacionpld'),

    # URLS para reportes de Seguimiento
    url(r'^seguimiento/$', views.seguimiento_tarjeta, name='seguimiento_tarjeta'),
    url(r'^seguimiento/tarjeta/$', views.seguimiento_tarjeta, name='seguimiento_tarjeta'),
    url(r'^seguimiento/pld/$', views.seguimiento_pld, name='seguimiento_pld'),
    url(r'^seguimiento/auto/$', views.seguimiento_auto, name='seguimiento_auto'),
    url(r'^seguimiento/adelanto/$', views.seguimiento_adelanto, name='seguimiento_adelanto'),
    url(r'^seguimiento/prestinmediato/$', views.seguimiento_prestinmediato, name='seguimiento_prestinmediato'),
    url(r'^seguimiento/increlinea/$', views.seguimiento_increlinea, name='seguimiento_increlinea'),
    url(r'^seguimiento/hipoteca/$', views.seguimiento_hipoteca, name='seguimiento_hipoteca'),
    url(r'^seguimiento/lifemiles/$', views.seguimiento_lifemiles, name='seguimiento_lifemiles'),

    # URLS para reportes de Hipotecario
    url(r'^hipotecario/$', views.hipoteca_ssff, name='hipoteca_ssff'),
    url(r'^hipotecario/ssff/$', views.hipoteca_ssff, name='hipoteca_ssff'),
    url(r'^hipotecario/territorio/$', views.hipoteca_conce, name='hipoteca_conces'),
    url(r'^hipotecario/seguimiento/$', views.hipoteca_segui, name='hipoteca_segui'),

    # URLS para carga de archivos
    url(r'^load_data/carga_rvgl/$', views.carga_rvgl, name='carga_rvgl'),
    #url(r'^load_data/carga_campana/$', views.carga_campana, name='carga_campana'),
    url(r'^load_data/carga_campana2/$', views.carga_campana2, name='carga_campana2'),
    url(r'^load_data/carga_caidas/$', views.carga_caidas, name='carga_caidas'),
    url(r'^load_data/carga_verificaciones/$', views.carga_verificaciones, name='carga_verificaciones'),
    url(r'^load_data/carga_evaluaciontc/$', views.carga_evaluaciontc, name='carga_evaluaciontc'),
    url(r'^load_data/carga_evaluacionpld/$', views.carga_evaluacionpld, name='carga_evaluacionpld'),
    url(r'^load_data/carga_seguimiento1/$', views.carga_seguimiento1, name='carga_seguimiento1'),
    url(r'^load_data/carga_flujoperativo/$', views.carga_flujoperativo, name='carga_flujoperativo'),
    url(r'^load_data/carga_hipotecassff/$', views.carga_hipotecassff, name='carga_hipotecassff'),
    url(r'^load_data/carga_hipotecaconce/$', views.carga_hipotecaconce, name='carga_hipotecaconce'),
    url(r'^load_data/carga_moras/$', views.carga_moras, name='carga_moras'),
    url(r'^load_data/carga_adelantosueldo/$', views.carga_adelantosueldo, name='carga_adelantosueldo'),
    url(r'^load_data/carga_prestinmediato/$', views.carga_prestinmediato, name='carga_prestinmediato'),
    url(r'^load_data/carga_altasempresa/$', views.carga_altasempresa, name='carga_altasempresa'),
    url(r'^load_data/carga_altassegmento/$', views.carga_altassegmento, name='carga_altassegmento'),
    url(r'^load_data/carga_increlinea/$', views.carga_increlinea, name='carga_increlinea'),
    url(r'^load_data/carga_lifemiles/$', views.carga_lifemiles, name='carga_lifemiles'),
    url(r'^load_data/$', views.load, name='load'),
    url(r'^mapa/$', views.mapa, name='mapa'),
]
