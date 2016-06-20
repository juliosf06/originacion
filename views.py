# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Max, Case, When, IntegerField, F, Q, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response as render
from django.template import RequestContext

from datetime import datetime, timedelta
from models import *
from forms import *
from django.contrib.auth import authenticate, login, logout

import csv, itertools
import sys


fecha_actual = datetime.now().strftime("%Y%m")
m1 = datetime.now()-timedelta(days=1*30)
before1 = m1.strftime("%Y%m")
m2 = datetime.now()-timedelta(days=2*30)
before2 = m2.strftime("%Y%m")
m3 = datetime.now()-timedelta(days=3*30)
before3 = m3.strftime("%Y%m")
m6 = datetime.now()-timedelta(days=6*30)
before6 = m6.strftime("%Y%m")
m7 = datetime.now()-timedelta(days=7*30)
before7 = m7.strftime("%Y%m")
m8 = datetime.now()-timedelta(days=8*30)
before8 = m8.strftime("%Y%m")
m9 = datetime.now()-timedelta(days=9*30)
before9 = m9.strftime("%Y%m")
m11 = datetime.now()-timedelta(days=11*30)
before11 = m11.strftime("%Y%m")
m12 = datetime.now()-timedelta(days=12*30)
before12 = m12.strftime("%Y%m")
m14 = datetime.now()-timedelta(days=14*30)
before14 = m14.strftime("%Y%m")
m18 = datetime.now()-timedelta(days=18*30)
before18 = m18.strftime("%Y%m")
print fecha_actual
print before9
#print before6
#print before12
#print before18

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

def prueba(request):
    banca = RVGL.objects.filter(mes_vigencia='201602').values('seco').annotate(num_seco=Count('seco')).order_by('seco')
    dictamen = RVGL.objects.filter(mes_vigencia='201602').values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
    static_url=settings.STATIC_URL

    return render('reports/prueba.html', locals(),
                  context_instance=RequestContext(request))

# 2.- Vistas para reportes de Campaña
def campana_resumen(request,fecha=fecha_actual):
    control_fecha = Campana2.objects.values('mes_vigencia').distinct().order_by('-mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    segmento_lista = Campana2.objects.values('segmento').exclude(segmento='REFERIDO').filter( mes_vigencia=fecha).order_by('segmento').distinct()
    clientes = Campana2.objects.values('segmento').filter(mes_vigencia= fecha).exclude(segmento='REFERIDO').annotate(num_clientes=Sum('ofertas')).order_by('segmento')
    montos2 = Campana2.objects.values('segmento').exclude(segmento='REFERIDO').annotate(monto=Sum(F('monto_tc')+F('monto_pld')+F('monto_veh')+F('monto_subrogacion')+F('monto_tc_entry_level')+F('monto_renovado')+F('monto_auto_2da')+F('monto_adelanto_sueldo')+F('monto_efectivo_plus')+F('monto_prestamo_inmediato')+F('monto_incr_linea'))).filter(mes_vigencia=fecha).order_by('segmento')
    detalles = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'), q_efectivo_plus=Sum('q_efectivo_plus'), q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea'),monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000), monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000), monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000), monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))
    total = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(total_q=Sum(F('q_tc')+F('q_pld')+F('q_veh')+F('q_subrogacion')+F('q_renovado')+F('q_auto_2da')+F('q_adelanto_sueldo')+F('q_efectivo_plus')+F('q_prestamo_inmediato')+F('q_incr_linea')),total_m=Sum(F('monto_tc')/1000000+F('monto_pld')/1000000+F('monto_veh')/1000000+F('monto_subrogacion')/1000000+F('monto_renovado')/1000000+F('monto_auto_2da')/1000000+F('monto_adelanto_sueldo')/1000000+F('monto_efectivo_plus')/1000000+F('monto_prestamo_inmediato')/1000000+F('monto_incr_linea')/1000000))
    detalles2 = zip(detalles,total)

    segmento_fast = Campana2.objects.values('segmento','tipo_clie' ).exclude(segmento__in=['NoCli','EMPLEADO','REFERIDO']).filter( mes_vigencia=fecha, tipo_clie='A1' ).annotate(cantidad=Sum('ofertas')).order_by('segmento')
    segmento_cs = Campana2.objects.filter(mes_vigencia=fecha, tipo_clie='1A').exclude(segmento__in=['NoCli','EMPLEADO','REFERIDO']).values('segmento','tipo_clie').annotate(cantidad=Sum('ofertas')).order_by('segmento')
    seg_tot = Campana2.objects.filter(mes_vigencia=fecha).values('segmento').exclude(segmento__in=['NoCli','EMPLEADO','REFERIDO']).annotate(total=Sum('ofertas')).order_by('segmento')
    segmento_cs2 = Campana2.objects.filter(mes_vigencia=fecha, tipo_clie='1A',segmento='NoCli').values('segmento','tipo_clie' ).annotate(cantidad=Sum('ofertas')).order_by('segmento')
    seg_tot2 = Campana2.objects.filter(mes_vigencia=fecha, segmento='NoCli').values('segmento').annotate(total=Sum('ofertas')).order_by('segmento')
    segmento = itertools.izip_longest(segmento_fast, segmento_cs,seg_tot)
    total2_fast = Campana2.objects.filter(mes_vigencia=fecha, tipo_clie='A1' ).values('tipo_clie').annotate(total_f=Sum('ofertas')).order_by('tipo_clie')
    total2_cs = Campana2.objects.filter(mes_vigencia=fecha, tipo_clie='1A').values('tipo_clie').annotate(total_c=Sum('ofertas')).order_by('tipo_clie')
    total2_tot = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(total_t=Sum('ofertas'))
    empleado_fast = Campana2.objects.values('tipo_clie').filter(mes_vigencia=fecha, tipo_clie='A1',segmento='EMPLEADO').annotate(cantidad=Sum('ofertas'))
    empleado_cs = Campana2.objects.values('tipo_clie').filter(mes_vigencia=fecha, tipo_clie='1A',segmento='EMPLEADO').annotate(cantidad=Sum('ofertas'))
    empleado_total = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha, segmento='EMPLEADO').annotate(cantidad=Sum('ofertas'))
    empleado=itertools.izip_longest(empleado_fast, empleado_cs, empleado_total)
    total2 = zip(total2_fast,total2_cs,total2_tot,total2_tot)
    no_clie = zip(segmento_cs2,seg_tot2)

    flujo_fast = Campana2.objects.values('verificacion','tipo_clie' ).filter(mes_vigencia=fecha,tipo_clie='A1').annotate(cantidad=Sum('ofertas')).order_by('verificacion')
    flujo_cs = Campana2.objects.values('verificacion','tipo_clie' ).filter(mes_vigencia=fecha,tipo_clie='1A').annotate(cantidad=Sum('ofertas')).order_by('verificacion')
    flujo_total1= Campana2.objects.values('verificacion').filter(mes_vigencia=fecha).annotate(total=Sum('ofertas')).order_by('verificacion')
    total_fast= Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,tipo_clie='A1').annotate(total=Sum('ofertas'))
    total_cs= Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,tipo_clie='1A').annotate(total=Sum('ofertas'))
    total3 = zip(total_fast,total_cs,total2_tot)
    flujo = zip(flujo_fast,flujo_cs,flujo_total1)

    flujo_fast_tdc = Campana2.objects.values('verificacion','tipo_clie' ).filter(mes_vigencia=fecha,tipo_clie='A1').annotate(cantidad=Sum('q_tc')).order_by('verificacion')
    flujo_cs_tdc = Campana2.objects.values('verificacion','tipo_clie' ).filter(mes_vigencia=fecha,tipo_clie='1A').annotate(cantidad=Sum('q_tc')).order_by('verificacion')
    flujo_total1_tdc= Campana2.objects.values('verificacion').filter(mes_vigencia=fecha).annotate(total=Sum('q_tc')).order_by('verificacion')
    total_fast_tdc= Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,tipo_clie='A1').annotate(total=Sum('q_tc'))
    total_cs_tdc= Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,tipo_clie='1A').annotate(total=Sum('q_tc'))
    total3_tot = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(total_t=Sum('q_tc'))
    total3_tdc = zip(total_fast_tdc,total_cs_tdc,total3_tot)
    flujo_tdc = zip(flujo_fast_tdc,flujo_cs_tdc,flujo_total1_tdc)

    prestamo_fast = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,tipo_clie='A1').annotate(pld=Sum('q_pld'),pat=Sum('q_prestamo_inmediato'))
    prestamo_cs = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,tipo_clie='1A').annotate(pld=Sum('q_pld'),pat=Sum('q_prestamo_inmediato'))
    prestamo_total = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha).annotate(pld=Sum('q_pld'),pat=Sum('q_prestamo_inmediato'))
    prestamo = zip(prestamo_fast, prestamo_cs, prestamo_total)  

    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_resumen.html', locals(),
                  context_instance=RequestContext(request))

#@login_required
#def campana_detalles(request):
    #detalles = Campana.objects.filter(mes_vigencia='201604').values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_tc_entry_level=Sum('q_tc_entry_level'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea'),monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000),monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000),monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000),monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))
    #control_segmentos = Campana.objects.all().values('segmento').distinct('segmento')
    #print detalles
    #static_url=settings.STATIC_URL
    #tipo_side = 1
    #return render('reports/campana_detalles.html', locals(),
                  #context_instance=RequestContext(request))

@login_required
def campana_detalles(request, segmento='TOTAL', fecha=fecha_actual):
    texto = str(segmento)
    lista = texto.split(",")
    control_fecha = Campana2.objects.values('mes_vigencia').distinct().order_by('-mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    control_segmentos = Campana2.objects.all().values('segmento').distinct('segmento')
    if segmento == 'TOTAL':
       detalles = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea')).annotate(monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000),monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000),monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000),monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))
    else:
       detalles = Campana2.objects.filter(segmento=segmento).filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea')).annotate(monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000),monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000),monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000),monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))

    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_detalles.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def campana_caidas(request, fecha=fecha_actual):
    combo_fechas = Caida.objects.values('mes_vigencia').distinct('mes_vigencia').order_by('-mes_vigencia')
    time = {}
    for i in combo_fechas:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    caidas_ms = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='MS').annotate(num_caidaxms=Sum('cantidad')).order_by('caida')
    caidas_ava = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='AVA').annotate(num_caidaxava=Sum('cantidad')).order_by('caida')
    caidas_noph = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='NO PH + PASIVO').annotate(num_caidaxnoph=Sum('cantidad')).order_by('caida')
    caidas_noclie = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='NO CLIENTE').annotate(num_caidaxnoclie=Sum('cantidad')).order_by('caida')
    caidas = zip(caidas_ms, caidas_ava, caidas_noph, caidas_noclie)
    static_url=settings.STATIC_URL
    grafica  = Caida.objects.values('caida').filter(mes_vigencia=fecha).exclude(segmento='PNN').annotate(num_caida=Sum('cantidad')).order_by('caida')
    total = Caida.objects.values('mes_vigencia').filter(mes_vigencia=fecha).exclude(segmento='PNN').annotate(total=Sum('cantidad'))
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
    #coord = reversed(coord)
    diferencia = zip(coord,[{ 'caida': 'Total Evaluados', 'num_caida': total[0]['total'] }]+list(grafica))
    diferencia = reversed(diferencia)

    return render('reports/campana_caidas.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def campana_exoneraciones(request, segmento='TOTAL'):
    texto = str(segmento)
    lista = texto.split(",")
    meses = Campana2.objects.values('mes_vigencia').distinct().order_by('mes_vigencia')
    if segmento == 'TOTAL':
        exo_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_ambas_dict = {}
	for i in meses:
	    for j in exo_ambas:
		if i['mes_vigencia'] == j['mes_vigencia']:
		    exo_ambas_dict[i['mes_vigencia']]=j['cantidad']
		    break
		else:
		    exo_ambas_dict[i['mes_vigencia']]=0

        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')

	esph = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='MS REGULAR').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	VLvalida = Exoneracion.objects.values( 'cat_cliente').filter(tipo='VL',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M','VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	pasiveros = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='PASIVERO >S/.1,000 X 6MESES').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	vip = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='MS VIP/PREMIUM').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	noph = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='NO PH ALTO VALOR').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	cts = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='CON CTS').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	tendencia = Exoneracion.objects.values('cat_cliente').filter(tipo='VL',motivo_exo__in=['TENENCIA DE VEH U12M','TENENCIA DE PLD U12M']).annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	dependiente = Exoneracion.objects.values('cat_cliente').filter(tipo='VL',motivo_exo='DEPENDIENTE / AFILIADO ACTIVO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	total1 = Exoneracion.objects.values('cat_cliente').filter(tipo='VL').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	tl1 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='MS REGULAR').annotate(cantidad=Sum('cantidad'))
	tl2 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M','VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad'))
	tl3 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='PASIVERO >S/.1,000 X 6MESES').annotate(cantidad=Sum('cantidad'))
	tl4 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='MS VIP/PREMIUM').annotate(cantidad=Sum('cantidad'))
	tl5 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='NO PH ALTO VALOR').annotate(cantidad=Sum('cantidad'))
	tl6 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='CON CTS').annotate(cantidad=Sum('cantidad'))
	tl7 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo__in=['TENENCIA DE VEH U12M','TENENCIA DE PLD U12M']).annotate(cantidad=Sum('cantidad'))
	tl8 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='DEPENDIENTE / AFILIADO ACTIVO').annotate(cantidad=Sum('cantidad'))
	tl9 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL').annotate(cantidad=Sum('cantidad'))

	vip2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='PREMIUM / VIP').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	pasivero2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='BUEN PASIVERO / BAJO RIESGO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	esph2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='PAGOHABER CON BUEN PERFIL').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	hipo2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='CON BUEN HIPOTECARIO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	veri2 = Exoneracion.objects.values('cat_cliente').filter(tipo='VD',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M','VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	equi2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='COMPRA EN EQUIFAX').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	ubi2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='UBIGEO EXONERADO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	fast2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='NULL').exclude(cat_cliente='9. No Identificado').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	total2 = Exoneracion.objects.values('cat_cliente').filter(tipo='VD').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	tv1 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='PREMIUM / VIP').annotate(cantidad=Sum('cantidad'))
	tv2 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='BUEN PASIVERO / BAJO RIESGO').annotate(cantidad=Sum('cantidad'))
	tv3 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='PAGOHABER CON BUEN PERFIL').annotate(cantidad=Sum('cantidad'))
	tv4 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='CON BUEN HIPOTECARIO').annotate(cantidad=Sum('cantidad'))
	tv5 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M', 'VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad'))
	tv6 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='COMPRA EN EQUIFAX').annotate(cantidad=Sum('cantidad'))
	tv7 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='UBIGEO EXONERADO').annotate(cantidad=Sum('cantidad'))
	tv8 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='NULL').annotate(cantidad=Sum('cantidad'))
	tv9 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD').annotate(cantidad=Sum('cantidad'))
    else:
        exo_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO AMBAS', segmento__in=lista).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_ambas_dict = {}
	for i in meses:
	    for j in exo_ambas:
		if i['mes_vigencia'] == j['mes_vigencia']:
		    exo_ambas_dict[i['mes_vigencia']]=j['cantidad']
		    break
		else:
		    exo_ambas_dict[i['mes_vigencia']]=0

        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL', segmento__in=lista).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD', segmento__in=lista).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS', segmento__in=lista).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')

	esph = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='MS REGULAR').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	VLvalida = Exoneracion.objects.values( 'cat_cliente').filter(tipo='VL',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M','VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	pasiveros = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='PASIVERO >S/.1,000 X 6MESES').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	vip = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='MS VIP/PREMIUM').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	noph = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='NO PH ALTO VALOR').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	cts = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VL',motivo_exo='CON CTS').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	tendencia = Exoneracion.objects.values('cat_cliente').filter(tipo='VL',motivo_exo__in=['TENENCIA DE VEH U12M','TENENCIA DE PLD U12M']).annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	dependiente = Exoneracion.objects.values('cat_cliente').filter(tipo='VL',motivo_exo='DEPENDIENTE / AFILIADO ACTIVO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	total1 = Exoneracion.objects.values('cat_cliente').filter(tipo='VL').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	tl1 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='MS REGULAR').annotate(cantidad=Sum('cantidad'))
	tl2 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M','VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad'))
	tl3 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='PASIVERO >S/.1,000 X 6MESES').annotate(cantidad=Sum('cantidad'))
	tl4 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='MS VIP/PREMIUM').annotate(cantidad=Sum('cantidad'))
	tl5 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='NO PH ALTO VALOR').annotate(cantidad=Sum('cantidad'))
	tl6 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='CON CTS').annotate(cantidad=Sum('cantidad'))
	tl7 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo__in=['TENENCIA DE VEH U12M','TENENCIA DE PLD U12M']).annotate(cantidad=Sum('cantidad'))
	tl8 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL',motivo_exo='DEPENDIENTE / AFILIADO ACTIVO').annotate(cantidad=Sum('cantidad'))
	tl9 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VL').annotate(cantidad=Sum('cantidad'))

	vip2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='PREMIUM / VIP').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	pasivero2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='BUEN PASIVERO / BAJO RIESGO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	esph2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='PAGOHABER CON BUEN PERFIL').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	hipo2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='CON BUEN HIPOTECARIO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	veri2 = Exoneracion.objects.values('cat_cliente').filter(tipo='VD',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M','VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	equi2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='COMPRA EN EQUIFAX').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	ubi2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='UBIGEO EXONERADO').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	fast2 = Exoneracion.objects.values('motivo_exo', 'cat_cliente').filter(tipo='VD',motivo_exo='NULL').exclude(cat_cliente='9. No Identificado').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	total2 = Exoneracion.objects.values('cat_cliente').filter(tipo='VD').annotate(cantidad=Sum('cantidad')).order_by('cat_cliente')
	tv1 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='PREMIUM / VIP').annotate(cantidad=Sum('cantidad'))
	tv2 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='BUEN PASIVERO / BAJO RIESGO').annotate(cantidad=Sum('cantidad'))
	tv3 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='PAGOHABER CON BUEN PERFIL').annotate(cantidad=Sum('cantidad'))
	tv4 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='CON BUEN HIPOTECARIO').annotate(cantidad=Sum('cantidad'))
	tv5 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo__in=['VERIFICACIONES VALIDAS EN ULT12M', 'VERIFICACIONES VALIDAS EN ULT6M']).annotate(cantidad=Sum('cantidad'))
	tv6 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='COMPRA EN EQUIFAX').annotate(cantidad=Sum('cantidad'))
	tv7 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='UBIGEO EXONERADO').annotate(cantidad=Sum('cantidad'))
	tv8 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD',motivo_exo='NULL').annotate(cantidad=Sum('cantidad'))
	tv9 = Exoneracion.objects.values('mes_vigencia').filter(tipo='VD').annotate(cantidad=Sum('cantidad'))

    control_segmentos = Campana2.objects.all().values('segmento').distinct('segmento')
    total_vl = itertools.izip_longest(tl1,tl2,tl3,tl4,tl5,tl6,tl7, tl8,tl9)
    total_vd = itertools.izip_longest(tv1,tv2,tv3,tv4,tv5,tv6,tv7, tv8,tv9)
    motivos = itertools.izip_longest(esph,VLvalida,pasiveros,vip,noph, cts, tendencia, dependiente,total1)
    motivos2 = itertools.izip_longest(vip2,pasivero2,esph2,hipo2,veri2, equi2,ubi2,fast2,total2)
    exoneraciones = itertools.izip_longest(exo_ambas,exo_vl,exo_vd,req_ambas)
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_exoneraciones.html', locals(),
                  context_instance=RequestContext(request))


#@login_required
#def campana_flujo(request):
    #flujo1 = FlujOperativo.objects.values('tipo','grupo_exoneracion').filter(mes_vigencia='201603',grupo_exoneracion='EXON. SOLO VL').annotate(num_flujo1=Sum('cantidad')).order_by('tipo')
    #flujo2 = FlujOperativo.objects.values('tipo','grupo_exoneracion').filter(mes_vigencia='201603',grupo_exoneracion='EXON. SOLO VD').annotate(num_flujo2=Sum('cantidad')).order_by('tipo')
    #flujo3 = FlujOperativo.objects.values('tipo','grupo_exoneracion').filter(mes_vigencia='201603',grupo_exoneracion='EXON. AMBAS').annotate(num_flujo3=Sum('cantidad')).order_by('tipo')
    #flujo4 = FlujOperativo.objects.values('tipo','grupo_exoneracion').filter(mes_vigencia='201603',grupo_exoneracion='REQUIERE AMBAS').annotate(num_flujo4=Sum('cantidad')).order_by('tipo')

    #flujo = zip(flujo1, flujo2, flujo3, flujo4)
    #static_url=settings.STATIC_URL
    #tipo_side = 1
    #return render('reports/campana_flujo.html', locals(),
                  #context_instance=RequestContext(request))


@login_required
def campana_flujo(request, fecha=fecha_actual):
    control_fecha = Campana2.objects.values('mes_vigencia').distinct().order_by('-mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    flujo1 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='EXONERADO AMBAS').annotate(num_flujo1=Sum('ofertas')).order_by('tipo_clie')
    flujo2 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='EXONERADO SOLO VD').annotate(num_flujo2=Sum('ofertas')).order_by('tipo_clie')
    flujo3 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='EXONERADO SOLO VL').annotate(num_flujo3=Sum('ofertas')).order_by('tipo_clie')
    flujo4 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='REQUIERE AMBAS').annotate(num_flujo4=Sum('ofertas')).order_by('tipo_clie')
    total1 = Campana2.objects.values('tipo_clie').filter(mes_vigencia=fecha).annotate(cantidad=Sum('ofertas'))
    t1 = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,verificacion='EXONERADO AMBAS').annotate(cantidad=Sum('ofertas')).order_by('verificacion')
    t2 = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,verificacion='EXONERADO SOLO VD').annotate(cantidad=Sum('ofertas')).order_by('verificacion')
    t3 = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,verificacion='EXONERADO SOLO VL').annotate(cantidad=Sum('ofertas')).order_by('verificacion')
    t4 = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha,verificacion='REQUIERE AMBAS').annotate(cantidad=Sum('ofertas')).order_by('verificacion')
    t5 = Campana2.objects.values('mes_vigencia').filter(mes_vigencia=fecha).annotate(cantidad=Sum('ofertas'))
    total = zip(t1,t2,t3,t4,t5)
    flujo = zip(flujo1, flujo2, flujo3, flujo4,total1)
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_flujo.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def campana_altasempresa(request):
    control_fecha = AltasEmpresa.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    fecha = []
    for i in control_fecha:
        fecha.append(i['mes_vigencia'])
    fecha1= fecha[0]
    fecha2= fecha[1]
    fecha3= fecha[2]
    fecha4= fecha[3]
    fecha5= fecha[4]
    fecha6= fecha[5]

    alta1_m1 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia=fecha6).annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m1 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia=fecha6).annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m1 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia=fecha6).annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m1 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia=fecha6).annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m2 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia=fecha5).annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m2 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia=fecha5).annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m2 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia=fecha5).annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m2 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia=fecha5).annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m3 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia=fecha4).annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m3 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia=fecha4).annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m3 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia=fecha4).annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m3 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia=fecha4).annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m4 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia=fecha3).annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m4 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia=fecha3).annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m4 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia=fecha3).annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m4 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia=fecha3).annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m5 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia=fecha2).annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m5 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia=fecha2).annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m5 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia=fecha2).annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m5 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia=fecha2).annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m6 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia=fecha1).annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m6 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia=fecha1).annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m6 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia=fecha1).annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m6 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia=fecha1).annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta_s1 = AltasSegmento.objects.values('segmento','grupo').filter(grupo='1.Oferta < SF').annotate(num_alta=Sum('cantidad')).order_by('segmento')
    alta_s2 = AltasSegmento.objects.values('segmento','grupo').filter(grupo='2.Oferta >= SF').annotate(num_alta=Sum('cantidad')).order_by('segmento')
    alta_st = AltasSegmento.objects.values('segmento').annotate(num_alta=Sum('cantidad')).order_by('segmento')
    alta_tot = AltasEmpresa.objects.values('mes_vigencia').annotate(total=Sum('cantidad')).order_by('mes_vigencia')
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_altasempresa.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campana_prestinmediato(request):
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_prestinmediato.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campanaweb(request):
    campanaweb = CampanaWeb.objects.all().order_by('fecha_recepcion')

    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_web.html', locals(),
                  context_instance=RequestContext(request))


# 3.- Vistas para reportes de RVGL
@login_required
def rvgl_resumen(request, fecha=fecha_actual, analista='TODOS'):
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    evaluacion = RVGL.objects.filter(mes_vigencia=fecha).values('analista').annotate(num_eval=Count('rvgl'),dias=Count('dias_eval')).order_by('analista')
    if analista == "TODOS":
    	banca = RVGL.objects.filter(mes_vigencia=fecha).values('seco').annotate(num_seco=Count('seco')).order_by('seco')
  	dictamen = RVGL.objects.filter(mes_vigencia=fecha).values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
        producto = RVGL.objects.filter(mes_vigencia=fecha).values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    	buro = RVGL.objects.exclude(dic_buro__in =['AL','NULL', '']).filter(mes_vigencia=fecha).values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')
    else:
    	banca = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('seco').annotate(num_seco=Count('seco')).order_by('seco')
  	dictamen = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
        producto = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    	buro = RVGL.objects.exclude(dic_buro__in =['AL','NULL']).filter(mes_vigencia=fecha, analista=analista).values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_resumen.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_resumenximporte(request, fecha=fecha_actual, analista='TODOS'):
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    if analista == 'TODOS':
  	importexdict = RVGL.objects.filter(mes_vigencia=fecha).values('dictamen').annotate(sum_importe=Sum('importe_solic')).order_by('dictamen')
        importexprod = RVGL.objects.filter(mes_vigencia=fecha).values('producto_esp').annotate(sum_importexprod=Sum('importe_solic')).order_by('producto_esp')

    else:
  	importexdict = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('dictamen').annotate(sum_importe=Sum('importe_solic')).order_by('dictamen')
        importexprod = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('producto_esp').annotate(sum_importexprod=Sum('importe_solic')).order_by('producto_esp')

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_resumenximporte.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def rvgl_tiempo(request, fecha=fecha_actual, analista='TODOS'):
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_seco = RVGL.objects.values('seco').distinct('seco')
    if analista == 'TODOS':
       tiempo10 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0', dias_eval__lte='3', seco__in=['BP','CA']).annotate(num_tiempo=Count(F('dias_eval') )).order_by('dias_eval')
       tiempo11 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15',seco__in=['BP','CA']).annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
       tiempo20 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0',dias_eval__lte='3', seco='BP3').annotate(num_tiempo=Count(F('dias_eval'))).order_by('dias_eval')
       tiempo21 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15', seco='BP3').annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
       dias = [".El mismo dia","1 Dia","2 Dias","3 Dias","mas 3 Dias"]
       lista = []
       num_tiempo = {}
       for i in tiempo10:
	   lista.append(i['num_tiempo'])
       for i in tiempo11:
           lista.append(i['num_tiempo'])
       if len(lista) == 0 :
           num_tiempo[".El mismo dia"] = 0
           num_tiempo["1 Dia"] = 0
           num_tiempo["2 Dias"] = 0
           num_tiempo["3 Dias"] = 0
           num_tiempo["mas 3 Dias"] = 0
       else:
	   j = 0
	   while j < len(lista):
              num_tiempo[dias[j]] = lista[j]
	      j +=1

       lista2 = []
       num_tiempo2 = {}
       for i in tiempo20:
	   lista2.append(i['num_tiempo'])
       for i in tiempo21:
           lista2.append(i['num_tiempo'])
       if len(lista) == 0 :
           num_tiempo2[".El mismo dia"] = 0
           num_tiempo2["1 Dia"] = 0
           num_tiempo2["2 Dias"] = 0
           num_tiempo2["3 Dias"] = 0
           num_tiempo2["mas 3 Dias"] = 0
       else:
	   j = 0
	   while j < len(lista2):
              num_tiempo2[dias[j]] = lista2[j]
	      j +=1
    else:
       tiempo10 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0', dias_eval__lte='3', seco__in=['BP','CA'],analista=analista).annotate(num_tiempo=Count(F('dias_eval')) ).order_by('dias_eval')
       tiempo11 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15',seco__in=['BP','CA'],analista=analista).annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
       tiempo20 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0',dias_eval__lte='3', seco='BP3',analista=analista).annotate(num_tiempo=Count(F('dias_eval'))).order_by('dias_eval')
       tiempo21 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15', seco='BP3',analista=analista).annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
       dias = [".El mismo dia","1 Dia","2 Dias","3 Dias","mas 3 Dias"]
       lista = []
       num_tiempo = {}
       for i in tiempo10:
	   lista.append(i['num_tiempo'])
       for i in tiempo11:
           lista.append(i['num_tiempo'])
       if len(lista) == 0 :
           num_tiempo[".El mismo dia"] = 0
           num_tiempo["1 Dia"] = 0
           num_tiempo["2 Dias"] = 0
           num_tiempo["3 Dias"] = 0
           num_tiempo["mas 3 Dias"] = 0
       else:
	   j = 0
	   while j < len(lista):
              num_tiempo[dias[j]] = lista[j]
	      j +=1

       lista2 = []
       num_tiempo2 = {}
       for i in tiempo20:
	   lista2.append(i['num_tiempo'])
       for i in tiempo21:
           lista2.append(i['num_tiempo'])
       if len(lista) == 0 :
           num_tiempo2[".El mismo dia"] = 0
           num_tiempo2["1 Dia"] = 0
           num_tiempo2["2 Dias"] = 0
           num_tiempo2["3 Dias"] = 0
           num_tiempo2["mas 3 Dias"] = 0
       else:
	   j = 0
	   while j < len(lista2):
              num_tiempo2[dias[j]] = lista2[j]
	      j +=1


    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_tiempo.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_mapa(request, fecha='201312'):
    meses = Mapa.objects.values('codmes').order_by('codmes').distinct()
    list_meses=[]; d=0
    for i in meses:
	list_meses.append(i['codmes'])
    d = len(list_meses)
    ubigeo = Mapa.objects.values('ubigeo').order_by('ubigeo').distinct()
    distrito = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA').annotate(mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    numero=Mapa.objects.values('ubigeo','codmes').filter(provincia='LIMA', codmes=fecha).annotate(num=Sum('ctas')).order_by('ubigeo')
    distrito1 = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA', codmes=fecha).annotate(mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    dict_moras = {}; dict_moras1 = {}; 
    dict_moras2 = {}; dict_moras3 = {};dict_moras4 = {};
    for i in distrito:
	if i['codmes']=='201312':
	   if i['mora']>3:
	      dict_moras[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras[i['ubigeo']]='#66BD63'
	if i['codmes']=='201412':
	   if i['mora']>3:
	      dict_moras1[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras1[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras1[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras1[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras1[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras1[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras1[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras1[i['ubigeo']]='#66BD63'
	if i['codmes']=='201512':
	   if i['mora']>3:
	      dict_moras2[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras2[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras2[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras2[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras2[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras2[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras2[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras2[i['ubigeo']]='#66BD63'
	if i['codmes']=='201604':
	   if i['mora']>3:
	      dict_moras3[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras3[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras3[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras3[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras3[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras3[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras3[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras3[i['ubigeo']]='#66BD63'

    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/mapa.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def departamentos_web(request,base=1):
    print base
    control_evaluacion=DepartamentosWeb.objects.values('base').distinct().order_by('base')
    departamentos = DepartamentosWeb.objects.values('departamento').distinct().order_by('departamento')
    eval_tc = DepartamentosWeb.objects.values('base', 'departamento').exclude(oferta_tc='0').filter(base=base).annotate(num_tdc=Count('oferta_tc')).order_by('base')
    dict_tc = {}
    for i in departamentos:
	for j in eval_tc:
	   if j['departamento']==i['departamento']:
		dict_tc[i['departamento']]=j['num_tdc']
		break
	   else:
		dict_tc[i['departamento']]=0
    eval_pld = DepartamentosWeb.objects.values('base', 'departamento').exclude(oferta_pld='0').filter(base=base).annotate(num_pld=Count('oferta_pld')).order_by('base')
    dict_pld = {}
    for i in departamentos:
	for j in eval_pld:
	   if i['departamento']==j['departamento']:
		dict_pld[i['departamento']]=j['num_pld']
		break
	   else:
		dict_pld[i['departamento']]=0

    ofertas_tc = DepartamentosWeb.objects.values('base').exclude(oferta_tc='0').annotate(num_tdc=Count('oferta_tc'),sum_tdc=Sum('oferta_tc')).order_by('base')
    ofertas_pld = DepartamentosWeb.objects.values('base').exclude(oferta_pld='0').annotate(num_pld=Count('oferta_pld'),sum_pld=Sum('oferta_pld')).order_by('base')
    ofertas=zip(ofertas_tc,ofertas_pld)
    efectividad = DepartamentosWeb.objects.values('base', 'departamento').filter(base=base).annotate(num_ofer=Sum('ofertas'),num_form=Sum('formalizado'),num_efec=Sum(F('formalizado'))*100/Sum(F('ofertas'))).order_by('base')
    dict_efec = {}; dict_ofer = {};
    dict_form = {}; dict_efect = {}; 
    for i in departamentos:
	for j in efectividad:
	   if i['departamento']==j['departamento']:
		if j['num_efec']<20:
		   dict_efec[i['departamento']]='#66BD63'
		if j['num_efec']>=20 and j['num_efec']<40:
		   dict_efec[i['departamento']]='#A6D974'
		if j['num_efec']>=40 and j['num_efec']<60:
		   dict_efec[i['departamento']]='#FED976'
		if j['num_efec']>=60 and j['num_efec']<80:
		   dict_efec[i['departamento']]='#FB8D29'
		if j['num_efec']>=80 and j['num_efec']<=100:
		   dict_efec[i['departamento']]='#E31A1C'
		break
	   else:
		dict_efec[i['departamento']]='silver'

    for i in departamentos:
	for j in efectividad:
	   if i['departamento']==j['departamento']:
		dict_form[i['departamento']]=j['num_form']
		dict_ofer[i['departamento']]=j['num_ofer']
		dict_efect[i['departamento']]=j['num_efec']
		break
	   else:
		dict_form[i['departamento']]=0
		dict_ofer[i['departamento']]=0
		dict_efect[i['departamento']]=0
    print dict_efec
    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/departamentos_web.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_resumenxsco(request, fecha=fecha_actual, analista='TODOS'):
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    dictamen = RVGL.objects.values('dictamen').distinct('dictamen').order_by('dictamen')
    if analista == 'TODOS':
       dictamenxsco_ap = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='AP').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
       listadict = ['APC','APS','DEN','DEV']
       scolista = []
       ap_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_ap:
	       if i['dictamen'] == j['dictamen']:
		  ap_dict[i['dictamen']]=j['num_dictamenxsco_ap']
		  break
	       else:
		  ap_dict[i['dictamen']]=0
       if len(ap_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(ap_dict[i['dictamen']])
       dictamenxsco_du = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='DU').annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
       du_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_du:
	       if i['dictamen'] == j['dictamen']:
		  du_dict[i['dictamen']]=j['num_dictamenxsco_du']
		  break
	       else:
		  du_dict[i['dictamen']]=0
       for i in dictamen:
           scolista.append(du_dict[i['dictamen']])
       dictamenxsco_re = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='RE').annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
       re_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_re:
	       if i['dictamen'] == j['dictamen']:
		  re_dict[i['dictamen']]=j['num_dictamenxsco_re']
		  break
	       else:
		  re_dict[i['dictamen']]=0
       for i in dictamen:
           scolista.append(re_dict[i['dictamen']])
       scoxllenado = RVGL.objects.filter(mes_vigencia=fecha).exclude(sco='O').values('sco').annotate(num_scoxllenado=Count('sco')).order_by('sco')
       scoxforzaje = RVGL.objects.filter(mes_vigencia=fecha).filter(dictamen_sco='RE').exclude(seg_prime='NULL').values('seg_prime').annotate(num_scoxforzaje=Count('seg_prime')).order_by('seg_prime')
       scoxdictamen = RVGL.objects.filter(mes_vigencia=fecha).exclude(dictamen_sco__in=['NULL','']).values('dictamen_sco' ).annotate(num_scoxdictamen=Count('dictamen_sco')).order_by('dictamen_sco')
    else:
       dictamenxsco_ap = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha,analista=analista).filter(dictamen_sco ='AP').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
       scolista = []
       ap_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_ap:
	       if i['dictamen'] == j['dictamen']:
		  ap_dict[i['dictamen']]=j['num_dictamenxsco_ap']
		  break
	       else:
		  ap_dict[i['dictamen']]=0
       if len(ap_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(ap_dict[i['dictamen']])

       dictamenxsco_du = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='DU', analista= analista).annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
       du_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_du:
	       if i['dictamen'] == j['dictamen']:
		  du_dict[i['dictamen']]=j['num_dictamenxsco_du']
		  break
	       else:
		  du_dict[i['dictamen']]=0
       if len(du_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(du_dict[i['dictamen']])
       dictamenxsco_re = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='RE',analista= analista).annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
       re_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_re:
	       if i['dictamen'] == j['dictamen']:
		  re_dict[i['dictamen']]=j['num_dictamenxsco_re']
		  break
	       else:
		  re_dict[i['dictamen']]=0
       if len(re_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(re_dict[i['dictamen']])
       scoxllenado = RVGL.objects.filter(mes_vigencia=fecha,analista= analista).exclude(sco='O').values('sco').annotate(num_scoxllenado=Count('sco')).order_by('sco')
       scoxforzaje = RVGL.objects.filter(mes_vigencia=fecha,analista= analista).filter(dictamen_sco='RE').exclude(seg_prime='NULL').values('seg_prime').annotate(num_scoxforzaje=Count('seg_prime')).order_by('seg_prime')
       scoxdictamen = RVGL.objects.filter(mes_vigencia=fecha,analista= analista).exclude(dictamen_sco__in=['NULL','']).values('dictamen_sco' ).annotate(num_scoxdictamen=Count('dictamen_sco')).order_by('dictamen_sco')

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_resumenxsco.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_top20terr(request, fecha=fecha_actual, analista='TODOS'):
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    if analista == 'TODOS':
       top20terr1 = RVGL.objects.filter(mes_vigencia=fecha).values('territorio_nuevo').exclude(territorio_nuevo='').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic')).order_by('-sum_top20terr1')[:20]
       top20terr2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0, territorio_nuevo='').values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
       top20terr = zip(top20terr1, top20terr2)
    else:
       top20terr1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('territorio_nuevo').exclude(territorio_nuevo='').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic')).order_by('-sum_top20terr1')[:20]
       top20terr2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0, territorio_nuevo='').values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
       top20terr = zip(top20terr1, top20terr2)

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20terr.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20gest(request, fecha=fecha_actual, analista='TODOS'):
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    if analista == 'TODOS':
       top20gest1 = RVGL.objects.filter(mes_vigencia=fecha).values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic'), sum_top20gest1=Sum('importe_solic')).order_by('-sum_top20gest1')[:20]
       top20gest2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest2=Count('importe_aprob'), sum_top20gest2=Sum('importe_aprob')).order_by('-sum_top20gest2')[:20]
       top20gest = zip(top20gest1,top20gest2)
    else:
       top20gest1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic'), sum_top20gest1=Sum('importe_solic')).order_by('-sum_top20gest1')[:20]
       top20gest2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest2=Count('importe_aprob'), sum_top20gest2=Sum('importe_aprob')).order_by('-sum_top20gest2')[:20]
       top20gest = zip(top20gest1,top20gest2)

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20gest.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20clie(request, fecha=fecha_actual, analista='TODOS'):
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    if analista == 'TODOS':
       top20clie1 = RVGL.objects.filter(mes_vigencia=fecha).values('cliente').annotate(num_top20clie1=Count('importe_solic'), sum_top20clie1=Sum('importe_solic')).order_by('cliente').order_by('-sum_top20clie1')[:20]
       top20clie2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0).values('cliente').annotate(num_top20clie2=Count('importe_aprob'), sum_top20clie2=Sum('importe_aprob')).order_by('-sum_top20clie2')[:20]
       top20clie = zip(top20clie1,top20clie2)
    else:
       top20clie1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('cliente').annotate(num_top20clie1=Count('importe_solic'), sum_top20clie1=Sum('importe_solic')).order_by('cliente').order_by('-sum_top20clie1')[:20]
       top20clie2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).values('cliente').annotate(num_top20clie2=Count('importe_aprob'), sum_top20clie2=Sum('importe_aprob')).order_by('-sum_top20clie2')[:20]
       top20clie = zip(top20clie1,top20clie2)

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20clie.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20ofic(request, fecha=fecha_actual, analista='TODOS'):
    control_analistas = RVGL.objects.values('analista').distinct('analista')
    control_fecha = RVGL.objects.values('mes_vigencia').distinct('mes_vigencia')
    time = {}
    for i in control_fecha:
        time[i['mes_vigencia']]=i['mes_vigencia']
    fecha = max(time.values())
    if analista == 'TODOS':
       top20ofic1 = RVGL.objects.filter(mes_vigencia=fecha).values('oficina').annotate(num_top20ofic1=Count('importe_solic'), sum_top20ofic1=Sum('importe_solic')).order_by('-sum_top20ofic1')[:20]
       top20ofic2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0).values('oficina').annotate(num_top20ofic2=Count('importe_aprob'), sum_top20ofic2=Sum('importe_aprob')).order_by('-sum_top20ofic2')[:20]
       top20ofic = zip(top20ofic1,top20ofic2)
    else:
       top20ofic1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('oficina').annotate(num_top20ofic1=Count('importe_solic'), sum_top20ofic1=Sum('importe_solic')).order_by('-sum_top20ofic1')[:20]
       top20ofic2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).values('oficina').annotate(num_top20ofic2=Count('importe_aprob'), sum_top20ofic2=Sum('importe_aprob')).order_by('-sum_top20ofic2')[:20]
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
    meses = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).order_by('mes_vigencia').distinct('mes_vigencia')

    total_form = Seguimiento1.objects.values('mes_vigencia', 'producto').filter(producto='03 Tarjeta', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    total_form_dict = {}
    for j in total_form:
	total_form_dict[j['mes_vigencia']]=j['formalizado']
    uno_form = Seguimiento1.objects.values('mes_vigencia', 'riesgos').filter(producto='03 Tarjeta', riesgos='UNO A UNO', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_fast = Seguimiento1.objects.values('mes_vigencia', 'origen').filter(producto='03 Tarjeta', origen='ORIGINACION FAST', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_uno = Seguimiento1.objects.values('mes_vigencia', 'origen').filter(producto='03 Tarjeta', origen='ORIGINACION MS', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    formalizados = zip(total_form,uno_form,camp_fast,camp_uno)

    camp_form = Seguimiento1.objects.values('mes_vigencia', 'riesgos').filter(producto='03 Tarjeta', riesgos='CAMP', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    fact_uno = Seguimiento1.objects.values('mes_vigencia', 'producto').filter(producto='03 Tarjeta', riesgos='UNO A UNO', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    fact_camp = Seguimiento1.objects.values('mes_vigencia', 'producto').filter(producto='03 Tarjeta', riesgos='CAMP', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    ticket = zip(fact_uno, fact_camp, uno_form, camp_form)

    seg_ava = Seguimiento1.objects.values('mes_vigencia', 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='1.AVA', mes_vigencia__gte=before14, mes_vigencia__lte=fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_ms = Seguimiento1.objects.values('mes_vigencia', 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='2.MS', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_noph = Seguimiento1.objects.values('mes_vigencia', 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='3.NoPH', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_nocli = Seguimiento1.objects.values('mes_vigencia', 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='4.NoCli', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    camp_seg = zip(seg_ava, seg_ms, seg_noph, seg_nocli, camp_form)

    rangos = Seguimiento1.objects.values('mes_vigencia','producto', 'rng_ing').filter(mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual,producto='03 Tarjeta').annotate(num_rango=Sum('form')).order_by('mes_vigencia')
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
	for j in rangos:
	   if i['mes_vigencia'] == j['mes_vigencia']:
		if j['rng_ing'] == '01 [3.5K - ...]':
		   rango1_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '02 [2.5K - 3.5K]':
		   rango2_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '03 [2K - 2.5K]':
		   rango3_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '04 [1.5K - 2K]':
		   rango4_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '05 [1K - 1.5K]':
		   rango5_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '06 [0 - 1K]':
		   rango6_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]

    meses_moras = Moras.objects.values('mes_form').filter(mes_form__gte=before18, mes_form__lte =before8).order_by('mes_form')

    mora6 = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('mora6')).order_by('mes_form')
    mora9 = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before11).annotate(sum_mora=Sum('mora9')).order_by('mes_form')
    mora12 = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before14).annotate(sum_mora=Sum('mora12')).order_by('mes_form')
    total_ctas = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    mora_6 = zip(mora6,total_ctas)
    mora_9 = zip(mora9,total_ctas)
    mora_12 = zip(mora12,total_ctas)
    
    total_moraxcamp = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before8,flg_camp='1. CAMPANA').annotate(sum_ctas=Sum('ctas')).order_by('mes_form')
    total_moraxcamp_dict = {}
    for i in meses_moras:
	for j in total_moraxcamp:
	    if i['mes_form'] == j['mes_form']:
               total_moraxcamp_dict[i['mes_form']]=j['sum_ctas']

    mora_camp = Moras.objects.values('mes_form','producto', 'flg_camp').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before8,flg_camp='1. CAMPANA').annotate(sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by('mes_form')
    mora6_camp_dict = {}
    mora9_camp_dict = {}
    mora12_camp_dict = {}
    for i in meses_moras:
	for j in mora_camp:
	    if i['mes_form'] == j['mes_form']:
		mora6_camp_dict[i['mes_form']]=j['sum_mora6']*100/total_moraxcamp_dict[i['mes_form']]
		if i['mes_form'] <= before11:
		   mora9_camp_dict[i['mes_form']]=j['sum_mora9']*100/total_moraxcamp_dict[i['mes_form']]
		if i['mes_form'] <= before14:
		   mora12_camp_dict[i['mes_form']]=j['sum_mora12']*100/total_moraxcamp_dict[i['mes_form']]

    total_morasxseg = Moras.objects.values('mes_form','producto', 'segmento').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    totalxava_moras_dict = {}
    totalxms_moras_dict = {}
    totalxnoph_moras_dict = {}
    totalxnocli_moras_dict = {}
    for i in meses_moras:
	for j in total_morasxseg:
	    if i['mes_form'] == j['mes_form']:
		if j['segmento']=='1.AVA':
             	   totalxava_moras_dict[i['mes_form']]=j['sum_mora']
		elif j['segmento']=='2.MS':
             	   totalxms_moras_dict[i['mes_form']]=j['sum_mora']
		elif j['segmento']=='3.NoPH':
             	   totalxnoph_moras_dict[i['mes_form']]=j['sum_mora']
		elif j['segmento']=='4.NoCli':
         	   totalxnocli_moras_dict[i['mes_form']]=j['sum_mora']

    moras = Moras.objects.values('mes_form', 'segmento', 'producto').filter(producto='03 Tarjeta',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by('mes_form')
    ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    for i in meses_moras:
       for j in moras:
          if i['mes_form'] == j['mes_form']:
	     if  j['segmento']=='1.AVA':
             	ava_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxava_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   ava_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxava_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   ava_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxava_moras_dict[i['mes_form']]		
	     elif  j['segmento']=='2.MS':
             	ms_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxms_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   ms_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxms_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   ms_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxms_moras_dict[i['mes_form']]
	     elif  j['segmento']=='3.NoPH':
             	noph_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxnoph_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   noph_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxnoph_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   noph_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxnoph_moras_dict[i['mes_form']]
	     elif  j['segmento']=='4.NoCli':
             	nocli_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxnocli_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   nocli_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxnocli_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   nocli_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxnocli_moras_dict[i['mes_form']]

    total_forzaje = Forzaje.objects.values('mes_vigencia').filter(producto='03 Tarjeta',mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    forzaje_dict = {}
    for i in meses:
	for j in total_forzaje:
	    if i['mes_vigencia'] == j['mes_vigencia']:
		forzaje_dict[j['mes_vigencia']]=j['cantidad']

    forzaje2 = Forzaje.objects.values('mes_vigencia', 'dic_global').filter(producto = '03 Tarjeta',mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    duda_dict = {}
    rechazo_dict = {}
    for i in meses:
       for j in forzaje2:
          if i['mes_vigencia'] == j['mes_vigencia']:
	     if  j['dic_global']=='DU':
             	duda_dict[i['mes_vigencia']]=j['cantidad']*100/forzaje_dict[i['mes_vigencia']]
	     elif  j['dic_global']=='RE':
             	rechazo_dict[i['mes_vigencia']]=j['cantidad']*100/forzaje_dict[i['mes_vigencia']]
       	     else:
             	duda_dict[i['mes_vigencia']]= 0
             	rechazo_dict[i['mes_vigencia']]= 0

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_tarjeta.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_pld(request):
    meses = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).order_by('mes_vigencia').distinct('mes_vigencia')

    total_form = Seguimiento1.objects.values('mes_vigencia', 'producto').filter(producto='01 Consumo', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    total_form_dict = {}
    for j in total_form:
	total_form_dict[j['mes_vigencia']]=j['formalizado']
    uno_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='01 Consumo', riesgos='UNO A UNO', mes_vigencia__gte=before14, mes_vigencia__lte = fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_fast = Seguimiento1.objects.values('mes_vigencia','origen').filter(producto = '01 Consumo', origen = 'ORIGINACION FAST', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_uno = Seguimiento1.objects.values('mes_vigencia', 'origen').filter(producto ='01 Consumo', origen = 'ORIGINACION MS', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    formalizados = zip(total_form,uno_form,camp_fast,camp_uno)

    camp_form = Seguimiento1.objects.values('mes_vigencia', 'riesgos').filter(producto='01 Consumo', riesgos='CAMP', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    fact_uno = Seguimiento1.objects.values('mes_vigencia', 'producto').filter(producto='01 Consumo', riesgos='UNO A UNO', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    fact_camp = Seguimiento1.objects.values('mes_vigencia', 'producto').filter(producto='01 Consumo', riesgos='CAMP', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    ticket = zip(fact_uno, fact_camp, uno_form, camp_form)

    seg_ava = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='1.AVA', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_ms = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='2.MS', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_noph = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='3.NoPH', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_nocli = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='4.NoCli', mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(seg=Sum('form')).order_by('mes_vigencia')
    camp_seg = zip(seg_ava, seg_ms, seg_noph, seg_nocli, camp_form)

    rangos = Seguimiento1.objects.values('mes_vigencia','producto', 'rng_ing').filter(mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual,producto='01 Consumo').annotate(num_rango=Sum('form')).order_by('mes_vigencia')
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
	for j in rangos:
	   if i['mes_vigencia'] == j['mes_vigencia']:
		if j['rng_ing'] == '01 [3.5K - ...]':
		   rango1_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '02 [2.5K - 3.5K]':
		   rango2_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '03 [2K - 2.5K]':
		   rango3_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '04 [1.5K - 2K]':
		   rango4_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '05 [1K - 1.5K]':
		   rango5_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '06 [0 - 1K]':
		   rango6_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]

    meses_moras = Moras.objects.values('mes_form').filter(mes_form__gte=before18, mes_form__lte =before8).order_by('mes_form')

    mora6 = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('mora6')).order_by('mes_form')
    mora9 = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before11).annotate(sum_mora=Sum('mora9')).order_by('mes_form')
    mora12 = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before14).annotate(sum_mora=Sum('mora12')).order_by('mes_form')
    total_ctas = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    mora_6 = zip(mora6,total_ctas)
    mora_9 = zip(mora9,total_ctas)
    mora_12 = zip(mora12,total_ctas)

    total_moraxcamp = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before8,flg_camp='1. CAMPANA').annotate(sum_ctas=Sum('ctas')).order_by('mes_form')
    total_moraxcamp_dict = {}
    for i in meses_moras:
	for j in total_moraxcamp:
	    if i['mes_form'] == j['mes_form']:
               total_moraxcamp_dict[i['mes_form']]=j['sum_ctas']

    mora_camp = Moras.objects.values('mes_form','producto', 'flg_camp').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before8,flg_camp='1. CAMPANA').annotate(sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by('mes_form')
    mora6_camp_dict = {}
    mora9_camp_dict = {}
    mora12_camp_dict = {}
    for i in meses_moras:
	for j in mora_camp:
	    if i['mes_form'] == j['mes_form']:
		mora6_camp_dict[i['mes_form']]=j['sum_mora6']*100/total_moraxcamp_dict[i['mes_form']]
		if i['mes_form'] <= before11:
		   mora9_camp_dict[i['mes_form']]=j['sum_mora9']*100/total_moraxcamp_dict[i['mes_form']]
		if i['mes_form'] <= before14:
		   mora12_camp_dict[i['mes_form']]=j['sum_mora12']*100/total_moraxcamp_dict[i['mes_form']]

    total_morasxseg = Moras.objects.values('mes_form','producto', 'segmento').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    totalxava_moras_dict = {}
    totalxms_moras_dict = {}
    totalxnoph_moras_dict = {}
    totalxnocli_moras_dict = {}
    for i in meses_moras:
	for j in total_morasxseg:
	    if i['mes_form'] == j['mes_form']:
		if j['segmento']=='1.AVA':
             	   totalxava_moras_dict[i['mes_form']]=j['sum_mora']
		elif j['segmento']=='2.MS':
             	   totalxms_moras_dict[i['mes_form']]=j['sum_mora']
		elif j['segmento']=='3.NoPH':
             	   totalxnoph_moras_dict[i['mes_form']]=j['sum_mora']
		elif j['segmento']=='4.NoCli':
         	   totalxnocli_moras_dict[i['mes_form']]=j['sum_mora']

    moras = Moras.objects.values('mes_form', 'segmento', 'producto').filter(producto='01 Consumo',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by('mes_form')
    ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    for i in meses_moras:
       for j in moras:
          if i['mes_form'] == j['mes_form']:
	     if  j['segmento']=='1.AVA':
             	ava_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxava_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   ava_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxava_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   ava_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxava_moras_dict[i['mes_form']]		
	     elif  j['segmento']=='2.MS':
             	ms_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxms_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   ms_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxms_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   ms_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxms_moras_dict[i['mes_form']]
	     elif  j['segmento']=='3.NoPH':
             	noph_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxnoph_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   noph_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxnoph_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   noph_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxnoph_moras_dict[i['mes_form']]
	     elif  j['segmento']=='4.NoCli':
             	nocli_mora6_dict[i['mes_form']]=j['sum_mora6']*100/totalxnocli_moras_dict[i['mes_form']]
		if i['mes_form'] <= before11:
             	   nocli_mora9_dict[i['mes_form']]=j['sum_mora9']*100/totalxnocli_moras_dict[i['mes_form']]
		if i['mes_form'] <= before14:
             	   nocli_mora12_dict[i['mes_form']]=j['sum_mora12']*100/totalxnocli_moras_dict[i['mes_form']]


    duda = Forzaje.objects.values('mes_vigencia').filter(producto='01 Consumo',mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual, dic_global='DU').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rechazo = Forzaje.objects.values('mes_vigencia').filter(producto='01 Consumo',mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual, dic_global='RE').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    total_forzaje = Forzaje.objects.values('mes_vigencia').filter(producto='01 Consumo',mes_vigencia__gte=before14, mes_vigencia__lte =fecha_actual).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    forzaje = zip(duda,rechazo,total_forzaje)

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_pld.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_auto(request):
    meses_total = Seguimiento1.objects.values('mes_vigencia').distinct('mes_vigencia').order_by('-mes_vigencia')
    time = []
    for i in meses_total:
        time.append(i['mes_vigencia'])
    meses = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).distinct('mes_vigencia').order_by('mes_vigencia')
    total_form = Seguimiento1.objects.values('mes_vigencia', 'producto').filter(producto='02 Auto',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    total_form_dict = {}
    for j in total_form:
	total_form_dict[j['mes_vigencia']]=j['formalizado']
    uno_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='02 Auto', riesgos='UNO A UNO',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='02 Auto', riesgos='CAMP',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_reg = Seguimiento1.objects.values('mes_vigencia','origen').filter(producto='02 Auto', origen__in=['ORIGINACION FAST','ORIGINACION MS'],mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    formalizados = zip(total_form,uno_form,camp_form)

    fact_uno = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='02 Auto', riesgos='UNO A UNO',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    fact_camp = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='02 Auto', riesgos='CAMP',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    ticket = zip(fact_uno, fact_camp, uno_form, camp_form)

    rangos = Seguimiento1.objects.values('mes_vigencia','producto', 'rng_ing').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],producto='02 Auto').annotate(num_rango=Sum('form')).order_by('mes_vigencia')
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
	for j in rangos:
	   if i['mes_vigencia'] == j['mes_vigencia']:
		if j['rng_ing'] == '01 [3.5K - ...]':
		   rango1_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '02 [2.5K - 3.5K]':
		   rango2_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '03 [2K - 2.5K]':
		   rango3_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '04 [1.5K - 2K]':
		   rango4_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		elif j['rng_ing'] == '05 [1K - 1.5K]':
		   rango5_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		if j['rng_ing'] == '06 [0 - 1K]':
		   rango6_dict[i['mes_vigencia']]=j['num_rango']*100/total_form_dict[i['mes_vigencia']]
		else:
		   rango6_dict[i['mes_vigencia']]=0

    meses_moras = Moras.objects.values('mes_form').order_by('-mes_form').distinct()
    moratime = []
    for i in meses_moras:
	moratime.append(i['mes_form'])
    mora6 = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte=moratime[16], mes_form__lte =moratime[6]).annotate(sum_mora=Sum('mora6')).order_by('mes_form')
    mora9 = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte=moratime[16], mes_form__lte =moratime[9]).annotate(sum_mora=Sum('mora9')).order_by('mes_form')
    mora12 = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte=moratime[16], mes_form__lte =moratime[12]).annotate(sum_mora=Sum('mora12')).order_by('mes_form')
    total_ctas = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte=moratime[16], mes_form__lte =moratime[6]).annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    moras6 = zip(mora6,total_ctas)
    moras9 = zip(mora9,total_ctas)
    moras12 = zip(mora12,total_ctas)

    duda = Forzaje.objects.values('mes_vigencia').filter(producto='02 Auto',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0], dic_global='DU').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rechazo = Forzaje.objects.values('mes_vigencia').filter(producto='02 Auto',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0], dic_global='RE').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    total_forzaje = Forzaje.objects.values('mes_vigencia').filter(producto='02 Auto',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    forzaje = zip(duda,rechazo,total_forzaje)

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_auto.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_adelanto(request):
    control_fecha = AdelantoSueldo.objects.values('mes_vigencia' ).distinct('mes_vigencia').order_by('-mes_vigencia')
    time = []
    for i in control_fecha:
        time.append(i['mes_vigencia'])
    fecha1= time[0]
    total_form = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    ticket = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('fact')).order_by('mes_vigencia')
    formalizados = zip(total_form,ticket)
    
    meses = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).distinct('mes_vigencia').order_by('mes_vigencia')
    total_rango = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).exclude(rng_suelgo='00 Sin Inf').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango_tot = {}
    for i in total_rango:
	rango_tot[i['mes_vigencia']]=i['formalizado']
    rango1 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo__in=['01 [0 - 700>','02 [700 - 1000]'], mes_vigencia__gte=time[13], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='03 [1001 - 1500]',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='04 [1501 - 2000]',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='05 [2001 - 2500]',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='06 [2501 - 3500]',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    rango6 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo__in=['07 [3501 - Mas>','07 [3501 - 5000]','08 [5001 - Mas>'],mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= 0

    buro1 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='[G1-G4]',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='G5',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='[G6-G8]',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='NB',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0

    mora30 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(formalizado=Sum('mora')).order_by('mes_vigencia')
    mora = itertools.izip_longest(mora30,total_rango,fillvalue='0')
    mora30_dict1 = {}
    mora30_dict2 = {}
    for i in meses:
       for j in mora30:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora30_dict1[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             mora30_dict2[i['mes_vigencia']]=j['formalizado']
             break
       	  else:
             mora30_dict1[i['mes_vigencia']]= 0
             mora30_dict2[i['mes_vigencia']]= 0

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_adelanto.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_prestinmediato(request):
    meses_tot = PrestInmediato.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    time = []
    for i in meses_tot:
        time.append(i['mes_vigencia'])
    fecha1= time[0]
    meses = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).order_by('-mes_vigencia').distinct()
    form = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    fact = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('fact')).order_by('mes_vigencia')
    ticket_ava = PrestInmediato.objects.values('mes_vigencia').filter(segmento='1.AVA',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas'), cantidad2=Sum('fact')).order_by('mes_vigencia')
    ticket_ms = PrestInmediato.objects.values('mes_vigencia').filter(segmento='2.MS',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas'), cantidad2=Sum('fact')).order_by('mes_vigencia')

    total_rango = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).exclude(rng_ingreso='').order_by('mes_vigencia')
    rango_tot = {}
    for i in total_rango:
	rango_tot[i['mes_vigencia']]=i['cantidad']
    rango1 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ingreso='05 [1K - 1.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ingreso='04 [1.5K - 2K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ingreso='03 [2K - 2.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ingreso='02 [2.5K - 3.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ingreso='01 [3.5K - ...]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    total_rango2 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango_tot2 = {}
    for i in total_rango2:
	rango_tot2[i['mes_vigencia']]=i['cantidad']
    buro1 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='[G1-G4]',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='G5',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='[G6-G8]',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='NB',mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0
    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_prestinmediato.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_increlinea(request):
    meses_total = IncreLinea.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    time = []
    for i in meses_total:
	time.append(i['mes_vigencia'])
    meses = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).order_by('-mes_vigencia').distinct()
    form = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form_dict = {}
    for i in form:
	form_dict[i['mes_vigencia']]=i['cantidad']
    ticket = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('cantidad')).order_by('mes_vigencia')
    ticket_dict = {}
    for i in meses:
       for j in ticket:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ticket_dict[i['mes_vigencia']]=j['cantidad']*1000000/form_dict[i['mes_vigencia']]
             break
       	  else:
             ticket_dict[i['mes_vigencia']]= 0
    form2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).exclude(segmento='').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form2_dict = {}
    for i in form2:
	form2_dict[i['mes_vigencia']]=i['cantidad']
    ava = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento__in=['Vip','Premium']).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ava_dict = {}
    for i in meses:
       for j in ava:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ava_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ava_dict[i['mes_vigencia']]= 0
    ms = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='MS').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ms_dict = {}
    for i in meses:
       for j in ms:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ms_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ms_dict[i['mes_vigencia']]= 0
    pasivo = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='Pasivo').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    pasivo_dict = {}
    for i in meses:
       for j in pasivo:
          if i['mes_vigencia'] == j['mes_vigencia']:
             pasivo_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             pasivo_dict[i['mes_vigencia']]= 0
    noph = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='No PH').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noph_dict = {}
    for i in meses:
       for j in noph:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noph_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noph_dict[i['mes_vigencia']]= 0
    noclie = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='NoCli').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noclie_dict = {}
    for i in meses:
       for j in noclie:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noclie_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noclie_dict[i['mes_vigencia']]= 0
    rango1 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='01 [-1000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='02 [1000-1500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='03 [1500-2000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='04 [2000-2500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='05 [2500-3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    rango6 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='06 [+3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= 0
    buro1 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='01 G1-G4').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='02 G5').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='03 G6-G8').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='NB').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0
    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_increlinea.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_lifemiles(request):
    meses_total = IncreLinea.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    time = []
    for i in meses_total:
	time.append(i['mes_vigencia'])
    meses = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).order_by('-mes_vigencia').distinct()
    form = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form_dict = {}
    for i in form:
	form_dict[i['mes_vigencia']]=i['cantidad']
    ticket = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).annotate(cantidad=Sum('imp_sol')).order_by('mes_vigencia')
    ticket_dict = {}
    for i in meses:
       for j in ticket:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ticket_dict[i['mes_vigencia']]=j['cantidad']*1000000/form_dict[i['mes_vigencia']]
             break
       	  else:
             ticket_dict[i['mes_vigencia']]= 0
    form2 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).exclude(segmento__in=['','PLAN CLIENTE']).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form2_dict = {}
    for i in form2:
	form2_dict[i['mes_vigencia']]=i['cantidad']
    ava = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento__in=['Vip','Premium']).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ava_dict = {}
    for i in meses:
       for j in ava:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ava_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ava_dict[i['mes_vigencia']]= 0
    ms = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='MS').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ms_dict = {}
    for i in meses:
       for j in ms:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ms_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ms_dict[i['mes_vigencia']]= 0
    pasivo = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='Pasivo').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    pasivo_dict = {}
    for i in meses:
       for j in pasivo:
          if i['mes_vigencia'] == j['mes_vigencia']:
             pasivo_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             pasivo_dict[i['mes_vigencia']]= 0
    noph = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='No PH').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noph_dict = {}
    for i in meses:
       for j in noph:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noph_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noph_dict[i['mes_vigencia']]= 0
    noclie = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='NoCli').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noclie_dict = {}
    for i in meses:
       for j in noclie:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noclie_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noclie_dict[i['mes_vigencia']]= 0
    rango1 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ing='01 [-1000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ing='02 [1000-1500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ing='03 [1500-2000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ing='04 [2000-2500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ing='05 [2500-3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    rango6 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_ing='06 [+3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= 0
    buro1 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='01 G1-G4').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='02 G5').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='03 G6-G8').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = Lifemiles.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='04 NB').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0
    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_lifemiles.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_increlifemiles(request):
    meses_total = IncreLinea.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    time = []
    for i in meses_total:
	time.append(i['mes_vigencia'])
    meses = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0]).order_by('-mes_vigencia').distinct()
    form = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form_dict={}
    for i in form:
	form_dict[i['mes_vigencia']]=i['cantidad']
    form2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], lifemiles='1').exclude(segmento='').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form2_dict={}
    for i in form2:
	form2_dict[i['mes_vigencia']]=i['cantidad']
    ticket = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],lifemiles='1').annotate(cantidad=Sum('cantidad')).order_by('mes_vigencia')
    ticket_dict={}
    for i in meses:
       for j in ticket:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ticket_dict[i['mes_vigencia']]=j['cantidad']*1000000/form_dict[i['mes_vigencia']]
             break
       	  else:
             ticket_dict[i['mes_vigencia']]= 0
    ava = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],segmento__in=['Vip','Premium'],lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ava_dict = {}
    for i in meses:
       for j in ava:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ava_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ava_dict[i['mes_vigencia']]= 0
    ms = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0], segmento='MS', lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ms_dict = {}
    for i in meses:
       for j in ms:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ms_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ms_dict[i['mes_vigencia']]= 0
    pasivo = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0], segmento='Pasivo',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    pasivo_dict = {}
    for i in meses:
       for j in pasivo:
          if i['mes_vigencia'] == j['mes_vigencia']:
             pasivo_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             pasivo_dict[i['mes_vigencia']]= 0
    noph = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0],segmento='No PH',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noph_dict = {}
    for i in meses:
       for j in noph:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noph_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noph_dict[i['mes_vigencia']]= 0
    noclie = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= time[12], mes_vigencia__lte =time[0], segmento='NoCli',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noclie_dict = {}
    for i in meses:
       for j in noclie:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noclie_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noclie_dict[i['mes_vigencia']]= 0
    rango1 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='01 [-1000>',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='02 [1000-1500>',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='03 [1500-2000>',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='04 [2000-2500>',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='05 [2500-3500>',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    rango6 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],rng_sueldo='06 [+3500>',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= 0
    buro1 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='01 G1-G4',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='02 G5',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='03 G6-G8',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0], buro='NB',lifemiles='1').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0

    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_increlifemiles.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_hipoteca(request):
    form = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual, producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    form_dict= {}
    for i in form:
       form_dict[i['mes_vigencia']]=i['cantidad']
    fact = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual, producto="04 Hipotecario").annotate(cantidad=Sum('facturacion')).order_by('mes_vigencia')
    meses = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual).order_by('mes_vigencia').distinct('mes_vigencia')
    rango1 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual,rng_ing='06 [0 - 1K]', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual,rng_ing='05 [1K - 1.5K]', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual,rng_ing='04 [1.5K - 2K]', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual,rng_ing='03 [2K - 2.5K]', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual,rng_ing='02 [2.5K - 3.5K]', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    rango6 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual,rng_ing='01 [3.5K - ...]', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= 0
    buro1 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual, dic_buro__in=['G1','G2'], producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual, dic_buro__in=['G3','G4'], producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual, dic_buro__in=['G5','G6'], producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual, dic_buro__in=['G7','G8'], producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0
    buro5 = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual, dic_buro='NB', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    buro5_dict = {}
    for i in meses:
       for j in buro5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro5_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro5_dict[i['mes_vigencia']]= 0

    meses_moras = Moras.objects.values('mes_form').filter(mes_form__gte=before18, mes_form__lte =before8).order_by('mes_form')

    mora6 = Moras.objects.values('mes_form','producto').filter(producto='04 Hipotecario',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('mora6')).order_by('mes_form')
    mora9 = Moras.objects.values('mes_form','producto').filter(producto='04 Hipotecario',mes_form__gte=before18, mes_form__lte =before11).annotate(sum_mora=Sum('mora9')).order_by('mes_form')
    mora12 = Moras.objects.values('mes_form','producto').filter(producto='04 Hipotecario',mes_form__gte=before18, mes_form__lte =before14).annotate(sum_mora=Sum('mora12')).order_by('mes_form')
    total_ctas = Moras.objects.values('mes_form','producto').filter(producto='04 Hipotecario',mes_form__gte=before18, mes_form__lte =before8).annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    mora_6 = zip(mora6,total_ctas)
    mora_9 = zip(mora9,total_ctas)
    mora_12 = zip(mora12,total_ctas)

    total_forzaje = Forzaje.objects.values('mes_vigencia').filter(producto='04 Hipotecario',mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    forzaje_dict = {}
    for i in meses:
	for j in total_forzaje:
	    if i['mes_vigencia'] == j['mes_vigencia']:
		forzaje_dict[j['mes_vigencia']]=j['cantidad']

    forzaje2 = Forzaje.objects.values('mes_vigencia', 'dic_global').filter(producto = '04 Hipotecario', mes_vigencia__gte=before12, mes_vigencia__lte =fecha_actual).exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    duda_dict = {}
    rechazo_dict = {}
    for i in meses:
       for j in forzaje2:
          if i['mes_vigencia'] == j['mes_vigencia']:
	     if  j['dic_global']=='DU':
             	duda_dict[i['mes_vigencia']]=j['cantidad']*100/forzaje_dict[i['mes_vigencia']]
	     elif  j['dic_global']=='RE':
             	rechazo_dict[i['mes_vigencia']]=j['cantidad']*100/forzaje_dict[i['mes_vigencia']]
       	     else:
             	duda_dict[i['mes_vigencia']]= 0
             	rechazo_dict[i['mes_vigencia']]= 0

    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_hipoteca.html', locals(),
                  context_instance=RequestContext(request))



# 6.- Vistas para reportes de HIPOTECARIO
@login_required
def hipoteca_ssff(request):
    control_fecha = HipotecaSSFF.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    time = []; timex = []; timez = []; timeu = []
    anual = []
    for i in control_fecha:
	time.append(i['mes_vigencia'])

    for i in control_fecha:
    	if '12' in i['mes_vigencia']:
	    anual.append(i['mes_vigencia'])
	else:
	    timex.append(i['mes_vigencia'])
    for i in control_fecha:
	if i['mes_vigencia'] > anual[0]:
	    timeu.append(i['mes_vigencia'])

    if time[0] == anual[0]:
		timez.append(anual[0])
	 	timez.append(timex[0])
		timez.append(timex[1])
		timez.append(timex[2])
		timez.append(anual[1])
		timez.append(anual[2])
		timez.append(anual[3])
    else:
	    if len(timeu) == 1:
		timez.append(timeu[0])
	 	timez.append(anual[0])
		timez.append(timex[0])
		timez.append(timex[1])
		timez.append(anual[1])
		timez.append(anual[2])
		timez.append(anual[3])
	    elif len(timeu) == 2:
		timez.append(timeu[0])
		timez.append(timeu[1])
	 	timez.append(anual[0])
		timez.append(timex[0])
		timez.append(anual[1])
		timez.append(anual[2])
		timez.append(anual[3])
	    else:
		timez.append(timeu[0])
		timez.append(timeu[1])
		timez.append(timeu[2])
	 	timez.append(anual[0])
		timez.append(anual[1])
		timez.append(anual[2])
		timez.append(anual[3])
  
    saldo_bcp = HipotecaSSFF.objects.values('mes_vigencia', 'banco').filter(banco='BCP',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo') ).order_by('mes_vigencia')
    saldo_bbva = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco='BBVA',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo') ).order_by('mes_vigencia')
    saldo_sco = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco='SCO',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo') ).order_by('mes_vigencia')
    saldo_ibk = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco='IBK',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo') ).order_by('mes_vigencia')
    saldo2_bcp = HipotecaSSFF.objects.values('mes_vigencia', 'banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='BCP',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo2_bbva = HipotecaSSFF.objects.values('mes_vigencia', 'banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='BBVA',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo2_sco = HipotecaSSFF.objects.values('mes_vigencia', 'banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='SCO',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo2_ibk = HipotecaSSFF.objects.values('mes_vigencia', 'banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='IBK',mes_vigencia__in=[timez[6],timez[5],timez[4],timez[3],timez[2],timez[1],timez[0]]).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    bcp = zip(saldo_bcp, saldo2_bcp)
    bbva = zip(saldo_bbva, saldo2_bbva)
    sco = zip(saldo_sco, saldo2_sco)
    ibk = zip(saldo_ibk, saldo2_ibk)
    saldo_jud = HipotecaSSFF.objects.values('mes_vigencia', 'banco', 'tipo_cuenta' ).filter(tipo_cuenta='JUD_HIPO', banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia=time[0] ).annotate(sum_jud=Sum('mto_saldo')).order_by('banco')
    saldo_ven = HipotecaSSFF.objects.values('mes_vigencia', 'banco', 'tipo_cuenta' ).filter(tipo_cuenta='VEN_HIPO', banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia=time[0] ).annotate(sum_ven=Sum('mto_saldo')).order_by('banco')
    saldo_ref = HipotecaSSFF.objects.values('mes_vigencia', 'banco', 'tipo_cuenta' ).filter(tipo_cuenta='REF_HIPO', banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia=time[0] ).annotate(sum_ref=Sum('mto_saldo')).order_by('banco')
    totales = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia=time[0]).annotate(total=Sum('mto_saldo')).order_by('banco')
    grafica2 = zip(saldo_jud,saldo_ven,saldo_ref,totales)

    static_url=settings.STATIC_URL
    tipo_side = 5
    return render('reports/hipoteca_ssff.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def hipoteca_conce(request):
    conce = HipotecaConce.objects.values('mes','territorio').filter(mes='201512').annotate(sum_inv=Sum('inversion')).order_by('territorio')

    static_url=settings.STATIC_URL
    tipo_side = 5
    return render('reports/hipoteca_conce.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def hipoteca_segui(request):
    evo_mora12 = Moras.objects.values('trimestre_form','producto').filter(producto='04 Hipotecario', trimestre_form__in=['2013-1','2013-2','2013-3', '2013-4','2014-1','2014-2','2014-3','2014-4']).annotate(sum_inv=Sum('mora12')).order_by('trimestre_form')
    evo_mora18 = Moras.objects.values('trimestre_form','producto').filter(producto='04 Hipotecario', trimestre_form__in=['2013-1','2013-2','2013-3', '2013-4','2014-1','2014-2','2014-3','2014-4']).annotate(sum_inv=Sum('mora18')).order_by('trimestre_form')
    evo_mora24 = Moras.objects.values('trimestre_form','producto').filter(producto='04 Hipotecario', trimestre_form__in=['2013-1','2013-2','2013-3', '2013-4','2014-1','2014-2','2014-3','2014-4']).annotate(sum_inv=Sum('mora24')).order_by('trimestre_form')
    evo_mora36 = Moras.objects.values('trimestre_form','producto').filter(producto='04 Hipotecario', trimestre_form__in=['2013-1','2013-2','2013-3', '2013-4','2014-1','2014-2','2014-3','2014-4']).annotate(sum_inv=Sum('mora36')).order_by('trimestre_form')
    total = Moras.objects.values('trimestre_form').filter(producto='04 Hipotecario').annotate(sum_ctas=Sum('ctas')).order_by('trimestre_form')
    mora12 = zip(evo_mora12, total)
    mora18 = zip(evo_mora18, total)
    mora24 = zip(evo_mora24, total)
    mora36 = zip(evo_mora36, total)

    static_url=settings.STATIC_URL
    tipo_side = 5
    return render('reports/hipoteca_seguimiento.html', locals(),
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

def json_mapa(request):
    periodo = request.POST['periodo']
    if periodo == '1':
	fecha='201312'
    elif periodo == '2':
	fecha='201412'
    elif periodo == '3':
	fecha='201512'
    elif periodo == '4':
	fecha='201604'
    meses = Mapa.objects.values('codmes').order_by('codmes').distinct()
    list_meses=[]; d=0
    for i in meses:
	list_meses.append(i['codmes'])
    d = len(list_meses)
    ubigeo = Mapa.objects.values('ubigeo').order_by('ubigeo').distinct()
    distrito = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA').annotate(mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    distrito1 = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA', codmes=fecha).annotate(mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    dict_moras = {}; dict_moras1 = {}; 
    dict_moras2 = {}; dict_moras3 = {};
    for i in distrito:
	if i['codmes']=='201312':
	   if i['mora']>3:
	      dict_moras[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras[i['ubigeo']]='#66BD63'
	if i['codmes']=='201412':
	   if i['mora']>3:
	      dict_moras1[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras1[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras1[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras1[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras1[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras1[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras1[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras1[i['ubigeo']]='#66BD63'
	if i['codmes']=='201512':
	   if i['mora']>3:
	      dict_moras2[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras2[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras2[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras2[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras2[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras2[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras2[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras2[i['ubigeo']]='#66BD63'
	if i['codmes']=='201604':
	   if i['mora']>3:
	      dict_moras3[i['ubigeo']]='#E31A1C'
	   if i['mora']>2 and i['mora']<=3:
	      dict_moras3[i['ubigeo']]='#FC4E2A'
	   if i['mora']>1.5 and i['mora']<=2:
	      dict_moras3[i['ubigeo']]='#FB8D29'
	   if i['mora']>1.2 and i['mora']<=1.5:
	      dict_moras3[i['ubigeo']]='#FEB228'
	   if i['mora']>0.9 and i['mora']<=1.2:
	      dict_moras3[i['ubigeo']]='#FED976'
	   if i['mora']>0.6 and i['mora']<=0.9:
	      dict_moras3[i['ubigeo']]='#FBE975'
	   if i['mora']>0.3 and i['mora']<=0.6:
	      dict_moras3[i['ubigeo']]='#A6D974'
	   if i['mora']<=0.3:
	      dict_moras3[i['ubigeo']]='#66BD63'

    return HttpResponse(distrito1)



# Vistas para carga de csv
def load(request):
    static_url=settings.STATIC_URL
    #Campana2.objects.all().delete()
    #RVGL.objects.all().delete()
    #Evaluaciontc.objects.all().delete()
    #Evaluacionpld.objects.all().delete()
    #Seguimiento1.objects.all().delete()
    #HipotecaConce.objects.all().delete()
    #Moras.objects.all().delete()
    #IncreLinea.objects.all().delete()
    #PrestInmediato.objects.all().delete()
    #Lifemiles.objects.all().delete()
    #Mapa.objects.all().delete()
    DepartamentosWeb.objects.all().delete()
    if request.user.is_authenticated():
        return render('reports/load.html', locals(),
                  context_instance=RequestContext(request))
    else:
        return campana_resumen(request)



# Vistas para manipular archivos
def carga_rvgl(request):
    if request.method == 'POST':
        form = UploadRVGL(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['rvgl']
            RVGLCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            print "no es valido"
            return load(campana_resumen)
    else:
        return load(campana_resumen)


#def carga_campana(request):
    #if request.method == 'POST':
        #form = UploadCampana(request.POST, request.FILES)
        #if form.is_valid():
            #csv_file = request.FILES['campana']
            #CampanaCsv.import_data(data = csv_file)
            #return campana_resumen(request)
        #else:
            #print "no es valido"
            #return load(campana_resumen)
    #else:
        #return load(campana_resumen)

def carga_campana2(request):
    if request.method == 'POST':
        form = UploadCampana2(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['campana2']
            Campana2Csv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            print "no es valido"
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_campanaweb(request):
    if request.method == 'POST':
        form = UploadCampanaWeb(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['campanaweb']
            CampanaWebCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            print "no es valido"
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_caidas(request):
    if request.method == 'POST':
        form = UploadCaida(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['caidas']
            CaidaCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_verificaciones(request):
    if request.method == 'POST':
        form = UploadVerificaciones(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['verificaciones']
            VerificacionesCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_evaluaciontc(request):
    if request.method == 'POST':
        form = UploadEvaluaciontc(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['evaluaciontc']
            EvaluaciontcCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_evaluacionpld(request):
    if request.method == 'POST':
        form = UploadEvaluacionpld(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['evaluacionpld']
            EvaluacionpldCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)


def carga_seguimiento1(request):
    Seguimiento1.objects.filter(mes_vigencia__gte=before3, mes_vigencia__lte =before1).delete()
    if request.method == 'POST':
        form = UploadSeguimiento1(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['seguimiento1']
            Seguimiento1Csv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_flujoperativo(request):
    if request.method == 'POST':
        form = UploadFlujOperativo(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['flujoperativo']
            FlujOperativoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_hipotecassff(request):
    if request.method == 'POST':
        form = UploadHipotecaSSFF(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['hipotecassff']
            HipotecaSSFFCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_hipotecaconce(request):
    if request.method == 'POST':
        form = UploadHipotecaConce(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['hipotecaconce']
            HipotecaConceCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_moras(request):
    Moras.objects.filter(mes_form__gte=before9, mes_form__lte =fecha_actual).delete()
    if request.method == 'POST':
        form = UploadMoras(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['moras']
            MorasCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_adelantosueldo(request):
    if request.method == 'POST':
        form = UploadAdelantoSueldo(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['adelantosueldo']
            AdelantoSueldoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_prestinmediato(request):
    if request.method == 'POST':
        form = UploadPrestInmediato(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['prestinmediato']
            PrestInmediatoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_altasempresa(request):
    if request.method == 'POST':
        form = UploadAltasEmpresa(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['altasempresa']
            AltasEmpresaCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_altassegmento(request):
    if request.method == 'POST':
        form = UploadAltasSegmento(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['altassegmento']
            AltasSegmentoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_increlinea(request):
    if request.method == 'POST':
        form = UploadIncreLinea(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['increlinea']
            IncreLineaCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_lifemiles(request):
    if request.method == 'POST':
        form = UploadLifemiles(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['lifemiles']
            LifemilesCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_exoneracion(request):
    if request.method == 'POST':
        form = UploadExoneracion(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['exoneracion']
            ExoneracionCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_forzaje(request):
    if request.method == 'POST':
        form = UploadForzaje(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['forzaje']
            ForzajeCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_mapa(request):
    if request.method == 'POST':
        form = UploadMapa(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['mapa']
            MapaCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_departamentosweb(request):
    if request.method == 'POST':
        form = UploadDepartamentosWeb(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['departamentosweb']
            DepartamentosWebCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

