# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.serializers import serialize
from django.db.models import Count, Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render_to_response as render
from django.template import RequestContext

from models import *
from forms import RVGLCsv, UploadRVGL

import csv


# 1.- Vista para links en contruccion
def login(request): #agregado
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/login.html', locals(),
                  context_instance=RequestContext(request))

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
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_banca.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_dictamen(request):
    dictamen = RVGL.objects.all().values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_dictamen.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_producto(request):
    producto = RVGL.objects.all().values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_producto.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_importexprod(request):
    importexprod = RVGL.objects.all().values('producto_esp').annotate(sum_importe=Sum('importe_solic')).order_by('producto_esp')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_importexprod.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_buro(request):
    buro = RVGL.objects.exclude(dic_buro='AL').exclude(dic_buro='NULL').values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')
    #buro = RVGL.objects.all().values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_buro.html', locals(),
                  context_instance=RequestContext(request))
    print buro

def rvgl_tiempo(request):
    tiempo = RVGL.objects.all().values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_tiempo.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_importexdict(request):
    importexdict = RVGL.objects.all().values('dictamen').annotate(sum_importe=Sum('importe_solic')).order_by('dictamen')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_importexdict.html', locals(),
                  context_instance=RequestContext(request))

def mapa(request):
    distrito = MoraDistrito.objects.filter(provincia='Lima')
    static_url=settings.STATIC_URL
    return render('reports/mapa.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_dictamenxsco(request):
    dictamenxsco_ap = RVGL.objects.filter(dictamen_sco='AP').values('dictamen').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco_du = RVGL.objects.filter(dictamen_sco='DU').values('dictamen').annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco_re = RVGL.objects.filter(dictamen_sco='RE').values('dictamen').annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
    static_url=settings.STATIC_URL
    rango =range(0,4)
    print rango
    tipo_side = 2
    return render('reports/rvgl_dictamenxsco.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_top20terr(request):
    top20terr1 = RVGL.objects.all().values('territorio_nuevo').annotate(num_top20terr1=Count('importe_solic')).order_by('-territorio_nuevo')[:20]
    top20terr2 = RVGL.objects.all().values('territorio_nuevo').annotate(sum_top20terr2=Sum('importe_solic')).order_by('-territorio_nuevo')[:20]
    top20terr3 = RVGL.objects.exclude(importe_aprob=0).values('territorio_nuevo').annotate(num_top20terr3=Count('importe_aprob')).order_by('-territorio_nuevo')[:20]
    top20terr4 = RVGL.objects.all().values('territorio_nuevo').annotate(sum_top20terr4=Sum('importe_aprob')).order_by('-territorio_nuevo')[:20]
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20terr.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_top20gest(request):
    top20gest1 = RVGL.objects.all().values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic')).order_by('ejecutivo_cuenta')[:20]
    top20gest2 = RVGL.objects.all().values('ejecutivo_cuenta').annotate(sum_top20gest2=Sum('importe_solic')).order_by('ejecutivo_cuenta')[:20]
    top20gest3 = RVGL.objects.exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest3=Count('importe_aprob')).order_by('ejecutivo_cuenta')[:20]
    top20gest4 = RVGL.objects.all().values('ejecutivo_cuenta').annotate(sum_top20gest4=Sum('importe_aprob')).order_by('ejecutivo_cuenta')[:20]
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20gest.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_top20clie(request):
    top20clie1 = RVGL.objects.all().values('cliente').annotate(num_top20clie1=Count('importe_solic')).order_by('cliente')[:20]
    top20clie2 = RVGL.objects.all().values('cliente').annotate(sum_top20clie2=Sum('importe_solic')).order_by('cliente')[:20]
    top20clie3 = RVGL.objects.exclude(importe_aprob=0).values('cliente').annotate(num_top20clie3=Count('importe_aprob')).order_by('cliente')[:20]
    top20clie4 = RVGL.objects.all().values('cliente').annotate(sum_top20clie4=Sum('importe_aprob')).order_by('cliente')[:20]
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20clie.html', locals(),
                  context_instance=RequestContext(request))

# Vistas para recibir consultas Ajax
def json_dictamen(request):
    periodo = request.POST['periodo']
    producto = request.POST['producto']
    #if request.method == 'TODOS'
    if request.POST['producto'] == 'TODOS':
        dictamen = RVGL.objects.all().values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')     
    else:    
        dictamen = RVGL.objects.filter(producto_esp=producto).values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
    return HttpResponse(dictamen)

def json_tiempo(request):
    periodo = request.POST['periodo']
    banca = request.POST['banca']
    #producto = request.POST['producto']
    #if request.method == 'TODOS'
    #if request.POST['producto'] == 'TODOS':
        #tiempo = RVGL.objects.all().values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')     
    #else:    
        #tiempo = RVGL.objects.filter(producto_esp=producto).values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')

    if request.POST['banca'] == 'TODOS':
        tiempo = RVGL.objects.all().values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')     
    else:    
        tiempo = RVGL.objects.filter(seco=banca).values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')
    return HttpResponse(tiempo)

def json_dictamenxsco(request):
    periodo = request.POST['periodo']
    producto = request.POST['producto']
    #if request.method == 'TODOS'
    if request.POST['producto'] == 'TODOS':
        dictamenxsco = RVGL.objects.all().values('dictamen').annotate(num_dictamenxsco=Count('dictamen_sco')).order_by('dictamen')     
    else:    
        dictamenxsco = RVGL.objects.filter(producto_esp=producto).values('dictamen').annotate(num_dictamenxsco=Count('dictamen_sco')).order_by('dictamen')
    return HttpResponse(dictamenxsco)


# Vistas para carga de csv
def load(request):
    static_url=settings.STATIC_URL
    RVGL.objects.all().delete()
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

