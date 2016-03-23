# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Case, When, IntegerField, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response as render
from django.template import RequestContext

from models import *
from forms import *
from django.contrib.auth import authenticate, login, logout

import csv


# 1.- Vista para links en contruccion
def login_reports(request): #agregado
    static_url=settings.STATIC_URL
    tipo_side = 1
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(username=username, password=password)
       if user is not None:
           if user.is_active:
               login(request, user)
               # Redirect to a success page.
	       print("User is valid, ative and authenticate")
               if 'next' in request.GET:
                   return HttpResponseRedirect(request.GET['next'])
               else:
                   return HttpResponseRedirect('/reports/campanas')
           else:
               # Return a 'disabled account' error message
	       print("The password is valid, but the account has been disabled!")
       else:
           mensaje="Usurio o password incorrectos"  
    return render('reports/login.html', locals(),
                  context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    # Redirect to a succes page
    return HttpResponseRedirect('/reports')

def dummy(request):
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/dummy.html', locals(),
                  context_instance=RequestContext(request))

# 2.- Vistas para reportes de Campaña
@login_required
def campana_ofertas(request):
    clientes = Verificaciones.objects.values('segmento').annotate(num_clientes=Sum(F('exonera_ambas')+F('exonera_solo_vl')+F('exonera_solo_vd')+F('requiere_ambas'))).filter(mes_vigencia='201604').order_by('segmento')
    ofertas = Campana.objects.all().filter(mes_vigencia='201604').distinct('segmento')
    montos = Campana.objects.values('segmento').annotate(monto=Sum(F('monto_tc')+F('monto_pld')+F('monto_veh')+F('monto_subrogacion')+F('monto_tc_entry_level')+F('monto_renovado')+F('monto_auto_2da')+F('monto_adelanto_sueldo')+F('monto_efectivo_plus')+F('monto_prestamo_inmediato')+F('monto_incr_linea'))).filter(mes_vigencia='201604').order_by('segmento')
    ofer = zip(ofertas, clientes, montos)
    static_url=settings.STATIC_URL
    tipo_side = 1
    print montos
    return render('reports/campana_ofertas.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campana_detalles(request):
    detalles = Campana.objects.filter(mes_vigencia='201603').filter(segmento='MS').distinct('segmento')
    control_segmentos = Campana.objects.all().values('segmento').distinct('segmento')
    print detalles
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_detalles.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campana_caidas(request):
    caidas_ms = Caida.objects.values('caida').filter(mes_vigencia='201603').filter(segmento='MS').annotate(num_caidaxms=Sum('cantidad')).order_by('caida')
    caidas_ava = Caida.objects.values('caida').filter(mes_vigencia='201603').filter(segmento='AVA').annotate(num_caidaxava=Sum('cantidad')).order_by('caida')
    caidas_noph = Caida.objects.values('caida').filter(mes_vigencia='201603').filter(segmento='NO PH + PASIVO').annotate(num_caidaxnoph=Sum('cantidad')).order_by('caida')
    caidas_noclie = Caida.objects.values('caida').filter(mes_vigencia='201603').filter(segmento='NO CLIENTE').annotate(num_caidaxnoclie=Sum('cantidad')).order_by('caida')
    caidas = zip(caidas_ms, caidas_ava, caidas_noph, caidas_noclie)
    print caidas
    static_url=settings.STATIC_URL
    grafica  = Caida.objects.values('caida').filter(mes_vigencia='201603').annotate(num_caida=Sum('cantidad')).order_by('caida')
    total = Caida.objects.values('mes_vigencia').filter(mes_vigencia='201603').annotate(total=Sum('cantidad'))
    coord = []
    coord.append({ 'label': 'Total Evaluados', 'x': 0, 'y': total[0]['total'] })
    cont = 0
    for i in grafica:
        if cont == 0:
            coord.append({'label':i['caida'], 'x': coord[cont]['y']-i['num_caida'], 'y': coord[cont]['y']})
        elif cont<9:
            coord.append({'label':i['caida'], 'x': coord[cont]['x']-i['num_caida'], 'y': coord[cont]['x']})
        cont=cont+1
    tipo_side = 1
    coord = reversed(coord)
    return render('reports/campana_caidas.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campana_exoneraciones(request):
    exoneraciones = Verificaciones.objects.values('mes_vigencia').filter(segmento='AVA').annotate(exoambas=Sum('exonera_ambas'), solovl=Sum('exonera_solo_vl'), solovd=Sum('exonera_solo_vd'), reqambas=Sum('requiere_ambas'), exovltc=Sum('exonera_vl_tc')).order_by('mes_vigencia')
    control_segmentos = Verificaciones.objects.all().values('segmento').distinct('segmento')
    print control_segmentos
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_exoneraciones.html', locals(),
                  context_instance=RequestContext(request))


# 3.- Vistas para reportes de RVGL
@login_required
def rvgl_banca(request):
    banca = RVGL.objects.filter(mes_vigencia='201602').values('seco').annotate(num_seco=Count('seco')).order_by('seco')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_banca.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_dictamen(request):
    dictamen = RVGL.objects.filter(mes_vigencia='201602').values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_dictamen.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_producto(request):
    producto = RVGL.objects.filter(mes_vigencia='201602').values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_producto.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_importexprod(request):
    importexprod = RVGL.objects.filter(mes_vigencia='201602').values('producto_esp').annotate(sum_importexprod=Sum('importe_solic')).order_by('producto_esp')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    print importexprod
    return render('reports/rvgl_importexprod.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_buro(request):
    buro = RVGL.objects.exclude(dic_buro='AL').exclude(dic_buro='NULL').filter(mes_vigencia='201602').values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_buro.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_tiempo(request):
    tiempo = RVGL.objects.filter(mes_vigencia='201602').values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    control_seco = RVGL.objects.all().values('seco').distinct('seco')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_tiempo.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_importexdict(request):
    importexdict = RVGL.objects.filter(mes_vigencia='201602').values('dictamen').annotate(sum_importe=Sum('importe_solic')).order_by('dictamen')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_importexdict.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def mapa(request):
    distrito = MoraDistrito.objects.filter(provincia='Lima')
    static_url=settings.STATIC_URL
    return render('reports/mapa.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_dictamenxsco(request):
    dictamenxsco_ap = RVGL.objects.filter(mes_vigencia='201602').filter(dictamen_sco='AP').values('dictamen').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco_du = RVGL.objects.filter(mes_vigencia='201602').filter(dictamen_sco='DU').values('dictamen').annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco_re = RVGL.objects.filter(mes_vigencia='201602').filter(dictamen_sco='RE').values('dictamen').annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco = zip(dictamenxsco_ap,dictamenxsco_du,dictamenxsco_re)
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_dictamenxsco.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_scoxllenado(request):
    scoxllenado = RVGL.objects.filter(mes_vigencia='201602').exclude(sco='O').values('sco').annotate(num_scoxllenado=Count('sco')).order_by('sco')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_scoxllenado.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_scoxforzaje(request):
    scoxforzaje = RVGL.objects.filter(mes_vigencia='201602').filter(dictamen_sco='RE').exclude(seg_prime='NULL').values('seg_prime').annotate(num_scoxforzaje=Count('seg_prime')).order_by('seg_prime')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_scoxforzaje.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_scoxdictamen(request):
    scoxdictamen = RVGL.objects.filter(mes_vigencia='201602').exclude(dictamen_sco='NULL').values('dictamen_sco').annotate(num_scoxdictamen=Count('dictamen_sco')).order_by('dictamen_sco')
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_scoxdictamen.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20terr(request):
    top20terr1 = RVGL.objects.filter(mes_vigencia='201602').exclude(territorio_nuevo='NULL').values('territorio_nuevo').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic') ).order_by('-sum_top20terr1')[:20]
    top20terr2 = RVGL.objects.filter(mes_vigencia='201602').exclude(importe_aprob=0).exclude(territorio_nuevo='NULL').values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    top20terr = zip(top20terr1, top20terr2)
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20terr.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20gest(request):
    top20gest1 = RVGL.objects.filter(mes_vigencia='201602').values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic'), sum_top20gest1=Sum('importe_solic')).order_by('-sum_top20gest1')[:20]
    top20gest2 = RVGL.objects.filter(mes_vigencia='201602').exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest2=Count('importe_aprob'), sum_top20gest2=Sum('importe_aprob')).order_by('-sum_top20gest2')[:20]
    top20gest = zip(top20gest1,top20gest2)
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20gest.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20clie(request):
    top20clie1 = RVGL.objects.filter(mes_vigencia='201602').values('cliente').annotate(num_top20clie1=Count('importe_solic'), sum_top20clie1=Sum('importe_solic')).order_by('cliente').order_by('-sum_top20clie1')[:20]
    top20clie2 = RVGL.objects.filter(mes_vigencia='201602').exclude(importe_aprob=0).values('cliente').annotate(num_top20clie2=Count('importe_aprob'), sum_top20clie2=Sum('importe_aprob')).order_by('-sum_top20clie2')[:20]
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    top20clie = zip(top20clie1,top20clie2)
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20clie.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20ofic(request):
    top20ofic1 = RVGL.objects.filter(mes_vigencia='201602').values('oficina').annotate(num_top20ofic1=Count('importe_solic'), sum_top20ofic1=Sum('importe_solic')).order_by('-sum_top20ofic1')[:20]
    top20ofic2 = RVGL.objects.filter(mes_vigencia='201602').exclude(importe_aprob=0).values('oficina').annotate(num_top20ofic2=Count('importe_aprob'), sum_top20ofic2=Sum('importe_aprob')).order_by('-sum_top20ofic2')[:20]
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    top20ofic = zip(top20ofic1,top20ofic2)
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20ofic.html', locals(),
                  context_instance=RequestContext(request))

# 4.- Vistas para reportes de EVALUACION
@login_required
def evaluacion_evaluaciontc(request):
    evaluaciontc = Evaluaciontc.objects.all().order_by('cliente').distinct('cliente')
    static_url=settings.STATIC_URL
    tipo_side = 3
    return render('reports/evaluacion_evaluaciontc.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def evaluacion_evaluacionpld(request):
    evaluacionpld = Evaluacionpld.objects.all().order_by('cliente').distinct('cliente')
    static_url=settings.STATIC_URL
    tipo_side = 3
    return render('reports/evaluacion_evaluacionpld.html', locals(),
                  context_instance=RequestContext(request))


# 5.- Vistas para reportes de SEGUIMIENTO
@login_required
def seguimiento_tarjeta(request):
    seg_tarjeta = Seguimiento1.objects.all().order_by('segmento').distinct('segmento')
    static_url=settings.STATIC_URL
    tipo_side = 3
    return render('reports/seguimiento_tarjeta.html', locals(),
                  context_instance=RequestContext(request))


# Vistas CAMPANA para recibir consultas Ajax
def json_ofertas(request):
    periodo = request.POST['periodo']
    clientes = Verificaciones.objects.values('segmento').annotate(num_clientes=Sum(F('exonera_ambas')+F('exonera_solo_vl')+F('exonera_solo_vd')+F('requiere_ambas'))).filter(mes_vigencia=periodo).order_by('segmento')
    ofertas = Campana.objects.all().filter(mes_vigencia=periodo).distinct('segmento')
    montos = Campana.objects.values('segmento').annotate(monto=Sum(F('monto_tc')+F('monto_pld')+F('monto_veh')+F('monto_subrogacion')+F('monto_tc_entry_level')+F('monto_renovado')+F('monto_auto_2da')+F('monto_adelanto_sueldo')+F('monto_efectivo_plus')+F('monto_prestamo_inmediato')+F('monto_incr_linea'))).filter(mes_vigencia=periodo).order_by('segmento')
    ofer = zip(ofertas, clientes, montos)
    return HttpResponse(clientes)

def json_detalles(request):
    periodo = request.POST['periodo']
    detalles = Campana.objects.filter(mes_vigencia=periodo).filter(segmento='MS').distinct('segmento').values()
    detalles1 = Campana.objects.values('q_tc','q_pld','q_veh','q_subrogacion','q_tc_entry_level', 'q_renovado', 'q_auto_2da', 'q_adelanto_sueldo','q_efectivo_plus','q_prestamo_inmediato','q_incr_linea').filter(mes_vigencia=periodo).filter(segmento='MS').distinct('segmento')
    return HttpResponse(zip(detalles,detalles1))

def json_caidas(request):
    periodo = request.POST['periodo']
    caidas_ms = Caida.objects.values('caida').filter(mes_vigencia=periodo).filter(segmento='MS').annotate(num_caidaxms=Sum('cantidad'))
    caidas_ava = Caida.objects.values('caida').filter(mes_vigencia=periodo).filter(segmento='AVA').annotate(num_caidaxava=Sum('cantidad'))
    caidas_noph = Caida.objects.values('caida').filter(mes_vigencia=periodo).filter(segmento='NO PH + PASIVO').annotate(num_caidaxnoph=Sum('cantidad'))
    caidas_noclie = Caida.objects.values('caida').filter(mes_vigencia=periodo).filter(segmento='NO CLIENTE').annotate(num_caidaxnoclie=Sum('cantidad'))
    caidas = zip(caidas_ms, caidas_ava, caidas_noph, caidas_noclie)
    return HttpResponse(caidas)

# Vistas RVGL para recibir consultas Ajax
def json_banca(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
    	banca = RVGL.objects.all().filter(mes_vigencia=periodo).values('seco').annotate(num_seco=Count('seco')).order_by('seco')
    else:
        banca = RVGL.objects.filter(analista=analista).filter(mes_vigencia=periodo).values('seco').annotate(num_seco=Count('seco')).order_by('seco')
    return HttpResponse(banca)

def json_dictamen(request):
    periodo = request.POST['periodo']
    producto = request.POST['producto']
    #if request.method == 'TODOS'
    if request.POST['producto'] == 'TODOS':
        dictamen = RVGL.objects.all().filter(mes_vigencia=periodo).values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')     
    else:    
        dictamen = RVGL.objects.filter(producto_esp=producto).filter(mes_vigencia=periodo).values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
    return HttpResponse(dictamen)

def json_producto(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
    	producto = RVGL.objects.all().filter(mes_vigencia=periodo).values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    else:
        producto = RVGL.objects.filter(analista=analista).filter(mes_vigencia=periodo).values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    return HttpResponse(producto)

def json_buro(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
    	buro = RVGL.objects.exclude(dic_buro='AL').exclude(dic_buro='NULL').filter(mes_vigencia=periodo).values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')
    else:
        buro = RVGL.objects.exclude(dic_buro='AL').exclude(dic_buro='NULL').filter(analista=analista).filter(mes_vigencia=periodo).values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')
    return HttpResponse(buro)

def json_importexprod(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
        importexprod = RVGL.objects.filter(mes_vigencia=periodo).values('producto_esp').annotate(sum_importexprod=Sum('importe_solic')).order_by('producto_esp')
    else:
        importexprod = RVGL.objects.filter(analista=analista).filter(mes_vigencia=periodo).values('producto_esp').annotate(sum_importexprod=Sum('importe_solic')).order_by('producto_esp')
    print importexprod
    return HttpResponse(importexprod)

def json_tiempo(request):
    periodo = request.POST['periodo']
    banca = request.POST['banca']
    analista = request.POST['analista']
    if request.POST['banca'] == 'TODOS': 
        tiempo = RVGL.objects.filter(mes_vigencia=periodo).filter(analista=analista).values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval') 
    else:
	if request.POST['analista'] == 'TODOS':
	   tiempo = RVGL.objects.filter(mes_vigencia=periodo).filter(seco=banca).values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')
	else:
    	   tiempo = RVGL.objects.filter(mes_vigencia=periodo).filter(seco=banca).filter(analista=analista).values('dias_eval').annotate(num_tiempo=Count('dias_eval')).order_by('dias_eval')
    return HttpResponse(tiempo)

def json_importexdict(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
        importexdict = RVGL.objects.filter(mes_vigencia=periodo).values('dictamen').annotate(sum_importexdict=Sum('importe_solic')).order_by('dictamen')
    else:
        importexdict = RVGL.objects.filter(analista=analista).filter(mes_vigencia=periodo).values('dictamen').annotate(sum_importexdict=Sum('importe_solic')).order_by('dictamen')
    return HttpResponse(importexdict)

def json_dictamenxsco(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
	dictamenxsco = RVGL.objects.filter(mes_vigencia=periodo).values('dictamen').annotate(num_dictamenxsco=Count('dictamen_sco')).order_by('dictamen')
    else:
        dictamenxsco = RVGL.objects.filter(mes_vigencia=periodo).filter(analista=analista).values('dictamen').annotate(num_dictamenxsco=Count('dictamen_sco')).order_by('dictamen')
    return HttpResponse(dictamenxsco)

def json_scoxllenado(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
	scoxllenado = RVGL.objects.filter(mes_vigencia=periodo).exclude(sco='O').values('sco').annotate(num_scoxllenado=Count('sco')).order_by('sco')
    else:
	scoxllenado = RVGL.objects.filter(mes_vigencia=periodo).filter(analista=analista).exclude(sco='O').values('sco').annotate(num_scoxllenado=Count('sco')).order_by('sco')
    return HttpResponse(scoxllenado)

def json_scoxforzaje(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    #if request.method == 'TODOS'
    if request.POST['analista'] == 'TODOS':
       scoxforzaje = RVGL.objects.filter(mes_vigencia=periodo).filter(dictamen_sco='RE').exclude(seg_prime='NULL').values('seg_prime').annotate(num_scoxforzaje=Count('seg_prime')).order_by('seg_prime')
    else:
       scoxforzaje = RVGL.objects.filter(mes_vigencia=periodo).filter(analista=analista).filter(dictamen_sco='RE').exclude(seg_prime='NULL').values('seg_prime').annotate(num_scoxforzaje=Count('seg_prime')).order_by('seg_prime')
    return HttpResponse(scoxforzaje)

def json_scoxdictamen(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    if request.POST['analista'] == 'TODOS':
       scoxdictamen = RVGL.objects.filter(mes_vigencia=periodo).exclude(dictamen_sco='NULL').values('dictamen_sco').annotate(num_scoxdictamen=Count('dictamen_sco')).order_by('dictamen_sco')
    else:
       scoxdictamen = RVGL.objects.filter(mes_vigencia=periodo).filter(analista=analista).exclude(dictamen_sco='NULL').values('dictamen_sco').annotate(num_scoxdictamen=Count('dictamen_sco')).order_by('dictamen_sco')
    return HttpResponse(scoxdictamen)

def json_top20terr(request):
    periodo = request.POST['periodo']
    analista = request.POST['analista']
    if request.POST['analista'] == 'TODOS':
       top20terr1 = RVGL.objects.filter(mes_vigencia=periodo).values('territorio_nuevo').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic')).order_by('-sum_top20terr1')[:20]
       top20terr2 = RVGL.objects.filter(mes_vigencia=periodo).exclude(importe_aprob=0).values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
    else:
       top20terr1 = RVGL.objects.filter(mes_vigencia=periodo).filter(analista=analista).values('territorio_nuevo').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic')).order_by('-sum_top20terr1')[:20]
       top20terr2 = RVGL.objects.filter(mes_vigencia=periodo).filter(analista=analista).exclude(importe_aprob=0).values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
    return HttpResponse(top20terr1, top20terr2)


# Vistas para carga de csv
def load(request):
    static_url=settings.STATIC_URL
    #RVGL.objects.all().delete()
    #Evaluaciontc.objects.all().delete()
    #Evaluacionpld.objects.all().delete()
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


def carga_campana(request):
    if request.method == 'POST':
        form = UploadCampana(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['campana']
            CampanaCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            print "no es valido"
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_caidas(request):
    if request.method == 'POST':
        form = UploadCaida(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['caidas']
            CaidaCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_verificaciones(request):
    if request.method == 'POST':
        form = UploadVerificaciones(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['verificaciones']
            VerificacionesCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_evaluaciontc(request):
    if request.method == 'POST':
        form = UploadEvaluaciontc(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['evaluaciontc']
            EvaluaciontcCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_evaluacionpld(request):
    if request.method == 'POST':
        form = UploadEvaluacionpld(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['evaluacionpld']
            EvaluacionpldCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_seguimiento1(request):
    if request.method == 'POST':
        form = UploadSegiumiento1(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['seguimiento1']
            Seguimiento1Csv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)
