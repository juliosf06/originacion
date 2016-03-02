# -*- coding: utf-8 -*-

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render_to_response as render
from django.template import RequestContext

from models import *
from forms import RVGLCsv, UploadRVGL

import csv


# 1.- Vista para links en contruccion
def dummy(request):
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/dummy.html', locals(),
                  context_instance=RequestContext(request))

# 2.- Vistas para reportes de Campaña
def campana_ofertas(request):
    campanas = Campana.objects.filter(mes_vigencia='201512')
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_ofertas.html', locals(),
                  context_instance=RequestContext(request))


# 3.- Vistas para reportes de RVGL
def rvgl_banca(request):
    banca = RVGL.objects.all().values('seco').annotate(num_seco=Count('seco')).order_by('seco')
    for i in banca:
        print i
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_banca.html', locals(),
                  context_instance=RequestContext(request))


def mapa(request):
    distrito = MoraDistrito.objects.filter(provincia='Lima')
    static_url=settings.STATIC_URL
    return render('reports/mapa.html', locals(),
                  context_instance=RequestContext(request))


# Vistas para carga de csv
def load(request):
    static_url=settings.STATIC_URL
    #RVGL.objects.all().delete()
    if request.user.is_authenticated():
        return render('reports/load.html', locals(),
                  context_instance=RequestContext(request))
    else:
        return campana_ofertas(request)



# Vistas para manipular archivos
def carga_rvgl(request):
    if request.method == 'POST':
        form = UploadRVGL(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['rvgl']
            RVGLCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            print "no es valido"
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

