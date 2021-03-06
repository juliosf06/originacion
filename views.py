# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Max, Case, When, IntegerField, F, Q, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response as render
from .forms import UploadFileForm
from decimal import *

from django.template import RequestContext

from datetime import datetime, timedelta
from models import *
from forms import *
from django.contrib.auth import authenticate, login, logout

import csv, itertools
import sys

from .models import Comentario

hoy = datetime.now().strftime("%d/%m/%Y")
hora = datetime.now().strftime("%H:%M")
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
next1 = datetime.now()+timedelta(days=1*30)
after1 = next1.strftime("%Y%m")

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
                   return HttpResponseRedirect('/reports/seguimiento')
           else:
               # Return a 'disabled account' error message
	       print("The password is valid, but the account has been disabled!")
       else:
           mensaje="Usurio o password incorrectos"  
    return render('reports/login.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def home(request):

    static_url=settings.STATIC_URL
    return render('reports/home.html', locals(),
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

    total_ofertas_meses=AltasTarjetas.objects.values('mes').annotate(Ofertas=Sum('ofertas'), Altas=Sum('altas'))
    print total_ofertas_meses
    
    static_url=settings.STATIC_URL
    tipo_side = 6
    return render('reports/prueba.html', locals(),
                  context_instance=RequestContext(request))

def prueba2(request):

    static_url=settings.STATIC_URL

    return render('reports/prueba2.html', locals(),
                  context_instance=RequestContext(request))

# 2.- Vistas para reportes de Campaña
def campana_resumen(request,fecha=''):

    control_fecha = Campana2.objects.values('mes_vigencia').distinct().order_by('-mes_vigencia')
    if fecha == '':
      fecha = control_fecha[0]['mes_vigencia']
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
def campana_detalles(request, segmento='TOTAL', fecha=''):
    texto = str(segmento)
    lista = texto.split(",")
    control_fecha = Campana2.objects.values('mes_vigencia').distinct().order_by('-mes_vigencia')
    if fecha == '':
      fecha = control_fecha[0]['mes_vigencia']
    control_segmentos = Campana2.objects.all().values_list('segmento', flat=True).distinct()
    if segmento == 'TOTAL':
       detalles = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea')).annotate(monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000),monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000),monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000),monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))
    else:
       detalles = Campana2.objects.filter(segmento=segmento).filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea')).annotate(monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000),monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000),monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000),monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))

    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_detalles.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def modelo_relacional(request):
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_modelo.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def campana_caidas(request, fecha=''):
    combo_fechas = Caida.objects.values_list('mes_vigencia', flat=True).distinct().order_by('-mes_vigencia')
    if fecha == '':
      fecha = combo_fechas[0]
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
    meses_dict = []
    for i in meses:
        meses_dict.append(i['mes_vigencia'])
    num_meses = len(meses_dict)
    print num_meses
    lista_meses = range(1,num_meses)
    if segmento == 'TOTAL':
        exo_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_ambas_dict = {}; exo_vl_dict = {}; exo_vd_dict = {}; req_ambas_dict = {};
        exo_ambas_list = []; exo_vl_list = []; exo_vd_list = []; req_ambas_list = [];
        for i in meses:
            for j in exo_ambas:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    exo_ambas_dict[i['mes_vigencia']]=j['cantidad']
                    exo_ambas_list.append(j['cantidad'])
                    break
                else:
                    exo_ambas_dict[i['mes_vigencia']]=0
                    exo_ambas_list.append(j['cantidad'])
            for j in exo_vl:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    exo_vl_dict[i['mes_vigencia']]=j['cantidad']
                    exo_vl_list.append(j['cantidad'])
                    break
                else:
                    exo_vl_dict[i['mes_vigencia']]=0
                    exo_vl_list.append(j['cantidad'])
            for j in exo_vd:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    exo_vd_dict[i['mes_vigencia']]=j['cantidad']
                    exo_vd_list.append(j['cantidad'])
                    break
                else:
                    exo_vd_dict[i['mes_vigencia']]=0
                    exo_vd_list.append(j['cantidad'])
            for j in req_ambas:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    req_ambas_dict[i['mes_vigencia']]=j['cantidad']
                    req_ambas_list.append(j['cantidad'])
                    break
                else:
                    req_ambas_dict[i['mes_vigencia']]=0
                    req_ambas_list.append(j['cantidad'])


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
        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL', segmento__in=lista).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD', segmento__in=lista).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS', segmento__in=lista).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_ambas_dict = {}; exo_vl_dict = {}; exo_vd_dict = {}; req_ambas_dict = {};
        exo_ambas_list = []; exo_vl_list = []; exo_vd_list = []; req_ambas_list = [];
        for i in meses:
            for j in exo_ambas:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    exo_ambas_dict[i['mes_vigencia']]=j['cantidad']
                    exo_ambas_list.append(j['cantidad'])
                    break
                else:
                    exo_ambas_dict[i['mes_vigencia']]=0
                    exo_ambas_list.append(j['cantidad'])
            for j in exo_vl:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    exo_vl_dict[i['mes_vigencia']]=j['cantidad']
                    exo_vl_list.append(j['cantidad'])
                    break
                else:
                    exo_vl_dict[i['mes_vigencia']]=0
                    exo_vl_list.append(j['cantidad'])
            for j in exo_vd:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    exo_vd_dict[i['mes_vigencia']]=j['cantidad']
                    exo_vd_list.append(j['cantidad'])
                    break
                else:
                    exo_vd_dict[i['mes_vigencia']]=0
                    exo_vd_list.append(j['cantidad'])
            for j in req_ambas:
                if i['mes_vigencia'] == j['mes_vigencia']:
                    req_ambas_dict[i['mes_vigencia']]=j['cantidad']
                    req_ambas_list.append(j['cantidad'])
                    break
                else:
                    req_ambas_dict[i['mes_vigencia']]=0
                    req_ambas_list.append(j['cantidad'])

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

    control_segmentos = Campana2.objects.all().values_list('segmento', flat=True).distinct()
    total_vl = itertools.izip_longest(tl1,tl2,tl3,tl4,tl5,tl6,tl7, tl8,tl9)
    total_vd = itertools.izip_longest(tv1,tv2,tv3,tv4,tv5,tv6,tv7, tv8,tv9)
    motivos = itertools.izip_longest(esph,VLvalida,pasiveros,vip,noph, cts, tendencia, dependiente,total1)
    motivos2 = itertools.izip_longest(vip2,pasivero2,esph2,hipo2,veri2, equi2,ubi2,fast2,total2)
    exoneraciones = itertools.izip_longest(exo_ambas,exo_vl,exo_vd,req_ambas)
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_exoneraciones.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def campana_flujo(request, fecha=''):
    control_fecha = Campana2.objects.values('mes_vigencia').distinct().order_by('-mes_vigencia')
    if fecha == '':
      fecha = control_fecha[0]['mes_vigencia']
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
def campanaweb(request,nivel='MES'):
    print nivel
    campanaweb = CampanaWeb.objects.all().order_by('num_eval')
    campanaweb2 = CampanaWeb.objects.values('mes').annotate(tot_clientes=Sum('num_clientes'), tot_formtdc=Sum('form_tdc'), tot_formpld=Sum('form_pld'), tot_filtro=Sum('total_filtros'), tot_tdcmoi=Sum('tdc_moi'), tot_tdcil=Sum('tdc_il'), tot_tdnew=Sum('tdc_nueva'), tot_tdc=Sum('tdc_total'), tot_pldmoi=Sum('pld_moi'), tot_pldnew=Sum('pld_nueva'), tot_pld=Sum('pld_total'), efe_tdc=Sum('tdc'), efe_pld=Sum('pld'), efe_pldform=Sum(F('pld'))*100/Sum(F('pld_total')), efe_tdcform=Sum(F('tdc'))*100/Sum(F('tdc_total')), tdc_por=Sum(F('tdc_total'))*100/Sum(F('form_tdc')), pld_por=Sum(F('pld_total'))*100/Sum(F('form_pld'))).order_by('mes')
    campanaweb3 = CampanaWeb.objects.values('semana').annotate(tot_clientes=Sum('num_clientes'), tot_formtdc=Sum('form_tdc'), tot_formpld=Sum('form_pld'), tot_filtro=Sum('total_filtros'), tot_tdcmoi=Sum('tdc_moi'), tot_tdcil=Sum('tdc_il'), tot_tdnew=Sum('tdc_nueva'), tot_tdc=Sum('tdc_total'), tot_pldmoi=Sum('pld_moi'), tot_pldnew=Sum('pld_nueva'), tot_pld=Sum('pld_total'), efe_tdc=Sum('tdc'), efe_pld=Sum('pld'), efe_pldform=Sum(F('pld'))*100/Sum(F('pld_total')), efe_tdcform=Sum(F('tdc'))*100/Sum(F('tdc_total')), tdc_por=Sum(F('tdc_total'))*100/Sum(F('form_tdc')), pld_por=Sum(F('pld_total'))*100/Sum(F('form_pld'))).order_by('semana')

    totales = CampanaWeb.objects.aggregate(total1=Sum('tdc_nueva'), total2=Sum('tdc_total'), total3=Sum('pld_nueva'), total4=Sum('pld_total'), total5=Sum('tdc'), total6=Sum('pld'))

    tdc_efec = CampanaEfec.objects.values('mes').filter(segmento0='TDC').annotate(ambas=Sum(F('form_ambas'))*100/Sum(F('sol_ambas')),solovl=Sum(F('form_solovd'))*100/Sum(F('sol_solovd')),solovd=Sum(F('form_solovl'))*100/Sum(F('sol_solovl')),requiere=Sum(F('form_req'))*100/Sum(F('sol_req')),total=Sum(F('form_total'))*100/Sum(F('sol_total')),nueva=Sum('total_apro'),formal=Sum('form'),porcentaje=Sum(F('form'))*100/Sum(F('total_apro'))).order_by('mes')
    tdc_efec2 = CampanaEfec.objects.values('semana').filter(segmento0='TDC').annotate(ambas=Sum(F('form_ambas'))*100/Sum(F('sol_ambas')),solovl=Sum(F('form_solovd'))*100/Sum(F('sol_solovd')),solovd=Sum(F('form_solovl'))*100/Sum(F('sol_solovl')),requiere=Sum(F('form_req'))*100/Sum(F('sol_req')),total=Sum(F('form_total'))*100/Sum(F('sol_total')),nueva=Sum('total_apro'),formal=Sum('form'),porcentaje=Sum(F('form'))*100/Sum(F('total_apro'))).order_by('semana')
    tdc_efec3 = CampanaEfec.objects.values('segmento1').filter(segmento0='TDC').annotate(ambas=Sum(F('form_ambas'))*100/Sum(F('sol_ambas')),solovl=Sum(F('form_solovd'))*100/Sum(F('sol_solovd')),solovd=Sum(F('form_solovl'))*100/Sum(F('sol_solovl')),requiere=Sum(F('form_req'))*100/Sum(F('sol_req')),total=Sum(F('form_total'))*100/Sum(F('sol_total')),nueva=Sum('total_apro'),formal=Sum('form'),porcentaje=Sum(F('form'))*100/Sum(F('total_apro'))).order_by('id_efec')

    tot1 = CampanaEfec.objects.values('form_ambas', 'form_solovd', 'form_solovl', 'form_req', 'form_total', 'sol_ambas', 'sol_solovd', 'sol_solovl', 'sol_req', 'sol_total', 'total_apro', 'form').filter(segmento1='TDC')
    tot2 = CampanaEfec.objects.values('form_ambas', 'form_solovd', 'form_solovl', 'form_req', 'form_total', 'sol_ambas', 'sol_solovd', 'sol_solovl', 'sol_req', 'sol_total', 'total_apro', 'form').filter(segmento1='PLD')
    tdc_equifax = CampanaEquifax.objects.values('filtro1', 'ambas', 'solovd', 'solovl', 'req', 'total').filter(filtro0='TDC-EQUIFAX').order_by('id_equifax')
    pld_equifax = CampanaEquifax.objects.values('filtro1', 'ambas', 'solovd', 'solovl', 'req', 'total').filter(filtro0='PLD-EQUIFAX').order_by('id_equifax')

    pld_efec = CampanaEfec.objects.values('mes').filter(segmento0='PLD').annotate(ambas=Sum(F('form_ambas'))*100/Sum(F('sol_ambas')),solovl=Sum(F('form_solovd'))*100/Sum(F('sol_solovd')),solovd=Sum(F('form_solovl'))*100/Sum(F('sol_solovl')),requiere=Sum(F('form_req'))*100/Sum(F('sol_req')),total=Sum(F('form_total'))*100/Sum(F('sol_total')),nueva=Sum('total_apro'),formal=Sum('form'),porcentaje=Sum(F('form'))*100/Sum(F('total_apro'))).order_by('mes')
    pld_efec2 = CampanaEfec.objects.values('semana').filter(segmento0='PLD').annotate(ambas=Sum(F('form_ambas'))*100/Sum(F('sol_ambas')),solovl=Sum(F('form_solovd'))*100/Sum(F('sol_solovd')),solovd=Sum(F('form_solovl'))*100/Sum(F('sol_solovl')),requiere=Sum(F('form_req'))*100/Sum(F('sol_req')),total=Sum(F('form_total'))*100/Sum(F('sol_total')),nueva=Sum('total_apro'),formal=Sum('form'),porcentaje=Sum(F('form'))*100/Sum(F('total_apro'))).order_by('semana')
    pld_efec3 = CampanaEfec.objects.values('segmento1').filter(segmento0='PLD').annotate(ambas=Sum(F('form_ambas'))*100/Sum(F('sol_ambas')),solovl=Sum(F('form_solovd'))*100/Sum(F('sol_solovd')),solovd=Sum(F('form_solovl'))*100/Sum(F('sol_solovl')),requiere=Sum(F('form_req'))*100/Sum(F('sol_req')),total=Sum(F('form_total'))*100/Sum(F('sol_total')),nueva=Sum('total_apro'),formal=Sum('form'),porcentaje=Sum(F('form'))*100/Sum(F('total_apro'))).order_by('id_efec')

    tdc_mejoras = CampanaEquifax.objects.values('filtro1', 'ambas', 'solovd', 'solovl', 'req', 'total').filter(filtro0='TDC-MEJORAS').order_by('id_equifax')

    #power_lab = CampanaLabSeg.objects.all().filter(filtro0='LABORAL',filtro1='POWER').order_by('filtro2')
    #power_seg = CampanaLabSeg.objects.all().filter(filtro0='SEGMENTO',filtro1='POWER').order_by('filtro2')
    #pulpin_lab = CampanaLabSeg.objects.all().filter(filtro0='LABORAL',filtro1='PULPIN').order_by('filtro2')
    #pulpin_seg = CampanaLabSeg.objects.all().filter(filtro0='SEGMENTO',filtro1='PULPIN').order_by('filtro2')

    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_web.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campanareglapat(request):


    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana_reglapat.html', locals(),
                  context_instance=RequestContext(request))

# 3.- Vistas para reportes de RVGL
@login_required
def rvgl_resumen(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()

    evaluacion = RVGL.objects.filter(mes_vigencia=fecha).values('analista').annotate(num_eval=Count('rvgl'),dias=Count('dias_eval')).order_by('analista')
    if analista == "TODOS":
    	banca = RVGL.objects.filter(mes_vigencia=fecha,base_rvgl='1').values('seco').annotate(num_seco=Count('seco')).order_by('seco')
  	dictamen = RVGL.objects.filter(mes_vigencia=fecha,base_rvgl='1').values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
        producto = RVGL.objects.filter(mes_vigencia=fecha,base_rvgl='1').values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    	buro = RVGL.objects.exclude(dic_buro__in =['NULL', '']).filter(mes_vigencia=fecha,base_sco='1').values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')
    else:
    	banca = RVGL.objects.filter(mes_vigencia=fecha, analista=analista,base_rvgl='1').values('seco').annotate(num_seco=Count('seco')).order_by('seco')
  	dictamen = RVGL.objects.filter(mes_vigencia=fecha, analista=analista,base_rvgl='1').values('dictamen').annotate(num_dictamen=Count('dictamen')).order_by('dictamen')
        producto = RVGL.objects.filter(mes_vigencia=fecha, analista=analista,base_rvgl='1').values('producto_esp').annotate(num_producto=Count('producto_esp')).order_by('producto_esp')
    	buro = RVGL.objects.exclude(dic_buro__in =['','NULL']).filter(mes_vigencia=fecha, analista=analista,base_sco='1').values('dic_buro').annotate(num_buro=Count('dic_buro')).order_by('dic_buro')

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_resumen.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_resumenximporte(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()
    if analista == 'TODOS':
  	importexdict = RVGL.objects.filter(mes_vigencia=fecha,base_rvgl='1').exclude(dictamen='PROCESO').values('dictamen').annotate(sum_importe=Sum('importe_solic')).order_by('dictamen')
        importexprod = RVGL.objects.filter(mes_vigencia=fecha,base_rvgl='1').exclude(dictamen='PROCESO').values('producto_esp').annotate(sum_importexprod=Sum('importe_solic')).order_by('producto_esp')

    else:
  	importexdict = RVGL.objects.filter(mes_vigencia=fecha, analista=analista,base_rvgl='1').exclude(dictamen='PROCESO').values('dictamen').annotate(sum_importe=Sum('importe_solic')).order_by('dictamen')
        importexprod = RVGL.objects.filter(mes_vigencia=fecha, analista=analista,base_rvgl='1').exclude(dictamen='PROCESO').values('producto_esp').annotate(sum_importexprod=Sum('importe_solic')).order_by('producto_esp')

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_resumenximporte.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def rvgl_tiempo(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()
    #control_seco = RVGL.objects.values('seco').distinct('seco')
    if analista == 'TODOS':
       tiempo10 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0', dias_eval__lte='3', seco__in=['BP','CA'], base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval') )).order_by('dias_eval')
       tiempo11 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15',seco__in=['BP','CA'], base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
       tiempo20 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0',dias_eval__lte='3', seco='BP3', base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval'))).order_by('dias_eval')
       tiempo21 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15', seco='BP3', base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
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
       tiempo10 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0', dias_eval__lte='3', seco__in=['BP','CA'],analista=analista, base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval')) ).order_by('dias_eval')
       tiempo11 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15',seco__in=['BP','CA'],analista=analista, base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
       tiempo20 = RVGL.objects.values('mes_vigencia','dias_eval' ).filter(mes_vigencia=fecha, dias_eval__gte='0',dias_eval__lte='3', seco='BP3',analista=analista, base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval'))).order_by('dias_eval')
       tiempo21 = RVGL.objects.values('mes_vigencia' ).filter(mes_vigencia=fecha, dias_eval__gte='4',dias_eval__lte='15', seco='BP3',analista=analista, base_rvgl='1').exclude(dictamen='PROCESO').annotate(num_tiempo=Count(F('dias_eval'))).order_by('mes_vigencia')
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
	if i['codmes']=='201607':
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
def departamentos_web(request,semana=1):
    orden = int(semana)
    control_evaluacion=DepartamentosWeb.objects.values('semana').distinct().order_by('semana')
    departamentos = DepartamentosWeb.objects.values('departamento').distinct().order_by('departamento')
    ofertas_tc = DepartamentosWeb.objects.values('semana').exclude(oferta_tc='0').annotate(num_tdc=Count('oferta_tc'),sum_tdc=Sum('oferta_tc')).order_by('semana')
    ofertas_pld = DepartamentosWeb.objects.values('semana').exclude(oferta_pld='0').annotate(num_pld=Count('oferta_pld'),sum_pld=Sum('oferta_pld')).order_by('semana')
    ofertas=zip(ofertas_tc,ofertas_pld)
    print orden
    if orden==0:
        eval_tc = DepartamentosWeb.objects.values('departamento').exclude(oferta_tc='0').annotate(num_tdc=Count('oferta_tc')).order_by('departamento')
        eval_pld = DepartamentosWeb.objects.values('departamento').exclude(oferta_pld='0').annotate(num_pld=Count('oferta_pld')).order_by('departamento')
        efectividad = DepartamentosWeb.objects.values('departamento').annotate(num_ofer=Sum('ofertas'),num_form=Sum('formalizado'),num_efec=Sum(F('formalizado'))*100/Sum(F('ofertas'))).order_by('departamento')
        total_form = DepartamentosWeb.objects.aggregate(num_form=Sum('formalizado'))
        print eval_tc
        dict_tc = {}; dict_pld = {};
        for i in departamentos:
            for j in eval_tc:
                if j['departamento']==i['departamento']:
                    dict_tc[i['departamento']]=j['num_tdc']
                    break
	        else:
		    dict_tc[i['departamento']]=0

    	for i in departamentos:
	   for j in eval_pld:
	      if i['departamento']==j['departamento']:
		 dict_pld[i['departamento']]=j['num_pld']
		 break
	      else:
		 dict_pld[i['departamento']]=0

    	dict_total = {}; 
    	for i in total_form:
	   dict_total['Total'] = i['num_form']
    	dict_form2 = {}; dict_efec2 = {};
    	for i in departamentos:
	   for j in efectividad:
	      if i['departamento']==j['departamento']:
		   if dict_total['Total']==0:
		      dict_form2[i['departamento']]=0
		   else:
		      dict_form2[i['departamento']]=j['num_form']*100/dict_total['Total']
		   break
	      else:
		   dict_form2[i['departamento']]=0

    	for key, value in dict_form2.items():
	   if value==0:
	      dict_efec2[key]='silver'
	   if value>0 and value<20:
	      dict_efec2[key]='#89D1F3'
	   if value>=20 and value<40:
	      dict_efec2[key]='#009EE5'
	   if value>=40 and value<60:
	      dict_efec2[key]='#094FA4'
	   if value>=60 and value<80:
	      dict_efec2[key]='#86C82D'
	   if value>=80 and value<=100:
	      dict_efec2[key]='#FDBD2C'

    	dict_efec = {}; dict_ofer = {};
    	dict_form = {}; dict_efect = {}; 
    	for i in departamentos:
	   for j in efectividad:
	      if i['departamento']==j['departamento']:
		  if j['num_efec']==0:
		     dict_efec[i['departamento']]='silver'
		  if j['num_efec']>0 and j['num_efec']<20:
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
    else:
    	eval_tc = DepartamentosWeb.objects.values('semana', 'departamento').exclude(oferta_tc='0').filter(semana=semana).annotate(num_tdc=Count('oferta_tc')).order_by('semana')
    	eval_pld = DepartamentosWeb.objects.values('semana', 'departamento').exclude(oferta_pld='0').filter(semana=semana).annotate(num_pld=Count('oferta_pld')).order_by('semana')
    	efectividad = DepartamentosWeb.objects.values('semana', 'departamento').filter(semana=semana).annotate(num_ofer=Sum('ofertas'),num_form=Sum('formalizado'),num_efec=Sum(F('formalizado'))*100/Sum(F('ofertas'))).order_by('semana')
    	total_form = DepartamentosWeb.objects.values('semana').filter(semana=semana).annotate(num_form=Sum('formalizado')).order_by('semana')
    	dict_tc = {}; dict_pld = {};
    	for i in departamentos:
	   for j in eval_tc:
	      if j['departamento']==i['departamento']:
		 dict_tc[i['departamento']]=j['num_tdc']
		 break
	      else:
		 dict_tc[i['departamento']]=0

    	for i in departamentos:
	   for j in eval_pld:
	      if i['departamento']==j['departamento']:
		 dict_pld[i['departamento']]=j['num_pld']
		 break
	      else:
		 dict_pld[i['departamento']]=0

    	dict_total = {}; 
    	for i in total_form:
	   dict_total['Total'] = i['num_form']
    	dict_form2 = {}; dict_efec2 = {};
    	for i in departamentos:
	   for j in efectividad:
	      if i['departamento']==j['departamento']:
		 if dict_total['Total']==0:
		    dict_form2[i['departamento']]=0
		 else:
		    dict_form2[i['departamento']]=j['num_form']*100/dict_total['Total']
		 break
	      else:
		 dict_form2[i['departamento']]=0

    	for key, value in dict_form2.items():
	   if value==0:
	      dict_efec2[key]='silver'
	   if value>0 and value<20:
	      dict_efec2[key]='#89D1F3'
	   if value>=20 and value<40:
	      dict_efec2[key]='#009EE5'
	   if value>=40 and value<60:
	      dict_efec2[key]='#094FA4'
	   if value>=60 and value<80:
	      dict_efec2[key]='#86C82D'
	   if value>=80 and value<=100:
	      dict_efec2[key]='#FDBD2C'

    	dict_efec = {}; dict_ofer = {};
    	dict_form = {}; dict_efect = {}; 
    	for i in departamentos:
	   for j in efectividad:
	      if i['departamento']==j['departamento']:
		 if j['num_efec']==0:
		    dict_efec[i['departamento']]='silver'
		 if j['num_efec']>0 and j['num_efec']<20:
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
    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/departamentos_web.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_resumenxsco(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()
    dictamen = RVGL.objects.exclude(dictamen='PROCESO').values_list('dictamen', flat=True).distinct().order_by('dictamen')
    if analista == 'TODOS':
       dictamenxsco_ap = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha,base_sco='1').filter(dictamen_sco='AP').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
       listadict = ['APC','APS','DEN','DEV']
       scolista = []
       ap_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_ap:
	       if i == j['dictamen']:
		  ap_dict[i]=j['num_dictamenxsco_ap']
		  break
	       else:
		  ap_dict[i]=0
       if len(ap_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(ap_dict[i])
       dictamenxsco_du = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha,base_sco='1').filter(dictamen_sco='DU').annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
       du_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_du:
	       if i == j['dictamen']:
		  du_dict[i]=j['num_dictamenxsco_du']
		  break
	       else:
		  du_dict[i]=0
       if len(du_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(du_dict[i])
       dictamenxsco_re = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha,base_sco='1').filter(dictamen_sco='RE').annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
       re_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_re:
	       if i == j['dictamen']:
		  re_dict[i]=j['num_dictamenxsco_re']
		  break
	       else:
		  re_dict[i]=0
       if len(re_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(re_dict[i])
       scoxllenado = RVGL.objects.filter(mes_vigencia=fecha).exclude(sco__in=['O','']).values('sco').annotate(num_scoxllenado=Count('sco')).order_by('sco')
       scoxforzaje = RVGL.objects.filter(mes_vigencia=fecha).filter(dictamen_sco='RE').exclude(seg_prime='NULL').values('seg_prime').annotate(num_scoxforzaje=Count('seg_prime')).order_by('seg_prime')
       scoxdictamen = RVGL.objects.filter(mes_vigencia=fecha).exclude(dictamen_sco__in=['NULL','']).values('dictamen_sco' ).annotate(num_scoxdictamen=Count('dictamen_sco')).order_by('dictamen_sco')
    else:
       dictamenxsco_ap = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha,analista=analista,base_sco='1').filter(dictamen_sco ='AP').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
       scolista = []
       ap_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_ap:
	       if i == j['dictamen']:
		  ap_dict[i]=j['num_dictamenxsco_ap']
		  break
	       else:
		  ap_dict[i]=0
       if len(ap_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(ap_dict[i])

       dictamenxsco_du = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha,base_sco='1').filter(dictamen_sco='DU', analista= analista).annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
       du_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_du:
	       if i == j['dictamen']:
		  du_dict[i]=j['num_dictamenxsco_du']
		  break
	       else:
		  du_dict[i]=0
       if len(du_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(du_dict[i])
       dictamenxsco_re = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha,base_sco='1').filter(dictamen_sco='RE',analista= analista).annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
       re_dict = {}
       for i in dictamen:
	   for j in dictamenxsco_re:
	       if i == j['dictamen']:
		  re_dict[i]=j['num_dictamenxsco_re']
		  break
	       else:
		  re_dict[i]=0
       if len(re_dict) == 0:
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
	  scolista.append(0) 
       else:      
          for i in dictamen:
              scolista.append(re_dict[i])
       scoxllenado = RVGL.objects.filter(mes_vigencia=fecha,analista= analista).exclude(sco__in=['O','']).values('sco').annotate(num_scoxllenado=Count('sco')).order_by('sco')
       scoxforzaje = RVGL.objects.filter(mes_vigencia=fecha,analista= analista).filter(dictamen_sco='RE').exclude(seg_prime='NULL').values('seg_prime').annotate(num_scoxforzaje=Count('seg_prime')).order_by('seg_prime')
       scoxdictamen = RVGL.objects.filter(mes_vigencia=fecha,analista= analista).exclude(dictamen_sco__in=['NULL','']).values('dictamen_sco' ).annotate(num_scoxdictamen=Count('dictamen_sco')).order_by('dictamen_sco')

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_resumenxsco.html', locals(),
                  context_instance=RequestContext(request))

def rvgl_top20terr(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()
    if analista == 'TODOS':
       top20terr1 = RVGL.objects.filter(mes_vigencia=fecha).values('territorio_nuevo').exclude(territorio_nuevo='').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20terr2 = RVGL.objects.values('territorio_nuevo').filter(mes_vigencia=fecha).exclude(importe_aprob=0).exclude(territorio_nuevo='').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
       print top20terr2
       top20terr = zip(top20terr2, top20terr1)
    else:
       top20terr1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('territorio_nuevo').exclude(territorio_nuevo='').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20terr2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).exclude(territorio_nuevo='').values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
       top20terr = zip(top20terr1, top20terr2)

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20terr.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20gest(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()
    if analista == 'TODOS':
       top20gest1 = RVGL.objects.filter(mes_vigencia=fecha).exclude(ejecutivo_cuenta='').values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic'), sum_top20gest1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20gest2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(ejecutivo_cuenta='').exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest2=Count('importe_aprob'), sum_top20gest2=Sum('importe_aprob')).order_by('-sum_top20gest2')[:20]
       top20gest = zip(top20gest1,top20gest2)
    else:
       top20gest1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(ejecutivo_cuenta='').values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic'), sum_top20gest1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20gest2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(ejecutivo_cuenta='').exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest2=Count('importe_aprob'), sum_top20gest2=Sum('importe_aprob')).order_by('-sum_top20gest2')[:20]
       top20gest = zip(top20gest1,top20gest2)

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20gest.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20clie(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()
    if analista == 'TODOS':
       top20clie1 = RVGL.objects.filter(mes_vigencia=fecha).exclude(cliente='').values('cliente').annotate(num_top20clie1=Count('importe_solic'), sum_top20clie1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20clie2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(cliente='').exclude(importe_aprob=0).values('cliente').annotate(num_top20clie2=Count('importe_aprob'), sum_top20clie2=Sum('importe_aprob')).order_by('-sum_top20clie2')[:20]
       top20clie = zip(top20clie1,top20clie2)
    else:
       top20clie1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(cliente='').values('cliente').annotate(num_top20clie1=Count('importe_solic'), sum_top20clie1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20clie2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).exclude(cliente='').values('cliente').annotate(num_top20clie2=Count('importe_aprob'), sum_top20clie2=Sum('importe_aprob')).order_by('-sum_top20clie2')[:20]
       top20clie = zip(top20clie1,top20clie2)

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20clie.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl_top20ofic(request, fecha=before2, analista='TODOS'):
    control_analistas = RVGL.objects.values_list('analista', flat=True).distinct()
    control_fecha = RVGL.objects.values_list('mes_vigencia', flat=True).distinct()
    if analista == 'TODOS':
       top20ofic1 = RVGL.objects.filter(mes_vigencia=fecha).exclude(oficina='').values('oficina').annotate(num_top20ofic1=Count('importe_solic'), sum_top20ofic1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20ofic2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(oficina='').exclude(importe_aprob=0).values('oficina').annotate(num_top20ofic2=Count('importe_aprob'), sum_top20ofic2=Sum('importe_aprob')).order_by('-sum_top20ofic2')[:20]
       top20ofic = zip(top20ofic1,top20ofic2)
    else:
       top20ofic1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(oficina='').values('oficina').annotate(num_top20ofic1=Count('importe_solic'), sum_top20ofic1=Sum('importe_solic'),sum_apro=Sum('importe_aprob')).order_by('-sum_apro')[:20]
       top20ofic2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(oficina='').exclude(importe_aprob=0).values('oficina').annotate(num_top20ofic2=Count('importe_aprob'), sum_top20ofic2=Sum('importe_aprob')).order_by('-sum_top20ofic2')[:20]
       top20ofic = zip(top20ofic1,top20ofic2)

    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_top20ofic.html', locals(),
                  context_instance=RequestContext(request))

# 4.- Vistas para reportes de EVALUACION
@login_required
def evaluacion_evaluaciontc(request):
    meses = Seguimiento.objects.values_list('mes_vigencia', flat=True).order_by('mes_vigencia').distinct()
    evaluaciontc = Evaluaciontc.objects.all().order_by('cliente')#.distinct('cliente')
    print evaluaciontc

    static_url=settings.STATIC_URL
    tipo_side = 3
    return render('reports/evaluacion_evaluaciontc.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def cartera_minorista(request):
    meses = Stock.objects.values('codmes').order_by('-codmes').distinct('codmes')
    meses_list= []
    for i in meses:
      meses_list.append(i['codmes'])
    num_list=len(meses_list)
    mes_inicial=meses_list[num_list-1]
    mes_final=meses_list[0]

    stock = Stock.objects.values('producto','codmes').filter(codmes__in=[mes_final,mes_inicial]).annotate(inversion=Sum('inv'),atraso=Sum('atrasada')).order_by('producto')
    inv_1602 = {}; inv_1702 = {}; varia_inv = {}; cartera_16={}; cartera_17={};
    atraso_16={}; atraso_17={};
    for i in stock:
      if i['codmes'] == meses_list[num_list-1]:
        if i['producto'] == 'PLD':
          inv_1602['1'] = i['inversion']
          cartera_16['1'] = i['atraso']*100/i['inversion']
          atraso_16['1'] = i['atraso']
        if i['producto'] == 'Auto':
          inv_1602['2'] = i['inversion']
          cartera_16['2'] = i['atraso']*100/i['inversion']
          atraso_16['2'] = i['atraso']
        if i['producto'] == 'TdC':
          inv_1602['3'] = i['inversion']
          cartera_16['3'] = i['atraso']*100/i['inversion']
          atraso_16['3'] = i['atraso']
        if i['producto'] == 'Hipoteca':
          inv_1602['4'] = i['inversion']
          cartera_16['4'] = i['atraso']*100/i['inversion']
          atraso_16['4'] = i['atraso']
      if i['codmes'] == meses_list[0]:
        if i['producto'] == 'PLD':
          inv_1702['1'] = i['inversion']
          cartera_17['1'] = i['atraso']*100/i['inversion']
          atraso_17['1'] = i['atraso']
        if i['producto'] == 'Auto':
          inv_1702['2'] = i['inversion']
          cartera_17['2'] = i['atraso']*100/i['inversion']
          atraso_17['2'] = i['atraso']
        if i['producto'] == 'TdC':
          inv_1702['3'] = i['inversion']
          cartera_17['3'] = i['atraso']*100/i['inversion']
          atraso_17['3'] = i['atraso']
        if i['producto'] == 'Hipoteca':
          inv_1702['4'] = i['inversion']
          cartera_17['4'] = i['atraso']*100/i['inversion']
          atraso_17['4'] = i['atraso']
    inv_1602['5']=inv_1602['1']+inv_1602['2']+inv_1602['3']+inv_1602['4']
    inv_1702['5']=inv_1702['1']+inv_1702['2']+inv_1702['3']+inv_1702['4']
    cartera_16['5'] = (atraso_16['1']+atraso_16['2']+atraso_16['3']+atraso_16['4'])*100/inv_1602['5']
    cartera_17['5'] = (atraso_17['1']+atraso_17['2']+atraso_17['3']+atraso_17['4'])*100/inv_1702['5']
    varia_inv['1']=(inv_1702['1']/inv_1602['1'])-1
    varia_inv['2']=(inv_1702['2']/inv_1602['2'])-1
    varia_inv['3']=(inv_1702['3']/inv_1602['3'])-1
    varia_inv['4']=(inv_1702['4']/inv_1602['4'])-1
    varia_inv['5']=(inv_1702['5']/inv_1602['5'])-1

    meses2 = Dotaciones.objects.values('codmes').order_by('-codmes').distinct('codmes')
    meses_list2= []
    for i in meses2:
      meses_list2.append(i['codmes'])
    num_list2=len(meses_list2)
    mes_inicial2=meses_list2[12]
    mes_final2=meses_list2[0]

    dotacion = Dotaciones.objects.values('producto','codmes').filter(codmes__in=[mes_final2,mes_inicial2]).annotate(dotacion=Sum('dotacion')).order_by('producto')
    dota_16 = {}; dota_17 = {}; varia_dota = {};
    for i in dotacion:
      if i['codmes'] == meses_list2[12]:
        if i['producto'] == 'PLD':
          dota_16['1'] = i['dotacion']/1000000
        if i['producto'] == 'Auto':
          dota_16['2'] = i['dotacion']/1000000
        if i['producto'] == 'TdC':
          dota_16['3'] = i['dotacion']/1000000
        if i['producto'] == 'Hipoteca':
          dota_16['4'] = i['dotacion']/1000000
      if i['codmes'] == meses_list2[0]:
        if i['producto'] == 'PLD':
          dota_17['1'] = i['dotacion']/1000000
        if i['producto'] == 'Auto':
          dota_17['2'] = i['dotacion']/1000000
        if i['producto'] == 'TdC':
          dota_17['3'] = i['dotacion']/1000000
        if i['producto'] == 'Hipoteca':
          dota_17['4'] = i['dotacion']/1000000
    dota_16['5']=dota_16['1']+dota_16['2']+dota_16['3']+dota_16['4']
    dota_17['5']=dota_17['1']+dota_17['2']+dota_17['3']+dota_17['4']
    varia_dota['1']=(dota_17['1']/dota_16['1'])-1
    varia_dota['2']=(dota_17['2']/dota_16['2'])-1
    varia_dota['3']=(dota_17['3']/dota_16['3'])-1
    varia_dota['4']=(dota_17['4']/dota_16['4'])-1
    varia_dota['5']=(dota_17['5']/dota_16['5'])-1

    riesgo_16 = Dotaciones.objects.values('producto').filter(codmes__gte=meses_list2[11]).annotate(riesgo=Avg('riesgo'),dotacion=Sum('dotacion'),salidas=Sum('salidas'))
    riesgo_17 = Dotaciones.objects.values('producto').filter(codmes__gte=meses_list2[23],codmes__lte=meses_list2[12]).annotate(riesgo=Avg('riesgo'),dotacion=Sum('dotacion'),salidas=Sum('salidas'))
    riesgo1_dict = {}; riesgo2_dict = {}; sum_dota=0; sum_salida=0; sum_riesgo=0;
    sum_dota1=0; sum_salida1=0; sum_riesgo1=0;
    for i in riesgo_16:
        if i['producto'] == 'PLD':
          riesgo1_dict['1'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
        if i['producto'] == 'Auto':
          riesgo1_dict['2'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
        if i['producto'] == 'TdC':
          riesgo1_dict['3'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
        if i['producto'] == 'Hipoteca':
          riesgo1_dict['4'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
    for i in riesgo_17:
        if i['producto'] == 'PLD':
          riesgo2_dict['1'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
        if i['producto'] == 'Auto':
          riesgo2_dict['2'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
        if i['producto'] == 'TdC':
          riesgo2_dict['3'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
        if i['producto'] == 'Hipoteca':
          riesgo2_dict['4'] = (i['dotacion']-i['salidas'])/Decimal(i['riesgo'])
    for i in riesgo_17:
      sum_dota = sum_dota + i['dotacion']
      sum_salida = sum_salida + i['salidas']
      sum_riesgo = sum_riesgo + i['riesgo']
    riesgo1_dict['5'] = (sum_dota-sum_salida)*100/Decimal(sum_riesgo)
    for i in riesgo_16:
      sum_dota1 = sum_dota1 + i['dotacion']
      sum_salida1 = sum_salida1 + i['salidas']
      sum_riesgo1 = sum_riesgo1 + i['riesgo']
    riesgo2_dict['5'] = (sum_dota1-sum_salida1)*100/Decimal(sum_riesgo1)

    meses_costo = CosteRiesgo.objects.values('codmes').order_by('-codmes').distinct('codmes')
    meses_costo_list= []
    for i in meses_costo:
      meses_costo_list.append(i['codmes'])
    #print meses_costo_list
    costo_mensual_total = CosteRiesgo.objects.values('codmes','m6_t','m9_t','m12_t','m6_c','m9_c','m12_c','m6_u','m9_u','m12_u').filter(producto='Consumo')
    cm6t_dict={};cm9t_dict={};cm12t_dict={};
    cm6c_dict={};cm9c_dict={};cm12c_dict={};
    cm6u_dict={};cm9u_dict={};cm12u_dict={};
    for i in costo_mensual_total:
      for j in meses_costo:
        if i['codmes']<=meses_costo_list[6]:
          cm6t_dict[i['codmes']]=i['m6_t']*100
          cm6c_dict[i['codmes']]=i['m6_c']*100
          cm6u_dict[i['codmes']]=i['m6_u']*100
        else:
          cm6t_dict[i['codmes']]=[]
          cm6c_dict[i['codmes']]=[]
          cm6u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[9]:
          cm9t_dict[i['codmes']]=i['m9_t']*100
          cm9c_dict[i['codmes']]=i['m9_c']*100
          cm9u_dict[i['codmes']]=i['m9_u']*100
        else:
          cm9t_dict[i['codmes']]=[]
          cm9c_dict[i['codmes']]=[]
          cm9u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[12]:
          cm12t_dict[i['codmes']]=i['m12_t']*100
          cm12c_dict[i['codmes']]=i['m12_c']*100
          cm12u_dict[i['codmes']]=i['m12_u']*100
        else:
          cm12t_dict[i['codmes']]=[]
          cm12c_dict[i['codmes']]=[]
          cm12u_dict[i['codmes']]=[]

    costo_mensual_totaltdc = CosteRiesgo.objects.values('codmes','m6_t','m9_t','m12_t','m6_c','m9_c','m12_c','m6_u','m9_u','m12_u').filter(producto='Tarjeta')
    tm6t_dict={};tm9t_dict={};tm12t_dict={};
    tm6c_dict={};tm9c_dict={};tm12c_dict={};
    tm6u_dict={};tm9u_dict={};tm12u_dict={};
    for i in costo_mensual_totaltdc:
      for j in meses_costo:
        if i['codmes']<=meses_costo_list[6]:
          tm6t_dict[i['codmes']]=i['m6_t']*100
          tm6c_dict[i['codmes']]=i['m6_c']*100
          tm6u_dict[i['codmes']]=i['m6_u']*100
        else:
          tm6t_dict[i['codmes']]=[]
          tm6c_dict[i['codmes']]=[]
          tm6u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[9]:
          tm9t_dict[i['codmes']]=i['m9_t']*100
          tm9c_dict[i['codmes']]=i['m9_c']*100
          tm9u_dict[i['codmes']]=i['m9_u']*100
        else:
          tm9t_dict[i['codmes']]=[]
          tm9c_dict[i['codmes']]=[]
          tm9u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[12]:
          tm12t_dict[i['codmes']]=i['m12_t']*100
          tm12c_dict[i['codmes']]=i['m12_c']*100
          tm12u_dict[i['codmes']]=i['m12_u']*100
        else:
          tm12t_dict[i['codmes']]=[]
          tm12c_dict[i['codmes']]=[]
          tm12u_dict[i['codmes']]=[]

    trimestre_costo = CosteRiesgo.objects.values('codmes').order_by('-codmes').distinct('codmes')
    trimestre_costo_list= []
    for i in trimestre_costo:
      trimestre_costo_list.append(i['codmes'])

    costo_trimestre_total = CosteRiesgo2.objects.values('codmes','subproducto','m1','m2','m3','m4','m5','m6','m7','m8','m9','m10','m11','m12').filter(producto='Consumo')
    cm1tr_dict={};cm2tr_dict={};cm3tr_dict={};cm4tr_dict={};cm5tr_dict={};cm6tr_dict={};cm7tr_dict={};cm8tr_dict={};cm9tr_dict={};cm10tr_dict={};cm11tr_dict={};cm12tr_dict={};
    cm1cr_dict={};cm2cr_dict={};cm3cr_dict={};cm4cr_dict={};cm5cr_dict={};cm6cr_dict={};cm7cr_dict={};cm8cr_dict={};cm9cr_dict={};cm10cr_dict={};cm11cr_dict={};cm12cr_dict={};
    cm1ur_dict={};cm2ur_dict={};cm3ur_dict={};cm4ur_dict={};cm5ur_dict={};cm6ur_dict={};cm7ur_dict={};cm8ur_dict={};cm9ur_dict={};cm10ur_dict={};cm11ur_dict={};cm12ur_dict={};
    for i in costo_trimestre_total:
      for j in trimestre_costo:
        if i['subproducto']=='TOTAL':
          cm1tr_dict[i['codmes']]=i['m1']*100
          cm2tr_dict[i['codmes']]=i['m2']*100
          cm3tr_dict[i['codmes']]=i['m3']*100
          cm4tr_dict[i['codmes']]=i['m4']*100
          cm5tr_dict[i['codmes']]=i['m5']*100
          cm6tr_dict[i['codmes']]=i['m6']*100
          cm7tr_dict[i['codmes']]=i['m7']*100
          cm8tr_dict[i['codmes']]=i['m8']*100
          cm9tr_dict[i['codmes']]=i['m9']*100
          cm10tr_dict[i['codmes']]=i['m10']*100
          cm11tr_dict[i['codmes']]=i['m11']*100
          cm12tr_dict[i['codmes']]=i['m12']*100
        else:
          cm1tr_dict[i['codmes']]=[]
          cm2tr_dict[i['codmes']]=[]
          cm3tr_dict[i['codmes']]=[]
          cm4tr_dict[i['codmes']]=[]
          cm5tr_dict[i['codmes']]=[]
          cm6tr_dict[i['codmes']]=[]
          cm7tr_dict[i['codmes']]=[]
          cm8tr_dict[i['codmes']]=[]
          cm9tr_dict[i['codmes']]=[]
          cm10tr_dict[i['codmes']]=[]
          cm11tr_dict[i['codmes']]=[]
          cm12tr_dict[i['codmes']]=[]
    print costo_trimestre_total


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/cartera_minorista.html', locals(),
                  context_instance=RequestContext(request))


# 5.- Vistas para reportes de SEGUIMIENTO
@login_required
def seguimiento_tdc(request, filtro1='mes_vigencia', filtro2='2012', filtro3='form'):
    filtro1 = str(filtro1)
    filtro2 = str(filtro2)
    filtro3 = str(filtro3)

    tiempo = Seguimiento.objects.values_list('periodo', flat=True).order_by('periodo').distinct()

    if filtro3 == 'form':
      tipo_form = 1
    else:
      tipo_form = 0

    if filtro1 == 'trimestre_form':
        meses = Seguimiento.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).exclude(trimestre_form__in=['']).order_by(filtro1).distinct()
        trimestre = 1
    else:
        meses = Seguimiento.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).order_by(filtro1).distinct()
        trimestre = 0

    total_form = Seguimiento.objects.values(filtro1, 'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3),cuentas=Sum('ctas')).order_by(filtro1)
    total_form_dict = {}; total_ctas_dict = {};
    for j in total_form:
        total_form_dict[j[filtro1]]=j['formalizado']
        total_ctas_dict[j[filtro1]]=j['cuentas']

    if filtro1 == 'trimestre_form':
        meses_fast = Seguimiento.objects.values('trimestre_form').filter(trimestre_form__gte='2014-4').order_by('-trimestre_form').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1
    else:
        meses_fast = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201410').order_by('-mes_vigencia').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1

    uno_a_uno = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_fast = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_regular = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    formUno_dict = {}; formFast_dict = {}; formRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                formUno_dict[i] = j['formalizado']
                break
            else:
                formUno_dict[i] = 0
        for j in camp_fast:
            if i == j[filtro1]:
                formFast_dict[i] = j['formalizado']
                break
            else:
                formFast_dict[i] = 0
        for j in camp_regular:
            if i == j[filtro1]:
                formRegular_dict[i] = j['formalizado']
                break
            else:
                formRegular_dict[i] = 0

    uno_a_uno = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_fast = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_regular = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    ticketUno_dict = {}; ticketFast_dict = {}; ticketRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                ticketUno_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketUno_dict[i] = []
        for j in camp_fast:
            if i == j[filtro1]:
                if i >= meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = j['facturacion']*1000000/j['formalizado']
                elif i < meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = []
                break
            else:
                ticketFast_dict[i] = []
        for j in camp_regular:
            if i == j[filtro1]:
                ticketRegular_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketRegular_dict[i] = []

    if filtro1 == 'trimestre_form':
        meses_moras = Seguimiento.objects.values('trimestre_form').order_by('-trimestre_form').distinct()
        mora_mes = Seguimiento.objects.values('trimestre_form').filter(trimestre_form__gte='2015-2', periodo__gte=filtro2).order_by('-trimestre_form').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 1
        num_mora6 = 2
        num_mora9 = 3
        num_mora12 = 4
        num_mora18 = 6 
        num_mora24 = 8 
        num_mora36 = 12 
    else:
        meses_moras = Seguimiento.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
        mora_mes = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201504', periodo__gte=filtro2).order_by('-mes_vigencia').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 4 
        num_mora6 = 6 
        num_mora9 = 9 
        num_mora12 = 12 
        num_mora18 = 18 
        num_mora24 = 24 
        num_mora36 = 36 

    morames_list = []
    for i in meses_moras:
        morames_list.append(i[filtro1])
    
    mora460 = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
    mora6 = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
    mora9 = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
    mora12 = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    mora18 = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora18'),cuentas=Sum('ctas')).order_by(filtro1)
    mora24 = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora24'),cuentas=Sum('ctas')).order_by(filtro1)
    mora36 = Seguimiento.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora36'),cuentas=Sum('ctas')).order_by(filtro1)
    mora460_dict = {}; mora6_dict = {}; mora9_dict = {}; mora12_dict = {};
    mora18_dict = {}; mora24_dict = {}; mora36_dict = {};
    for j in mora460:
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora460:
        if j[filtro1] <= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=[]
    for j in mora6:
        if j[filtro1] <= morames_list[num_mora6]:
            mora6_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora9:
        if j[filtro1] <= morames_list[num_mora9]:
            mora9_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora12:
        if j[filtro1] <= morames_list[num_mora12]:
            mora12_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora18:
        if j[filtro1] <= morames_list[num_mora18]:
            mora18_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora24:
        if j[filtro1] <= morames_list[num_mora24]:
            mora24_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora36:
        if j[filtro1] <= morames_list[num_mora36]:
            mora36_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']

    mora_ingresos = Seguimiento.objects.values(filtro1,'rng_ing').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora9=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
    MoraIngreso1_dict = {}; MoraIngreso2_dict = {}; MoraIngreso3_dict = {}; MoraIngreso4_dict = {}; MoraIngreso5_dict = {}; MoraIngreso6_dict = {};
    for j in mora_ingresos:
      if j[filtro1]<=morames_list[num_mora9]:
        if j['rng_ing']=='01 [3.5K - ...]':
          MoraIngreso1_dict[j[filtro1]]=j['sum_mora9']*100/j['cuentas']
        elif j['rng_ing']=='02 [2.5K - 3.5K]':
          MoraIngreso2_dict[j[filtro1]]=j['sum_mora9']*100/j['cuentas']
        elif j['rng_ing']=='03 [2K - 2.5K]':
          MoraIngreso3_dict[j[filtro1]]=j['sum_mora9']*100/j['cuentas']
        elif j['rng_ing']=='04 [1.5K - 2K]':
          MoraIngreso4_dict[j[filtro1]]=j['sum_mora9']*100/j['cuentas']
        elif j['rng_ing']=='05 [1K - 1.5K]':
          MoraIngreso5_dict[j[filtro1]]=j['sum_mora9']*100/j['cuentas']
        elif j['rng_ing']=='06 [0 - 1K]':
          MoraIngreso6_dict[j[filtro1]]=j['sum_mora9']*100/j['cuentas']


    rangos = Seguimiento.objects.values(filtro1, 'rng_ing').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(num_rango=Sum(filtro3)).order_by(filtro1)
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
      for j in rangos:
        if i == j[filtro1]:
          if j['rng_ing'] == '01 [3.5K - ...]':
            rango1_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '02 [2.5K - 3.5K]':
            rango2_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '03 [2K - 2.5K]':
            rango3_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '04 [1.5K - 2K]':
            rango4_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '05 [1K - 1.5K]':
            rango5_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '06 [0 - 1K]':
            rango6_dict[i]=j['num_rango']*100/total_form_dict[i]

    formxcampxuno = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_form_dict = {}; uno_form_dict = {};
    for i in meses:
        for j in formxcampxuno:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                camp_form_dict[i] = j['formalizado']
                break
            else:
                camp_form_dict[i] = 0
        for j in formxcampxuno:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_form_dict[i] = j['formalizado']
                break
            else:
                uno_form_dict[i] = 0

    seg_ava = Seguimiento.objects.values(filtro1).filter(riesgos='CAMP', producto='03 Tarjeta', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ms = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_noph = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_nocli = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ava_dict = {}; seg_ms_dict = {}; seg_noph_dict = {}; seg_nocli_dict = {};
    useg_ms_dict = {}; useg_noph_dict = {}; useg_nocli_dict = {};
    for i in meses:
        for j in seg_ava:
            if i == j[filtro1]:
                seg_ava_dict[i] = j['seg']
                break
            else:
                seg_ava_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_ms_dict[i] = j['seg']
                break
            else:
                seg_ms_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_ms_dict[i] = j['seg']
                break
            else:
                useg_ms_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_noph_dict[i] = j['seg']
                break
            else:
                seg_noph_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_noph_dict[i] = j['seg']
                break
            else:
                useg_noph_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_nocli_dict[i] = j['seg']
                break
            else:
                seg_nocli_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_nocli_dict[i] = j['seg']
                break
            else:
                useg_nocli_dict[i] = 0

    total_ctasxmorasxcampxuno = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12'),sum_mora18=Sum('mora18'), sum_mora24=Sum('mora24'), sum_mora36=Sum('mora36')).order_by(filtro1)
    total_ctasxcamp_dict = {}; mora460_camp_dict = {}; mora6_camp_dict = {}; mora9_camp_dict = {}; mora12_camp_dict = {}; mora18_camp_dict = {}; mora24_camp_dict = {}; mora36_camp_dict = {};
    mora460_uno_dict = {}; mora6_uno_dict = {}; mora9_uno_dict = {}; mora12_uno_dict = {}; mora18_uno_dict = {}; mora24_uno_dict = {}; mora36_uno_dict = {};
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_camp_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_camp_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_camp_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_camp_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_camp_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_camp_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_uno_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_uno_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_uno_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_uno_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_uno_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_uno_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']


    moras = Seguimiento.objects.values(filtro1, 'segmento', 'riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO 6 MESES - SEGMENTOS
    ava_mora460_dict = {}; ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora460_dict = {}; ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora460_dict = {}; noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora460_dict = {}; nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    #INCUMPLIMIENTO 6 MESES SEGMENTO - UNO A UNO
    dict_moraunoms = {}; dict_moraunonoph = {}; dict_moraunonocli = {};
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['segmento']=='1.AVA':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ava_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ava_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ava_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ava_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ava_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']     
              elif  j['segmento']=='2.MS':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ms_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ms_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ms_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ms_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ms_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      noph_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      noph_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      noph_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      noph_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      noph_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      nocli_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      nocli_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      nocli_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      nocli_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      nocli_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['segmento']=='2.MS':
                if i <= morames_list[num_mora6]:
                      dict_moraunoms[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora6]:
                      dict_moraunonoph[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora6]:
                      dict_moraunonocli[i]=j['sum_mora6']*100/j['sum_ctas']

    depen = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum(filtro3)).order_by(filtro1)
    indep = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    pnn = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    no_recon = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    depen_dict = {}; indep_dict = {}; pnn_dict = {}; no_recon_dict = {}; totxcamp_laboral = {};
    udepen_dict = {}; uindep_dict = {}; upnn_dict = {}; uno_recon_dict = {};
    for i in meses:
        for j in depen:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                depen_dict[i] = j['seg']
                break
            else:
                depen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                indep_dict[i] = j['seg']
                break
            else:
                indep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                pnn_dict[i] = j['seg']
                break
            else:
                pnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                no_recon_dict[i] = j['seg']
                break
            else:
                no_recon_dict[i] = 0
        for j in depen:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                udepen_dict[i] = j['seg']
                break
            else:
                udepen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uindep_dict[i] = j['seg']
                break
            else:
                uindep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                upnn_dict[i] = j['seg']
                break
            else:
                upnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_recon_dict[i] = j['seg']
                break
            else:
                uno_recon_dict[i] = 0

    morascat = Seguimiento.objects.values(filtro1, 'cat_persona','riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO RELACION LABORAL CAMPANAS
    dep_mora460_dict = {}; dep_mora6_dict = {}; dep_mora9_dict = {}; dep_mora12_dict = {}
    indep_mora460_dict = {}; indep_mora6_dict = {}; indep_mora9_dict = {}; indep_mora12_dict = {}
    pnn_mora460_dict = {}; pnn_mora6_dict = {}; pnn_mora9_dict = {}; pnn_mora12_dict = {}
    norec_mora460_dict = {}; norec_mora6_dict = {}; norec_mora9_dict = {}; norec_mora12_dict = {}
    #INCUMPLMIENTO 6 MESES RELACION LABORAL - UNO A UNO
    dict_moracamdep = {}; dict_moracamind = {}; 
    dict_moracampnn = {}; dict_moracamnor = {};
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['cat_persona']=='1. Dependiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      dep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      dep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      dep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      dep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      dep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']    
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      indep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      indep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      indep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      indep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      indep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      pnn_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      pnn_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      pnn_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      pnn_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      pnn_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      norec_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      norec_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      norec_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      norec_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      norec_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['cat_persona']=='1. Dependiente':
                if i <= morames_list[num_mora6]:
                      dict_moracamdep[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora6]:
                      dict_moracamind[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora6]:
                      dict_moracampnn[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora6]:
                      dict_moracamnor[i]=j['sum_mora6']*100/j['sum_ctas']

    buroxform = Seguimiento.objects.values(filtro1, 'buro_camp').filter(digital='',riesgos='CAMP', producto='03 Tarjeta', periodo__gte=filtro2).annotate(seg=Sum(filtro3),cuentas=Sum('ctas'),sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_burog1 = {}; dict_burog5 = {};
    dict_burog6 = {}; dict_buronb = {};
    for i in meses:
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G1-G4':
                dict_burog1[i] = j['seg']
                break
              else:
                dict_burog1[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G5':
                dict_burog5[i] = j['seg']
                break
              else:
                dict_burog5[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G6-G8':
                dict_burog6[i] = j['seg']
                break
              else:
                dict_burog6[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'NB':
                dict_buronb[i] = j['seg']
                break
              else:
                dict_buronb[i] = 0

    dict_mora6buro1 = {}; dict_mora6buro2 = {}; 
    dict_mora6buro3 = {}; dict_mora6buro4 = {};
    for i in buroxform:
        if i['buro_camp'] == 'G1-G4':
            if i <= morames_list[num_mora6]:
              if i['cuentas']==0 or i['cuentas']==' ' or i['cuentas']=='':
                dict_mora6buro1[i[filtro1]] = 0
              else:
                dict_mora6buro1[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G5':
            if i <= morames_list[num_mora6]:
              if i['cuentas']==0 or i['cuentas']==' ' or i['cuentas']=='':
                dict_mora6buro2[i[filtro1]] = 0
              else:
                dict_mora6buro2[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G6-G8':
            if i <= morames_list[num_mora6]:
              if i['cuentas']==0 or i['cuentas']==' ' or i['cuentas']=='':
                dict_mora6buro3[i[filtro1]] = 0
              else:
                dict_mora6buro3[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'NB':
            if i <= morames_list[num_mora6]:
              if i['cuentas']==0 or i['cuentas']==' ' or i['cuentas']=='':
                dict_mora6buro4[i[filtro1]] = 0
              else:
                dict_mora6buro4[i[filtro1]] = i['sum_mora6']*100/i['cuentas']

    total_forzaje = Forzaje.objects.values(filtro1).filter(producto='03 Tarjeta').annotate(cantidad=Sum('form')).order_by(filtro1)
    forzaje_dict = {}
    for i in meses:
     for j in total_forzaje:
         if i == j[filtro1]:
          forzaje_dict[j[filtro1]]=j['cantidad']

    forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '03 Tarjeta').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    duda_dict = {}; rechazo_dict = {};
    for i in meses:
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='DU':
                    duda_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                duda_dict[i]= 0
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='RE':
                    rechazo_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                rechazo_dict[i]= 0

    form_cluster = Seguimiento.objects.values(filtro1, 'cluster').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum(filtro3)).order_by(filtro1)
    form_modes_dict = {}; form_desli_dict = {}; form_progre_dict = {};
    form_aspi_dict = {}; form_prospe_dict = {}; form_sd_dict = {};
    for i in meses:
        for j in form_cluster:
            if i == j[filtro1]:
              if j['cluster'] == '1. Modestos':
                form_modes_dict[i] = j['formalizados']
              elif j['cluster'] == '2. Desligados':
                form_desli_dict[i] = j['formalizados']
              elif j['cluster'] == '3. Progresistas':
                form_progre_dict[i] = j['formalizados']
              elif j['cluster'] == '4. Aspirantes':
                form_aspi_dict[i] = j['formalizados']
              elif j['cluster'] == '5. Prosperos':
                form_prospe_dict[i] = j['formalizados']
              elif j['cluster'] == '0. S.D.':
                form_sd_dict[i] = j['formalizados']

    form_clusterxmora = Seguimiento.objects.values(filtro1, 'cluster').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    modes_mora6_dict = {}; desli_mora6_dict = {}; 
    progre_mora460_dict = {}; progre_mora6_dict = {}; progre_mora9_dict = {}; progre_mora12_dict = {}
    aspi_mora460_dict = {}; aspi_mora6_dict = {}; aspi_mora9_dict = {}; aspi_mora12_dict = {}
    prospe_mora460_dict = {}; prospe_mora6_dict = {}; prospe_mora9_dict = {}; prospe_mora12_dict = {}
    for i in meses:
       for j in form_clusterxmora:
          if i == j[filtro1]:
            if  j['cluster']=='1. Modestos':
                if i <= morames_list[num_mora6]:
                    modes_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='2. Desligados':
                if i <= morames_list[num_mora6]:
                    desli_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='3. Progresistas':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    progre_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    progre_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    progre_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    progre_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    progre_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='4. Aspirantes':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    aspi_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    aspi_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    aspi_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    aspi_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    aspi_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='5. Prosperos':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    prospe_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    prospe_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    prospe_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    prospe_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    prospe_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']

    meses_costo = CosteRiesgo.objects.values_list('codmes', flat=True).order_by('-codmes').distinct()
    meses_costo_list= []
    for i in meses_costo:
      meses_costo_list.append(i)

    costo_mensual_totaltdc = CosteRiesgo.objects.values('codmes','m6_t','m9_t','m12_t','m6_c','m9_c','m12_c','m6_u','m9_u','m12_u').filter(producto='Tarjeta')
    tm6t_dict={};tm9t_dict={};tm12t_dict={};mm6t_dict={};
    tm6c_dict={};tm9c_dict={};tm12c_dict={};mm6c_dict={};
    tm6u_dict={};tm9u_dict={};tm12u_dict={};mm6u_dict={};
    for i in costo_mensual_totaltdc:
      for j in meses_costo:
        if i['codmes']<=meses_costo_list[6]:
          tm6t_dict[i['codmes']]=i['m6_t']*100
          tm6c_dict[i['codmes']]=i['m6_c']*100
          tm6u_dict[i['codmes']]=i['m6_u']*100
        else:
          tm6t_dict[i['codmes']]=[]
          tm6c_dict[i['codmes']]=[]
          tm6u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[9]:
          tm9t_dict[i['codmes']]=i['m9_t']*100
          tm9c_dict[i['codmes']]=i['m9_c']*100
          tm9u_dict[i['codmes']]=i['m9_u']*100
        else:
          tm9t_dict[i['codmes']]=[]
          tm9c_dict[i['codmes']]=[]
          tm9u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[12]:
          tm12t_dict[i['codmes']]=i['m12_t']*100
          tm12c_dict[i['codmes']]=i['m12_c']*100
          tm12u_dict[i['codmes']]=i['m12_u']*100
        else:
          tm12t_dict[i['codmes']]=[]
          tm12c_dict[i['codmes']]=[]
          tm12u_dict[i['codmes']]=[]

    if filtro1 == 'trimestre_form':
      for i in meses:
        mm6t_dict[i]=[]
        mm6c_dict[i]=[]
        mm6u_dict[i]=[]
    else:
      len_meses = len(meses_costo_list)-1
      for i in meses:
        if i >= meses_costo_list[len_meses] and i <= meses_costo_list[0]:
          mm6t_dict[i]=tm6t_dict[i]
          mm6c_dict[i]=tm6c_dict[i]
          mm6u_dict[i]=tm6u_dict[i]
        else:
          mm6t_dict[i]=[]
          mm6c_dict[i]=[]
          mm6u_dict[i]=[]


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_tdc.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_tdcter(request, filtro1='mes_vigencia', filtro2='2012', filtro3='form'):
    filtro1 = str(filtro1)
    filtro2 = str(filtro2)
    filtro3 = str(filtro3)

    tiempo = SeguimientoTer.objects.values_list('periodo', flat=True).order_by('periodo').distinct()

    if filtro3 == 'form':
      tipo_form = 1
    else:
      tipo_form = 0

    if filtro1 == 'trimestre_form':
        meses = SeguimientoTer.objects.values_list(filtro1, flat=true).filter(periodo__gte=filtro2).exclude(trimestre_form__in=['']).order_by(filtro1).distinct()
        trimestre = 1
    else:
        meses = SeguimientoTer.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).order_by(filtro1).distinct()
        trimestre = 0

    total_form = SeguimientoTer.objects.values(filtro1, 'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3),cuentas=Sum('ctas')).order_by(filtro1)
    total_form_dict = {}; total_ctas_dict = {};
    for j in total_form:
        total_form_dict[j[filtro1]]=j['formalizado']
        total_ctas_dict[j[filtro1]]=j['cuentas']

    if filtro1 == 'trimestre_form':
        meses_fast = SeguimientoTer.objects.values('trimestre_form').filter(trimestre_form__gte='2014-4').order_by('-trimestre_form').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1
    else:
        meses_fast = SeguimientoTer.objects.values('mes_vigencia').filter(mes_vigencia__gte='201410').order_by('-mes_vigencia').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1

    uno_a_uno = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_fast = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_regular = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    formUno_dict = {}; formFast_dict = {}; formRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                formUno_dict[i] = j['formalizado']
                break
            else:
                formUno_dict[i] = 0
        for j in camp_fast:
            if i == j[filtro1]:
                formFast_dict[i] = j['formalizado']
                break
            else:
                formFast_dict[i] = 0
        for j in camp_regular:
            if i == j[filtro1]:
                formRegular_dict[i] = j['formalizado']
                break
            else:
                formRegular_dict[i] = 0

    uno_a_uno = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_fast = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_regular = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    ticketUno_dict = {}; ticketFast_dict = {}; ticketRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                ticketUno_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketUno_dict[i] = []
        for j in camp_fast:
            if i == j[filtro1]:
                if i >= meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = j['facturacion']*1000000/j['formalizado']
                elif i < meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = []
                break
            else:
                ticketFast_dict[i] = []
        for j in camp_regular:
            if i == j[filtro1]:
                ticketRegular_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketRegular_dict[i] = []

    if filtro1 == 'trimestre_form':
        meses_moras = SeguimientoTer.objects.values('trimestre_form').order_by('-trimestre_form').distinct()
        mora_mes = SeguimientoTer.objects.values('trimestre_form').filter(trimestre_form__gte='2015-2', periodo__gte=filtro2).order_by('-trimestre_form').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 1
        num_mora6 = 2
        num_mora9 = 3
        num_mora12 = 4
        num_mora18 = 6 
        num_mora24 = 8 
        num_mora36 = 12 
    else:
        meses_moras = SeguimientoTer.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
        mora_mes = SeguimientoTer.objects.values('mes_vigencia').filter(mes_vigencia__gte='201504', periodo__gte=filtro2).order_by('-mes_vigencia').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 4 
        num_mora6 = 6 
        num_mora9 = 9 
        num_mora12 = 12 
        num_mora18 = 18 
        num_mora24 = 24 
        num_mora36 = 36 

    morames_list = []
    for i in meses_moras:
        morames_list.append(i[filtro1])
    
    mora460 = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
    mora6 = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
    mora9 = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
    mora12 = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    mora18 = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora18'),cuentas=Sum('ctas')).order_by(filtro1)
    mora24 = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora24'),cuentas=Sum('ctas')).order_by(filtro1)
    mora36 = SeguimientoTer.objects.values(filtro1).filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora36'),cuentas=Sum('ctas')).order_by(filtro1)
    mora460_dict = {}; mora6_dict = {}; mora9_dict = {}; mora12_dict = {};
    mora18_dict = {}; mora24_dict = {}; mora36_dict = {};
    for j in mora460:
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora460:
        if j[filtro1] <= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=[]
    for j in mora6:
        if j[filtro1] <= morames_list[num_mora6]:
            mora6_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora9:
        if j[filtro1] <= morames_list[num_mora9]:
            mora9_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora12:
        if j[filtro1] <= morames_list[num_mora12]:
            mora12_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora18:
        if j[filtro1] <= morames_list[num_mora18]:
            mora18_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora24:
        if j[filtro1] <= morames_list[num_mora24]:
            mora24_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora36:
        if j[filtro1] <= morames_list[num_mora36]:
            mora36_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']

    rangos = SeguimientoTer.objects.values(filtro1, 'rng_ing').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(num_rango=Sum(filtro3)).order_by(filtro1)
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
      for j in rangos:
        if i == j[filtro1]:
          if j['rng_ing'] == '01 [3.5K - ...]':
            rango1_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '02 [2.5K - 3.5K]':
            rango2_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '03 [2K - 2.5K]':
            rango3_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '04 [1.5K - 2K]':
            rango4_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '05 [1K - 1.5K]':
            rango5_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '06 [0 - 1K]':
            rango6_dict[i]=j['num_rango']*100/total_form_dict[i]

    formxcampxuno = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_form_dict = {}; uno_form_dict = {};
    for i in meses:
        for j in formxcampxuno:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                camp_form_dict[i] = j['formalizado']
                break
            else:
                camp_form_dict[i] = 0
        for j in formxcampxuno:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_form_dict[i] = j['formalizado']
                break
            else:
                uno_form_dict[i] = 0

    seg_ava = SeguimientoTer.objects.values(filtro1).filter(riesgos='CAMP', producto='03 Tarjeta', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ms = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_noph = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_nocli = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ava_dict = {}; seg_ms_dict = {}; seg_noph_dict = {}; seg_nocli_dict = {};
    useg_ms_dict = {}; useg_noph_dict = {}; useg_nocli_dict = {};
    for i in meses:
        for j in seg_ava:
            if i == j[filtro1]:
                seg_ava_dict[i] = j['seg']
                break
            else:
                seg_ava_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_ms_dict[i] = j['seg']
                break
            else:
                seg_ms_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_ms_dict[i] = j['seg']
                break
            else:
                useg_ms_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_noph_dict[i] = j['seg']
                break
            else:
                seg_noph_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_noph_dict[i] = j['seg']
                break
            else:
                useg_noph_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_nocli_dict[i] = j['seg']
                break
            else:
                seg_nocli_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_nocli_dict[i] = j['seg']
                break
            else:
                useg_nocli_dict[i] = 0

    total_ctasxmorasxcampxuno = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12'),sum_mora18=Sum('mora18'), sum_mora24=Sum('mora24'), sum_mora36=Sum('mora36')).order_by(filtro1)
    total_ctasxcamp_dict = {}; mora460_camp_dict = {}; mora6_camp_dict = {}; mora9_camp_dict = {}; mora12_camp_dict = {}; mora18_camp_dict = {}; mora24_camp_dict = {}; mora36_camp_dict = {};
    mora460_uno_dict = {}; mora6_uno_dict = {}; mora9_uno_dict = {}; mora12_uno_dict = {}; mora18_uno_dict = {}; mora24_uno_dict = {}; mora36_uno_dict = {};
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_camp_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_camp_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_camp_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_camp_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_camp_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_camp_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_uno_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_uno_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_uno_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_uno_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_uno_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_uno_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']


    moras = SeguimientoTer.objects.values(filtro1, 'segmento', 'riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO 6 MESES - SEGMENTOS
    ava_mora460_dict = {}; ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora460_dict = {}; ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora460_dict = {}; noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora460_dict = {}; nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    #INCUMPLIMIENTO 6 MESES SEGMENTO - UNO A UNO
    dict_moraunoms = {}; dict_moraunonoph = {}; dict_moraunonocli = {};
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['segmento']=='1.AVA':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ava_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ava_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ava_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ava_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ava_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']     
              elif  j['segmento']=='2.MS':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ms_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ms_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ms_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ms_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ms_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      noph_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      noph_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      noph_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      noph_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      noph_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      nocli_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      nocli_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      nocli_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      nocli_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      nocli_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['segmento']=='2.MS':
                if i <= morames_list[num_mora6]:
                      dict_moraunoms[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora6]:
                      dict_moraunonoph[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora6]:
                    if j['sum_ctas'] == 0:
                      dict_moraunonocli[i]=[]
                    else:
                      dict_moraunonocli[i]=j['sum_mora6']*100/j['sum_ctas']

    depen = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum(filtro3)).order_by(filtro1)
    indep = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    pnn = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    no_recon = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='03 Tarjeta', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    depen_dict = {}; indep_dict = {}; pnn_dict = {}; no_recon_dict = {}; totxcamp_laboral = {};
    udepen_dict = {}; uindep_dict = {}; upnn_dict = {}; uno_recon_dict = {};
    for i in meses:
        for j in depen:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                depen_dict[i] = j['seg']
                break
            else:
                depen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                indep_dict[i] = j['seg']
                break
            else:
                indep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                pnn_dict[i] = j['seg']
                break
            else:
                pnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                no_recon_dict[i] = j['seg']
                break
            else:
                no_recon_dict[i] = 0
        for j in depen:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                udepen_dict[i] = j['seg']
                break
            else:
                udepen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uindep_dict[i] = j['seg']
                break
            else:
                uindep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                upnn_dict[i] = j['seg']
                break
            else:
                upnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_recon_dict[i] = j['seg']
                break
            else:
                uno_recon_dict[i] = 0

    morascat = SeguimientoTer.objects.values(filtro1, 'cat_persona','riesgos').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO RELACION LABORAL CAMPANAS
    dep_mora460_dict = {}; dep_mora6_dict = {}; dep_mora9_dict = {}; dep_mora12_dict = {}
    indep_mora460_dict = {}; indep_mora6_dict = {}; indep_mora9_dict = {}; indep_mora12_dict = {}
    pnn_mora460_dict = {}; pnn_mora6_dict = {}; pnn_mora9_dict = {}; pnn_mora12_dict = {}
    norec_mora460_dict = {}; norec_mora6_dict = {}; norec_mora9_dict = {}; norec_mora12_dict = {}
    #INCUMPLMIENTO 6 MESES RELACION LABORAL - UNO A UNO
    dict_moracamdep = {}; dict_moracamind = {}; 
    dict_moracampnn = {}; dict_moracamnor = {};
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['cat_persona']=='1. Dependiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      dep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      dep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      dep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      dep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      dep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']    
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      indep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      indep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      indep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      indep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      indep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      pnn_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      pnn_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      pnn_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      pnn_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      pnn_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      norec_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      norec_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      norec_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      norec_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      norec_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['cat_persona']=='1. Dependiente':
                if i <= morames_list[num_mora6]:
                      dict_moracamdep[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora6]:
                      dict_moracamind[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora6]:
                    if j['sum_ctas']==0:
                      dict_moracampnn[i]=[]
                    else:
                      dict_moracampnn[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora6]:
                      dict_moracamnor[i]=j['sum_mora6']*100/j['sum_ctas']

    buroxform = SeguimientoTer.objects.values(filtro1, 'buro_camp').filter(digital='',riesgos='CAMP', producto='03 Tarjeta', periodo__gte=filtro2).annotate(seg=Sum(filtro3),cuentas=Sum('ctas'),sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_burog1 = {}; dict_burog5 = {};
    dict_burog6 = {}; dict_buronb = {};
    for i in meses:
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G1-G4':
                dict_burog1[i] = j['seg']
                break
              else:
                dict_burog1[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G5':
                dict_burog5[i] = j['seg']
                break
              else:
                dict_burog5[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G6-G8':
                dict_burog6[i] = j['seg']
                break
              else:
                dict_burog6[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'NB':
                dict_buronb[i] = j['seg']
                break
              else:
                dict_buronb[i] = 0

    dict_mora6buro1 = {}; dict_mora6buro2 = {}; 
    dict_mora6buro3 = {}; dict_mora6buro4 = {};
    for i in buroxform:
        if i['buro_camp'] == 'G1-G4':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro1[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G5':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro2[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G6-G8':
            if i[filtro1] <= morames_list[num_mora6]:
              if i['cuentas']==0:
                dict_mora6buro3[i[filtro1]] = []
              else:
                dict_mora6buro3[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'NB':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro4[i[filtro1]] = i['sum_mora6']*100/i['cuentas']

    total_forzaje = Forzaje.objects.values(filtro1).filter(producto='03 Tarjeta').annotate(cantidad=Sum('form')).order_by(filtro1)
    forzaje_dict = {}
    for i in meses:
     for j in total_forzaje:
         if i == j[filtro1]:
          forzaje_dict[j[filtro1]]=j['cantidad']

    forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '03 Tarjeta').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    duda_dict = {}; rechazo_dict = {};
    for i in meses:
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='DU':
                    duda_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                duda_dict[i]= 0
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='RE':
                    rechazo_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                rechazo_dict[i]= 0

    form_cluster = SeguimientoTer.objects.values(filtro1, 'cluster').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum(filtro3)).order_by(filtro1)
    form_modes_dict = {}; form_desli_dict = {}; form_progre_dict = {};
    form_aspi_dict = {}; form_prospe_dict = {}; form_sd_dict = {};
    for i in meses:
        for j in form_cluster:
            if i == j[filtro1]:
              if j['cluster'] == '1. Modestos':
                form_modes_dict[i] = j['formalizados']
              elif j['cluster'] == '2. Desligados':
                form_desli_dict[i] = j['formalizados']
              elif j['cluster'] == '3. Progresistas':
                form_progre_dict[i] = j['formalizados']
              elif j['cluster'] == '4. Aspirantes':
                form_aspi_dict[i] = j['formalizados']
              elif j['cluster'] == '5. Prosperos':
                form_prospe_dict[i] = j['formalizados']
              elif j['cluster'] == '0. S.D.':
                form_sd_dict[i] = j['formalizados']

    form_clusterxmora = SeguimientoTer.objects.values(filtro1, 'cluster').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    modes_mora6_dict = {}; desli_mora6_dict = {}; 
    progre_mora460_dict = {}; progre_mora6_dict = {}; progre_mora9_dict = {}; progre_mora12_dict = {}
    aspi_mora460_dict = {}; aspi_mora6_dict = {}; aspi_mora9_dict = {}; aspi_mora12_dict = {}
    prospe_mora460_dict = {}; prospe_mora6_dict = {}; prospe_mora9_dict = {}; prospe_mora12_dict = {}
    for i in meses:
       for j in form_clusterxmora:
          if i == j[filtro1]:
            if  j['cluster']=='1. Modestos':
                if i <= morames_list[num_mora6]:
                    modes_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='2. Desligados':
                if i <= morames_list[num_mora6]:
                    desli_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='3. Progresistas':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    progre_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    progre_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    progre_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    progre_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    progre_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='4. Aspirantes':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    aspi_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    aspi_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    aspi_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    aspi_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    aspi_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='5. Prosperos':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    prospe_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    prospe_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    prospe_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    prospe_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    prospe_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']

    meses_costo = CosteRiesgo.objects.values_list('codmes', flat=True).order_by('-codmes').distinct()
    meses_costo_list= []
    for i in meses_costo:
      meses_costo_list.append(i)

    costo_mensual_totaltdc = CosteRiesgo.objects.values('codmes','m6_t','m9_t','m12_t','m6_c','m9_c','m12_c','m6_u','m9_u','m12_u').filter(producto='Tarjeta')
    tm6t_dict={};tm9t_dict={};tm12t_dict={};mm6t_dict={};
    tm6c_dict={};tm9c_dict={};tm12c_dict={};mm6c_dict={};
    tm6u_dict={};tm9u_dict={};tm12u_dict={};mm6u_dict={};
    for i in costo_mensual_totaltdc:
      for j in meses_costo:
        if i['codmes']<=meses_costo_list[6]:
          tm6t_dict[i['codmes']]=i['m6_t']*100
          tm6c_dict[i['codmes']]=i['m6_c']*100
          tm6u_dict[i['codmes']]=i['m6_u']*100
        else:
          tm6t_dict[i['codmes']]=[]
          tm6c_dict[i['codmes']]=[]
          tm6u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[9]:
          tm9t_dict[i['codmes']]=i['m9_t']*100
          tm9c_dict[i['codmes']]=i['m9_c']*100
          tm9u_dict[i['codmes']]=i['m9_u']*100
        else:
          tm9t_dict[i['codmes']]=[]
          tm9c_dict[i['codmes']]=[]
          tm9u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[12]:
          tm12t_dict[i['codmes']]=i['m12_t']*100
          tm12c_dict[i['codmes']]=i['m12_c']*100
          tm12u_dict[i['codmes']]=i['m12_u']*100
        else:
          tm12t_dict[i['codmes']]=[]
          tm12c_dict[i['codmes']]=[]
          tm12u_dict[i['codmes']]=[]

    if filtro1 == 'trimestre_form':
      for i in meses:
        mm6t_dict[i]=[]
        mm6c_dict[i]=[]
        mm6u_dict[i]=[]
    else:
      len_meses = len(meses_costo_list)-1
      for i in meses:
        if i >= meses_costo_list[len_meses] and i <= meses_costo_list[0]:
          mm6t_dict[i]=tm6t_dict[i]
          mm6c_dict[i]=tm6c_dict[i]
          mm6u_dict[i]=tm6u_dict[i]
        else:
          mm6t_dict[i]=[]
          mm6c_dict[i]=[]
          mm6u_dict[i]=[]


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_tdcter.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def seguimiento_tarjeta(request, filtro1='mes_vigencia', filtro2='2011'):
    filtro1 = str(filtro1)
    filtro2 = str(filtro2)
    side_tarjeta = 1

    tiempo = Seguimiento1.objects.values('periodo').order_by('periodo').distinct('periodo')
    time_list = []
    for i in tiempo:
        time_list.append(i['periodo'])

    if filtro1 == 'trimestre_form':
        meses = Seguimiento1.objects.values(filtro1).filter(periodo__gte=filtro2).order_by(filtro1).distinct(filtro1)
        trimestre = 1
    else:
        meses = Seguimiento1.objects.values(filtro1).filter(periodo__gte=filtro2).order_by(filtro1).distinct(filtro1)
        trimestre = 0
    meses_list = []
    for i in meses:
        meses_list.append(i[filtro1])

    if filtro1 == 'trimestre_form':
        total_form = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizado=Sum('form'),cuentas=Sum('ctas')).order_by(filtro1)
    else:
        total_form = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizado=Sum('form'),cuentas=Sum('ctas')).order_by(filtro1)
    total_form_dict = {}; total_ctas_dict = {};
    for j in total_form:
	   total_form_dict[j[filtro1]]=j['formalizado']
    for j in total_form:
       total_ctas_dict[j[filtro1]]=j['cuentas']

    if filtro1 == 'trimestre_form':
        uno_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_fast = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='03 Tarjeta', origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_uno = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='03 Tarjeta', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    else:
        uno_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_fast = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='03 Tarjeta', origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_uno = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='03 Tarjeta', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    uno_form_dict = {}; camp_fast_dict = {}; camp_uno_dict = {};
    for i in meses:
        for j in uno_form:
            if i[filtro1] == j[filtro1]:
                uno_form_dict[i[filtro1]] = j['formalizado']
                break
            else:
                uno_form_dict[i[filtro1]] = 0
        for j in camp_fast:
            if i[filtro1] == j[filtro1]:
                camp_fast_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_fast_dict[i[filtro1]] = 0
        for j in camp_uno:
            if i[filtro1] == j[filtro1]:
                camp_uno_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_uno_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        camp_formf = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_formu = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    else:
        camp_formf = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_formu = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    camp_formf_dict = {}; camp_formu_dict = {};
    for i in meses:
        for j in camp_formf:
            if i[filtro1] == j[filtro1]:
                camp_formf_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_formf_dict[i[filtro1]] = 0
        for j in camp_formu:
            if i[filtro1] == j[filtro1]:
                camp_formu_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_formu_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        meses_fast = Seguimiento1.objects.values('trimestre_form').filter(trimestre_form__gte='2014-4').order_by('-trimestre_form').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1
    else:
        meses_fast = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte='201410').order_by('-mes_vigencia').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1

    if filtro1 == 'trimestre_form':
        fact_uno = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='03 Tarjeta', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campf = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='03 Tarjeta', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campu = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='03 Tarjeta', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
    else:
        fact_uno = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='03 Tarjeta', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campf = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='03 Tarjeta', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campu = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='03 Tarjeta', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
    fact_uno_dict = {}; fact_campf_dict = {}; fact_campu_dict = {};
    for i in meses:
        for j in fact_uno:
            if i[filtro1] == j[filtro1]:
                fact_uno_dict[i[filtro1]] = j['facturacion']*1000000/uno_form_dict[i[filtro1]]
                break
            else:
                fact_uno_dict[i[filtro1]] = 0
        for j in fact_campu:
            if i[filtro1] == j[filtro1]:
                fact_campu_dict[i[filtro1]] = j['facturacion']*1000000/camp_formu_dict[i[filtro1]]
                break
            else:
                fact_campu_dict[i[filtro1]] = 0
        for j in fact_campf:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] >= meses_fast_list[num_meses_fast] and i[filtro1] <= meses_fast_list[0]:
                    fact_campf_dict[i[filtro1]] = j['facturacion']*1000000/camp_formf_dict[i[filtro1]]
                    break
        for j in fact_campf:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] < meses_fast_list[num_meses_fast]:
                    fact_campf_dict[i[filtro1]] = 0
                    break
        for j in fact_campf:
            if i[filtro1] < meses_fast_list[num_meses_fast]:
                fact_campf_dict[i[filtro1]] = 0
                break

    if filtro1 == 'trimestre_form':
        camp_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    else:
        camp_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    camp_form_dict = {};
    for i in meses:
        for j in camp_form:
            if i[filtro1] == j[filtro1]:
                camp_form_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_form_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        seg_ava = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        seg_ava = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    seg_ava_dict = {}; seg_ms_dict = {}; seg_noph_dict = {}; seg_nocli_dict = {};
    for i in meses:
        for j in seg_ava:
            if i[filtro1] == j[filtro1]:
                seg_ava_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_ava_dict[i[filtro1]] = 0
        for j in seg_ms:
            if i[filtro1] == j[filtro1]:
                seg_ms_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_ms_dict[i[filtro1]] = 0
        for j in seg_noph:
            if i[filtro1] == j[filtro1]:
                seg_noph_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_noph_dict[i[filtro1]] = 0
        for j in seg_nocli:
            if i[filtro1] == j[filtro1]:
                seg_nocli_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_nocli_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        useg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        useg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    useg_ms_dict = {}; useg_noph_dict = {}; useg_nocli_dict = {};
    for i in meses:
        for j in useg_ms:
            if i[filtro1] == j[filtro1]:
                useg_ms_dict[i[filtro1]] = j['seg']
                break
            else:
                useg_ms_dict[i[filtro1]] = 0
        for j in useg_noph:
            if i[filtro1] == j[filtro1]:
                useg_noph_dict[i[filtro1]] = j['seg']
                break
            else:
                useg_noph_dict[i[filtro1]] = 0
        for j in useg_nocli:
            if i[filtro1] == j[filtro1]:
                useg_nocli_dict[i[filtro1]] = j['seg']
                break
            else:
                useg_nocli_dict[i[filtro1]] = 0 

    if filtro1 == 'trimestre_form':
        depen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        indep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        pnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        no_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        depen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        indep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        pnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        no_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    depen_dict = {}; indep_dict = {}; pnn_dict = {}; no_recon_dict = {};
    for i in meses:
        for j in depen:
            if i[filtro1] == j[filtro1]:
                depen_dict[i[filtro1]] = j['seg']
                break
            else:
                depen_dict[i[filtro1]] = 0
        for j in indep:
            if i[filtro1] == j[filtro1]:
                indep_dict[i[filtro1]] = j['seg']
                break
            else:
                indep_dict[i[filtro1]] = 0
        for j in pnn:
            if i[filtro1] == j[filtro1]:
                pnn_dict[i[filtro1]] = j['seg']
                break
            else:
                pnn_dict[i[filtro1]] = 0
        for j in no_recon:
            if i[filtro1] == j[filtro1]:
                no_recon_dict[i[filtro1]] = j['seg']
                break
            else:
                no_recon_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        udepen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        uindep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        upnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        uno_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        udepen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        uindep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        upnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        uno_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='03 Tarjeta', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    udepen_dict = {}; uindep_dict = {}; upnn_dict = {}; uno_recon_dict = {};
    for i in meses:
        for j in udepen:
            if i[filtro1] == j[filtro1]:
                udepen_dict[i[filtro1]] = j['seg']
                break
            else:
                udepen_dict[i[filtro1]] = 0
        for j in uindep:
            if i[filtro1] == j[filtro1]:
                uindep_dict[i[filtro1]] = j['seg']
                break
            else:
                uindep_dict[i[filtro1]] = 0
        for j in upnn:
            if i[filtro1] == j[filtro1]:
                upnn_dict[i[filtro1]] = j['seg']
                break
            else:
                upnn_dict[i[filtro1]] = 0
        for j in uno_recon:
            if i[filtro1] == j[filtro1]:
                uno_recon_dict[i[filtro1]] = j['seg']
                break
            else:
                uno_recon_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        rangos = Seguimiento1.objects.values(filtro1,'producto', 'rng_ing').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(num_rango=Sum('form')).order_by(filtro1)
    else:
        rangos = Seguimiento1.objects.values(filtro1,'producto', 'rng_ing').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(num_rango=Sum('form')).order_by(filtro1)
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
	   for j in rangos:
	     if i[filtro1] == j[filtro1]:
		    if j['rng_ing'] == '01 [3.5K - ...]':
		      rango1_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
		    elif j['rng_ing'] == '02 [2.5K - 3.5K]':
		      rango2_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
		    elif j['rng_ing'] == '03 [2K - 2.5K]':
		      rango3_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
		    elif j['rng_ing'] == '04 [1.5K - 2K]':
		      rango4_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
		    elif j['rng_ing'] == '05 [1K - 1.5K]':
		      rango5_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
		    elif j['rng_ing'] == '06 [0 - 1K]':
		      rango6_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]


    if filtro1 == 'trimestre_form':
        meses_moras = Seguimiento1.objects.values('trimestre_form').order_by('-trimestre_form').distinct()
        mora_mes = Seguimiento1.objects.values('trimestre_form').filter(trimestre_form__gte='2015-2', periodo__gte=filtro2).order_by('-trimestre_form').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 1
        num_mora6 = 2
        num_mora9 = 3
        num_mora12 = 4
    else:
        meses_moras = Seguimiento1.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
        mora_mes = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte='201504', periodo__gte=filtro2).order_by('-mes_vigencia').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 4 #4
        num_mora6 = 6 #6
        num_mora9 = 9 #9
        num_mora12 = 12 #12

    morames_list = []
    for i in meses_moras:
        morames_list.append(i[filtro1])

    if filtro1 == 'trimestre_form':
        mora460 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
        mora6 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
        mora9 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
        mora12 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    else:
        mora460 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
        mora6 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
        mora9 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
        mora12 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    mora460_dict = {}; mora6_dict = {}; mora9_dict = {}; mora12_dict = {};
    for j in mora460:
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora460:
        if j[filtro1] <= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=[]
    for j in mora6:
        if j[filtro1] <= morames_list[num_mora6]:
            mora6_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora9:
        if j[filtro1] <= morames_list[num_mora9]:
            mora9_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora12:
        if j[filtro1] <= morames_list[num_mora12]:
            mora12_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']

    if filtro1 == 'trimestre_form':
        total_moraxcamp = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    else:
        total_moraxcamp = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    total_moraxcamp_dict = {}
    for i in meses_moras:
        for j in total_moraxcamp:
            if i[filtro1] == j[filtro1]:
               total_moraxcamp_dict[i[filtro1]]=j['sum_ctas']

    if filtro1 == 'trimestre_form':
        mora_camp = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        mora_camp = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    mora460_camp_dict = {}; mora6_camp_dict = {}; mora9_camp_dict = {}; mora12_camp_dict = {};
    for i in meses_moras:
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    mora460_camp_dict[i[filtro1]]=j['sum_mora460']*100/total_moraxcamp_dict[i[filtro1]]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_lista]:
                    mora460_camp_dict[i[filtro1]]=[]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora6]:
                    mora6_camp_dict[i[filtro1]]=j['sum_mora6']*100/total_moraxcamp_dict[i[filtro1]]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora9]:
                    mora9_camp_dict[i[filtro1]]=j['sum_mora9']*100/total_moraxcamp_dict[i[filtro1]]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora12]:
                    mora12_camp_dict[i[filtro1]]=j['sum_mora12']*100/total_moraxcamp_dict[i[filtro1]]
                    break

    if filtro1 == 'trimestre_form':
        total_moraxuno = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    else:
        total_moraxuno = Seguimiento1.objects.values(filtro1,'producto').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    total_moraxuno_dict = {}
    for i in meses:
        for j in total_moraxuno:
            if i[filtro1] == j[filtro1]:
               total_moraxuno_dict[i[filtro1]]=j['sum_ctas']

    if filtro1 == 'trimestre_form':
        mora_uno = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        mora_uno = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    mora460_uno_dict = {}; mora6_uno_dict = {}; mora9_uno_dict = {}; mora12_uno_dict = {};
    for i in meses_moras:
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    mora460_uno_dict[i[filtro1]]=j['sum_mora460']*100/total_moraxuno_dict[i[filtro1]]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_lista]:
                    mora460_uno_dict[i[filtro1]]=[]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora6]:
                    mora6_uno_dict[i[filtro1]]=j['sum_mora6']*100/total_moraxuno_dict[i[filtro1]]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora9]:
                    mora9_uno_dict[i[filtro1]]=j['sum_mora9']*100/total_moraxuno_dict[i[filtro1]]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora12]:
                    mora12_uno_dict[i[filtro1]]=j['sum_mora12']*100/total_moraxuno_dict[i[filtro1]]
                    break

    if filtro1 == 'trimestre_form':
        total_morasxseg = Seguimiento1.objects.values(filtro1,'producto', 'segmento').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    else:
        total_morasxseg = Seguimiento1.objects.values(filtro1,'producto', 'segmento').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    totalxava_moras_dict = {}
    totalxms_moras_dict = {}
    totalxnoph_moras_dict = {}
    totalxnocli_moras_dict = {}
    for i in meses:
        for j in total_morasxseg:
            if i[filtro1] == j[filtro1]:
                if j['segmento']=='1.AVA':
                    totalxava_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['segmento']=='2.MS':
                    totalxms_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['segmento']=='3.NoPH':
                    totalxnoph_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['segmento']=='4.NoCli':
                    totalxnocli_moras_dict[i[filtro1]]=j['sum_mora']

    if filtro1 == 'trimestre_form':
        moras = Seguimiento1.objects.values(filtro1, 'segmento', 'producto').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        moras = Seguimiento1.objects.values(filtro1, 'segmento', 'producto').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    ava_mora460_dict = {}; ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora460_dict = {}; ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora460_dict = {}; noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora460_dict = {}; nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    for i in meses:
       for j in moras:
          if i[filtro1] == j[filtro1]:
            if  j['segmento']=='1.AVA':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    ava_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxava_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    ava_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    ava_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxava_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    ava_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxava_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    ava_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxava_moras_dict[i[filtro1]]     
            elif  j['segmento']=='2.MS':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    ms_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxms_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    ms_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    ms_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxms_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    ms_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxms_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    ms_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxms_moras_dict[i[filtro1]]
            elif  j['segmento']=='3.NoPH':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    noph_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxnoph_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    noph_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    noph_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxnoph_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    noph_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxnoph_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    noph_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxnoph_moras_dict[i[filtro1]]
            elif  j['segmento']=='4.NoCli':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    nocli_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxnocli_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    nocli_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    nocli_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxnocli_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    nocli_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxnocli_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    nocli_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxnocli_moras_dict[i[filtro1]]

    if filtro1 == 'trimestre_form':
        moratot = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    else:
        moratot = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    dict_moratotms = {}; dict_moratotnoph = {}; dict_moratotnocl = {};
    for i in moratot:
        if i['segmento'] == '2.MS':
            dict_moratotms[i[filtro1]] = i['cuentas']
        if i['segmento'] == '3.NoPH':
            dict_moratotnoph[i[filtro1]] = i['cuentas']
        if i['segmento'] == '4.NoCli':
            dict_moratotnocl[i[filtro1]] = i['cuentas']

    if filtro1 == 'trimestre_form':
        morauno_seg = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    else:
        morauno_seg = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_moraunoms = {}; dict_moraunonoph = {}; dict_moraunonocli = {};
    for i in morauno_seg:
        if i[filtro1] <= morames_list[num_mora6]:
            if i['segmento'] == '2.MS':
                dict_moraunoms[i[filtro1]] = i['sum_mora6']*100/dict_moratotms[i[filtro1]]
    for i in morauno_seg:
        if i[filtro1] <= morames_list[num_mora6]:  
            if i['segmento'] == '3.NoPH':
                dict_moraunonoph[i[filtro1]] = i['sum_mora6']*100/dict_moratotnoph[i[filtro1]]
    for i in morauno_seg:
        if i[filtro1] <= morames_list[num_mora6]:
            if i['segmento'] == '4.NoCli':
                dict_moraunonocli[i[filtro1]] = i['sum_mora6']*100/dict_moratotnocl[i[filtro1]]

    if filtro1 == 'trimestre_form':
        total_morasxcat = Seguimiento1.objects.values(filtro1, 'producto', 'cat_persona').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    else:
        total_morasxcat = Seguimiento1.objects.values(filtro1, 'producto', 'cat_persona').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    totalxdep_moras_dict = {}
    totalxind_moras_dict = {}
    totalxpnn_moras_dict = {}
    totalxnorec_moras_dict = {}
    for i in meses:
        for j in total_morasxcat:
            if i[filtro1] == j[filtro1]:
                if j['cat_persona']=='1. Dependiente':
                    totalxdep_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cat_persona']=='2. Independiente':
                    totalxind_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cat_persona']=='3. PNN':
                    totalxpnn_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cat_persona']=='4.No Reconocido':
                    totalxnorec_moras_dict[i[filtro1]]=j['sum_mora']

    if filtro1 == 'trimestre_form':
        morascat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        morascat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto').filter(producto='03 Tarjeta', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    dep_mora460_dict = {}; dep_mora6_dict = {}; dep_mora9_dict = {}; dep_mora12_dict = {}
    indep_mora460_dict = {}; indep_mora6_dict = {}; indep_mora9_dict = {}; indep_mora12_dict = {}
    pnn_mora460_dict = {}; pnn_mora6_dict = {}; pnn_mora9_dict = {}; pnn_mora12_dict = {}
    norec_mora460_dict = {}; norec_mora6_dict = {}; norec_mora9_dict = {}; norec_mora12_dict = {}
    for i in meses:
       for j in morascat:
          if i[filtro1] == j[filtro1]:
            if  j['cat_persona']=='1. Dependiente':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    dep_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxdep_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    dep_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    dep_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxdep_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    dep_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxdep_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    dep_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxdep_moras_dict[i[filtro1]]     
            elif  j['cat_persona']=='2. Independiente':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    indep_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxind_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    indep_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    indep_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxind_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    indep_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxind_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    indep_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxind_moras_dict[i[filtro1]]
            elif  j['cat_persona']=='3. PNN':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    pnn_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxpnn_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    pnn_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    pnn_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxpnn_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    pnn_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxpnn_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    pnn_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxpnn_moras_dict[i[filtro1]]
            elif  j['cat_persona']=='4.No Reconocido':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    norec_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxnorec_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    norec_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    norec_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxnorec_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    norec_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxnorec_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    norec_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxnorec_moras_dict[i[filtro1]]

    if filtro1 == 'trimestre_form':
        total_morascluster = Seguimiento1.objects.values(filtro1, 'producto', 'cluster').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    else:
        total_morascluster = Seguimiento1.objects.values(filtro1, 'producto', 'cluster').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    totalxsd_moras_dict = {}
    totalxmode_moras_dict = {}
    totalxdesl_moras_dict = {}
    totalxprogre_moras_dict = {}
    totalxaspi_moras_dict = {}
    totalxprospe_moras_dict = {}
    for i in meses:
        for j in total_morascluster:
            if i[filtro1] == j[filtro1]:
                if j['cluster']=='0. S.D.':
                    totalxsd_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cluster']=='1. Modestos':
                    totalxmode_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cluster']=='2. Desligados':
                    totalxdesl_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cluster']=='3. Progresistas':
                    totalxprogre_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cluster']=='4. Aspirantes':
                    totalxaspi_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cluster']=='5. Prosperos':
                    totalxprospe_moras_dict[i[filtro1]]=j['sum_mora']

    if filtro1 == 'trimestre_form':
        morascluster = Seguimiento1.objects.values(filtro1, 'cluster', 'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        morascluster = Seguimiento1.objects.values(filtro1, 'cluster', 'producto').filter(producto='03 Tarjeta', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    sd_mora460_dict = {}; sd_mora6_dict = {}; sd_mora9_dict = {}; sd_mora12_dict = {}
    modes_mora460_dict = {}; modes_mora6_dict = {}; modes_mora9_dict = {}; modes_mora12_dict = {}
    desli_mora460_dict = {}; desli_mora6_dict = {}; desli_mora9_dict = {}; desli_mora12_dict = {}
    progre_mora460_dict = {}; progre_mora6_dict = {}; progre_mora9_dict = {}; progre_mora12_dict = {}
    aspi_mora460_dict = {}; aspi_mora6_dict = {}; aspi_mora9_dict = {}; aspi_mora12_dict = {}
    prospe_mora460_dict = {}; prospe_mora6_dict = {}; prospe_mora9_dict = {}; prospe_mora12_dict = {}
    for i in meses:
       for j in morascluster:
          if i[filtro1] == j[filtro1]:
            if  j['cluster']=='0. S.D.':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    sd_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxsd_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    sd_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    sd_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxsd_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    sd_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxsd_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    sd_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxsd_moras_dict[i[filtro1]]     
            elif  j['cluster']=='1. Modestos':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    modes_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxmode_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    modes_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    modes_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxmode_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    modes_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxmode_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    modes_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxmode_moras_dict[i[filtro1]]
            elif  j['cluster']=='2. Desligados':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    desli_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxdesl_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    desli_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    desli_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxdesl_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    desli_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxdesl_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    desli_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxdesl_moras_dict[i[filtro1]]
            elif  j['cluster']=='3. Progresistas':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    progre_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxprogre_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    progre_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    progre_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxprogre_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    progre_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxprogre_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    progre_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxprogre_moras_dict[i[filtro1]]
            elif  j['cluster']=='4. Aspirantes':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    aspi_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxaspi_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    aspi_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    aspi_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxaspi_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    aspi_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxaspi_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    aspi_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxaspi_moras_dict[i[filtro1]]
            elif  j['cluster']=='5. Prosperos':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    prospe_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxprospe_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    prospe_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    prospe_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxprospe_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    prospe_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxprospe_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    prospe_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxprospe_moras_dict[i[filtro1]]



    if filtro1 == 'trimestre_form':
        moratot2 = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto','riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    else:
        moratot2 = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto','riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    dict_moratotdep = {};
    dict_moratotind = {};
    dict_moratotnoph = {};
    dict_moratotnocl = {};
    for i in moratot2:
        if i['cat_persona'] == '1. Dependiente':
            dict_moratotdep[i[filtro1]] = i['cuentas']
        if i['cat_persona'] == '2. Independiente':
            dict_moratotind[i[filtro1]] = i['cuentas']
        if i['cat_persona'] == '3. PNN':
            dict_moratotnoph[i[filtro1]] = i['cuentas']
        if i['cat_persona'] == '4.No Reconocido':
            dict_moratotnocl[i[filtro1]] = i['cuentas']

    if filtro1 == 'trimestre_form':
        morauno_cat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    else:
        morauno_cat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_moracamdep = {}; dict_moracamind = {}; 
    dict_moracampnn = {}; dict_moracamnor = {};
    for i in morauno_cat:
        if i['cat_persona'] == '1. Dependiente':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracamdep[i[filtro1]] = i['sum_mora6']*100/dict_moratotdep[i[filtro1]]
        elif i['cat_persona'] == '2. Independiente':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracamind[i[filtro1]] = i['sum_mora6']*100/dict_moratotind[i[filtro1]]
        elif i['cat_persona'] == '3. PNN':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracampnn[i[filtro1]] = i['sum_mora6']*100/dict_moratotnoph[i[filtro1]]
        elif i['cat_persona'] == '4.No Reconocido':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracamnor[i[filtro1]] = i['sum_mora6']*100/dict_moratotnocl[i[filtro1]]

    if filtro1 == 'trimestre_form':
        moraburo = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    else:
        moraburo = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    dict_moraburo1 = {}; dict_moraburo2 = {};
    dict_moraburo3 = {}; dict_moraburo4 = {};
    for i in moraburo:
        if i['buro_camp'] == 'G1-G4':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo1[i[filtro1]] = i['cuentas']
        elif i['buro_camp'] == 'G5':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo2[i[filtro1]] = i['cuentas']
        elif i['buro_camp'] == 'G6-G8':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo3[i[filtro1]] = i['cuentas']
        elif i['buro_camp'] == 'NB':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo4[i[filtro1]] = i['cuentas']

    if filtro1 == 'trimestre_form':
        burog1 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='G1-G4', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog5 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='G5', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog6 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='G6-G8', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        buronb = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='NB', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burotot = Seguimiento1.objects.values(filtro1).filter(riesgos='CAMP', producto='03 Tarjeta').annotate(seg=Sum('form')).order_by(filtro1)
    else:
        burog1 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='G1-G4', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog5 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='G5', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog6 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='G6-G8', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        buronb = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='03 Tarjeta', buro_camp='NB', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burotot = Seguimiento1.objects.values(filtro1).filter(riesgos='CAMP', producto='03 Tarjeta').annotate(seg=Sum('form')).order_by(filtro1)
    dict_burog1 = {}; dict_burog5 = {};
    dict_burog6 = {}; dict_buronb = {};
    for i in meses:
        for j in burog1:
            if i[filtro1] == j[filtro1]:
                dict_burog1[i[filtro1]] = j['seg']
                break
            else:
                dict_burog1[i[filtro1]] = 0
        for j in burog5:
            if i[filtro1] == j[filtro1]:
                dict_burog5[i[filtro1]] = j['seg']
                break
            else:
                dict_burog5[i[filtro1]] = 0
        for j in burog6:
            if i[filtro1] == j[filtro1]:
                dict_burog6[i[filtro1]] = j['seg']
                break
            else:
                dict_burog6[i[filtro1]] = 0
        for j in buronb:
            if i[filtro1] == j[filtro1]:
                dict_buronb[i[filtro1]] = j['seg']
                break
            else:
                dict_buronb[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        mora6_buro = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        mora6_buro = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='03 Tarjeta',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6'), sum_mora12=Sum('mora12')).order_by(filtro1)
    dict_mora6buro1 = {}; dict_mora6buro2 = {}; 
    dict_mora6buro3 = {}; dict_mora6buro4 = {};
    dict_mora12buro1 = {}; dict_mora12buro2 = {}; 
    dict_mora12buro3 = {}; dict_mora12buro4 = {};
    for i in mora6_buro:
        if i['buro_camp'] == 'G1-G4':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro1[i[filtro1]] = i['sum_mora6']*100/dict_moraburo1[i[filtro1]]
                dict_mora12buro1[i[filtro1]] = i['sum_mora12']*100/dict_moraburo1[i[filtro1]]
        if i['buro_camp'] == 'G5':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro2[i[filtro1]] = i['sum_mora6']*100/dict_moraburo2[i[filtro1]]
                dict_mora12buro2[i[filtro1]] = i['sum_mora12']*100/dict_moraburo2[i[filtro1]]
        if i['buro_camp'] == 'G6-G8':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro3[i[filtro1]] = i['sum_mora6']*100/dict_moraburo3[i[filtro1]]
                dict_mora12buro3[i[filtro1]] = i['sum_mora12']*100/dict_moraburo3[i[filtro1]]
        if i['buro_camp'] == 'NB':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro4[i[filtro1]] = i['sum_mora6']*100/dict_moraburo4[i[filtro1]]
                dict_mora12buro4[i[filtro1]] = i['sum_mora12']*100/dict_moraburo4[i[filtro1]]

    if filtro1 == 'trimestre_form':
        form_modestos = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='1. Modestos', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_desligados = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='2. Desligados', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_progresistas = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='3. Progresistas', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_aspirantes = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='4. Aspirantes', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_prosperos = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='5. Prosperos', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_sd = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='0. S.D.', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
    else:
        form_modestos = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='1. Modestos', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_desligados = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='2. Desligados', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_progresistas = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='3. Progresistas', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_aspirantes = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='4. Aspirantes', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_prosperos = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='5. Prosperos', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
        form_sd = Seguimiento1.objects.values(filtro1, 'cluster').filter(cluster='0. S.D.', producto='03 Tarjeta', periodo__gte=filtro2).annotate(formalizados=Sum('form')).order_by(filtro1)
    form_modes_dict = {}; form_desli_dict = {}; form_progre_dict = {};
    form_aspi_dict = {}; form_prospe_dict = {}; form_sd_dict = {};
    for i in meses:
        for j in form_modestos:
            if i[filtro1] == j[filtro1]:
                form_modes_dict[i[filtro1]] = j['formalizados']#*100/total_form_dict[i[filtro1]]
                break
            else:
                form_modes_dict[i[filtro1]] = 0
        for j in form_desligados:
            if i[filtro1] == j[filtro1]:
                form_desli_dict[i[filtro1]] = j['formalizados']#*100/total_form_dict[i[filtro1]]
                break
            else:
                form_desli_dict[i[filtro1]] = 0
        for j in form_progresistas:
            if i[filtro1] == j[filtro1]:
                form_progre_dict[i[filtro1]] = j['formalizados']#*100/total_form_dict[i[filtro1]]
                break
            else:
                form_progre_dict[i[filtro1]] = 0
        for j in form_aspirantes:
            if i[filtro1] == j[filtro1]:
                form_aspi_dict[i[filtro1]] = j['formalizados']#*100/total_form_dict[i[filtro1]]
                break
            else:
                form_aspi_dict[i[filtro1]] = 0
        for j in form_prosperos:
            if i[filtro1] == j[filtro1]:
                form_prospe_dict[i[filtro1]] = j['formalizados']#*100/total_form_dict[i[filtro1]]
                break
            else:
                form_prospe_dict[i[filtro1]] = 0
        for j in form_sd:
            if i[filtro1] == j[filtro1]:
                form_sd_dict[i[filtro1]] = j['formalizados']#*100/total_form_dict[i[filtro1]]
                break
            else:
                form_sd_dict[i[filtro1]] = 0


    if filtro1 == 'trimestre_form':
        total_forzaje = Forzaje.objects.values(filtro1).filter(producto='03 Tarjeta').annotate(cantidad=Sum('form')).order_by(filtro1)
    else:
        total_forzaje = Forzaje.objects.values(filtro1).filter(producto='03 Tarjeta').annotate(cantidad=Sum('form')).order_by(filtro1)
    forzaje_dict = {}
    for i in meses:
	   for j in total_forzaje:
	       if i[filtro1] == j[filtro1]:
		      forzaje_dict[j[filtro1]]=j['cantidad']

    if filtro1 == 'trimestre_form':
        forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '03 Tarjeta').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    else:
        forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '03 Tarjeta').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    duda_dict = {}
    rechazo_dict = {}
    for i in meses:
        for j in forzaje2:
            if i[filtro1] == j[filtro1]:
	           if  j['dic_global']=='DU':
                    duda_dict[i[filtro1]]=j['cantidad']*100/forzaje_dict[i[filtro1]]
                    break
            else:
                duda_dict[i[filtro1]]= 0
        for j in forzaje2:
            if i[filtro1] == j[filtro1]:
	           if  j['dic_global']=='RE':
                    rechazo_dict[i[filtro1]]=j['cantidad']*100/forzaje_dict[i[filtro1]]
                    break
            else:
                rechazo_dict[i[filtro1]]= 0

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_tarjeta.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_prestamo(request, filtro1='mes_vigencia', filtro2='2012', filtro3='form'):
    filtro1 = str(filtro1)
    filtro2 = str(filtro2)
    filtro3 = str(filtro3)

    tiempo = Seguimiento.objects.values_list('periodo', flat=True).order_by('periodo').distinct()
    print tiempo

    if filtro3 == 'form':
      tipo_form = 1
    else:
      tipo_form = 0

    if filtro1 == 'trimestre_form':
        meses = Seguimiento.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).exclude(trimestre_form__in=['']).order_by(filtro1).distinct()
        trimestre = 1
    else:
        meses = Seguimiento.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).order_by(filtro1).distinct()
        trimestre = 0

    total_form = Seguimiento.objects.values(filtro1, 'producto').filter(producto='01 Consumo', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3),cuentas=Sum('ctas')).order_by(filtro1)
    total_form_dict = {}; total_ctas_dict = {};
    for i in meses:
      for j in total_form:
        if i == j[filtro1]:
          total_form_dict[j[filtro1]]=j['formalizado']
          total_ctas_dict[j[filtro1]]=j['cuentas']

    if filtro1 == 'trimestre_form':
        meses_fast = Seguimiento.objects.values('trimestre_form').filter(trimestre_form__gte='2014-4').order_by('-trimestre_form').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1
    else:
        meses_fast = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201410').order_by('-mes_vigencia').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1

    uno_a_uno = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_fast = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_regular = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    formUno_dict = {}; formFast_dict = {}; formRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                formUno_dict[i] = j['formalizado']
                break
            else:
                formUno_dict[i] = 0
        for j in camp_fast:
            if i == j[filtro1]:
                formFast_dict[i] = j['formalizado']
                break
            else:
                formFast_dict[i] = 0
        for j in camp_regular:
            if i == j[filtro1]:
                formRegular_dict[i] = j['formalizado']
                break
            else:
                formRegular_dict[i] = 0

    uno_a_uno = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_fast = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_regular = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    ticketUno_dict = {}; ticketFast_dict = {}; ticketRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                ticketUno_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketUno_dict[i] = []
        for j in camp_fast:
            if i == j[filtro1]:
                if i >= meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = j['facturacion']*1000000/j['formalizado']
                elif i < meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = []
                break
            else:
                ticketFast_dict[i] = []
        for j in camp_regular:
            if i == j[filtro1]:
                ticketRegular_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketRegular_dict[i] = []

    if filtro1 == 'trimestre_form':
        meses_moras = Seguimiento.objects.values('trimestre_form').order_by('-trimestre_form').distinct()
        mora_mes = Seguimiento.objects.values('trimestre_form').filter(trimestre_form__gte='2015-2', periodo__gte=filtro2).order_by('-trimestre_form').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 1
        num_mora6 = 2
        num_mora9 = 3
        num_mora12 = 4
        num_mora18 = 6 
        num_mora24 = 8 
        num_mora36 = 12 
    else:
        meses_moras = Seguimiento.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
        mora_mes = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201504', periodo__gte=filtro2).order_by('-mes_vigencia').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 4 
        num_mora6 = 6 
        num_mora9 = 9 
        num_mora12 = 12 
        num_mora18 = 18 
        num_mora24 = 24 
        num_mora36 = 36 

    morames_list = []
    for i in meses_moras:
        morames_list.append(i[filtro1])
    
    mora460 = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
    mora6 = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
    mora9 = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
    mora12 = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    mora18 = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora18'),cuentas=Sum('ctas')).order_by(filtro1)
    mora24 = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora24'),cuentas=Sum('ctas')).order_by(filtro1)
    mora36 = Seguimiento.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora36'),cuentas=Sum('ctas')).order_by(filtro1)
    mora460_dict = {}; mora6_dict = {}; mora9_dict = {}; mora12_dict = {};
    mora18_dict = {}; mora24_dict = {}; mora36_dict = {};
    for j in mora460:
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora460:
        if j[filtro1] <= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=[]
    for j in mora6:
        if j[filtro1] <= morames_list[num_mora6]:
            mora6_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora9:
        if j[filtro1] <= morames_list[num_mora9]:
            mora9_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora12:
        if j[filtro1] <= morames_list[num_mora12]:
            mora12_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora18:
        if j[filtro1] <= morames_list[num_mora18]:
            mora18_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora24:
        if j[filtro1] <= morames_list[num_mora24]:
            mora24_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora36:
        if j[filtro1] <= morames_list[num_mora36]:
            mora36_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']

    rangos = Seguimiento.objects.values(filtro1, 'rng_ing').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(num_rango=Sum(filtro3)).order_by(filtro1)
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
      for j in rangos:
        if i == j[filtro1]:
          if j['rng_ing'] == '01 [3.5K - ...]':
            rango1_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '02 [2.5K - 3.5K]':
            rango2_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '03 [2K - 2.5K]':
            rango3_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '04 [1.5K - 2K]':
            rango4_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '05 [1K - 1.5K]':
            rango5_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '06 [0 - 1K]':
            rango6_dict[i]=j['num_rango']*100/total_form_dict[i]

    formxcampxuno = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_form_dict = {}; uno_form_dict = {};
    for i in meses:
        for j in formxcampxuno:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                camp_form_dict[i] = j['formalizado']
                break
            else:
                camp_form_dict[i] = 0
        for j in formxcampxuno:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_form_dict[i] = j['formalizado']
                break
            else:
                uno_form_dict[i] = 0

    seg_ava = Seguimiento.objects.values(filtro1).filter(riesgos='CAMP', producto='01 Consumo', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ms = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_noph = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_nocli = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ava_dict = {}; seg_ms_dict = {}; seg_noph_dict = {}; seg_nocli_dict = {};
    useg_ms_dict = {}; useg_noph_dict = {}; useg_nocli_dict = {};
    for i in meses:
        for j in seg_ava:
            if i == j[filtro1]:
                seg_ava_dict[i] = j['seg']
                break
            else:
                seg_ava_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_ms_dict[i] = j['seg']
                break
            else:
                seg_ms_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_ms_dict[i] = j['seg']
                break
            else:
                useg_ms_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_noph_dict[i] = j['seg']
                break
            else:
                seg_noph_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_noph_dict[i] = j['seg']
                break
            else:
                useg_noph_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_nocli_dict[i] = j['seg']
                break
            else:
                seg_nocli_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_nocli_dict[i] = j['seg']
                break
            else:
                useg_nocli_dict[i] = 0

    total_ctasxmorasxcampxuno = Seguimiento.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12'),sum_mora18=Sum('mora18'), sum_mora24=Sum('mora24'), sum_mora36=Sum('mora36')).order_by(filtro1)
    total_ctasxcamp_dict = {}; mora460_camp_dict = {}; mora6_camp_dict = {}; mora9_camp_dict = {}; mora12_camp_dict = {}; mora18_camp_dict = {}; mora24_camp_dict = {}; mora36_camp_dict = {};
    mora460_uno_dict = {}; mora6_uno_dict = {}; mora9_uno_dict = {}; mora12_uno_dict = {}; mora18_uno_dict = {}; mora24_uno_dict = {}; mora36_uno_dict = {};
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_camp_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_camp_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_camp_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_camp_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_camp_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_camp_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_uno_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_uno_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_uno_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_uno_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_uno_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_uno_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']


    moras = Seguimiento.objects.values(filtro1, 'segmento', 'riesgos').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO 6 MESES - SEGMENTOS
    ava_mora460_dict = {}; ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora460_dict = {}; ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora460_dict = {}; noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora460_dict = {}; nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    #INCUMPLIMIENTO 6 MESES SEGMENTO - UNO A UNO
    dict_moraunoms = {}; dict_moraunonoph = {}; dict_moraunonocli = {};
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['segmento']=='1.AVA':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ava_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ava_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ava_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ava_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ava_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']     
              elif  j['segmento']=='2.MS':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ms_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ms_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ms_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ms_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ms_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      noph_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      noph_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      noph_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      noph_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      noph_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      nocli_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      nocli_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      nocli_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      nocli_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      nocli_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['segmento']=='2.MS':
                if i <= morames_list[num_mora6]:
                      dict_moraunoms[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora6]:
                      dict_moraunonoph[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora6]:
                      dict_moraunonocli[i]=j['sum_mora6']*100/j['sum_ctas']

    depen = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum(filtro3)).order_by(filtro1)
    indep = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    pnn = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    no_recon = Seguimiento.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    depen_dict = {}; indep_dict = {}; pnn_dict = {}; no_recon_dict = {}; totxcamp_laboral = {};
    udepen_dict = {}; uindep_dict = {}; upnn_dict = {}; uno_recon_dict = {};
    for i in meses:
        for j in depen:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                depen_dict[i] = j['seg']
                break
            else:
                depen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                indep_dict[i] = j['seg']
                break
            else:
                indep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                pnn_dict[i] = j['seg']
                break
            else:
                pnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                no_recon_dict[i] = j['seg']
                break
            else:
                no_recon_dict[i] = 0
        for j in depen:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                udepen_dict[i] = j['seg']
                break
            else:
                udepen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uindep_dict[i] = j['seg']
                break
            else:
                uindep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                upnn_dict[i] = j['seg']
                break
            else:
                upnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_recon_dict[i] = j['seg']
                break
            else:
                uno_recon_dict[i] = 0

    morascat = Seguimiento.objects.values(filtro1, 'cat_persona','riesgos').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO RELACION LABORAL CAMPANAS
    dep_mora460_dict = {}; dep_mora6_dict = {}; dep_mora9_dict = {}; dep_mora12_dict = {}
    indep_mora460_dict = {}; indep_mora6_dict = {}; indep_mora9_dict = {}; indep_mora12_dict = {}
    pnn_mora460_dict = {}; pnn_mora6_dict = {}; pnn_mora9_dict = {}; pnn_mora12_dict = {}
    norec_mora460_dict = {}; norec_mora6_dict = {}; norec_mora9_dict = {}; norec_mora12_dict = {}
    #INCUMPLMIENTO 6 MESES RELACION LABORAL - UNO A UNO
    dict_moracamdep = {}; dict_moracamind = {}; 
    dict_moracampnn = {}; dict_moracamnor = {};
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['cat_persona']=='1. Dependiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      dep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      dep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      dep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      dep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      dep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']    
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      indep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      indep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      indep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      indep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      indep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      pnn_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      pnn_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      pnn_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      pnn_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      pnn_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      norec_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      norec_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      norec_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      norec_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      norec_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['cat_persona']=='1. Dependiente':
                if i <= morames_list[num_mora6]:
                      dict_moracamdep[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora6]:
                      dict_moracamind[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora6]:
                      dict_moracampnn[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora6]:
                      dict_moracamnor[i]=j['sum_mora6']*100/j['sum_ctas']

    buroxform = Seguimiento.objects.values(filtro1, 'buro_camp').filter(digital='',riesgos='CAMP', producto='01 Consumo', periodo__gte=filtro2).annotate(seg=Sum(filtro3),cuentas=Sum('ctas'),sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_burog1 = {}; dict_burog5 = {};
    dict_burog6 = {}; dict_buronb = {};
    for i in meses:
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G1-G4':
                dict_burog1[i] = j['seg']
                break
              else:
                dict_burog1[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G5':
                dict_burog5[i] = j['seg']
                break
              else:
                dict_burog5[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G6-G8':
                dict_burog6[i] = j['seg']
                break
              else:
                dict_burog6[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'NB':
                dict_buronb[i] = j['seg']
                break
              else:
                dict_buronb[i] = 0

    dict_mora6buro1 = {}; dict_mora6buro2 = {}; 
    dict_mora6buro3 = {}; dict_mora6buro4 = {};
    for i in buroxform:
        if i['buro_camp'] == 'G1-G4':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro1[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G5':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro2[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G6-G8':
            if i[filtro1] <= morames_list[num_mora6]:
              if i['cuentas'] == 0:
                dict_mora6buro3[i[filtro1]] = 0
              else:
                dict_mora6buro3[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'NB':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro4[i[filtro1]] = i['sum_mora6']*100/i['cuentas']

    total_forzaje = Forzaje.objects.values(filtro1).filter(producto='01 Consumo').annotate(cantidad=Sum('form')).order_by(filtro1)
    forzaje_dict = {}
    for i in meses:
     for j in total_forzaje:
         if i == j[filtro1]:
          forzaje_dict[j[filtro1]]=j['cantidad']

    forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '01 Consumo').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    duda_dict = {}; rechazo_dict = {};
    for i in meses:
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='DU':
                    duda_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                duda_dict[i]= 0
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='RE':
                    rechazo_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                rechazo_dict[i]= 0

    form_cluster = Seguimiento.objects.values(filtro1, 'cluster').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(formalizados=Sum(filtro3)).order_by(filtro1)
    form_modes_dict = {}; form_desli_dict = {}; form_progre_dict = {};
    form_aspi_dict = {}; form_prospe_dict = {}; form_sd_dict = {};
    for i in meses:
        for j in form_cluster:
            if i == j[filtro1]:
              if j['cluster'] == '1. Modestos':
                form_modes_dict[i] = j['formalizados']
              elif j['cluster'] == '2. Desligados':
                form_desli_dict[i] = j['formalizados']
              elif j['cluster'] == '3. Progresistas':
                form_progre_dict[i] = j['formalizados']
              elif j['cluster'] == '4. Aspirantes':
                form_aspi_dict[i] = j['formalizados']
              elif j['cluster'] == '5. Prosperos':
                form_prospe_dict[i] = j['formalizados']
              elif j['cluster'] == '0. S.D.':
                form_sd_dict[i] = j['formalizados']

    form_clusterxmora = Seguimiento.objects.values(filtro1, 'cluster').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(formalizados=Sum('form'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    modes_mora6_dict = {}; desli_mora6_dict = {}; 
    progre_mora460_dict = {}; progre_mora6_dict = {}; progre_mora9_dict = {}; progre_mora12_dict = {}
    aspi_mora460_dict = {}; aspi_mora6_dict = {}; aspi_mora9_dict = {}; aspi_mora12_dict = {}
    prospe_mora460_dict = {}; prospe_mora6_dict = {}; prospe_mora9_dict = {}; prospe_mora12_dict = {}
    for i in meses:
       for j in form_clusterxmora:
          if i == j[filtro1]:
            if  j['cluster']=='1. Modestos':
                if i <= morames_list[num_mora6]:
                    modes_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='2. Desligados':
                if i <= morames_list[num_mora6]:
                    desli_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='3. Progresistas':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    progre_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    progre_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    progre_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    progre_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    progre_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='4. Aspirantes':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    aspi_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    aspi_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    aspi_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    aspi_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    aspi_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='5. Prosperos':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    prospe_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    prospe_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    prospe_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    prospe_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    prospe_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']

    meses_costo = CosteRiesgo.objects.values_list('codmes', flat=True).order_by('-codmes').distinct()
    meses_costo_list= []
    for i in meses_costo:
      meses_costo_list.append(i)

    costo_mensual_total = CosteRiesgo.objects.values('codmes','m6_t','m9_t','m12_t','m6_c','m9_c','m12_c','m6_u','m9_u','m12_u').filter(producto='Consumo')
    cm6t_dict={};cm9t_dict={};cm12t_dict={};mm6t_dict={};
    cm6c_dict={};cm9c_dict={};cm12c_dict={};mm6c_dict={};
    cm6u_dict={};cm9u_dict={};cm12u_dict={};mm6u_dict={};
    for i in costo_mensual_total:
      for j in meses_costo:
        if i['codmes']<=meses_costo_list[6]:
          cm6t_dict[i['codmes']]=i['m6_t']*100
          cm6c_dict[i['codmes']]=i['m6_c']*100
          cm6u_dict[i['codmes']]=i['m6_u']*100
        else:
          cm6t_dict[i['codmes']]=[]
          cm6c_dict[i['codmes']]=[]
          cm6u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[9]:
          cm9t_dict[i['codmes']]=i['m9_t']*100
          cm9c_dict[i['codmes']]=i['m9_c']*100
          cm9u_dict[i['codmes']]=i['m9_u']*100
        else:
          cm9t_dict[i['codmes']]=[]
          cm9c_dict[i['codmes']]=[]
          cm9u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[12]:
          cm12t_dict[i['codmes']]=i['m12_t']*100
          cm12c_dict[i['codmes']]=i['m12_c']*100
          cm12u_dict[i['codmes']]=i['m12_u']*100
        else:
          cm12t_dict[i['codmes']]=[]
          cm12c_dict[i['codmes']]=[]
          cm12u_dict[i['codmes']]=[]

    if filtro1 == 'trimestre_form':
      for i in meses:
        mm6t_dict[i]=[]
        mm6c_dict[i]=[]
        mm6u_dict[i]=[]
    else:
      len_meses = len(meses_costo_list)-1
      for i in meses:
        if i >= meses_costo_list[len_meses] and i <= meses_costo_list[0]:
          mm6t_dict[i]=cm6t_dict[i]
          mm6c_dict[i]=cm6c_dict[i]
          mm6u_dict[i]=cm6u_dict[i]
        else:
          mm6t_dict[i]=[]
          mm6c_dict[i]=[]
          mm6u_dict[i]=[]
          


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_prestamo.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_prestamoter(request, filtro1='mes_vigencia', filtro2='2012', filtro3='form'):
    filtro1 = str(filtro1)
    filtro2 = str(filtro2)
    filtro3 = str(filtro3)

    tiempo = SeguimientoTer.objects.values_list('periodo', flat=True).order_by('periodo').distinct()

    if filtro3 == 'form':
      tipo_form = 1
    else:
      tipo_form = 0

    if filtro1 == 'trimestre_form':
        meses = SeguimientoTer.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).exclude(trimestre_form__in=['']).order_by(filtro1).distinct()
        trimestre = 1
    else:
        meses = SeguimientoTer.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).order_by(filtro1).distinct()
        trimestre = 0

    total_form = SeguimientoTer.objects.values(filtro1, 'producto').filter(producto='01 Consumo', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3),cuentas=Sum('ctas')).order_by(filtro1)
    total_form_dict = {}; total_ctas_dict = {};
    for i in meses:
      for j in total_form:
        if i == j[filtro1]:
          total_form_dict[j[filtro1]]=j['formalizado']
          total_ctas_dict[j[filtro1]]=j['cuentas']

    if filtro1 == 'trimestre_form':
        meses_fast = SeguimientoTer.objects.values('trimestre_form').filter(trimestre_form__gte='2014-4').order_by('-trimestre_form').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1
    else:
        meses_fast = SeguimientoTer.objects.values('mes_vigencia').filter(mes_vigencia__gte='201410').order_by('-mes_vigencia').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1

    uno_a_uno = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_fast = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_regular = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    formUno_dict = {}; formFast_dict = {}; formRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                formUno_dict[i] = j['formalizado']
                break
            else:
                formUno_dict[i] = 0
        for j in camp_fast:
            if i == j[filtro1]:
                formFast_dict[i] = j['formalizado']
                break
            else:
                formFast_dict[i] = 0
        for j in camp_regular:
            if i == j[filtro1]:
                formRegular_dict[i] = j['formalizado']
                break
            else:
                formRegular_dict[i] = 0

    uno_a_uno = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', origen='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_fast = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', origen='FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    camp_regular = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', origen='REGULAR', periodo__gte=filtro2).annotate(formalizado=Sum('form'),facturacion=Sum('facturacion')).order_by(filtro1)
    ticketUno_dict = {}; ticketFast_dict = {}; ticketRegular_dict = {};
    for i in meses:
        for j in uno_a_uno:
            if i == j[filtro1]:
                ticketUno_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketUno_dict[i] = []
        for j in camp_fast:
            if i == j[filtro1]:
                if i >= meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = j['facturacion']*1000000/j['formalizado']
                elif i < meses_fast_list[num_meses_fast]:
                  ticketFast_dict[i] = []
                break
            else:
                ticketFast_dict[i] = []
        for j in camp_regular:
            if i == j[filtro1]:
                ticketRegular_dict[i] = j['facturacion']*1000000/j['formalizado']
                break
            else:
                ticketRegular_dict[i] = []

    if filtro1 == 'trimestre_form':
        meses_moras = SeguimientoTer.objects.values('trimestre_form').order_by('-trimestre_form').distinct()
        mora_mes = SeguimientoTer.objects.values('trimestre_form').filter(trimestre_form__gte='2015-2', periodo__gte=filtro2).order_by('-trimestre_form').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 1
        num_mora6 = 2
        num_mora9 = 3
        num_mora12 = 4
        num_mora18 = 6 
        num_mora24 = 8 
        num_mora36 = 12 
    else:
        meses_moras = SeguimientoTer.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
        mora_mes = SeguimientoTer.objects.values('mes_vigencia').filter(mes_vigencia__gte='201504', periodo__gte=filtro2).order_by('-mes_vigencia').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 4 
        num_mora6 = 6 
        num_mora9 = 9 
        num_mora12 = 12 
        num_mora18 = 18 
        num_mora24 = 24 
        num_mora36 = 36 

    morames_list = []
    for i in meses_moras:
        morames_list.append(i[filtro1])
    
    mora460 = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
    mora6 = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
    mora9 = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
    mora12 = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    mora18 = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora18'),cuentas=Sum('ctas')).order_by(filtro1)
    mora24 = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora24'),cuentas=Sum('ctas')).order_by(filtro1)
    mora36 = SeguimientoTer.objects.values(filtro1).filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora36'),cuentas=Sum('ctas')).order_by(filtro1)
    mora460_dict = {}; mora6_dict = {}; mora9_dict = {}; mora12_dict = {};
    mora18_dict = {}; mora24_dict = {}; mora36_dict = {};
    for j in mora460:
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora460:
        if j[filtro1] <= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=[]
    for j in mora6:
        if j[filtro1] <= morames_list[num_mora6]:
            mora6_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora9:
        if j[filtro1] <= morames_list[num_mora9]:
            mora9_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora12:
        if j[filtro1] <= morames_list[num_mora12]:
            mora12_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora18:
        if j[filtro1] <= morames_list[num_mora18]:
            mora18_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora24:
        if j[filtro1] <= morames_list[num_mora24]:
            mora24_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora36:
        if j[filtro1] <= morames_list[num_mora36]:
            mora36_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']

    rangos = SeguimientoTer.objects.values(filtro1, 'rng_ing').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(num_rango=Sum(filtro3)).order_by(filtro1)
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
      for j in rangos:
        if i == j[filtro1]:
          if j['rng_ing'] == '01 [3.5K - ...]':
            rango1_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '02 [2.5K - 3.5K]':
            rango2_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '03 [2K - 2.5K]':
            rango3_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '04 [1.5K - 2K]':
            rango4_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '05 [1K - 1.5K]':
            rango5_dict[i]=j['num_rango']*100/total_form_dict[i]
          elif j['rng_ing'] == '06 [0 - 1K]':
            rango6_dict[i]=j['num_rango']*100/total_form_dict[i]

    formxcampxuno = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', periodo__gte=filtro2, origen__in=['FAST','REGULAR','UNO A UNO']).annotate(formalizado=Sum(filtro3)).order_by(filtro1)
    camp_form_dict = {}; uno_form_dict = {};
    for i in meses:
        for j in formxcampxuno:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                camp_form_dict[i] = j['formalizado']
                break
            else:
                camp_form_dict[i] = 0
        for j in formxcampxuno:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_form_dict[i] = j['formalizado']
                break
            else:
                uno_form_dict[i] = 0

    seg_ava = SeguimientoTer.objects.values(filtro1).filter(riesgos='CAMP', producto='01 Consumo', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ms = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_noph = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_nocli = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    seg_ava_dict = {}; seg_ms_dict = {}; seg_noph_dict = {}; seg_nocli_dict = {};
    useg_ms_dict = {}; useg_noph_dict = {}; useg_nocli_dict = {};
    for i in meses:
        for j in seg_ava:
            if i == j[filtro1]:
                seg_ava_dict[i] = j['seg']
                break
            else:
                seg_ava_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_ms_dict[i] = j['seg']
                break
            else:
                seg_ms_dict[i] = 0
        for j in seg_ms:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_ms_dict[i] = j['seg']
                break
            else:
                useg_ms_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_noph_dict[i] = j['seg']
                break
            else:
                seg_noph_dict[i] = 0
        for j in seg_noph:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_noph_dict[i] = j['seg']
                break
            else:
                useg_noph_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                seg_nocli_dict[i] = j['seg']
                break
            else:
                seg_nocli_dict[i] = 0
        for j in seg_nocli:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                useg_nocli_dict[i] = j['seg']
                break
            else:
                useg_nocli_dict[i] = 0

    total_ctasxmorasxcampxuno = SeguimientoTer.objects.values(filtro1,'riesgos').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12'),sum_mora18=Sum('mora18'), sum_mora24=Sum('mora24'), sum_mora36=Sum('mora36')).order_by(filtro1)
    total_ctasxcamp_dict = {}; mora460_camp_dict = {}; mora6_camp_dict = {}; mora9_camp_dict = {}; mora12_camp_dict = {}; mora18_camp_dict = {}; mora24_camp_dict = {}; mora36_camp_dict = {};
    mora460_uno_dict = {}; mora6_uno_dict = {}; mora9_uno_dict = {}; mora12_uno_dict = {}; mora18_uno_dict = {}; mora24_uno_dict = {}; mora36_uno_dict = {};
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_camp_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_camp_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_camp_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_camp_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_camp_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_camp_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'CAMP':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_camp_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=j['sum_mora460']*100/j['sum_ctas']
        elif j[filtro1] < morames_list[num_lista]:
          mora460_uno_dict[j[filtro1]]=[]
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora6]:
          mora6_uno_dict[j[filtro1]]=j['sum_mora6']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora9]:
          mora9_uno_dict[j[filtro1]]=j['sum_mora9']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora12]:
          mora12_uno_dict[j[filtro1]]=j['sum_mora12']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora18]:
          mora18_uno_dict[j[filtro1]]=j['sum_mora18']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora24]:
          mora24_uno_dict[j[filtro1]]=j['sum_mora24']*100/j['sum_ctas']
    for j in total_ctasxmorasxcampxuno:
      if j['riesgos'] == 'UNO A UNO':
        if j[filtro1] <= morames_list[num_mora36]:
          mora36_uno_dict[j[filtro1]]=j['sum_mora36']*100/j['sum_ctas']


    moras = SeguimientoTer.objects.values(filtro1, 'segmento', 'riesgos').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO 6 MESES - SEGMENTOS
    ava_mora460_dict = {}; ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora460_dict = {}; ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora460_dict = {}; noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora460_dict = {}; nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    #INCUMPLIMIENTO 6 MESES SEGMENTO - UNO A UNO
    dict_moraunoms = {}; dict_moraunonoph = {}; dict_moraunonocli = {};
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['segmento']=='1.AVA':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ava_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ava_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ava_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ava_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ava_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']     
              elif  j['segmento']=='2.MS':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      ms_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      ms_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      ms_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      ms_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      ms_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      noph_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      noph_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      noph_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      noph_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      noph_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      nocli_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i < morames_list[num_lista]:
                      nocli_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      nocli_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      nocli_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      nocli_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in moras:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['segmento']=='2.MS':
                if i <= morames_list[num_mora6]:
                      dict_moraunoms[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='3.NoPH':
                  if i <= morames_list[num_mora6]:
                      dict_moraunonoph[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['segmento']=='4.NoCli':
                  if i <= morames_list[num_mora6]:
                      dict_moraunonocli[i]=j['sum_mora6']*100/j['sum_ctas']

    depen = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum(filtro3)).order_by(filtro1)
    indep = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    pnn = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    no_recon = SeguimientoTer.objects.values(filtro1,'riesgos').filter(digital='', producto='01 Consumo', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum(filtro3)).order_by(filtro1)
    depen_dict = {}; indep_dict = {}; pnn_dict = {}; no_recon_dict = {}; totxcamp_laboral = {};
    udepen_dict = {}; uindep_dict = {}; upnn_dict = {}; uno_recon_dict = {};
    for i in meses:
        for j in depen:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                depen_dict[i] = j['seg']
                break
            else:
                depen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                indep_dict[i] = j['seg']
                break
            else:
                indep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                pnn_dict[i] = j['seg']
                break
            else:
                pnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'CAMP':
            if i == j[filtro1]:
                no_recon_dict[i] = j['seg']
                break
            else:
                no_recon_dict[i] = 0
        for j in depen:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                udepen_dict[i] = j['seg']
                break
            else:
                udepen_dict[i] = 0
        for j in indep:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uindep_dict[i] = j['seg']
                break
            else:
                uindep_dict[i] = 0
        for j in pnn:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                upnn_dict[i] = j['seg']
                break
            else:
                upnn_dict[i] = 0
        for j in no_recon:
          if j['riesgos'] == 'UNO A UNO':
            if i == j[filtro1]:
                uno_recon_dict[i] = j['seg']
                break
            else:
                uno_recon_dict[i] = 0

    morascat = SeguimientoTer.objects.values(filtro1, 'cat_persona','riesgos').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    #INCUMPLIMIENTO RELACION LABORAL CAMPANAS
    dep_mora460_dict = {}; dep_mora6_dict = {}; dep_mora9_dict = {}; dep_mora12_dict = {}
    indep_mora460_dict = {}; indep_mora6_dict = {}; indep_mora9_dict = {}; indep_mora12_dict = {}
    pnn_mora460_dict = {}; pnn_mora6_dict = {}; pnn_mora9_dict = {}; pnn_mora12_dict = {}
    norec_mora460_dict = {}; norec_mora6_dict = {}; norec_mora9_dict = {}; norec_mora12_dict = {}
    #INCUMPLMIENTO 6 MESES RELACION LABORAL - UNO A UNO
    dict_moracamdep = {}; dict_moracamind = {}; 
    dict_moracampnn = {}; dict_moracamnor = {};
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'CAMP':
              if  j['cat_persona']=='1. Dependiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      dep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      dep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      dep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      dep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      dep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']    
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      indep_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      indep_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      indep_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      indep_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      indep_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      pnn_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      pnn_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      pnn_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      pnn_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      pnn_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                      norec_mora460_dict[i]=j['sum_mora460']*100/j['sum_ctas']
                  if i <= morames_list[num_lista]:
                      norec_mora460_dict[i]=[]
                  if i <= morames_list[num_mora6]:
                      norec_mora6_dict[i]=j['sum_mora6']*100/j['sum_ctas']
                  if i <= morames_list[num_mora9]:
                      norec_mora9_dict[i]=j['sum_mora9']*100/j['sum_ctas']
                  if i <= morames_list[num_mora12]:
                      norec_mora12_dict[i]=j['sum_mora12']*100/j['sum_ctas']
    for i in meses:
       for j in morascat:
          if i == j[filtro1]:
            if j['riesgos'] == 'UNO A UNO':
              if  j['cat_persona']=='1. Dependiente':
                if i <= morames_list[num_mora6]:
                      dict_moracamdep[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='2. Independiente':
                  if i <= morames_list[num_mora6]:
                      dict_moracamind[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='3. PNN':
                  if i <= morames_list[num_mora6]:
                      dict_moracampnn[i]=j['sum_mora6']*100/j['sum_ctas']
              elif  j['cat_persona']=='4.No Reconocido':
                  if i <= morames_list[num_mora6]:
                      dict_moracamnor[i]=j['sum_mora6']*100/j['sum_ctas']

    buroxform = SeguimientoTer.objects.values(filtro1, 'buro_camp').filter(digital='',riesgos='CAMP', producto='01 Consumo', periodo__gte=filtro2).annotate(seg=Sum(filtro3),cuentas=Sum('ctas'),sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_burog1 = {}; dict_burog5 = {};
    dict_burog6 = {}; dict_buronb = {};
    for i in meses:
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G1-G4':
                dict_burog1[i] = j['seg']
                break
              else:
                dict_burog1[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G5':
                dict_burog5[i] = j['seg']
                break
              else:
                dict_burog5[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'G6-G8':
                dict_burog6[i] = j['seg']
                break
              else:
                dict_burog6[i] = 0
        for j in buroxform:
            if i == j[filtro1]:
              if j['buro_camp'] == 'NB':
                dict_buronb[i] = j['seg']
                break
              else:
                dict_buronb[i] = 0

    dict_mora6buro1 = {}; dict_mora6buro2 = {}; 
    dict_mora6buro3 = {}; dict_mora6buro4 = {};
    for i in buroxform:
        if i['buro_camp'] == 'G1-G4':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro1[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G5':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro2[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'G6-G8':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro3[i[filtro1]] = i['sum_mora6']*100/i['cuentas']
        if i['buro_camp'] == 'NB':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro4[i[filtro1]] = i['sum_mora6']*100/i['cuentas']

    total_forzaje = Forzaje.objects.values(filtro1).filter(producto='01 Consumo').annotate(cantidad=Sum('form')).order_by(filtro1)
    forzaje_dict = {}
    for i in meses:
     for j in total_forzaje:
         if i == j[filtro1]:
          forzaje_dict[j[filtro1]]=j['cantidad']

    forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '01 Consumo').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    duda_dict = {}; rechazo_dict = {};
    for i in meses:
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='DU':
                    duda_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                duda_dict[i]= 0
        for j in forzaje2:
            if i == j[filtro1]:
             if  j['dic_global']=='RE':
                    rechazo_dict[i]=j['cantidad']*100/forzaje_dict[i]
                    break
            else:
                rechazo_dict[i]= 0

    form_cluster = SeguimientoTer.objects.values(filtro1, 'cluster').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(formalizados=Sum(filtro3)).order_by(filtro1)
    form_modes_dict = {}; form_desli_dict = {}; form_progre_dict = {};
    form_aspi_dict = {}; form_prospe_dict = {}; form_sd_dict = {};
    for i in meses:
        for j in form_cluster:
            if i == j[filtro1]:
              if j['cluster'] == '1. Modestos':
                form_modes_dict[i] = j['formalizados']
              elif j['cluster'] == '2. Desligados':
                form_desli_dict[i] = j['formalizados']
              elif j['cluster'] == '3. Progresistas':
                form_progre_dict[i] = j['formalizados']
              elif j['cluster'] == '4. Aspirantes':
                form_aspi_dict[i] = j['formalizados']
              elif j['cluster'] == '5. Prosperos':
                form_prospe_dict[i] = j['formalizados']
              elif j['cluster'] == '0. S.D.':
                form_sd_dict[i] = j['formalizados']

    form_clusterxmora = SeguimientoTer.objects.values(filtro1, 'cluster').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(formalizados=Sum('form'),sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    modes_mora6_dict = {}; desli_mora6_dict = {}; 
    progre_mora460_dict = {}; progre_mora6_dict = {}; progre_mora9_dict = {}; progre_mora12_dict = {}
    aspi_mora460_dict = {}; aspi_mora6_dict = {}; aspi_mora9_dict = {}; aspi_mora12_dict = {}
    prospe_mora460_dict = {}; prospe_mora6_dict = {}; prospe_mora9_dict = {}; prospe_mora12_dict = {}
    for i in meses:
       for j in form_clusterxmora:
          if i == j[filtro1]:
            if  j['cluster']=='1. Modestos':
                if i <= morames_list[num_mora6]:
                    modes_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='2. Desligados':
                if i <= morames_list[num_mora6]:
                    desli_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
            elif  j['cluster']=='3. Progresistas':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    progre_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    progre_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    progre_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    progre_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    progre_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='4. Aspirantes':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    aspi_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    aspi_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    aspi_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    aspi_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    aspi_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']
            elif  j['cluster']=='5. Prosperos':
                if i <= morames_list[num_mora4] and i >= morames_list[num_lista]:
                    prospe_mora460_dict[i]=j['sum_mora460']*100/j['formalizados']
                if i <= morames_list[num_lista]:
                    prospe_mora460_dict[i]=[]
                if i <= morames_list[num_mora6]:
                    prospe_mora6_dict[i]=j['sum_mora6']*100/j['formalizados']
                if i <= morames_list[num_mora9]:
                    prospe_mora9_dict[i]=j['sum_mora9']*100/j['formalizados']
                if i <= morames_list[num_mora12]:
                    prospe_mora12_dict[i]=j['sum_mora12']*100/j['formalizados']

    meses_costo = CosteRiesgo.objects.values_list('codmes', flat=True).order_by('-codmes').distinct()
    meses_costo_list= []
    for i in meses_costo:
      meses_costo_list.append(i)

    costo_mensual_total = CosteRiesgo.objects.values('codmes','m6_t','m9_t','m12_t','m6_c','m9_c','m12_c','m6_u','m9_u','m12_u').filter(producto='Consumo')
    cm6t_dict={};cm9t_dict={};cm12t_dict={};mm6t_dict={};
    cm6c_dict={};cm9c_dict={};cm12c_dict={};mm6c_dict={};
    cm6u_dict={};cm9u_dict={};cm12u_dict={};mm6u_dict={};
    for i in costo_mensual_total:
      for j in meses_costo:
        if i['codmes']<=meses_costo_list[6]:
          cm6t_dict[i['codmes']]=i['m6_t']*100
          cm6c_dict[i['codmes']]=i['m6_c']*100
          cm6u_dict[i['codmes']]=i['m6_u']*100
        else:
          cm6t_dict[i['codmes']]=[]
          cm6c_dict[i['codmes']]=[]
          cm6u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[9]:
          cm9t_dict[i['codmes']]=i['m9_t']*100
          cm9c_dict[i['codmes']]=i['m9_c']*100
          cm9u_dict[i['codmes']]=i['m9_u']*100
        else:
          cm9t_dict[i['codmes']]=[]
          cm9c_dict[i['codmes']]=[]
          cm9u_dict[i['codmes']]=[]
        if i['codmes']<=meses_costo_list[12]:
          cm12t_dict[i['codmes']]=i['m12_t']*100
          cm12c_dict[i['codmes']]=i['m12_c']*100
          cm12u_dict[i['codmes']]=i['m12_u']*100
        else:
          cm12t_dict[i['codmes']]=[]
          cm12c_dict[i['codmes']]=[]
          cm12u_dict[i['codmes']]=[]

    if filtro1 == 'trimestre_form':
      for i in meses:
        mm6t_dict[i]=[]
        mm6c_dict[i]=[]
        mm6u_dict[i]=[]
    else:
      len_meses = len(meses_costo_list)-1
      for i in meses:
        if i >= meses_costo_list[len_meses]:
          mm6t_dict[i]=cm6t_dict[i]
          mm6c_dict[i]=cm6c_dict[i]
          mm6u_dict[i]=cm6u_dict[i]
        else:
          mm6t_dict[i]=[]
          mm6c_dict[i]=[]
          mm6u_dict[i]=[]
          


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_prestamoter.html', locals(),
                  context_instance=RequestContext(request))



def geolocalizacion(request):

  return render('reports/geolocalizacion.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_pld(request, filtro1='mes_vigencia', filtro2='2011'):
    filtro1 = str(filtro1)
    filtro2 = str(filtro2)
    side_tarjeta = 1

    tiempo = Seguimiento1.objects.values('periodo').order_by('periodo').distinct('periodo')
    time_list = []
    for i in tiempo:
        time_list.append(i['periodo'])

    if filtro1 == 'trimestre_form':
        meses = Seguimiento1.objects.values(filtro1).filter(periodo__gte=filtro2).order_by(filtro1).distinct(filtro1)
        trimestre = 1
    else:
        meses = Seguimiento1.objects.values(filtro1).filter(periodo__gte=filtro2).order_by(filtro1).distinct(filtro1)
        trimestre = 0
    meses_list = []
    for i in meses:
        meses_list.append(i[filtro1])

    if filtro1 == 'trimestre_form':
        total_form = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(formalizado=Sum('form'),cuentas=Sum('ctas')).order_by(filtro1)
    else:
        total_form = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(formalizado=Sum('form'),cuentas=Sum('ctas')).order_by(filtro1)
    total_form_dict = {}; total_ctas_dict = {};
    for j in total_form:
       total_form_dict[j[filtro1]]=j['formalizado']
    for j in total_form:
       total_ctas_dict[j[filtro1]]=j['cuentas']

    if filtro1 == 'trimestre_form':
        uno_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_fast = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='01 Consumo', origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_uno = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='01 Consumo', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    else:
        uno_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_fast = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='01 Consumo', origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_uno = Seguimiento1.objects.values(filtro1, 'origen').filter(producto='01 Consumo', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    uno_form_dict = {}; camp_fast_dict = {}; camp_uno_dict = {};
    for i in meses:
        for j in uno_form:
            if i[filtro1] == j[filtro1]:
                uno_form_dict[i[filtro1]] = j['formalizado']
                break
            else:
                uno_form_dict[i[filtro1]] = 0
        for j in camp_fast:
            if i[filtro1] == j[filtro1]:
                camp_fast_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_fast_dict[i[filtro1]] = 0
        for j in camp_uno:
            if i[filtro1] == j[filtro1]:
                camp_uno_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_uno_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        camp_formf = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_formu = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    else:
        camp_formf = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
        camp_formu = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    camp_formf_dict = {}; camp_formu_dict = {};
    for i in meses:
        for j in camp_formf:
            if i[filtro1] == j[filtro1]:
                camp_formf_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_formf_dict[i[filtro1]] = 0
        for j in camp_formu:
            if i[filtro1] == j[filtro1]:
                camp_formu_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_formu_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        meses_fast = Seguimiento1.objects.values('trimestre_form').filter(trimestre_form__gte='2014-4').order_by('-trimestre_form').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1
    else:
        meses_fast = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte='201410').order_by('-mes_vigencia').distinct()
        meses_fast_list= []
        for i in meses_fast:
            meses_fast_list.append(i[filtro1])
        num_meses_fast = len(meses_fast_list)-1

    if filtro1 == 'trimestre_form':
        fact_uno = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='01 Consumo', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campf = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='01 Consumo', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campu = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='01 Consumo', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
    else:
        fact_uno = Seguimiento1.objects.values(filtro1, 'producto').filter(producto='01 Consumo', riesgos='UNO A UNO', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campf = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='01 Consumo', riesgos='CAMP',origen='ORIGINACION FAST', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
        fact_campu = Seguimiento1.objects.values(filtro1, 'producto', 'origen').filter(producto='01 Consumo', riesgos='CAMP', origen='ORIGINACION MS', periodo__gte=filtro2).annotate(facturacion=Sum('facturacion')).order_by(filtro1)
    fact_uno_dict = {}; fact_campf_dict = {}; fact_campu_dict = {};
    for i in meses:
        for j in fact_uno:
            if i[filtro1] == j[filtro1]:
                fact_uno_dict[i[filtro1]] = j['facturacion']*1000000/uno_form_dict[i[filtro1]]
                break
            else:
                fact_uno_dict[i[filtro1]] = 0
        for j in fact_campu:
            if i[filtro1] == j[filtro1]:
                fact_campu_dict[i[filtro1]] = j['facturacion']*1000000/camp_formu_dict[i[filtro1]]
                break
            else:
                fact_campu_dict[i[filtro1]] = 0
        for j in fact_campf:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] >= meses_fast_list[num_meses_fast] and i[filtro1] <= meses_fast_list[0]:
                    fact_campf_dict[i[filtro1]] = j['facturacion']*1000000/camp_formf_dict[i[filtro1]]
                    break
        for j in fact_campf:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] < meses_fast_list[num_meses_fast]:
                    fact_campf_dict[i[filtro1]] = []
                    break
        for j in fact_campf:
            if i[filtro1] < meses_fast_list[num_meses_fast]:
                fact_campf_dict[i[filtro1]] = []
                break

    if filtro1 == 'trimestre_form':
        camp_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    else:
        camp_form = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(formalizado=Sum('form')).order_by(filtro1)
    camp_form_dict = {};
    for i in meses:
        for j in camp_form:
            if i[filtro1] == j[filtro1]:
                camp_form_dict[i[filtro1]] = j['formalizado']
                break
            else:
                camp_form_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        seg_ava = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        seg_ava = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='1.AVA', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    seg_ava_dict = {}; seg_ms_dict = {}; seg_noph_dict = {}; seg_nocli_dict = {};
    for i in meses:
        for j in seg_ava:
            if i[filtro1] == j[filtro1]:
                seg_ava_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_ava_dict[i[filtro1]] = 0
        for j in seg_ms:
            if i[filtro1] == j[filtro1]:
                seg_ms_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_ms_dict[i[filtro1]] = 0
        for j in seg_noph:
            if i[filtro1] == j[filtro1]:
                seg_noph_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_noph_dict[i[filtro1]] = 0
        for j in seg_nocli:
            if i[filtro1] == j[filtro1]:
                seg_nocli_dict[i[filtro1]] = j['seg']
                break
            else:
                seg_nocli_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        useg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        useg_ms = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_noph = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        useg_nocli = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    useg_ms_dict = {}; useg_noph_dict = {}; useg_nocli_dict = {};
    for i in meses:
        for j in useg_ms:
            if i[filtro1] == j[filtro1]:
                useg_ms_dict[i[filtro1]] = j['seg']
                break
            else:
                useg_ms_dict[i[filtro1]] = 0
        for j in useg_noph:
            if i[filtro1] == j[filtro1]:
                useg_noph_dict[i[filtro1]] = j['seg']
                break
            else:
                useg_noph_dict[i[filtro1]] = 0
        for j in useg_nocli:
            if i[filtro1] == j[filtro1]:
                useg_nocli_dict[i[filtro1]] = j['seg']
                break
            else:
                useg_nocli_dict[i[filtro1]] = 0 

    if filtro1 == 'trimestre_form':
        depen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        indep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        pnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        no_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        depen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        indep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        pnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        no_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='CAMP', producto='01 Consumo', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    depen_dict = {}; indep_dict = {}; pnn_dict = {}; no_recon_dict = {};
    for i in meses:
        for j in depen:
            if i[filtro1] == j[filtro1]:
                depen_dict[i[filtro1]] = j['seg']
                break
            else:
                depen_dict[i[filtro1]] = 0
        for j in indep:
            if i[filtro1] == j[filtro1]:
                indep_dict[i[filtro1]] = j['seg']
                break
            else:
                indep_dict[i[filtro1]] = 0
        for j in pnn:
            if i[filtro1] == j[filtro1]:
                pnn_dict[i[filtro1]] = j['seg']
                break
            else:
                pnn_dict[i[filtro1]] = 0
        for j in no_recon:
            if i[filtro1] == j[filtro1]:
                no_recon_dict[i[filtro1]] = j['seg']
                break
            else:
                no_recon_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        udepen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        uindep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        upnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        uno_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    else:
        udepen = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        uindep = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        upnn = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        uno_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(riesgos='UNO A UNO', producto='01 Consumo', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    udepen_dict = {}; uindep_dict = {}; upnn_dict = {}; uno_recon_dict = {};
    for i in meses:
        for j in udepen:
            if i[filtro1] == j[filtro1]:
                udepen_dict[i[filtro1]] = j['seg']
                break
            else:
                udepen_dict[i[filtro1]] = 0
        for j in uindep:
            if i[filtro1] == j[filtro1]:
                uindep_dict[i[filtro1]] = j['seg']
                break
            else:
                uindep_dict[i[filtro1]] = 0
        for j in upnn:
            if i[filtro1] == j[filtro1]:
                upnn_dict[i[filtro1]] = j['seg']
                break
            else:
                upnn_dict[i[filtro1]] = 0
        for j in uno_recon:
            if i[filtro1] == j[filtro1]:
                uno_recon_dict[i[filtro1]] = j['seg']
                break
            else:
                uno_recon_dict[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        rangos = Seguimiento1.objects.values(filtro1,'producto', 'rng_ing').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(num_rango=Sum('form')).order_by(filtro1)
    else:
        rangos = Seguimiento1.objects.values(filtro1,'producto', 'rng_ing').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(num_rango=Sum('form')).order_by(filtro1)
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
        for j in rangos:
            if i[filtro1] == j[filtro1]:
                if j['rng_ing'] == '01 [3.5K - ...]':
                    rango1_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
                elif j['rng_ing'] == '02 [2.5K - 3.5K]':
                    rango2_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
                elif j['rng_ing'] == '03 [2K - 2.5K]':
                    rango3_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
                elif j['rng_ing'] == '04 [1.5K - 2K]':
                    rango4_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
                elif j['rng_ing'] == '05 [1K - 1.5K]':
                    rango5_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]
                elif j['rng_ing'] == '06 [0 - 1K]':
                    rango6_dict[i[filtro1]]=j['num_rango']*100/total_form_dict[i[filtro1]]


    if filtro1 == 'trimestre_form':
        meses_moras = Seguimiento1.objects.values('trimestre_form').order_by('-trimestre_form').distinct()
        mora_mes = Seguimiento1.objects.values('trimestre_form').filter(trimestre_form__gte='2015-2', periodo__gte=filtro2).order_by('-trimestre_form').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 1
        num_mora6 = 2
        num_mora9 = 3
        num_mora12 = 4
    else:
        meses_moras = Seguimiento1.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
        mora_mes = Seguimiento1.objects.values('mes_vigencia').filter(mes_vigencia__gte='201504', periodo__gte=filtro2).order_by('-mes_vigencia').distinct()
        menor2015_list= []
        for i in mora_mes:
            menor2015_list.append(i[filtro1])
        num_lista = len(menor2015_list)
        num_mora4 = 4 #4
        num_mora6 = 6 #6
        num_mora9 = 9 #10
        num_mora12 = 12 #12

    morames_list = []
    for i in meses_moras:
        morames_list.append(i[filtro1])

    if filtro1 == 'trimestre_form':
        mora460 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
        mora6 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
        mora9 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
        mora12 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    else:
        mora460 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora4_60'),cuentas=Sum('ctas')).order_by(filtro1)
        mora6 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by(filtro1)
        mora9 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by(filtro1)
        mora12 = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
    mora460_dict = {}; mora6_dict = {}; mora9_dict = {}; mora12_dict = {};
    for j in mora460:
        if j[filtro1] <= morames_list[num_mora4] and j[filtro1] >= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora460:
        if j[filtro1] <= morames_list[num_lista]:
            mora460_dict[j[filtro1]]=[]
    for j in mora6:
        if j[filtro1] <= morames_list[num_mora6]:
            mora6_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora9:
        if j[filtro1] <= morames_list[num_mora9]:
            mora9_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora12:
        if j[filtro1] <= morames_list[num_mora12]:
            mora12_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']

    if filtro1 == 'trimestre_form':
        total_moraxcamp = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    else:
        total_moraxcamp = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    total_moraxcamp_dict = {}
    for i in meses_moras:
        for j in total_moraxcamp:
            if i[filtro1] == j[filtro1]:
               total_moraxcamp_dict[i[filtro1]]=j['sum_ctas']

    if filtro1 == 'trimestre_form':
        mora_camp = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        mora_camp = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    mora460_camp_dict = {}; mora6_camp_dict = {}; mora9_camp_dict = {}; mora12_camp_dict = {};
    for i in meses_moras:
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    mora460_camp_dict[i[filtro1]]=j['sum_mora460']*100/total_moraxcamp_dict[i[filtro1]]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_lista]:
                    mora460_camp_dict[i[filtro1]]=[]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora6]:
                    mora6_camp_dict[i[filtro1]]=j['sum_mora6']*100/total_moraxcamp_dict[i[filtro1]]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora9]:
                    mora9_camp_dict[i[filtro1]]=j['sum_mora9']*100/total_moraxcamp_dict[i[filtro1]]
                    break
        for j in mora_camp:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora12]:
                    mora12_camp_dict[i[filtro1]]=j['sum_mora12']*100/total_moraxcamp_dict[i[filtro1]]
                    break

    if filtro1 == 'trimestre_form':
        total_moraxuno = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    else:
        total_moraxuno = Seguimiento1.objects.values(filtro1,'producto').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_ctas=Sum('ctas')).order_by(filtro1)
    total_moraxuno_dict = {}
    for i in meses:
        for j in total_moraxuno:
            if i[filtro1] == j[filtro1]:
               total_moraxuno_dict[i[filtro1]]=j['sum_ctas']

    if filtro1 == 'trimestre_form':
        mora_uno = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        mora_uno = Seguimiento1.objects.values(filtro1,'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    mora460_uno_dict = {}; mora6_uno_dict = {}; mora9_uno_dict = {}; mora12_uno_dict = {};
    for i in meses_moras:
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    mora460_uno_dict[i[filtro1]]=j['sum_mora460']*100/total_moraxuno_dict[i[filtro1]]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_lista]:
                    mora460_uno_dict[i[filtro1]]=[]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora6]:
                    mora6_uno_dict[i[filtro1]]=j['sum_mora6']*100/total_moraxuno_dict[i[filtro1]]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora9]:
                    mora9_uno_dict[i[filtro1]]=j['sum_mora9']*100/total_moraxuno_dict[i[filtro1]]
                    break
        for j in mora_uno:
            if i[filtro1] == j[filtro1]:
                if i[filtro1] <= morames_list[num_mora12]:
                    mora12_uno_dict[i[filtro1]]=j['sum_mora12']*100/total_moraxuno_dict[i[filtro1]]
                    break

    if filtro1 == 'trimestre_form':
        total_morasxseg = Seguimiento1.objects.values(filtro1,'producto', 'segmento').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    else:
        total_morasxseg = Seguimiento1.objects.values(filtro1,'producto', 'segmento').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    totalxava_moras_dict = {}
    totalxms_moras_dict = {}
    totalxnoph_moras_dict = {}
    totalxnocli_moras_dict = {}
    for i in meses:
        for j in total_morasxseg:
            if i[filtro1] == j[filtro1]:
                if j['segmento']=='1.AVA':
                    totalxava_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['segmento']=='2.MS':
                    totalxms_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['segmento']=='3.NoPH':
                    totalxnoph_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['segmento']=='4.NoCli':
                    totalxnocli_moras_dict[i[filtro1]]=j['sum_mora']

    if filtro1 == 'trimestre_form':
        moras = Seguimiento1.objects.values(filtro1, 'segmento', 'producto').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        moras = Seguimiento1.objects.values(filtro1, 'segmento', 'producto').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    ava_mora460_dict = {}; ava_mora6_dict = {}; ava_mora9_dict = {}; ava_mora12_dict = {}
    ms_mora460_dict = {}; ms_mora6_dict = {}; ms_mora9_dict = {}; ms_mora12_dict = {}
    noph_mora460_dict = {}; noph_mora6_dict = {}; noph_mora9_dict = {}; noph_mora12_dict = {}
    nocli_mora460_dict = {}; nocli_mora6_dict = {}; nocli_mora9_dict = {}; nocli_mora12_dict = {}
    for i in meses:
       for j in moras:
          if i[filtro1] == j[filtro1]:
            if  j['segmento']=='1.AVA':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    ava_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxava_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    ava_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    ava_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxava_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    ava_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxava_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    ava_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxava_moras_dict[i[filtro1]]     
            elif  j['segmento']=='2.MS':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    ms_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxms_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    ms_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    ms_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxms_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    ms_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxms_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    ms_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxms_moras_dict[i[filtro1]]
            elif  j['segmento']=='3.NoPH':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    noph_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxnoph_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    noph_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    noph_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxnoph_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    noph_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxnoph_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    noph_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxnoph_moras_dict[i[filtro1]]
            elif  j['segmento']=='4.NoCli':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    nocli_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxnocli_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    nocli_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    nocli_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxnocli_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    nocli_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxnocli_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    nocli_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxnocli_moras_dict[i[filtro1]]

    if filtro1 == 'trimestre_form':
        moratot = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    else:
        moratot = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    dict_moratotms = {}; dict_moratotnoph = {}; dict_moratotnocl = {};
    for i in moratot:
        if i['segmento'] == '2.MS':
            dict_moratotms[i[filtro1]] = i['cuentas']
        if i['segmento'] == '3.NoPH':
            dict_moratotnoph[i[filtro1]] = i['cuentas']
        if i['segmento'] == '4.NoCli':
            dict_moratotnocl[i[filtro1]] = i['cuentas']

    if filtro1 == 'trimestre_form':
        morauno_seg = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    else:
        morauno_seg = Seguimiento1.objects.values(filtro1, 'segmento', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_moraunoms = {}; dict_moraunonoph = {}; dict_moraunonocli = {};
    for i in morauno_seg:
        if i[filtro1] <= morames_list[num_mora6]:
            if i['segmento'] == '2.MS':
                dict_moraunoms[i[filtro1]] = i['sum_mora6']*100/dict_moratotms[i[filtro1]]
    for i in morauno_seg:
        if i[filtro1] <= morames_list[num_mora6]:  
            if i['segmento'] == '3.NoPH':
                dict_moraunonoph[i[filtro1]] = i['sum_mora6']*100/dict_moratotnoph[i[filtro1]]
    for i in morauno_seg:
        if i[filtro1] <= morames_list[num_mora6]:
            if i['segmento'] == '4.NoCli':
                dict_moraunonocli[i[filtro1]] = i['sum_mora6']*100/dict_moratotnocl[i[filtro1]]

    if filtro1 == 'trimestre_form':
        total_morasxcat = Seguimiento1.objects.values(filtro1, 'producto', 'cat_persona').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    else:
        total_morasxcat = Seguimiento1.objects.values(filtro1, 'producto', 'cat_persona').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora=Sum('ctas')).order_by(filtro1)
    totalxdep_moras_dict = {}
    totalxind_moras_dict = {}
    totalxpnn_moras_dict = {}
    totalxnorec_moras_dict = {}
    for i in meses:
        for j in total_morasxcat:
            if i[filtro1] == j[filtro1]:
                if j['cat_persona']=='1. Dependiente':
                    totalxdep_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cat_persona']=='2. Independiente':
                    totalxind_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cat_persona']=='3. PNN':
                    totalxpnn_moras_dict[i[filtro1]]=j['sum_mora']
                elif j['cat_persona']=='4.No Reconocido':
                    totalxnorec_moras_dict[i[filtro1]]=j['sum_mora']

    if filtro1 == 'trimestre_form':
        morascat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        morascat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto').filter(producto='01 Consumo', riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora460=Sum('mora4_60'),sum_mora6=Sum('mora6'), sum_mora9=Sum('mora9'), sum_mora12=Sum('mora12')).order_by(filtro1)
    dep_mora460_dict = {}; dep_mora6_dict = {}; dep_mora9_dict = {}; dep_mora12_dict = {}
    indep_mora460_dict = {}; indep_mora6_dict = {}; indep_mora9_dict = {}; indep_mora12_dict = {}
    pnn_mora460_dict = {}; pnn_mora6_dict = {}; pnn_mora9_dict = {}; pnn_mora12_dict = {}
    norec_mora460_dict = {}; norec_mora6_dict = {}; norec_mora9_dict = {}; norec_mora12_dict = {}
    for i in meses:
       for j in morascat:
          if i[filtro1] == j[filtro1]:
            if  j['cat_persona']=='1. Dependiente':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    dep_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxdep_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    dep_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    dep_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxdep_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    dep_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxdep_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    dep_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxdep_moras_dict[i[filtro1]]     
            elif  j['cat_persona']=='2. Independiente':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    indep_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxind_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    indep_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    indep_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxind_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    indep_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxind_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    indep_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxind_moras_dict[i[filtro1]]
            elif  j['cat_persona']=='3. PNN':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    pnn_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxpnn_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    pnn_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    pnn_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxpnn_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    pnn_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxpnn_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    pnn_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxpnn_moras_dict[i[filtro1]]
            elif  j['cat_persona']=='4.No Reconocido':
                if i[filtro1] <= morames_list[num_mora4] and i[filtro1] >= morames_list[num_lista]:
                    norec_mora460_dict[i[filtro1]]=j['sum_mora460']*100/totalxnorec_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_lista]:
                    norec_mora460_dict[i[filtro1]]=[]
                if i[filtro1] <= morames_list[num_mora6]:
                    norec_mora6_dict[i[filtro1]]=j['sum_mora6']*100/totalxnorec_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora9]:
                    norec_mora9_dict[i[filtro1]]=j['sum_mora9']*100/totalxnorec_moras_dict[i[filtro1]]
                if i[filtro1] <= morames_list[num_mora12]:
                    norec_mora12_dict[i[filtro1]]=j['sum_mora12']*100/totalxnorec_moras_dict[i[filtro1]]

    if filtro1 == 'trimestre_form':
        moratot2 = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto','riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    else:
        moratot2 = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto','riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    dict_moratotdep = {};
    dict_moratotind = {};
    dict_moratotnoph = {};
    dict_moratotnocl = {};
    for i in moratot2:
        if i['cat_persona'] == '1. Dependiente':
            dict_moratotdep[i[filtro1]] = i['cuentas']
        if i['cat_persona'] == '2. Independiente':
            dict_moratotind[i[filtro1]] = i['cuentas']
        if i['cat_persona'] == '3. PNN':
            dict_moratotnoph[i[filtro1]] = i['cuentas']
        if i['cat_persona'] == '4.No Reconocido':
            dict_moratotnocl[i[filtro1]] = i['cuentas']

    if filtro1 == 'trimestre_form':
        morauno_cat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    else:
        morauno_cat = Seguimiento1.objects.values(filtro1, 'cat_persona', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='UNO A UNO', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6')).order_by(filtro1)
    dict_moracamdep = {}; dict_moracamind = {}; 
    dict_moracampnn = {}; dict_moracamnor = {};
    for i in morauno_cat:
        if i['cat_persona'] == '1. Dependiente':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracamdep[i[filtro1]] = i['sum_mora6']*100/dict_moratotdep[i[filtro1]]
        elif i['cat_persona'] == '2. Independiente':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracamind[i[filtro1]] = i['sum_mora6']*100/dict_moratotind[i[filtro1]]
        elif i['cat_persona'] == '3. PNN':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracampnn[i[filtro1]] = i['sum_mora6']*100/dict_moratotnoph[i[filtro1]]
        elif i['cat_persona'] == '4.No Reconocido':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moracamnor[i[filtro1]] = i['sum_mora6']*100/dict_moratotnocl[i[filtro1]]

    if filtro1 == 'trimestre_form':
        moraburo = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    else:
        moraburo = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(cuentas=Sum('ctas')).order_by(filtro1)
    dict_moraburo1 = {}; dict_moraburo2 = {};
    dict_moraburo3 = {}; dict_moraburo4 = {};
    for i in moraburo:
        if i['buro_camp'] == 'G1-G4':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo1[i[filtro1]] = i['cuentas']
        elif i['buro_camp'] == 'G5':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo2[i[filtro1]] = i['cuentas']
        elif i['buro_camp'] == 'G6-G8':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo3[i[filtro1]] = i['cuentas']
        elif i['buro_camp'] == 'NB':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_moraburo4[i[filtro1]] = i['cuentas']

    if filtro1 == 'trimestre_form':
        burog1 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='G1-G4', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog5 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='G5', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog6 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='G6-G8', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        buronb = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='NB', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burotot = Seguimiento1.objects.values(filtro1).filter(riesgos='CAMP', producto='01 Consumo').annotate(seg=Sum('form')).order_by(filtro1)
    else:
        burog1 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='G1-G4', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog5 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='G5', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burog6 = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='G6-G8', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        buronb = Seguimiento1.objects.values(filtro1, 'buro_camp').filter(riesgos='CAMP', producto='01 Consumo', buro_camp='NB', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        burotot = Seguimiento1.objects.values(filtro1).filter(riesgos='CAMP', producto='01 Consumo').annotate(seg=Sum('form')).order_by(filtro1)
    dict_burog1 = {}; dict_burog5 = {};
    dict_burog6 = {}; dict_buronb = {};
    for i in meses:
        for j in burog1:
            if i[filtro1] == j[filtro1]:
                dict_burog1[i[filtro1]] = j['seg']
                break
            else:
                dict_burog1[i[filtro1]] = 0
        for j in burog5:
            if i[filtro1] == j[filtro1]:
                dict_burog5[i[filtro1]] = j['seg']
                break
            else:
                dict_burog5[i[filtro1]] = 0
        for j in burog6:
            if i[filtro1] == j[filtro1]:
                dict_burog6[i[filtro1]] = j['seg']
                break
            else:
                dict_burog6[i[filtro1]] = 0
        for j in buronb:
            if i[filtro1] == j[filtro1]:
                dict_buronb[i[filtro1]] = j['seg']
                break
            else:
                dict_buronb[i[filtro1]] = 0

    if filtro1 == 'trimestre_form':
        mora6_buro = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6'), sum_mora12=Sum('mora12')).order_by(filtro1)
    else:
        mora6_buro = Seguimiento1.objects.values(filtro1, 'buro_camp', 'producto', 'riesgos').filter(producto='01 Consumo',riesgos='CAMP', periodo__gte=filtro2).annotate(sum_mora6=Sum('mora6'), sum_mora12=Sum('mora12')).order_by(filtro1)
    dict_mora6buro1 = {}; dict_mora6buro2 = {}; 
    dict_mora6buro3 = {}; dict_mora6buro4 = {};
    dict_mora12buro1 = {}; dict_mora12buro2 = {}; 
    dict_mora12buro3 = {}; dict_mora12buro4 = {};
    for i in mora6_buro:
        if i['buro_camp'] == 'G1-G4':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro1[i[filtro1]] = i['sum_mora6']*100/dict_moraburo1[i[filtro1]]
                dict_mora12buro1[i[filtro1]] = i['sum_mora12']*100/dict_moraburo1[i[filtro1]]
        if i['buro_camp'] == 'G5':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro2[i[filtro1]] = i['sum_mora6']*100/dict_moraburo2[i[filtro1]]
                dict_mora12buro2[i[filtro1]] = i['sum_mora12']*100/dict_moraburo2[i[filtro1]]
        if i['buro_camp'] == 'G6-G8':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro3[i[filtro1]] = i['sum_mora6']*100/dict_moraburo3[i[filtro1]]
                dict_mora12buro3[i[filtro1]] = i['sum_mora12']*100/dict_moraburo3[i[filtro1]]
        if i['buro_camp'] == 'NB':
            if i[filtro1] <= morames_list[num_mora6]:
                dict_mora6buro4[i[filtro1]] = i['sum_mora6']*100/dict_moraburo4[i[filtro1]]
                dict_mora12buro4[i[filtro1]] = i['sum_mora12']*100/dict_moraburo4[i[filtro1]]

    if filtro1 == 'trimestre_form':
        total_forzaje = Forzaje.objects.values(filtro1).filter(producto='01 Consumo').annotate(cantidad=Sum('form')).order_by(filtro1)
    else:
        total_forzaje = Forzaje.objects.values(filtro1).filter(producto='01 Consumo').annotate(cantidad=Sum('form')).order_by(filtro1)
    forzaje_dict = {}
    for i in meses:
       for j in total_forzaje:
           if i[filtro1] == j[filtro1]:
              forzaje_dict[j[filtro1]]=j['cantidad']

    if filtro1 == 'trimestre_form':
        forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '01 Consumo').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    else:
        forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '01 Consumo').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    duda_dict = {}
    rechazo_dict = {}
    for i in meses:
        for j in forzaje2:
            if i[filtro1] == j[filtro1]:
               if  j['dic_global']=='DU':
                    duda_dict[i[filtro1]]=j['cantidad']*100/forzaje_dict[i[filtro1]]
                    break
            else:
                duda_dict[i[filtro1]]= 0
        for j in forzaje2:
            if i[filtro1] == j[filtro1]:
               if  j['dic_global']=='RE':
                    rechazo_dict[i[filtro1]]=j['cantidad']*100/forzaje_dict[i[filtro1]]
                    break
            else:
                rechazo_dict[i[filtro1]]= 0

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_pld.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_auto(request):
    meses_total = Seguimiento.objects.values_list('mes_vigencia', flat=True).distinct().order_by('-mes_vigencia')
    time = []
    for i in meses_total:
        time.append(i)

    meses = Seguimiento.objects.values_list('mes_vigencia', flat=True).filter(mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).distinct().order_by('mes_vigencia')
    form = Seguimiento.objects.values('mes_vigencia', 'producto').filter(producto='02 Auto',origen__in=['UNO A UNO','REGULAR'],mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    form_dict = {}
    for j in form:
      form_dict[j['mes_vigencia']]=j['formalizado']
    uno_form = Seguimiento.objects.values('mes_vigencia','origen').filter(producto='02 Auto', origen='UNO A UNO',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_reg = Seguimiento.objects.values('mes_vigencia','origen').filter(producto='02 Auto', origen='REGULAR',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    uno_form_dict={}; camp_reg_dict={};
    for i in meses:
      for j in uno_form:
        if i == j['mes_vigencia']:
          uno_form_dict[i]=j['formalizado']
    for i in meses:
      for j in camp_reg:
        if i == j['mes_vigencia']:
          camp_reg_dict[i]=j['formalizado']

    fact_uno = Seguimiento.objects.values('mes_vigencia','producto').filter(producto='02 Auto', riesgos='UNO A UNO',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    fact_camp = Seguimiento.objects.values('mes_vigencia','producto').filter(producto='02 Auto', riesgos='CAMP',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    fact_uno_dict={}; fact_camp_dict={};
    for i in meses:
      for j in fact_uno:
        if i == j['mes_vigencia']:
          fact_uno_dict[i]=j['facturacion']
    for i in meses:
      for j in fact_camp:
        if i == j['mes_vigencia']:
          fact_camp_dict[i]=j['facturacion']

    total_form = Seguimiento.objects.values('mes_vigencia', 'producto').filter(producto='02 Auto',origen__in=['UNO A UNO','REGULAR','FAST'],mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    total_form_dict = {}
    for j in total_form:
      total_form_dict[j['mes_vigencia']]=j['formalizado']

    rangos = Seguimiento.objects.values('mes_vigencia','producto', 'rng_ing').filter(mes_vigencia__gte=time[12], mes_vigencia__lte =time[0],producto='02 Auto').annotate(num_rango=Sum('form')).order_by('mes_vigencia')
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {}
    rango4_dict = {}; rango5_dict = {}; rango6_dict = {}
    for i in meses:
	for j in rangos:
	   if i == j['mes_vigencia']:
		if j['rng_ing'] == '01 [3.5K - ...]':
		   rango1_dict[i]=j['num_rango']*100/total_form_dict[i]
		elif j['rng_ing'] == '02 [2.5K - 3.5K]':
		   rango2_dict[i]=j['num_rango']*100/total_form_dict[i]
		elif j['rng_ing'] == '03 [2K - 2.5K]':
		   rango3_dict[i]=j['num_rango']*100/total_form_dict[i]
		elif j['rng_ing'] == '04 [1.5K - 2K]':
		   rango4_dict[i]=j['num_rango']*100/total_form_dict[i]
		elif j['rng_ing'] == '05 [1K - 1.5K]':
		   rango5_dict[i]=j['num_rango']*100/total_form_dict[i]
		if j['rng_ing'] == '06 [0 - 1K]':
		   rango6_dict[i]=j['num_rango']*100/total_form_dict[i]
		else:
		   rango6_dict[i]=0

    meses_moras = Seguimiento.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    num_mora6 = 6 
    num_mora9 = 9 
    num_mora12 = 12 

    morames_list = []
    for i in meses_moras:
        morames_list.append(i['mes_vigencia'])
    
    mora6 = Seguimiento.objects.values('mes_vigencia').filter(producto='02 Auto').annotate(sum_mora=Sum('mora6'),cuentas=Sum('ctas')).order_by('mes_vigencia')
    mora9 = Seguimiento.objects.values('mes_vigencia').filter(producto='02 Auto').annotate(sum_mora=Sum('mora9'),cuentas=Sum('ctas')).order_by('mes_vigencia')
    mora12 = Seguimiento.objects.values('mes_vigencia').filter(producto='02 Auto').annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by('mes_vigencia')
    mora6_dict = {}; mora9_dict = {}; mora12_dict = {};
    for j in mora6:
        if j['mes_vigencia'] <= morames_list[num_mora6]:
            mora6_dict[j['mes_vigencia']]=j['sum_mora']*100/j['cuentas']
    for j in mora9:
        if j['mes_vigencia'] <= morames_list[num_mora9]:
            mora9_dict[j['mes_vigencia']]=j['sum_mora']*100/j['cuentas']
    for j in mora12:
        if j['mes_vigencia'] <= morames_list[num_mora12]:
            mora12_dict[j['mes_vigencia']]=j['sum_mora']*100/j['cuentas']

    duda = Forzaje.objects.values('mes_vigencia').filter(producto='02 Auto',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0], dic_global='DU').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    rechazo = Forzaje.objects.values('mes_vigencia').filter(producto='02 Auto',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0], dic_global='RE').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    total_forzaje = Forzaje.objects.values('mes_vigencia').filter(producto='02 Auto',mes_vigencia__gte=time[12], mes_vigencia__lte=time[0]).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    forzaje = zip(duda,rechazo,total_forzaje)

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_auto.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def resumen_seguimiento(request):
    meses_total = Seguimiento1.objects.values('mes_vigencia').distinct('mes_vigencia').order_by('-mes_vigencia')
    time = []
    for i in meses_total:
        time.append(i['mes_vigencia'])

    form_total= Seguimiento1.objects.values('mes_vigencia').filter(periodo=('2016')).annotate(cantidad=Sum('form'),factura=Sum('facturacion')).order_by('mes_vigencia')
    form_producto = Seguimiento1.objects.values('mes_vigencia','producto').filter(periodo=('2016')).annotate(cantidad=Sum('form'),factura=Sum('facturacion')).order_by('mes_vigencia')
    pldform_dict={}; autoform_dict={}; tdcform_dict={}; hipoform_dict={};
    for i in form_producto:
      if i['producto'] == '01 Consumo':
        pldform_dict[i['mes_vigencia']]=i['cantidad']
      if i['producto'] == '02 Auto':
        autoform_dict[i['mes_vigencia']]=i['cantidad']
      if i['producto'] == '03 Tarjeta':
        tdcform_dict[i['mes_vigencia']]=i['cantidad']
      if i['producto'] == '04 Hipotecario':
        hipoform_dict[i['mes_vigencia']]=i['cantidad']

    form_producto2015 = Seguimiento1.objects.values('periodo','producto').filter(periodo=('2015')).exclude(mes_vigencia='201512').annotate(cantidad=Sum('form'),factura=Sum('facturacion')).order_by('producto')
    form_producto2016 = Seguimiento1.objects.values('periodo','producto').filter(periodo=('2016')).annotate(cantidad=Sum('form'),factura=Sum('facturacion')).order_by('producto')

    form_cluster2015 = Seguimiento1.objects.values('periodo','cluster').filter(periodo=('2015')).exclude(mes_vigencia='201512').exclude(cluster__in=['0. S.D.','1. Modestos','2. Desligados']).annotate(cantidad=Sum('form'),factura=Sum('facturacion')).order_by('cluster')
    form_cluster2016 = Seguimiento1.objects.values('periodo','cluster').filter(periodo=('2016')).exclude(cluster__in=['0. S.D.','1. Modestos','2. Desligados']).annotate(cantidad=Sum('form'),factura=Sum('facturacion')).order_by('cluster')

    mes_inicial = '201411'
    mes_final = '201511'
    mora_productoxprogre = Seguimiento1.objects.values('producto','cluster').filter(mes_vigencia__gte=mes_inicial,mes_vigencia__lte=mes_final,cluster='3. Progresistas').annotate(mora=Sum('mora12'),cuentas=Sum('ctas')).order_by('producto')
    mora_productoxaspi = Seguimiento1.objects.values('producto','cluster').filter(mes_vigencia__gte=mes_inicial,mes_vigencia__lte=mes_final, cluster='4. Aspirantes').annotate(mora=Sum('mora12'),cuentas=Sum('ctas')).order_by('producto')
    mora_productoxprospe = Seguimiento1.objects.values('producto','cluster').filter(mes_vigencia__gte=mes_inicial,mes_vigencia__lte=mes_final, cluster='5. Prosperos').annotate(mora=Sum('mora12'),cuentas=Sum('ctas')).order_by('producto')

    mes_inicial2 = '201311'
    mes_final2 = '201411'
    mora_productoxprogre2 = Seguimiento1.objects.values('producto','cluster').filter(mes_vigencia__gte=mes_inicial2,mes_vigencia__lte=mes_final2,cluster='3. Progresistas').annotate(mora=Sum('mora12'),cuentas=Sum('ctas')).order_by('producto')
    mora_productoxaspi2 = Seguimiento1.objects.values('producto','cluster').filter(mes_vigencia__gte=mes_inicial2,mes_vigencia__lte=mes_final2, cluster='4. Aspirantes').annotate(mora=Sum('mora12'),cuentas=Sum('ctas')).order_by('producto')
    mora_productoxprospe2 = Seguimiento1.objects.values('producto','cluster').filter(mes_vigencia__gte=mes_inicial2,mes_vigencia__lte=mes_final2, cluster='5. Prosperos').annotate(mora=Sum('mora12'),cuentas=Sum('ctas')).order_by('producto')

    form_segmento = Seguimiento1.objects.values('mes_vigencia','segmento').filter(periodo='2016').exclude(segmento__in=['AVA','PNN']).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    ava_dict={}; ms_dict={}; noph_dict={}; nocli_dict={};
    for i in form_segmento:
      if i['segmento'] == '1.AVA':
        ava_dict[i['mes_vigencia']]=i['cantidad']
      if i['segmento'] == '2.MS':
        ms_dict[i['mes_vigencia']]=i['cantidad']
      if i['segmento'] == '3.NoPH':
        noph_dict[i['mes_vigencia']]=i['cantidad']
      if i['segmento'] == '4.NoCli':
        nocli_dict[i['mes_vigencia']]=i['cantidad']
    form_segmento2015 = Seguimiento1.objects.values('periodo','segmento').filter(periodo='2015').exclude(segmento__in=['AVA','PNN']).exclude(mes_vigencia='201512').annotate(cantidad=Sum('form')).order_by('segmento')
    form_segmento2016 = Seguimiento1.objects.values('periodo','segmento').filter(periodo='2016').exclude(segmento__in=['AVA','PNN']).annotate(cantidad=Sum('form')).order_by('segmento')

    form_buro = Seguimiento1.objects.values('mes_vigencia','buro_camp').filter(periodo='2016').exclude(buro_camp__in=['','AL','AP',' ']).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    buro1_dict={}; buro2_dict={}; buro3_dict={}; buro4_dict={};
    for i in form_buro:
      if i['buro_camp'] == 'G1-G4':
        buro1_dict[i['mes_vigencia']]=i['cantidad']
      if i['buro_camp'] == 'G5':
        buro2_dict[i['mes_vigencia']]=i['cantidad']
      if i['buro_camp'] == 'G6-G8':
        buro3_dict[i['mes_vigencia']]=i['cantidad']
      if i['buro_camp'] == 'NB':
        buro4_dict[i['mes_vigencia']]=i['cantidad']
    print buro2_dict
    form_buro2015 = Seguimiento1.objects.values('periodo','buro_camp').filter(periodo='2015').exclude(buro_camp__in=['','AL','AP',' ']).exclude(mes_vigencia='201512').annotate(cantidad=Sum('form')).order_by('buro_camp')
    form_buro2016 = Seguimiento1.objects.values('periodo','buro_camp').filter(periodo='2016').exclude(buro_camp__in=['','AL','AP',' ']).annotate(cantidad=Sum('form')).order_by('buro_camp')

    form_forzaje = Forzaje.objects.values('mes_vigencia','dic_global').filter(periodo='2016').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    duda_dict={}; rechazo_dict={}; 
    for i in form_forzaje:
      if i['dic_global'] == 'DU':
        duda_dict[i['mes_vigencia']]=i['cantidad']
      if i['dic_global'] == 'RE':
        rechazo_dict[i['mes_vigencia']]=i['cantidad']
    form_forzaje2 = Forzaje.objects.values('mes_vigencia','dic_global').filter(periodo='2015').exclude(dic_global='AP').exclude(mes_vigencia='201512').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    duda2_dict={}; rechazo2_dict={}; 
    for i in form_forzaje2:
      if i['dic_global'] == 'DU':
        duda2_dict[i['mes_vigencia']]=i['cantidad']
      if i['dic_global'] == 'RE':
        rechazo2_dict[i['mes_vigencia']]=i['cantidad']
    form_forzaje2015 = Forzaje.objects.values('periodo', 'dic_global').filter(periodo='2015').exclude(dic_global='AP').exclude(mes_vigencia='201512').annotate(cantidad=Sum('form')).order_by('dic_global')
    form_forzaje2016 = Forzaje.objects.values('periodo', 'dic_global').filter(periodo='2016').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by('dic_global')

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/resumen_seguimiento.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def resumen_campanas(request):
    ofertas_tdc_pld = Campana2.objects.values('mes_vigencia').filter(mes_vigencia__gte='201601',mes_vigencia__lte='201611').annotate(cantidad_tdc=Sum('q_tc'),cantidad_pld=Sum('q_pld'))
    formal_tdc_pld = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto__in=['01 Consumo','03 Tarjeta'],mes_vigencia__gte='201601',mes_vigencia__lte='201611').annotate(cantidad=Sum('form'))
    efecxtdc = {}; efecxpld ={};
    for i in formal_tdc_pld:
      for j in ofertas_tdc_pld:
        if i['mes_vigencia'] == j['mes_vigencia']:
          if i['producto'] == '01 Consumo':          
            efecxpld[i['mes_vigencia']] = i['cantidad']*100/j['cantidad_pld']
          if i['producto'] == '03 Tarjeta':          
            efecxtdc[i['mes_vigencia']] = i['cantidad']*100/j['cantidad_pld']
    ofertas_tdc_pld2015 = Campana2.objects.values('mes_vigencia').filter(mes_vigencia__gte='201501',mes_vigencia__lte='201511').annotate(cantidad_tdc=Sum('q_tc'),cantidad_pld=Sum('q_pld'))
    formal_tdc_pld2015 = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto__in=['01 Consumo','03 Tarjeta'],mes_vigencia__gte='201501',mes_vigencia__lte='201511').annotate(cantidad=Sum('form'))
    efecxtdc2015 = {}; efecxpld2015 ={};
    for i in formal_tdc_pld2015:
      for j in ofertas_tdc_pld2015:
        if i['mes_vigencia'] == j['mes_vigencia']:
          if i['producto'] == '01 Consumo':          
            efecxpld2015[i['mes_vigencia']] = i['cantidad']*100/j['cantidad_pld']
          if i['producto'] == '03 Tarjeta':          
            efecxtdc2015[i['mes_vigencia']] = i['cantidad']*100/j['cantidad_pld']

    ofertas_tdc_pld2015 = Campana2.objects.all().filter(mes_vigencia__gte='201501',mes_vigencia__lte='201511').aggregate(cantidad_tdc=Sum('q_tc'),cantidad_pld=Sum('q_pld'),suma_tdc=Sum('monto_tc'),suma_pld=Sum('monto_pld'))
    ofertas_tdc_pld2016 = Campana2.objects.all().filter(mes_vigencia__gte='201601',mes_vigencia__lte='201611').aggregate(cantidad_tdc=Sum('q_tc'),cantidad_pld=Sum('q_pld'),suma_tdc=Sum('monto_tc'),suma_pld=Sum('monto_pld'))

    ofertas_seg2015 = Campana2.objects.values('segmento').filter(mes_vigencia__gte='201501',mes_vigencia__lte='201511',segmento__in=['AVA','MS','No PH','NoCli']).annotate(cantidad_tdc=Sum('q_tc'),cantidad_pld=Sum('q_pld'),suma_tdc=Sum('monto_tc'))
    ofertas_seg2016 = Campana2.objects.values('segmento').filter(mes_vigencia__gte='201601',mes_vigencia__lte='201611',segmento__in=['AVA','MS','No PH','NoCli']).annotate(cantidad_tdc=Sum('q_tc'),cantidad_pld=Sum('q_pld'),suma_tdc=Sum('monto_tc'))
    
    meses = EfectividadTC.objects.values('mes_vigencia').distinct().order_by('mes_vigencia')
    categorias2015 = EfectividadTC.objects.values('tipo_clie').filter(mes_vigencia__lte='201512').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('tipo_clie')
    categorias2016 = EfectividadTC.objects.values('tipo_clie').filter(mes_vigencia__gte='201601').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('tipo_clie')
    categorias = EfectividadTC.objects.values('mes_vigencia','tipo_clie').filter(mes_vigencia__gte='201601').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    dict_dep = {}; dict_indep = {}; dict_pnn = {}; dict_nr = {};
    for i in meses:
      for j in categorias:
        if i['mes_vigencia'] == j['mes_vigencia']:
          if j['tipo_clie'] == 'DEPENDIENTE':
            dict_dep[i['mes_vigencia']] = j['cant_tc']
          elif j['tipo_clie'] == 'INDEPENDIENTE':
            dict_indep[i['mes_vigencia']] = j['cant_tc']
          elif j['tipo_clie'] == 'PNN':
            dict_pnn[i['mes_vigencia']] = j['cant_tc']
          elif j['tipo_clie'] == 'NO RECONOCIDO':
            dict_nr[i['mes_vigencia']] = j['cant_tc']
          else:
            dict_dep[i['mes_vigencia']] = 0
            dict_indep[i['mes_vigencia']] = 0
            dict_pnn[i['mes_vigencia']] = 0
            dict_nr[i['mes_vigencia']] = 0

    buro1 = EfectividadTC.objects.values('mes_vigencia').filter(buro__in=['G1','G2','G3','G4'],mes_vigencia__gte='201601').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro1_dict = {}; ticket_buro1 = {};
    for i in buro1:
        buro1_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro1[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']

    buro2 = EfectividadTC.objects.values('mes_vigencia',).filter(buro__in=['G5'],mes_vigencia__gte='201601').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro2_dict = {}; ticket_buro2 = {};
    for i in buro2:
        buro2_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro2[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']

    buro3 = EfectividadTC.objects.values('mes_vigencia').filter(buro__in=['G6','G7','G8'],mes_vigencia__gte='201601').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro3_dict = {}; ticket_buro3 = {};
    for i in buro3:
        buro3_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro3[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']

    buro4 = EfectividadTC.objects.values('mes_vigencia',).filter(buro__in=['NB'],mes_vigencia__gte='201601').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro4_dict = {}; ticket_buro4 = {};
    for i in buro4:
        buro4_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro4[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']

    buro1_2015 = EfectividadTC.objects.filter(buro__in=['G1','G2','G3','G4'],mes_vigencia__lte='201512').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))
    buro2_2015 = EfectividadTC.objects.filter(buro__in=['G5'],mes_vigencia__lte='201512').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))
    buro3_2015 = EfectividadTC.objects.filter(buro__in=['G6','G7','G8'],mes_vigencia__lte='201512').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))
    buro4_2015 = EfectividadTC.objects.filter(buro__in=['NB'],mes_vigencia__lte='201512').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))

    buro1_2016 = EfectividadTC.objects.filter(buro__in=['G1','G2','G3','G4'],mes_vigencia__gte='201601').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))
    buro2_2016 = EfectividadTC.objects.filter(buro__in=['G5'],mes_vigencia__gte='201601').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))
    buro3_2016 = EfectividadTC.objects.filter(buro__in=['G6','G7','G8'],mes_vigencia__gte='201601').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))
    buro4_2016 = EfectividadTC.objects.filter(buro__in=['NB'],mes_vigencia__gte='201601').aggregate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form'))

    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/resumen_campanas.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_adelanto(request):
    control_fecha = AdelantoSueldo.objects.values_list('mes_vigencia', flat=True).distinct().order_by('-mes_vigencia')
    time = []
    for i in control_fecha:
        time.append(i)
    fecha1= time[0]
    total_form = AdelantoSueldo.objects.values('mes_vigencia').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    ticket = AdelantoSueldo.objects.values('mes_vigencia').annotate(formalizado=Sum('fact')).order_by('mes_vigencia')
    formalizados = zip(total_form,ticket)
    
    meses = AdelantoSueldo.objects.values_list('mes_vigencia', flat=True).distinct().order_by('mes_vigencia')
    total_rango = AdelantoSueldo.objects.values('mes_vigencia').exclude(rng_suelgo='00 Sin Inf').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango_tot = {}
    for i in total_rango:
	rango_tot[i['mes_vigencia']]=i['formalizado']
    rango1 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo__in=['01 [0 - 700>','02 [700 - 1000]']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i == j['mes_vigencia']:
             rango1_dict[i]=j['formalizado']*100/rango_tot[i]
	     break
       	  else:
             rango1_dict[i]= 0
    rango2 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='03 [1001 - 1500]').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i == j['mes_vigencia']:
             rango2_dict[i]=j['formalizado']*100/rango_tot[i]
	     break
       	  else:
             rango2_dict[i]= 0
    rango3 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='04 [1501 - 2000]').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i == j['mes_vigencia']:
             rango3_dict[i]=j['formalizado']*100/rango_tot[i]
	     break
       	  else:
             rango3_dict[i]= 0
    rango4 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='05 [2001 - 2500]').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i == j['mes_vigencia']:
             rango4_dict[i]=j['formalizado']*100/rango_tot[i]
	     break
       	  else:
             rango4_dict[i]= 0
    rango5 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='06 [2501 - 3500]').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i == j['mes_vigencia']:
             rango5_dict[i]=j['formalizado']*100/rango_tot[i]
	     break
       	  else:
             rango5_dict[i]= 0
    rango6 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo__in=['07 [3501 - Mas>','07 [3501 - 5000]','08 [5001 - Mas>']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i == j['mes_vigencia']:
             rango6_dict[i]=j['formalizado']*100/rango_tot[i]
             break
       	  else:
             rango6_dict[i]= 0

    total_form = AdelantoSueldo.objects.values('mes_vigencia').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    total_dict = {}
    for j in total_form:
        total_dict[j['mes_vigencia']] = j['formalizado']
    
    laboral = AdelantoSueldo.objects.values('mes_vigencia','laboral').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    dep_dict = {}; indep_dict = {}; pnn_dict = {}; nr_dict = {};
    totdep_dict = {}; totindep_dict = {}; totpnn_dict = {}; totnr_dict = {};
    for i in meses:
        for j in laboral:
            if i == j['mes_vigencia']:
                if j['laboral'] == '1. Dependiente':
                    dep_dict[i]=j['formalizado']*100/total_dict[i]
                    totdep_dict[i]=j['formalizado']
                if j['laboral'] == '2. Independiente':
                    indep_dict[i]=j['formalizado']*100/total_dict[i]
                    totindep_dict[i]=j['formalizado']
                if j['laboral'] == '3. PNN':
                    pnn_dict[i]=j['formalizado']*100/total_dict[i]
                    totpnn_dict[i]=j['formalizado']
                if j['laboral'] == '4.No Reconocido':
                    nr_dict[i]=j['formalizado']*100/total_dict[i]
                    totnr_dict[i]=j['formalizado']


    buro1 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='[G1-G4]').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}; buro1_tot = {};
    for i in meses:
       for j in buro1:
          if i == j['mes_vigencia']:
             buro1_dict[i]=j['formalizado']*100/rango_tot[i]
             buro1_tot[i]=j['formalizado']
             break
       	  else:
             buro1_dict[i]= 0
    buro2 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='G5').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}; buro2_tot = {};
    for i in meses:
       for j in buro2:
          if i == j['mes_vigencia']:
             buro2_dict[i]=j['formalizado']*100/rango_tot[i]
             buro2_tot[i]=j['formalizado']
             break
       	  else:
             buro2_dict[i]= 0
    buro3 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='[G6-G8]').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}; buro3_tot = {};
    for i in meses:
       for j in buro3:
          if i == j['mes_vigencia']:
             buro3_dict[i]=j['formalizado']*100/rango_tot[i]
             buro3_tot[i]=j['formalizado']
             break
       	  else:
             buro3_dict[i]= 0
    buro4 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='NB').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}; buro4_tot = {};
    for i in meses:
       for j in buro4:
          if i == j['mes_vigencia']:
             buro4_dict[i]=j['formalizado']*100/rango_tot[i]
             buro4_tot[i]=j['formalizado']
             break
       	  else:
             buro4_dict[i]= 0

    meses_sit =AdelantoSueldo.objects.values('mes_vigencia').filter( mes_vigencia__lte =time[2]).order_by('mes_vigencia')

    mora30 = AdelantoSueldo.objects.values('mes_vigencia').filter( mes_vigencia__lte =time[2]).annotate(formalizado=Sum('mora')).order_by('mes_vigencia')
    mora = itertools.izip_longest(mora30,total_rango,fillvalue='0')
    mora30_dict1 = {}
    mora30_dict2 = {}
    for i in meses_sit:
       for j in mora30:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora30_dict1[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             mora30_dict2[i['mes_vigencia']]=j['formalizado']
             break
       	  else:
             mora30_dict1[i['mes_vigencia']]= 0
             mora30_dict2[i['mes_vigencia']]= 0

    total_sit =AdelantoSueldo.objects.values('mes_vigencia').filter( mes_vigencia__lte =time[2]).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sit_total = {}
    for i in total_sit:
	sit_total[i['mes_vigencia']]=i['formalizado']

    sueldo1 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[2],rng_suelgo__in=['01 [0 - 700>','02 [700 - 1000]','03 [1001 - 1500]']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sueldo2 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[2],rng_suelgo__in=['04 [1501 - 2000]','05 [2001 - 2500]']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sueldo3 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[2],rng_suelgo__in=['06 [2501 -3500]','07 [3501 - 3500]','08 [5001 - Mas>']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sueldo1_dict = {} 
    sueldo2_dict = {} 
    sueldo3_dict = {}
    for i in meses_sit:
        for j in sueldo1:
            if i['mes_vigencia'] == j['mes_vigencia']:
                sueldo1_dict[i['mes_vigencia']]=j['formalizado']
                break
            else:
                sueldo1_dict[i['mes_vigencia']]= 0
        for j in sueldo2:
            if i['mes_vigencia'] == j['mes_vigencia']:
                sueldo2_dict[i['mes_vigencia']]=j['formalizado']
                break
            else:
                sueldo2_dict[i['mes_vigencia']]= 0
        for j in sueldo3:
            if i['mes_vigencia'] == j['mes_vigencia']:
                sueldo3_dict[i['mes_vigencia']]=j['formalizado']
                break
            else:
                sueldo3_dict[i['mes_vigencia']]= 0

    mora0 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[2],rng_suelgo__in=['01 [0 - 700>','02 [700 - 1000]','03 [1001 - 1500]']).annotate(formalizado=Sum('mora')).order_by('mes_vigencia')
    mora1 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[2],rng_suelgo__in=['04 [1501 - 2000]','05 [2001 - 2500]']).annotate(formalizado=Sum('mora')).order_by('mes_vigencia')
    mora2 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[2],rng_suelgo__in=['06 [2501 -3500]','07 [3501 - 3500]','08 [5001 - Mas>']).annotate(formalizado=Sum('mora')).order_by('mes_vigencia')
    mora0_dict = {} 
    mora1_dict = {} 
    mora2_dict = {} 
    for i in meses_sit:
       for j in mora0:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora0_dict[i['mes_vigencia']]=j['formalizado']*100/sueldo1_dict[i['mes_vigencia']]
             break
       	  else:
             mora0_dict[i['mes_vigencia']]= 0
       for j in mora1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora1_dict[i['mes_vigencia']]=j['formalizado']*100/sueldo2_dict[i['mes_vigencia']]
             break
       	  else:
             mora1_dict[i['mes_vigencia']]= 0
       for j in mora2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora2_dict[i['mes_vigencia']]=j['formalizado']*100/sueldo3_dict[i['mes_vigencia']]
             break
       	  else:
             mora2_dict[i['mes_vigencia']]= 0

    moradep = AdelantoSueldo.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[2],laboral='1. Dependiente').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    moraindep = AdelantoSueldo.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[2],laboral='2. Independiente').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    morapnn = AdelantoSueldo.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[2],laboral='3. PNN').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    moranr = AdelantoSueldo.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[2],laboral='4.No Reconocido').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    moradep_dict = {}; morainde_dict={}; morapnn_dict = {}; moranr_dict = {};
    for i in meses_sit:
        for j in moradep:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moradep_dict[i['mes_vigencia']] = j['mora']*100/totdep_dict[i['mes_vigencia']]
                break
            else:
                moradep_dict[i['mes_vigencia']] = 0
        for j in moraindep:
            if i['mes_vigencia'] == j['mes_vigencia']:
                morainde_dict[i['mes_vigencia']] = j['mora']*100/totindep_dict[i['mes_vigencia']]
                break
            else:
                morainde_dict[i['mes_vigencia']] = 0
        for j in morapnn:
            if i['mes_vigencia'] == j['mes_vigencia']:
                morapnn_dict[i['mes_vigencia']] = j['mora']*100/totpnn_dict[i['mes_vigencia']]
                break
            else:
                morapnn_dict[i['mes_vigencia']] = 0
        for j in moranr:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moranr_dict[i['mes_vigencia']] = j['mora']*100/totnr_dict[i['mes_vigencia']]
                break
            else:
                moranr_dict[i['mes_vigencia']] = 0

    moraburo1= AdelantoSueldo.objects.values('mes_vigencia','rng_buro').filter(mes_vigencia__lte =time[2],rng_buro='[G1-G4]').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    moraburo2 = AdelantoSueldo.objects.values('mes_vigencia','rng_buro').filter(mes_vigencia__lte =time[2],rng_buro='G5').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    moraburo3 = AdelantoSueldo.objects.values('mes_vigencia','rng_buro').filter(mes_vigencia__lte =time[2],rng_buro='[G6-G8]').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    moraburo4 = AdelantoSueldo.objects.values('mes_vigencia','rng_buro').filter(mes_vigencia__lte =time[2],rng_buro='NB').annotate(mora=Sum('mora')).order_by('mes_vigencia')
    moraburo1_dict = {}; moraburo2_dict={}; moraburo3_dict = {}; moraburo4_dict = {};
    for i in meses_sit:
        for j in moraburo1:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moraburo1_dict[i['mes_vigencia']] = j['mora']*100/buro1_tot[i['mes_vigencia']]
                break
            else:
                moraburo1_dict[i['mes_vigencia']] = 0
        for j in moraburo2:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moraburo2_dict[i['mes_vigencia']] = j['mora']*100/buro2_tot[i['mes_vigencia']]
                break
            else:
                moraburo2_dict[i['mes_vigencia']] = 0
        for j in moraburo3:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moraburo3_dict[i['mes_vigencia']] = j['mora']*100/buro3_tot[i['mes_vigencia']]
                break
            else:
                moraburo3_dict[i['mes_vigencia']] = 0
        for j in moraburo4:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moraburo4_dict[i['mes_vigencia']] = j['mora']*100/buro4_tot[i['mes_vigencia']]
                break
            else:
                moraburo4_dict[i['mes_vigencia']] = 0
    

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
    meses = PrestInmediato.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    form = PrestInmediato.objects.values('mes_vigencia').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form_dict = {}
    for i in form:
        form_dict[i['mes_vigencia']] = i['cantidad']

    fact = PrestInmediato.objects.values('mes_vigencia').annotate(cantidad=Sum('fact')).order_by('mes_vigencia')
    ticket_ava = PrestInmediato.objects.values('mes_vigencia').filter(segmento='1.AVA').annotate(cantidad=Sum('ctas'), cantidad2=Sum('fact')).order_by('mes_vigencia')
    ticket_ms = PrestInmediato.objects.values('mes_vigencia').filter(segmento='2.MS').annotate(cantidad=Sum('ctas'), cantidad2=Sum('fact')).order_by('mes_vigencia')

    total_rango = PrestInmediato.objects.values('mes_vigencia').annotate(cantidad=Sum('ctas')).exclude(rng_ingreso__in=['','NULL','06 [0 - 1k]']).order_by('mes_vigencia')
    rango_tot = {}
    for i in total_rango:
	   rango_tot[i['mes_vigencia']]=i['cantidad']

    rango1 = PrestInmediato.objects.values('mes_vigencia').filter(rng_ingreso='05 [1K - 1.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = PrestInmediato.objects.values('mes_vigencia').filter(rng_ingreso='04 [1.5K - 2K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = PrestInmediato.objects.values('mes_vigencia').filter(rng_ingreso='03 [2K - 2.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = PrestInmediato.objects.values('mes_vigencia').filter(rng_ingreso='02 [2.5K - 3.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = PrestInmediato.objects.values('mes_vigencia').filter(rng_ingreso='01 [3.5K - ...]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    total_rango2 = PrestInmediato.objects.values('mes_vigencia').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango_tot2 = {}
    for i in total_rango2:
	   rango_tot2[i['mes_vigencia']]=i['cantidad']
    buro1 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='[G1-G4]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='G5').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='[G6-G8]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='NB').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0

    total = PrestInmediato.objects.values('mes_vigencia').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    total_dict = {};
    for i in total:
        total_dict[i['mes_vigencia']] = i['formalizado']

    dependiente = PrestInmediato.objects.values('mes_vigencia','laboral').filter(laboral='1. Dependiente').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    independiente = PrestInmediato.objects.values('mes_vigencia','laboral').filter(laboral='2. Independiente').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    pnn = PrestInmediato.objects.values('mes_vigencia','laboral').filter(laboral='3. PNN').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    no_reconocido = PrestInmediato.objects.values('mes_vigencia','laboral').filter(laboral='4.No Reconocido').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    dep_dict = {}; indep_dict = {}; pnn_dict = {}; nr_dict = {};
    totdep_dict = {}; totindep_dict = {}; totpnn_dict = {}; totnr_dict = {};
    for i in meses_tot:
        for j in dependiente:
            if i['mes_vigencia'] == j['mes_vigencia']:
                dep_dict[i['mes_vigencia']]=j['formalizado']*100/total_dict[i['mes_vigencia']]
                totdep_dict[i['mes_vigencia']]=j['formalizado']
                break
            else:
                dep_dict[i['mes_vigencia']]=0
        for j in independiente:
            if i['mes_vigencia'] == j['mes_vigencia']:
                indep_dict[i['mes_vigencia']]=j['formalizado']*100/total_dict[i['mes_vigencia']]
                totindep_dict[i['mes_vigencia']]=j['formalizado']
                break
            else:
                indep_dict[i['mes_vigencia']]=0
        for j in pnn:
            if i['mes_vigencia'] == j['mes_vigencia']:
                pnn_dict[i['mes_vigencia']]=j['formalizado']*100/total_dict[i['mes_vigencia']]
                totpnn_dict[i['mes_vigencia']]=j['formalizado']
                break
            else:
                pnn_dict[i['mes_vigencia']]=0
        for j in no_reconocido:
            if i['mes_vigencia'] == j['mes_vigencia']:
                nr_dict[i['mes_vigencia']]=j['formalizado']*100/total_dict[i['mes_vigencia']]
                totnr_dict[i['mes_vigencia']]=j['formalizado']
                break
            else:
                nr_dict[i['mes_vigencia']]=0

    
    meses_sit =PrestInmediato.objects.values('mes_vigencia').filter( mes_vigencia__lte =time[6]).order_by('mes_vigencia')
    total_sit =PrestInmediato.objects.values('mes_vigencia').filter( mes_vigencia__lte =time[6]).exclude(rng_ingreso__in=['','NULL','06 [0 - 1k]']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sit_total = {}
    for i in total_sit:
        sit_total[i['mes_vigencia']]=i['formalizado']

    sueldo1 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[6],rng_ingreso__in=['05 [1K - 1.5K]']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sueldo2 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[6],rng_ingreso__in=['04 [1.5K - 2K]','03 [2K - 2.5K]']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sueldo3 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[6],rng_ingreso__in=['02 [2.5K - 3.5K]','01 [3.5K - ...]']).annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    sueldo1_dict = {} 
    sueldo2_dict = {} 
    sueldo3_dict = {} 
    for i in meses_sit:
        for j in sueldo1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             sueldo1_dict[i['mes_vigencia']]=j['formalizado']
             break
          else:
             sueldo1_dict[i['mes_vigencia']]= 0
        for j in sueldo2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             sueldo2_dict[i['mes_vigencia']]=j['formalizado']
             break
          else:
             sueldo2_dict[i['mes_vigencia']]= 0
        for j in sueldo3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             sueldo3_dict[i['mes_vigencia']]=j['formalizado']
             break
          else:
             sueldo3_dict[i['mes_vigencia']]= 0

    mora0 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[6],rng_ingreso__in=['05 [1K - 1.5K]']).annotate(formalizado=Sum('mora6')).order_by('mes_vigencia')
    mora1 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[6],rng_ingreso__in=['04 [1.5K - 2K]','03 [2K - 2.5K]']).annotate(formalizado=Sum('mora6')).order_by('mes_vigencia')
    mora2 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__lte =time[6],rng_ingreso__in=['02 [2.5K - 3.5K]','01 [3.5K - ...]']).annotate(formalizado=Sum('mora6')).order_by('mes_vigencia')
    mora0_dict = {} 
    mora1_dict = {} 
    mora2_dict = {} 
    for i in meses_sit:
       for j in mora0:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora0_dict[i['mes_vigencia']]=j['formalizado']*100/sueldo1_dict[i['mes_vigencia']]
             break
          else:
             mora0_dict[i['mes_vigencia']]= 0
       for j in mora1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora1_dict[i['mes_vigencia']]=j['formalizado']*100/sueldo2_dict[i['mes_vigencia']]
             break
          else:
             mora1_dict[i['mes_vigencia']]= 0
       for j in mora2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             mora2_dict[i['mes_vigencia']]=j['formalizado']*100/sueldo3_dict[i['mes_vigencia']]
             break
          else:
             mora2_dict[i['mes_vigencia']]= 0

    moradep = PrestInmediato.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[6],laboral='1. Dependiente').annotate(mora=Sum('mora6')).order_by('mes_vigencia')
    moraindep = PrestInmediato.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[6],laboral='2. Independiente').annotate(mora=Sum('mora6')).order_by('mes_vigencia')
    morapnn = PrestInmediato.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[6],laboral='3. PNN').annotate(mora=Sum('mora6')).order_by('mes_vigencia')
    moranr = PrestInmediato.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte =time[6],laboral='4.No Reconocido').annotate(mora=Sum('mora6')).order_by('mes_vigencia')
    moradep_dict = {}; morainde_dict={}; morapnn_dict = {}; moranr_dict = {};
    for i in meses_sit:
        for j in moradep:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moradep_dict[i['mes_vigencia']] = j['mora']*100/totdep_dict[i['mes_vigencia']]
                break
            else:
                moradep_dict[i['mes_vigencia']] = 0
        for j in moraindep:
            if i['mes_vigencia'] == j['mes_vigencia']:
                morainde_dict[i['mes_vigencia']] = j['mora']*100/totindep_dict[i['mes_vigencia']]
                break
            else:
                morainde_dict[i['mes_vigencia']] = 0
        for j in morapnn:
            if i['mes_vigencia'] == j['mes_vigencia']:
                morapnn_dict[i['mes_vigencia']] = j['mora']*100/totpnn_dict[i['mes_vigencia']]
                break
            else:
                morapnn_dict[i['mes_vigencia']] = 0
        for j in moranr:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moranr_dict[i['mes_vigencia']] = j['mora']*100/totnr_dict[i['mes_vigencia']]
                break
            else:
                moranr_dict[i['mes_vigencia']] = 0


    ava = PrestInmediato.objects.values('mes_vigencia','segmento').filter(segmento='1.AVA').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    ms = PrestInmediato.objects.values('mes_vigencia','segmento').filter(segmento='2.MS').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    noph = PrestInmediato.objects.values('mes_vigencia','segmento').filter(segmento='3.NoPH').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    ava_dict = {}; ms_dict = {}; noph_dict = {};
    totava_dict = {}; totms_dict = {}; totnoph_dict = {};
    for i in meses_tot:
        for j in ava:
            if i['mes_vigencia'] == j['mes_vigencia']:
                ava_dict[i['mes_vigencia']] = j['formalizado']*100/form_dict[i['mes_vigencia']]
                totava_dict[i['mes_vigencia']] = j['formalizado']
                break
            else:
                ava_dict[i['mes_vigencia']] = 0
        for j in ms:
            if i['mes_vigencia'] == j['mes_vigencia']:
                ms_dict[i['mes_vigencia']] = j['formalizado']*100/form_dict[i['mes_vigencia']]
                totms_dict[i['mes_vigencia']] = j['formalizado']
                break
            else:
                ms_dict[i['mes_vigencia']] = 0
        for j in noph:
            if i['mes_vigencia'] == j['mes_vigencia']:
                noph_dict[i['mes_vigencia']] = j['formalizado']*100/form_dict[i['mes_vigencia']]
                totnoph_dict[i['mes_vigencia']] = j['formalizado']
                break
            else:
                noph_dict[i['mes_vigencia']] = 0

    moraava = PrestInmediato.objects.values('mes_vigencia','segmento').filter(mes_vigencia__lte =time[6],segmento='1.AVA').annotate(mora=Sum('mora6')).order_by('mes_vigencia')
    morams = PrestInmediato.objects.values('mes_vigencia','segmento').filter(mes_vigencia__lte =time[6],segmento='2.MS').annotate(mora=Sum('mora6')).order_by('mes_vigencia')
    moranoph = PrestInmediato.objects.values('mes_vigencia','segmento').filter(mes_vigencia__lte =time[6],segmento='3.NoPH').annotate(mora=Sum('mora6')).order_by('mes_vigencia')
    moraava_dict = {}; morams_dict = {}; moranoph_dict = {};
    for i in meses_sit:
        for j in moraava:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moraava_dict[i['mes_vigencia']] = j['mora']*100/totava_dict[i['mes_vigencia']]
                break
            else:
                moraava_dict[i['mes_vigencia']] = 0
        for j in morams:
            if i['mes_vigencia'] == j['mes_vigencia']:
                morams_dict[i['mes_vigencia']] = j['mora']*100/totms_dict[i['mes_vigencia']]
                break
            else:
                morams_dict[i['mes_vigencia']] = 0
        for j in moranoph:
            if i['mes_vigencia'] == j['mes_vigencia']:
                moranoph_dict[i['mes_vigencia']] = j['mora']*100/totnoph_dict[i['mes_vigencia']]
                break
            else:
                moranoph_dict[i['mes_vigencia']] = 0

    print morams
    print totms_dict

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
    meses = IncreLinea.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
    form = IncreLinea.objects.values('mes_vigencia').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form_dict = {}
    for i in form:
	form_dict[i['mes_vigencia']]=i['cantidad']
    ticket = IncreLinea.objects.values('mes_vigencia').annotate(cantidad=Sum('cantidad')).order_by('mes_vigencia')
    ticket_dict = {}
    for i in meses:
       for j in ticket:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ticket_dict[i['mes_vigencia']]=j['cantidad']*1000000/form_dict[i['mes_vigencia']]
             break
       	  else:
             ticket_dict[i['mes_vigencia']]= 0
    form2 = IncreLinea.objects.values('mes_vigencia').exclude(segmento='').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form2_dict = {}
    for i in form2:
	form2_dict[i['mes_vigencia']]=i['cantidad']
    meses_mora = IncreLinea.objects.values_list('mes_vigencia', flat=True).filter(mes_vigencia__lte=time[12]).order_by('mes_vigencia').distinct()
    ava = IncreLinea.objects.values('mes_vigencia').filter(segmento__in=['Vip','Premium']).annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    ava_mora = IncreLinea.objects.values('mes_vigencia').filter(segmento__in=['Vip','Premium'],mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),mora12=Sum('mora12')).order_by('mes_vigencia')
    ava_dict = {}; moraava_dict = {};
    for i in meses:
        for j in ava:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ava_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ava_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
        for j in ava_mora:
          if i == j['mes_vigencia']:
             moraava_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             moraava_dict[i]= 0

    ms = IncreLinea.objects.values('mes_vigencia').filter(segmento='MS').annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    ms_mora = IncreLinea.objects.values('mes_vigencia').filter(segmento='MS',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    ms_dict = {}; morams_dict = {};
    for i in meses:
       for j in ms:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ms_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ms_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in ms_mora:
          if i == j['mes_vigencia']:
             morams_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             morams_dict[i]= 0
    pasivo = IncreLinea.objects.values('mes_vigencia').filter(segmento='Pasivo').annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    pasivo_mora = IncreLinea.objects.values('mes_vigencia').filter(segmento='Pasivo',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    pasivo_dict = {}; morapasivo_dict = {};
    for i in meses:
       for j in pasivo:
          if i['mes_vigencia'] == j['mes_vigencia']:
             pasivo_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             pasivo_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in pasivo_mora:
          if i == j['mes_vigencia']:
             morapasivo_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             morapasivo_dict[i]= 0
    noph = IncreLinea.objects.values('mes_vigencia').filter(segmento='No PH').annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    noph_mora = IncreLinea.objects.values('mes_vigencia').filter(segmento='No PH',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    noph_dict = {}; moranoph_dict = {};
    for i in meses:
       for j in noph:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noph_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noph_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in noph_mora:
          if i == j['mes_vigencia']:
             moranoph_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             moranoph_dict[i]= 0
    noclie = IncreLinea.objects.values('mes_vigencia').filter(segmento='NoCli').annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    noclie_mora = IncreLinea.objects.values('mes_vigencia').filter(segmento='NoCli',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),cantidad_uso=Sum('ctas_uso'),mora12=Sum('mora12')).order_by('mes_vigencia')
    noclie_dict = {}; moranoclie_dict = {};
    for i in meses:
       for j in noclie:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noclie_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noclie_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in noclie_mora:
          if i == j['mes_vigencia']:
             moranoclie_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             moranoclie_dict[i]= 0

    totrango = IncreLinea.objects.values('mes_vigencia').exclude(rng_sueldo__in=['00 Sin Ingreso','EMPLEADOS']).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    totrango_dict = {}
    for i in totrango:
        totrango_dict[i['mes_vigencia']]=i['cantidad']
    rango1 = IncreLinea.objects.values('mes_vigencia').filter(rng_sueldo='01 [-1000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/totrango_dict[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= []
    rango2 = IncreLinea.objects.values('mes_vigencia').filter(rng_sueldo='02 [1000-1500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/totrango_dict[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= []
    rango3 = IncreLinea.objects.values('mes_vigencia').filter(rng_sueldo='03 [1500-2000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/totrango_dict[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= []
    rango4 = IncreLinea.objects.values('mes_vigencia').filter(rng_sueldo='04 [2000-2500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/totrango_dict[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= []
    rango5 = IncreLinea.objects.values('mes_vigencia').filter(rng_sueldo='05 [2500-3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/totrango_dict[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= []
    rango6 = IncreLinea.objects.values('mes_vigencia').filter(rng_sueldo='06 [+3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['cantidad']*100/totrango_dict[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= []
    buro1 = IncreLinea.objects.values('mes_vigencia').filter(buro='01 G1-G4').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro1_mora = IncreLinea.objects.values('mes_vigencia').filter(buro='01 G1-G4',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),mora12=Sum('mora12')).order_by('mes_vigencia')
    buro1_dict = {}; moraburo1_dict = {};
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in buro1_mora:
          if i == j['mes_vigencia']:
             moraburo1_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             moraburo1_dict[i]= 0
    buro2 = IncreLinea.objects.values('mes_vigencia').filter(buro='02 G5').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro2_mora = IncreLinea.objects.values('mes_vigencia').filter(buro='02 G5',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),mora12=Sum('mora12')).order_by('mes_vigencia')
    buro2_dict = {}; moraburo2_dict = {};
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in buro2_mora:
          if i == j['mes_vigencia']:
             moraburo2_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             moraburo2_dict[i]= 0
    buro3 = IncreLinea.objects.values('mes_vigencia').filter(buro='03 G6-G8').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro3_mora = IncreLinea.objects.values('mes_vigencia').filter(buro='03 G6-G8',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),mora12=Sum('mora12')).order_by('mes_vigencia')
    buro3_dict = {}; moraburo3_dict = {};
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in buro3_mora:
          if i == j['mes_vigencia']:
             moraburo3_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             moraburo3_dict[i]= 0
    buro4 = IncreLinea.objects.values('mes_vigencia').filter(buro='NB').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro4_mora = IncreLinea.objects.values('mes_vigencia').filter(buro='NB',mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),mora12=Sum('mora12')).order_by('mes_vigencia')
    buro4_dict = {}; moraburo4_dict = {};
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0
    for i in meses_mora:
       for j in buro4_mora:
          if i == j['mes_vigencia']:
             moraburo4_dict[i]=j['mora12']*100/j['cantidad']
             break
          else:
             moraburo4_dict[i]= 0

    cat_cliente = IncreLinea.objects.values('mes_vigencia','laboral').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    moracat_cliente = IncreLinea.objects.values('mes_vigencia','laboral').filter(mes_vigencia__lte=time[12]).annotate(cantidad=Sum('ctas'),mora12=Sum('mora12')).order_by('mes_vigencia')
    dep_dict = {}; inde_dict = {}; pnn_dict = {}; nr_dict = {};
    moradep_dict = {}; morainde_dict = {}; morapnn_dict = {}; moranr_dict = {};
    for i in meses:
        for j in cat_cliente:
            if i['mes_vigencia'] == j['mes_vigencia']:
                if j['laboral'] == '1. Dependiente':
                    dep_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
                    break
            else:
                dep_dict[i['mes_vigencia']]=0
        for j in cat_cliente:
            if i['mes_vigencia'] == j['mes_vigencia']:
                if j['laboral'] == '2. Independiente':
                    inde_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
                    break
            else:
                inde_dict[i['mes_vigencia']]=0
        for j in cat_cliente:
            if i['mes_vigencia'] == j['mes_vigencia']:
                if j['laboral'] == '3. PNN':
                    pnn_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
                    break
            else:
                pnn_dict[i['mes_vigencia']]=0
        for j in cat_cliente:
            if i['mes_vigencia'] == j['mes_vigencia']:
                if j['laboral'] == '4.No Reconocido':
                    nr_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
                    break
            else:
                nr_dict[i['mes_vigencia']]=0
    for i in meses_mora:
        for j in moracat_cliente:
            if i == j['mes_vigencia']:
                if j['laboral'] == '1. Dependiente':
                    moradep_dict[i]=j['mora12']*100/j['cantidad']
                    break
            else:
                moradep_dict[i]=0
        for j in moracat_cliente:
            if i == j['mes_vigencia']:
                if j['laboral'] == '2. Independiente':
                    morainde_dict[i]=j['mora12']*100/j['cantidad']
                    break
            else:
                morainde_dict[i]=0
        for j in moracat_cliente:
            if i == j['mes_vigencia']:
                if j['laboral'] == '3. PNN':
                    morapnn_dict[i]=j['mora12']*100/j['cantidad']
                    break
            else:
                morapnn_dict[i]=0
        for j in moracat_cliente:
            if i == j['mes_vigencia']:
                if j['laboral'] == '4.No Reconocido':
                    moranr_dict[i]=j['mora12']*100/j['cantidad']
                    break
            else:
                moranr_dict[i]=0




    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_increlinea.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_lifemiles(request):
    meses = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502').order_by('-mes_vigencia').distinct()

    form_fact = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502',flg_lifemiles='1').exclude(segmento='').annotate(formalizado=Sum('form'),fact=Sum('facturacion')).order_by('mes_vigencia')
    form_dict = {}; ticket_dict = {};
    for i in form_fact:
        form_dict[i['mes_vigencia']] = i['formalizado']
        ticket_dict[i['mes_vigencia']] = i['fact']*1000000/i['formalizado']

    segmentos = Seguimiento.objects.values('mes_vigencia','segmento').filter(mes_vigencia__gte='201502',flg_lifemiles='1').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    ava_dict = {}; ms_dict = {}; noph_dict={}; nocli_dict={};
    for i in meses:
        for j in segmentos:
            if j['segmento'] == '1.AVA':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    ava_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    ava_dict[i['mes_vigencia']]=[]
        for j in segmentos:
            if j['segmento'] == '2.MS':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    ms_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    ms_dict[i['mes_vigencia']]=[]
        for j in segmentos:
            if j['segmento'] == '3.NoPH':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    noph_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    noph_dict[i['mes_vigencia']]=[]
        for j in segmentos:
            if j['segmento'] == '4.NoCli':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    nocli_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    nocli_dict[i['mes_vigencia']]=[]

    totrango = Seguimiento.objects.values('mes_vigencia').exclude(rng_ing='').filter(mes_vigencia__gte='201502',flg_lifemiles='1').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    totrango_dict = {};
    for i in totrango:
        totrango_dict[i['mes_vigencia']]=i['formalizado']
    rango = Seguimiento.objects.values('mes_vigencia','rng_ing').exclude(rng_ing='').filter(mes_vigencia__gte='201502',flg_lifemiles='1').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    rango1_dict={}; rango2_dict={}; rango3_dict={}; rango4_dict={}; rango5_dict={}; rango6_dict={};
    for i in meses:
        for j in rango:
            if j['rng_ing'] == '06 [0 - 1K]':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    rango1_dict[i['mes_vigencia']]=j['formalizado']*100/totrango_dict[i['mes_vigencia']]
                    break
                else:
                    rango1_dict[i['mes_vigencia']]=[]
        for j in rango:
            if j['rng_ing'] == '05 [1K - 1.5K]':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    rango2_dict[i['mes_vigencia']]=j['formalizado']*100/totrango_dict[i['mes_vigencia']]
                    break
                else:
                    rango2_dict[i['mes_vigencia']]=[]
        for j in rango:
            if j['rng_ing'] == '04 [1.5K - 2K]':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    rango3_dict[i['mes_vigencia']]=j['formalizado']*100/totrango_dict[i['mes_vigencia']]
                    break
                else:
                    rango3_dict[i['mes_vigencia']]=[]
        for j in rango:
            if j['rng_ing'] == '03 [2K - 2.5K]':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    rango4_dict[i['mes_vigencia']]=j['formalizado']*100/totrango_dict[i['mes_vigencia']]
                    break
                else:
                    rango4_dict[i['mes_vigencia']]=[]
        for j in rango:
            if j['rng_ing'] == '02 [2.5K - 3.5K]':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    rango5_dict[i['mes_vigencia']]=j['formalizado']*100/totrango_dict[i['mes_vigencia']]
                    break
                else:
                    rango5_dict[i['mes_vigencia']]=[]
        for j in rango:
            if j['rng_ing'] == '01 [3.5K - ...]':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    rango6_dict[i['mes_vigencia']]=j['formalizado']*100/totrango_dict[i['mes_vigencia']]
                    break
                else:
                    rango6_dict[i['mes_vigencia']]=[]

    buro = Seguimiento.objects.values('mes_vigencia','buro_camp').filter(mes_vigencia__gte='201502',flg_lifemiles='1').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    buro1_dict={}; buro2_dict={}; buro3_dict={}; buro4_dict={};
    for i in meses:
        for j in buro:
            if j['buro_camp'] == 'G1-G4':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    buro1_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    buro1_dict[i['mes_vigencia']]=[]
        for j in buro:
            if j['buro_camp'] == 'G5':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    buro2_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    buro2_dict[i['mes_vigencia']]=[]
        for j in buro:
            if j['buro_camp'] == 'G6-G8':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    buro3_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    buro3_dict[i['mes_vigencia']]=[]
        for j in buro:
            if j['buro_camp'] == 'NB':
                if i['mes_vigencia'] == j['mes_vigencia']:
                    buro4_dict[i['mes_vigencia']]=j['formalizado']*100/form_dict[i['mes_vigencia']]
                    break
                else:
                    buro4_dict[i['mes_vigencia']]=[]

    meses_list = [];
    for i in meses:
        meses_list.append(i['mes_vigencia'])
    mora6 = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502',flg_lifemiles='1').annotate(mora=Sum('mora6'),cta=Sum('ctas')).order_by('mes_vigencia')
    mora9 = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502',flg_lifemiles='1').annotate(mora=Sum('mora9'),cta=Sum('ctas')).order_by('mes_vigencia')
    mora12 = Seguimiento.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502',flg_lifemiles='1').annotate(mora=Sum('mora12'),cta=Sum('ctas')).order_by('mes_vigencia')
    mora6_dict={}; mora9_dict={}; mora12_dict={};
    for j in mora6:
        if j['mes_vigencia'] <= meses_list[6]:
            mora6_dict[j['mes_vigencia']]=j['mora']*100/j['cta']
    for j in mora9:
        if j['mes_vigencia'] <= meses_list[9]:
            mora9_dict[j['mes_vigencia']]=j['mora']*100/j['cta']
    for j in mora12:
        if j['mes_vigencia'] <= meses_list[12]:
            mora12_dict[j['mes_vigencia']]=j['mora']*100/j['cta']
    print mora12

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
def seguimiento_hipoteca(request, fecha='201312', filtro1='mes_vigencia', filtro2='2011'):
    filtro1 = str(filtro1)
    filtro2 = str(filtro2)

    tiempo = Seguimiento.objects.values_list('periodo', flat=True).order_by('periodo').distinct()
    time_list = []
    for i in tiempo:
        time_list.append(i)

    if filtro1 == 'trimestre_form' or len(time_list) < 5:
        num_index = 14
    else:
        num_index = 8

    if filtro1 == 'trimestre_form':
        meses = Seguimiento.objects.values_list(filtro1, flat=True).order_by(filtro1).distinct()
        trimestre = 1
    else:
        meses = Seguimiento.objects.values_list(filtro1, flat=True).filter(periodo__gte=filtro2).order_by(filtro1).distinct()
        trimestre = 0
    meses_list = []
    for i in meses:
        meses_list.append(i)

    if filtro1 == 'trimestre_form':
        total_form = Seguimiento.objects.values(filtro1, 'producto').filter(producto='04 Hipotecario',origen__in=['FAST','UNO A UNO','REGULAR']).annotate(formalizado=Sum('form'),cantidad=Sum('facturacion')).order_by(filtro1)
    else:
        total_form = Seguimiento.objects.values(filtro1, 'producto').filter(producto='04 Hipotecario', periodo__gte=filtro2,origen__in=['FAST','UNO A UNO','REGULAR']).annotate(formalizado=Sum('form'),cantidad=Sum('facturacion')).order_by(filtro1)
    total_form_dict = {}; total_fac_dict = {};
    for j in total_form:
       total_form_dict[j[filtro1]]=j['formalizado']
    for j in total_form:
       total_fac_dict[j[filtro1]]=j['cantidad']

    if filtro1 == 'trimestre_form':
        seg_ms = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', segmento='2.MS').annotate(seg=Sum('form')).order_by(filtro1)
        seg_noph = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', segmento='3.NoPH').annotate(seg=Sum('form')).order_by(filtro1)
        seg_nocli = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', segmento='4.NoCli').annotate(seg=Sum('form')).order_by(filtro1)
    else:
        seg_ms = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', segmento='2.MS', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_noph = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', segmento='3.NoPH', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        seg_nocli = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', segmento='4.NoCli', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    seg_ms_dict = {}; seg_noph_dict = {}; seg_nocli_dict = {};
    for i in meses:
        for j in seg_ms:
            if i == j[filtro1]:
                seg_ms_dict[i] = j['seg']
                break
            else:
                seg_ms_dict[i] = 0
        for j in seg_noph:
            if i == j[filtro1]:
                seg_noph_dict[i] = j['seg']
                break
            else:
                seg_noph_dict[i] = 0
        for j in seg_nocli:
            if i == j[filtro1]:
                seg_nocli_dict[i] = j['seg']
                break
            else:
                seg_nocli_dict[i] = 0

    if filtro1 == 'trimestre_form':
        depen = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='1. Dependiente').annotate(seg = Sum('form')).order_by(filtro1)
        indep = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='2. Independiente').annotate(seg=Sum('form')).order_by(filtro1)
        pnn = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='3. PNN').annotate(seg=Sum('form')).order_by(filtro1)
        no_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='4.No Reconocido').annotate(seg=Sum('form')).order_by(filtro1)
    else:
        depen = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='1. Dependiente', periodo__gte=filtro2).annotate(seg = Sum('form')).order_by(filtro1)
        indep = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='2. Independiente', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        pnn = Seguimiento.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='3. PNN', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
        no_recon = Seguimiento1.objects.values(filtro1, 'riesgos').filter(producto='04 Hipotecario', cat_persona='4.No Reconocido', periodo__gte=filtro2).annotate(seg=Sum('form')).order_by(filtro1)
    depen_dict = {}; indep_dict = {}; pnn_dict = {}; no_recon_dict = {};
    for i in meses:
        for j in depen:
            if i == j[filtro1]:
                depen_dict[i] = j['seg']
                break
            else:
                depen_dict[i] = 0
        for j in indep:
            if i == j[filtro1]:
                indep_dict[i] = j['seg']
                break
            else:
                indep_dict[i] = 0
        for j in pnn:
            if i == j[filtro1]:
                pnn_dict[i] = j['seg']
                break
            else:
                pnn_dict[i] = 0
        for j in no_recon:
            if i == j[filtro1]:
                no_recon_dict[i] = j['seg']
                break
            else:
                no_recon_dict[i] = 0

    if filtro1 == 'trimestre_form':
        rangos = Seguimiento.objects.values(filtro1,'producto', 'rng_ing').filter(producto='04 Hipotecario').annotate(num_rango=Sum('form')).order_by(filtro1)
    else:
        rangos = Seguimiento.objects.values(filtro1,'producto', 'rng_ing').filter(producto='04 Hipotecario', periodo__gte=filtro2).annotate(num_rango=Sum('form')).order_by(filtro1)
    rango1_dict = {}; rango2_dict = {}; rango3_dict = {};
    rango4_dict = {}; rango5_dict = {};
    for i in meses:
        for j in rangos:
            if i == j[filtro1]:
                if j['rng_ing'] == '01 [3.5K - ...]':
                    rango1_dict[i]=j['num_rango']*100/total_form_dict[i]
                    break
                else:
                    rango1_dict[i]=[]
        for j in rangos:
            if i == j[filtro1]:
                if j['rng_ing'] == '02 [2.5K - 3.5K]':
                    rango2_dict[i]=j['num_rango']*100/total_form_dict[i]
                    break
                else:
                    rango2_dict[i]=[]
        for j in rangos:
            if i == j[filtro1]:
                if j['rng_ing'] == '03 [2K - 2.5K]':
                    rango3_dict[i]=j['num_rango']*100/total_form_dict[i]
                    break
                else:
                    rango3_dict[i]=[]
        for j in rangos:
            if i == j[filtro1]:
                if j['rng_ing'] == '04 [1.5K - 2K]':
                    rango4_dict[i]=j['num_rango']*100/total_form_dict[i]
                    break
                else:
                    rango4_dict[i]=[]
        for j in rangos:
            if i == j[filtro1]:
                if j['rng_ing'] == '05 [1K - 1.5K]':
                    rango5_dict[i]=j['num_rango']*100/total_form_dict[i]
                    break
                else:
                    rango5_dict[i]=[]

    buro1 = Seguimiento.objects.values(filtro1).filter(buro_camp='G1-G4', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by(filtro1)
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i == j[filtro1]:
             buro1_dict[i]=j['cantidad']*100/total_form_dict[i]
             break
       	  else:
             buro1_dict[i]= 0
    buro2 = Seguimiento.objects.values(filtro1).filter(buro_camp='G5', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by(filtro1)
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i == j[filtro1]:
             buro2_dict[i]=j['cantidad']*100/total_form_dict[i]
             break
       	  else:
             buro2_dict[i]= 0
    buro3 = Seguimiento.objects.values(filtro1).filter(buro_camp='G6-G8', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by(filtro1)
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i == j[filtro1]:
             buro3_dict[i]=j['cantidad']*100/total_form_dict[i]
             break
       	  else:
             buro3_dict[i]= 0
    buro4 = Seguimiento.objects.values(filtro1).filter(buro_camp='NB', producto="04 Hipotecario").annotate(cantidad=Sum('form')).order_by(filtro1)
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i == j[filtro1]:
             buro4_dict[i]=j['cantidad']*100/total_form_dict[i]
             break
       	  else:
             buro4_dict[i]= 0

    if filtro1 == 'trimestre_form':
        meses_moras = Seguimiento.objects.values('trimestre_form').order_by('-trimestre_form').distinct()
        num_mora12 = 3 #3
        num_mora24 = 7 #7
        num_mora36 = 11 #11
    else:
        meses_moras = Seguimiento.objects.values('mes_vigencia').order_by('-mes_vigencia').distinct()
        num_mora12 = 12 #11
        num_mora24 = 24 #23
        num_mora36 = 36 #35

    morames_list = []
    for i in meses_moras:
        morames_list.append(i[filtro1])

    if filtro1 == 'trimestre_form':
        mora12 = Seguimiento.objects.values(filtro1,'producto').filter(producto='04 Hipotecario').annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
        mora24 = Seguimiento.objects.values(filtro1,'producto').filter(producto='04 Hipotecario').annotate(sum_mora=Sum('mora24'),cuentas=Sum('ctas')).order_by(filtro1)
        mora36 = Seguimiento.objects.values(filtro1,'producto').filter(producto='04 Hipotecario').annotate(sum_mora=Sum('mora36'),cuentas=Sum('ctas')).order_by(filtro1)
    else:
        mora12 = Seguimiento.objects.values(filtro1,'producto').filter(producto='04 Hipotecario', periodo__gte=filtro2).annotate(sum_mora=Sum('mora12'),cuentas=Sum('ctas')).order_by(filtro1)
        mora24 = Seguimiento.objects.values(filtro1,'producto').filter(producto='04 Hipotecario', periodo__gte=filtro2).annotate(sum_mora=Sum('mora24'),cuentas=Sum('ctas')).order_by(filtro1)
        mora36 = Seguimiento.objects.values(filtro1,'producto').filter(producto='04 Hipotecario', periodo__gte=filtro2).annotate(sum_mora=Sum('mora36'),cuentas=Sum('ctas')).order_by(filtro1)
    mora12_dict = {}; mora24_dict = {}; mora36_dict = {};
    for j in mora12:
        if j[filtro1] <= morames_list[num_mora12]:
            mora12_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora24:
        if j[filtro1] <= morames_list[num_mora24]:
            mora24_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']
    for j in mora36:
        if j[filtro1] <= morames_list[num_mora36]:
            mora36_dict[j[filtro1]]=j['sum_mora']*100/j['cuentas']

    total_forzaje = Forzaje.objects.values(filtro1).filter(producto='04 Hipotecario').annotate(cantidad=Sum('form')).order_by(filtro1)
    forzaje_dict = {}
    for i in meses:
	for j in total_forzaje:
	    if i == j[filtro1]:
		forzaje_dict[j[filtro1]]=j['cantidad']

    forzaje2 = Forzaje.objects.values(filtro1, 'dic_global').filter(producto = '04 Hipotecario').exclude(dic_global='AP').annotate(cantidad=Sum('form')).order_by(filtro1)
    duda_dict = {}
    rechazo_dict = {}
    for i in meses:
       for j in forzaje2:
          if i == j[filtro1]:
	     if  j['dic_global']=='DU':
             	duda_dict[i]=j['cantidad']*100/forzaje_dict[i]
	     elif  j['dic_global']=='RE':
             	rechazo_dict[i]=j['cantidad']*100/forzaje_dict[i]
       	     else:
             	duda_dict[i]= 0
             	rechazo_dict[i]= 0

    meses_mapa = Mapa.objects.values('codmes').order_by('codmes').distinct()
    list_meses=[]; d=0
    for i in meses_mapa:
	list_meses.append(i['codmes'])
    d = len(list_meses)
    ubigeo = Mapa.objects.values('ubigeo').order_by('ubigeo').distinct()
    distrito = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA').annotate(mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    contrato=Mapa.objects.values('ubigeo','codmes').filter(provincia='LIMA', codmes=fecha).annotate(num=Sum('ctas')).order_by('ubigeo')
    dict_ctas = {}
    for i in contrato:
	dict_ctas[i['ubigeo']]=i['num']
    distrito1 = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA', codmes=fecha).annotate(contrato=Sum(F('ctas')),inver=Sum(F('inv')),mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    dict_contra = {} 
    dict_inv = {} 
    dict_morac = {}
    for i in distrito1:
	dict_contra[i['ubigeo']]=i['contrato']
	dict_inv[i['ubigeo']]=i['inver']
	dict_morac[i['ubigeo']]=i['mora']
    vinculo_dep = Mapa.objects.values('ubigeo','codmes').filter(provincia='LIMA', codmes=fecha,vinculo='1. Dependiente').annotate(contrato=Sum(F('ctas'))).order_by('ubigeo')
    dict_vinculo = {}
    for i in vinculo_dep:
	dict_vinculo[i['ubigeo']]=i['contrato']*100/dict_ctas[i['ubigeo']]

    dict_moras = {}; dict_moras1 = {}; 
    dict_moras2 = {}; dict_moras3 = {};dict_moras4 = {};
    dict_moras5 = {}; dict_moras6 = {};
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
	        dict_moras[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
	        dict_moras[i['ubigeo']]='#A6D974'
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
          dict_moras1[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras1[i['ubigeo']]='#A6D974'
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
          dict_moras2[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras2[i['ubigeo']]='#A6D974'
      if i['codmes']=='201607':
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
          dict_moras3[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras3[i['ubigeo']]='#A6D974'
      if i['codmes']=='201608':
        if i['mora']>3:
          dict_moras4[i['ubigeo']]='#E31A1C'
        if i['mora']>2 and i['mora']<=3:
          dict_moras4[i['ubigeo']]='#FC4E2A'
        if i['mora']>1.5 and i['mora']<=2:
          dict_moras4[i['ubigeo']]='#FB8D29'
        if i['mora']>1.2 and i['mora']<=1.5:
          dict_moras4[i['ubigeo']]='#FEB228'
        if i['mora']>0.9 and i['mora']<=1.2:
          dict_moras4[i['ubigeo']]='#FED976'
        if i['mora']>0.6 and i['mora']<=0.9:
          dict_moras4[i['ubigeo']]='#FBE975'
        if i['mora']>0.3 and i['mora']<=0.6:
          dict_moras4[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras4[i['ubigeo']]='#A6D974'
      if i['codmes']=='201609':
        if i['mora']>3:
          dict_moras5[i['ubigeo']]='#E31A1C'
        if i['mora']>2 and i['mora']<=3:
          dict_moras5[i['ubigeo']]='#FC4E2A'
        if i['mora']>1.5 and i['mora']<=2:
          dict_moras5[i['ubigeo']]='#FB8D29'
        if i['mora']>1.2 and i['mora']<=1.5:
          dict_moras5[i['ubigeo']]='#FEB228'
        if i['mora']>0.9 and i['mora']<=1.2:
          dict_moras5[i['ubigeo']]='#FED976'
        if i['mora']>0.6 and i['mora']<=0.9:
          dict_moras5[i['ubigeo']]='#FBE975'
        if i['mora']>0.3 and i['mora']<=0.6:
          dict_moras5[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras5[i['ubigeo']]='#A6D974'
      if i['codmes']=='201610':
        if i['mora']>3:
          dict_moras6[i['ubigeo']]='#E31A1C'
        if i['mora']>2 and i['mora']<=3:
          dict_moras6[i['ubigeo']]='#FC4E2A'
        if i['mora']>1.5 and i['mora']<=2:
          dict_moras6[i['ubigeo']]='#FB8D29'
        if i['mora']>1.2 and i['mora']<=1.5:
          dict_moras6[i['ubigeo']]='#FEB228'
        if i['mora']>0.9 and i['mora']<=1.2:
          dict_moras6[i['ubigeo']]='#FED976'
        if i['mora']>0.6 and i['mora']<=0.9:
          dict_moras6[i['ubigeo']]='#FBE975'
        if i['mora']>0.3 and i['mora']<=0.6:
          dict_moras6[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras6[i['ubigeo']]='#A6D974'


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

    conce = HipotecaConce.objects.values('mes','territorio').filter(mes='201512').annotate(sum_inv=Sum('inversion')).order_by('territorio')
    limaprov = Mapa.objects.values('codmes','lima_prov').annotate(num=Sum('ctas')).order_by('codmes')
    dict_lp1= {}; dict_lp2 = {}; dict_lp3 = {}; dict_lp4 = {};
    dict_lp5 = {}; dict_lp6 = {}; dict_lp7 = {};
    for i in limaprov:
	    if i['codmes'] == '201312':
	       dict_lp1[i['lima_prov']] = i['num']
    for i in limaprov:
	    if i['codmes'] == '201412':
	       dict_lp2[i['lima_prov']] = i['num']
    for i in limaprov:
	    if i['codmes'] == '201512':
	       dict_lp3[i['lima_prov']] = i['num']
    for i in limaprov:
	    if i['codmes'] == '201607':
	       dict_lp4[i['lima_prov']] = i['num']
    for i in limaprov:
        if i['codmes'] == '201608':
            dict_lp5[i['lima_prov']] = i['num']
    for i in limaprov:
        if i['codmes'] == '201609':
            dict_lp6[i['lima_prov']] = i['num']
    for i in limaprov:
        if i['codmes'] == '201610': 
            dict_lp7[i['lima_prov']] = i['num']

    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_hipoteca.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_web(request):

    meses = Seguimiento1.objects.values('mes_vigencia').order_by('mes_vigencia').distinct()
    print meses
    print 'holis'

    formalizado = Seguimiento1.objects.values('mes_vigencia','digital').filter(digital=1).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    form_dict = {};
    for i in formalizado:
        if i['mes_vigencia'] >= '201605':
            form_dict[i['mes_vigencia']]=i['cantidad']

    tipo_camp = Seguimiento1.objects.values('mes_vigencia','canal_digital').annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    moi_dict = {}; rescate_dict = {};
    for j in tipo_camp:
        if j['mes_vigencia'] >= '201605':
            if j['canal_digital'] == 'FLUJO_MOI':
                moi_dict[j['mes_vigencia']]=j['cantidad']
    for j in tipo_camp:
        if j['mes_vigencia'] >= '201605':
            if j['canal_digital'] == 'RESCATE':
                rescate_dict[j['mes_vigencia']]=j['cantidad']

    tipo_cliente = Seguimiento1.objects.values('mes_vigencia','digital','cat_persona').filter(digital=1).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    dep_dict = {}; inde_dict = {}; 
    pnn_dict = {}; nr_dict = {}; 
    for j in tipo_cliente:
        if j['mes_vigencia'] >= '201605':
            if j['cat_persona'] == '1. Dependiente':
                dep_dict[j['mes_vigencia']]=j['cantidad']
    for j in tipo_cliente:
        if j['mes_vigencia'] >= '201605':
            if j['cat_persona'] == '2. Independiente':
                inde_dict[j['mes_vigencia']]=j['cantidad']
    for j in tipo_cliente:
        if j['mes_vigencia'] >= '201605':
            if j['cat_persona'] == '3. PNN':
                pnn_dict[j['mes_vigencia']]=j['cantidad']
    for j in tipo_cliente:
        if j['mes_vigencia'] >= '201605':
            if j['cat_persona'] == '4.No Reconocido':
                nr_dict[j['mes_vigencia']]=j['cantidad']

    buro = Seguimiento1.objects.values('mes_vigencia','digital','buro_camp').filter(digital=1).annotate(cantidad=Sum('form')).order_by('mes_vigencia')
    buro1_dict = {}; buro2_dict = {}; 
    buro3_dict = {}; buro4_dict = {}; 
    for j in buro:
        if j['mes_vigencia'] >= '201605':
            if j['buro_camp'] == 'G1-G4':
                buro1_dict[j['mes_vigencia']]=j['cantidad']
    for j in buro:
        if j['mes_vigencia'] >= '201605':
            if j['buro_camp'] == 'G5':
                buro2_dict[j['mes_vigencia']]=j['cantidad']
    for j in buro:
        if j['mes_vigencia'] >= '201605':
            if j['buro_camp'] == 'G6-G8':
                buro3_dict[j['mes_vigencia']]=j['cantidad']
    for j in buro:
        if j['mes_vigencia'] >= '201605':
            if j['buro_camp'] == 'NB':
                buro4_dict[j['mes_vigencia']]=j['cantidad']


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_web.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_telefonica(request):

    formalizados = FormTelefonica.objects.values('cosecha').annotate(sum_fact=Sum('capital_financiar'),num_form=Sum('form'),mora3=Sum('m3')).order_by('cosecha')
    form_dict = {}; m3_dict = {}; fact_dict = {}; ticket_dict = {};
    for i in formalizados:
        form_dict[i['cosecha']]=i['num_form']
        fact_dict[i['cosecha']] = i['sum_fact']
        ticket_dict[i['cosecha']] = i['sum_fact']/i['num_form']
        if i['cosecha']<='201612':
          m3_dict[i['cosecha']] = i['mora3']*100/i['num_form']
        else:
          m3_dict[i['cosecha']] = []
        

    form_rango = FormTelefonica.objects.values('cosecha','rng_financiar').filter(rng_financiar__in=['1. <=100','2. <=250','3. <=350','4. <=500']).annotate(num_form=Sum('form')).order_by('cosecha')
    rng1_dict = {}; rng2_dict = {}; rng3_dict = {}; rng4_dict = {};
    for i in form_rango:
      if i['rng_financiar']=='1. <=100':
        rng1_dict[i['cosecha']]=i['num_form']*100/form_dict[i['cosecha']]
      if i['rng_financiar']=='2. <=250':
        rng2_dict[i['cosecha']]=i['num_form']*100/form_dict[i['cosecha']]
      if i['rng_financiar']=='3. <=350':
        rng3_dict[i['cosecha']]=i['num_form']*100/form_dict[i['cosecha']]
      if i['rng_financiar']=='4. <=500':
        rng4_dict[i['cosecha']]=i['num_form']*100/form_dict[i['cosecha']]

    form_rango2 = FormTelefonica.objects.values('cosecha').filter(rng_financiar__in=['5. <=1000','6. >1000']).annotate(num_form=Sum('form')).order_by('cosecha')
    rng5_dict = {};
    for i in form_rango2:
      rng5_dict[i['cosecha']]=i['num_form']*100/form_dict[i['cosecha']]

    data_stock = StockTelefonica.objects.values('codmes').annotate(sum_deuda=Sum('deuda'),mora30=Sum('mora_30'),sum_vencido=Sum('vencido'),sum_judicial=Sum('judicial'),sum_ref_vencido=Sum('ref_vencido'),sum_ref_judicial=Sum('ref_judicial')).order_by('codmes')
    deuda_dict={}; mora30_dict={}; mora_contable_dict={};
    for i in data_stock:
      deuda_dict[i['codmes']]=i['sum_deuda']/1000000
      mora30_dict[i['codmes']]=i['mora30']*100/i['sum_deuda']
      mora_contable_dict[i['codmes']]=(i['sum_vencido']+i['sum_judicial']+i['sum_ref_vencido']+i['sum_ref_judicial'])*100/i['sum_deuda']


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/seguimiento_telefonica.html', locals(),
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


# Vista para borrar data 
@login_required
def delete(request, base=0, fecha=after1, numsemana=0):
    numsemana = int(numsemana)
    control_fecha1 = RVGL.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha1:
        if fecha == i['mes_vigencia'] and base == '1':
            RVGL.objects.filter(mes_vigencia=fecha).delete()

    control_fecha2 = Campana2.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha2:
        if fecha == i['mes_vigencia'] and base == '2':
            Campana2.objects.filter(mes_vigencia=fecha).delete()

    if fecha == '000000' and base == '3':
        CampanaWeb.objects.all().delete()

    if fecha == '000001' and base == '4':
        CampanaEfec.objects.all().delete()

    #if fecha == '000002' and base == '5':
        #CampanaLabSeg.objects.all().delete()

    if fecha == '000003' and base == '6':
        CampanaEquifax.objects.all().delete()

    if fecha == '000004' and base == '7':
        Seguimiento1.objects.all().delete()

    #if fecha == '000005' and base == '17':
        #Moras.objects.all().delete()

    if fecha == '000006' and base == '11':
        Forzaje.objects.all().delete()

    if fecha == '000007' and base == '18':
        EfectividadTC.objects.all().delete()

    if fecha == '000008' and base == '2':
        Campana2.objects.all().delete()

    if fecha == '000009' and base == '9':
        AdelantoSueldo.objects.all().delete()

    if fecha == '000010' and base == '10':
        PrestInmediato.objects.all().delete()

    if fecha == '000011' and base == '13':
        IncreLinea.objects.all().delete()

    if fecha == '000012' and base == '19':
        Mapa.objects.all().delete()

    if fecha == '000013' and base == '20':
        Seguimiento.objects.all().delete()

    if fecha == '000014' and base == '21':
        Caida.objects.all().delete()

    if fecha == '000015' and base == '22':
        CosteRiesgo.objects.all().delete()

    if fecha == '000016' and base == '23':
        CosteRiesgo2.objects.all().delete()

    if fecha == '000017' and base == '24':
        Stock.objects.all().delete()

    if fecha == '000018' and base == '25':
        Dotaciones.objects.all().delete()

    if fecha == '000019' and base == '26':
        SeguimientoTer.objects.all().delete()

    control_fecha15 = Seguimiento.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha15:
        if fecha == i['mes_vigencia'] and base == '20':
            Seguimiento.objects.filter(mes_vigencia=fecha).delete()

    control_fecha3 = Seguimiento1.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha3:
        if fecha == i['mes_vigencia'] and base == '7':
            Seguimiento1.objects.filter(mes_vigencia=fecha).delete()

    control_semana0 = DepartamentosWeb.objects.values('semana').order_by('semana').distinct('semana')
    for i in control_semana0:
        if numsemana == i['semana'] and base == '8':
            DepartamentosWeb.objects.filter(semana=numsemana).delete()

    control_fecha4 = AdelantoSueldo.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha4:
        if fecha == i['mes_vigencia'] and base == '9':
            AdelantoSueldo.objects.filter(mes_vigencia=fecha).delete()

    control_fecha5 = PrestInmediato.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha5:
        if fecha == i['mes_vigencia'] and base == '10':
            PrestInmediato.objects.filter(mes_vigencia=fecha).delete()

    control_fecha6 = Forzaje.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha6:
        if fecha == i['mes_vigencia'] and base == '11':
            Forzaje.objects.filter(mes_vigencia=fecha).delete()

    control_fecha7 = Lifemiles.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha7:
        if fecha == i['mes_vigencia'] and base == '12':
            Lifemiles.objects.filter(mes_vigencia=fecha).delete()

    control_fecha8 = IncreLinea.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha8:
        if fecha == i['mes_vigencia'] and base == '13':
            IncreLinea.objects.filter(mes_vigencia=fecha).delete()

    control_fecha9 = FlujOperativo.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha9:
        if fecha == i['mes_vigencia'] and base == '14':
            FlujOperativo.objects.filter(mes_vigencia=fecha).delete()

    control_fecha10 = HipotecaSSFF.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha10:
        if fecha == i['mes_vigencia'] and base == '15':
            HipotecaSSFF.objects.filter(mes_vigencia=fecha).delete()

    control_fecha11 = HipotecaConce.objects.values('mes_form').order_by('mes_form').distinct('mes_form')
    for i in control_fecha11:
        if fecha == i['mes_form'] and base == '16':
            HipotecaConce.objects.filter(mes_form=fecha).delete()

    #control_fecha12 = Moras.objects.values('mes_form').order_by('mes_form').distinct('mes_form')
    #for i in control_fecha12:
        #if fecha == i['mes_form'] and base == '17':
            #Moras.objects.filter(mes_form=fecha).delete()

    control_fecha13 = EfectividadTC.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha13:
        if fecha == i['mes_vigencia'] and base == '18':
            EfectividadTC.objects.filter(mes_vigencia=fecha).delete()

    control_fecha14 = Mapa.objects.values('codmes').order_by('codmes').distinct('codmes')
    for i in control_fecha14:
        if fecha == i['codmes'] and base == '19':
            Mapa.objects.filter(codmes=fecha).delete()

    control_fecha16 = Caida.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha16:
        if fecha == i['mes_vigencia'] and base == '21':
            Caida.objects.filter(mes_vigencia=fecha).delete()

    control_fecha17 = CosteRiesgo.objects.values('codmes').order_by('codmes').distinct('codmes')
    for i in control_fecha17:
        if fecha == i['codmes'] and base == '22':
            CosteRiesgo.objects.filter(codmes=fecha).delete()

    control_fecha18 = CosteRiesgo2.objects.values('codmes').order_by('codmes').distinct('codmes')
    for i in control_fecha18:
        if fecha == i['codmes'] and base == '23':
            CosteRiesgo2.objects.filter(codmes=fecha).delete()

    control_fecha19 = Stock.objects.values('codmes').order_by('codmes').distinct('codmes')
    for i in control_fecha19:
        if fecha == i['codmes'] and base == '24':
            Stock.objects.filter(codmes=fecha).delete()

    control_fecha20 = Dotaciones.objects.values('codmes').order_by('codmes').distinct('codmes')
    for i in control_fecha20:
        if fecha == i['codmes'] and base == '25':
            Dotaciones.objects.filter(codmes=fecha).delete()

    control_fecha21 = SeguimientoTer.objects.values('mes_vigencia').order_by('mes_vigencia').distinct('mes_vigencia')
    for i in control_fecha21:
        if fecha == i['mes_vigencia'] and base == '26':
            SeguimientoTer.objects.filter(mes_vigencia=fecha).delete()
    

    static_url=settings.STATIC_URL

    return render('reports/delete.html', locals(),
                  context_instance=RequestContext(request))


# Vista para comentarios
@login_required
def comentario(request, filtro1='1', filtro2='1', filtro3='1'):
    meses = Seguimiento1.objects.values_list('mes_vigencia', flat=True).distinct().order_by('mes_vigencia')
    filtro1 = str(filtro1)
    filtro2 = str(filtro2.replace('_','/'))
    filtro3 = str(filtro3.replace('_',':'))
    coment = Comentario.objects.all()
    coment2 = Comentario.objects.values('periodo','comentario').filter(periodo='201510')

    if filtro1 == '1':
        username = None
        if request.method == 'POST':
            if request.user.is_authenticated():
                username = request.user.username
                periodo = request.POST.get('periodo')
                hora1 = datetime.now().strftime("%H:%M:%S")
                title = request.POST.get('titulo')
                comentario = request.POST.get('comentarios')
                comentario = comentario.encode('utf-8')
                comentario2 = str(comentario.replace('\r\n','<br/>'))
                comentario_instance = Comentario.objects.create(usuario=username,titulo=title,periodo=periodo,comentario=comentario2, tiempo=hoy, hora=hora1 )
                comentario_instance2 = ComentarioBackup.objects.create(usuario=username,titulo=title,periodo=periodo,comentario=comentario2, tiempo=hoy, hora=hora1 ) 
                comments = Comentario.objects.values('usuario','tiempo').order_by('usuario')
    else:
        Comentario.objects.filter(usuario=filtro1,tiempo=filtro2,hora=filtro3).delete()


    static_url=settings.STATIC_URL
    tipo_side = 4
    return render('reports/comentario.html', locals(),
                  context_instance=RequestContext(request))

# Vista para tarjetas campana
@login_required
def tarjeta_campana(request):
    segmentos = Campana2.objects.values('mes_vigencia').annotate(cant_tc=Sum('q_tc')).order_by('mes_vigencia')
    segmentos_totales = Campana2.objects.values('mes_vigencia','segmento').annotate(cant_tc=Sum('q_tc')).order_by('mes_vigencia')
    totales_ava = {}; totales_ms = {}; totales_noph = {}; totales_nc = {};
    for i in segmentos_totales:
        if i['segmento'] == 'AVA':
            totales_ava[i['mes_vigencia']] = i['cant_tc']
        if i['segmento'] == 'MS':
            totales_ms[i['mes_vigencia']] = i['cant_tc']
        if i['segmento'] == 'No PH':
            totales_noph[i['mes_vigencia']] = i['cant_tc']
        if i['segmento'] == 'NoCli':
            totales_nc[i['mes_vigencia']] = i['cant_tc']

    segmento_ava = Campana2.objects.values('mes_vigencia','segmento').filter(segmento='AVA').annotate(cant_tc=Sum('q_tc')).order_by('mes_vigencia')
    segmento_ms = Campana2.objects.values('mes_vigencia','segmento').filter(segmento='MS').annotate(cant_tc=Sum('q_tc')).order_by('mes_vigencia')
    segmento_noph = Campana2.objects.values('mes_vigencia','segmento').filter(segmento='No PH').annotate(cant_tc=Sum('q_tc')).order_by('mes_vigencia')
    segmento_nocli = Campana2.objects.values('mes_vigencia','segmento').filter(segmento='NoCli').annotate(cant_tc=Sum('q_tc')).order_by('mes_vigencia')
    grafica_segmento = zip(segmento_ava, segmento_ms, segmento_noph, segmento_nocli, segmentos)
    
    tickets_ava = EfectividadTC.objects.values('mes_vigencia','segmento').filter(segmento='AVA').annotate(cant_ticket=Sum('total_form'),monto_ticket=Sum('monto_form'),monto_oferta=Sum('monto_ofer')).order_by('mes_vigencia')
    tickets_ms = EfectividadTC.objects.values('mes_vigencia','segmento').filter(segmento='MS').annotate(cant_ticket=Sum('total_form'),monto_ticket=Sum('monto_form'),monto_oferta=Sum('monto_ofer')).order_by('mes_vigencia')
    tickets_noph = EfectividadTC.objects.values('mes_vigencia','segmento').filter(segmento='No PH').annotate(cant_ticket=Sum('total_form'),monto_ticket=Sum('monto_form'),monto_oferta=Sum('monto_ofer')).order_by('mes_vigencia')
    tickets_nocli = EfectividadTC.objects.values('mes_vigencia','segmento').filter(segmento='NoCli').annotate(cant_ticket=Sum('total_form'),monto_ticket=Sum('monto_form'),monto_oferta=Sum('monto_ofer')).order_by('mes_vigencia')
    grafica_tickets = zip(tickets_ava, tickets_ms, tickets_noph, tickets_nocli)

    meses = EfectividadTC.objects.values('mes_vigencia').distinct().order_by('mes_vigencia')
    cantidad_total = EfectividadTC.objects.values('mes_vigencia').annotate(cant_tc=Sum('total_form')).order_by('mes_vigencia')
    totales_dict = {};
    for i in meses:
        for j in cantidad_total:
            if i['mes_vigencia'] == j['mes_vigencia']:
                totales_dict[i['mes_vigencia']] = j['cant_tc']

    segmentos_efect = EfectividadTC.objects.values('mes_vigencia','segmento').annotate(cant_tc=Sum('total_form')).order_by('mes_vigencia')
    ava_dict = {}; ms_dict = {}; noph_dict = {}; nocli_dict = {};
    for i in meses:
      for j in segmentos_efect:
        if i['mes_vigencia'] == j['mes_vigencia']:
          if j['segmento'] == 'AVA':
            ava_dict[i['mes_vigencia']] = j['cant_tc']/totales_ava[i['mes_vigencia']]
          elif j['segmento'] == 'MS':
            ms_dict[i['mes_vigencia']] = j['cant_tc']/totales_ms[i['mes_vigencia']]
          elif j['segmento'] == 'No PH':
            noph_dict[i['mes_vigencia']] = j['cant_tc']/totales_noph[i['mes_vigencia']]
          elif j['segmento'] == 'NoCli':
            nocli_dict[i['mes_vigencia']] = j['cant_tc']/totales_nc[i['mes_vigencia']]
          else:
            ava_dict[i['mes_vigencia']] = 0
            ms_dict[i['mes_vigencia']] = 0
            noph_dict[i['mes_vigencia']] = 0
            nocli_dict[i['mes_vigencia']] = 0


    categorias = EfectividadTC.objects.values('mes_vigencia','tipo_clie').annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    dict_dep = {}; dict_indep = {}; dict_pnn = {}; dict_nr = {};
    ticket_dep = {}; ticket_indep = {}; ticket_pnn = {}; ticket_nr = {};
    for i in meses:
      for j in categorias:
        if i['mes_vigencia'] == j['mes_vigencia']:
          if j['tipo_clie'] == 'DEPENDIENTE':
            dict_dep[i['mes_vigencia']] = j['cant_tc']
            ticket_dep[i['mes_vigencia']] = j['monto_ticket']/j['cant_tc']
          elif j['tipo_clie'] == 'INDEPENDIENTE':
            dict_indep[i['mes_vigencia']] = j['cant_tc']
            ticket_indep[i['mes_vigencia']] = j['monto_ticket']/j['cant_tc']
          elif j['tipo_clie'] == 'PNN':
            dict_pnn[i['mes_vigencia']] = j['cant_tc']
            ticket_pnn[i['mes_vigencia']] = j['monto_ticket']/j['cant_tc']
          elif j['tipo_clie'] == 'NO RECONOCIDO':
            dict_nr[i['mes_vigencia']] = j['cant_tc']
            ticket_nr[i['mes_vigencia']] = j['monto_ticket']/j['cant_tc']
          else:
            dict_dep[i['mes_vigencia']] = 0
            dict_indep[i['mes_vigencia']] = 0
            dict_pnn[i['mes_vigencia']] = 0
            dict_nr[i['mes_vigencia']] = 0
            ticket_dep[i['mes_vigencia']] = 0
            ticket_indep[i['mes_vigencia']] = 0
            ticket_pnn[i['mes_vigencia']] = 0
            ticket_nr[i['mes_vigencia']] = 0


    buro1 = EfectividadTC.objects.values('mes_vigencia').filter(buro__in=['G1','G2','G3','G4']).annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro1_dict = {}; ticket_buro1 = {};
    for i in buro1:
        buro1_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro1[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']

    buro2 = EfectividadTC.objects.values('mes_vigencia',).filter(buro__in=['G5']).annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro2_dict = {}; ticket_buro2 = {};
    for i in buro2:
        buro2_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro2[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']

    buro3 = EfectividadTC.objects.values('mes_vigencia').filter(buro__in=['G6','G7','G8']).annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro3_dict = {}; ticket_buro3 = {};
    for i in buro3:
        buro3_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro3[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']

    buro4 = EfectividadTC.objects.values('mes_vigencia',).filter(buro__in=['NB']).annotate(cant_tc=Sum('total_form'),monto_ticket=Sum('monto_form')).order_by('mes_vigencia')
    buro4_dict = {}; ticket_buro4 = {};
    for i in buro4:
        buro4_dict[i['mes_vigencia']] = i['cant_tc']
        ticket_buro4[i['mes_vigencia']] = i['monto_ticket']/i['cant_tc']


    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_tarjeta.html', locals(),
                  context_instance=RequestContext(request))

# Vista para Altas Seguimiento
@login_required
def altas_seguimiento(request):

    meses = AltasSeguimiento.objects.values('mes_alta').distinct().order_by('mes_alta')
    
    altas_tot = AltasSeguimiento.objects.values('mes_alta').annotate(cant=Sum('ctas')).order_by('mes_alta')
    tot_dict = {}
    for i in altas_tot:
        tot_dict[i['mes_alta']] = i['cant']
    
    altas_banco = AltasSeguimiento.objects.values('mes_alta','empresa').annotate(cant=Sum('ctas')).order_by('mes_alta')
    bbva_dict = {}; bcp_dict = {}; ibk_dict = {}; sco_dict = {}; citi_dict = {};
    for i in meses:
      for j in altas_banco:
        if i['mes_alta'] == j['mes_alta']:
          if j['empresa'] == '0.BBVA':
            bbva_dict[i['mes_alta']] = j['cant']*100/tot_dict[i['mes_alta']]
          elif j['empresa'] == '1.BCP':
            bcp_dict[i['mes_alta']] = j['cant']*100/tot_dict[i['mes_alta']]
          elif j['empresa'] == '2.IBK':
            ibk_dict[i['mes_alta']] = j['cant']*100/tot_dict[i['mes_alta']]
          elif j['empresa'] == '3.SCO':
            sco_dict[i['mes_alta']] = j['cant']*100/tot_dict[i['mes_alta']]
          elif j['empresa'] == '9.CITI':
            citi_dict[i['mes_alta']] = j['cant']*100/tot_dict[i['mes_alta']]
          else:
            bbva_dict[i['mes_alta']] = 0
            bcp_dict[i['mes_alta']] = 0
            ibk_dict[i['mes_alta']] = 0
            sco_dict[i['mes_alta']] = 0
            citi_dict[i['mes_alta']] = 0

    buro_total= AltasSeguimiento.objects.values('mes_alta','empresa').annotate(cant=Sum('ctas')).order_by('mes_alta')
    burobbva_dict = {}; burobcp_dict = {}; buroibk_dict = {}; burosco_dict = {};
    burociti_dict = {};
    for i in buro_total:
        if i['empresa'] == '0.BBVA':
            burobbva_dict[i['mes_alta']] = i['cant']
        if i['empresa'] == '1.BCP':
            burobcp_dict[i['mes_alta']] = i['cant']
        if i['empresa'] == '2.IBK':
            buroibk_dict[i['mes_alta']] = i['cant']
        if i['empresa'] == '3.SCO':
            burosco_dict[i['mes_alta']] = i['cant']
        if i['empresa'] == '9.CITI':
            burociti_dict[i['mes_alta']] = i['cant']

    buro= AltasSeguimiento.objects.values('mes_alta','buro','empresa').annotate(cant=Sum('ctas')).order_by('mes_alta')
    buro1_bbva = {}; buro2_bbva = {}; buro3_bbva = {}; buro4_bbva = {}; buro5_bbva = {};
    buro1_bcp = {}; buro2_bcp = {}; buro3_bcp = {}; buro4_bcp = {}; buro5_bcp = {};
    buro1_ibk = {}; buro2_ibk = {}; buro3_ibk = {}; buro4_ibk = {}; buro5_ibk = {};
    for i in meses:
      for j in buro:
        if i['mes_alta'] == j['mes_alta']:
            if j['empresa'] == '0.BBVA':
              if j['buro'] == '1. G1-G3':
                buro1_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['buro'] == '2. G4-G5':
                buro2_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['buro'] == '3. G6':
                buro3_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['buro'] == '4. G7-G8':
                buro4_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['buro'] == '5. NB':
                buro5_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              else:
                buro1_bbva[i['mes_alta']] = 0
                buro2_bbva[i['mes_alta']] = 0
                buro3_bbva[i['mes_alta']] = 0
                buro4_bbva[i['mes_alta']] = 0
                buro5_bbva[i['mes_alta']] = 0
            if j['empresa'] == '1.BCP':
              if j['buro'] == '1. G1-G3':
                buro1_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['buro'] == '2. G4-G5':
                buro2_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['buro'] == '3. G6':
                buro3_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['buro'] == '4. G7-G8':
                buro4_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['buro'] == '5. NB':
                buro5_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              else:
                buro1_bcp[i['mes_alta']] = 0
                buro2_bcp[i['mes_alta']] = 0
                buro3_bcp[i['mes_alta']] = 0
                buro4_bcp[i['mes_alta']] = 0
                buro5_bcp[i['mes_alta']] = 0
            if j['empresa'] == '2.IBK':
              if j['buro'] == '1. G1-G3':
                buro1_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['buro'] == '2. G4-G5':
                buro2_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['buro'] == '3. G6':
                buro3_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['buro'] == '4. G7-G8':
                buro4_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['buro'] == '5. NB':
                buro5_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              else:
                buro1_ibk[i['mes_alta']] = 0
                buro2_ibk[i['mes_alta']] = 0
                buro3_ibk[i['mes_alta']] = 0
                buro4_ibk[i['mes_alta']] = 0
                buro5_ibk[i['mes_alta']] = 0

    cliente= AltasSeguimiento.objects.values('mes_alta','cat_cliente','empresa').annotate(cant=Sum('ctas')).order_by('mes_alta')
    dep_bbva = {}; indep_bbva = {}; pnn_bbva = {}; nr_bbva = {}; otro_bbva = {};
    dep_bcp = {}; indep_bcp = {}; pnn_bcp = {}; nr_bcp = {}; otro_bcp = {};
    dep_ibk = {}; indep_ibk = {}; pnn_ibk = {}; nr_ibk = {}; otro_ibk = {};
    for i in meses:
      for j in cliente:
        if j['empresa'] == '0.BBVA':
            if i['mes_alta'] == j['mes_alta']:
              if j['cat_cliente'] == '1. Dependiente':
                dep_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['cat_cliente'] == '2. Independiente':
                indep_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['cat_cliente'] == '3. PNN':
                pnn_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['cat_cliente'] == '4.No Reconocido':
                nr_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['cat_cliente'] == '':
                otro_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              else:
                dep_bbva[i['mes_alta']] = 0
                indep_bbva[i['mes_alta']] = 0
                pnn_bbva[i['mes_alta']] = 0
                nr_bbva[i['mes_alta']] = 0
                otro_bbva[i['mes_alta']] = 0
        if j['empresa'] == '1.BCP':
            if i['mes_alta'] == j['mes_alta']:
              if j['cat_cliente'] == '1. Dependiente':
                dep_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['cat_cliente'] == '2. Independiente':
                indep_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['cat_cliente'] == '3. PNN':
                pnn_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['cat_cliente'] == '4.No Reconocido':
                nr_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['cat_cliente'] == '':
                otro_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              else:
                dep_bcp[i['mes_alta']] = 0
                indep_bcp[i['mes_alta']] = 0
                pnn_bcp[i['mes_alta']] = 0
                nr_bcp[i['mes_alta']] = 0
                otro_bcp[i['mes_alta']] = 0
        if j['empresa'] == '2.IBK':
            if i['mes_alta'] == j['mes_alta']:
              if j['cat_cliente'] == '1. Dependiente':
                dep_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['cat_cliente'] == '2. Independiente':
                indep_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['cat_cliente'] == '3. PNN':
                pnn_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['cat_cliente'] == '4.No Reconocido':
                nr_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['cat_cliente'] == '':
                otro_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              else:
                dep_ibk[i['mes_alta']] = 0
                indep_ibk[i['mes_alta']] = 0
                pnn_ibk[i['mes_alta']] = 0
                nr_ibk[i['mes_alta']] = 0
                otro_ibk[i['mes_alta']] = 0

    ingresos_bbva= AltasSeguimiento.objects.values('mes_alta','rg_ingreso','empresa').annotate(cant=Sum('ctas')).order_by('mes_alta')
    ing1_bbva = {}; ing2_bbva = {}; ing3_bbva = {}; ing4_bbva = {}; ing5_bbva = {}; ing6_bbva = {}; ing7_bbva = {}; 
    ing1_bcp = {}; ing2_bcp = {}; ing3_bcp = {}; ing4_bcp = {}; ing5_bcp = {}; ing6_bcp = {}; ing7_bcp = {}; 
    ing1_ibk = {}; ing2_ibk = {}; ing3_ibk = {}; ing4_ibk = {}; ing5_ibk = {}; ing6_ibk = {}; ing7_ibk = {}; 
    for i in meses:
      for j in ingresos_bbva:
        if j['empresa'] == '0.BBVA':
            if i['mes_alta'] == j['mes_alta']:
              if j['rg_ingreso'] == '00 En blanco':
                ing1_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '01 0-1Mil':
                ing2_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '02 1-1.5Mil':
                ing3_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '03 1.5-2.5Mil':
                ing4_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '04 2.5-3.5Mil':
                ing5_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '05 3.5-4.5Mil':
                ing6_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '06 +4.5Mil':
                ing7_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              else:
                ing1_bbva[i['mes_alta']] = 0
                ing2_bbva[i['mes_alta']] = 0
                ing3_bbva[i['mes_alta']] = 0
                ing4_bbva[i['mes_alta']] = 0
                ing5_bbva[i['mes_alta']] = 0
                ing6_bbva[i['mes_alta']] = 0
                ing7_bbva[i['mes_alta']] = 0
        if j['empresa'] == '1.BCP':
            if i['mes_alta'] == j['mes_alta']:
              if j['rg_ingreso'] == '00 En blanco':
                ing1_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '01 0-1Mil':
                ing2_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '02 1-1.5Mil':
                ing3_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '03 1.5-2.5Mil':
                ing4_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '04 2.5-3.5Mil':
                ing5_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '05 3.5-4.5Mil':
                ing6_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '06 +4.5Mil':
                ing7_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              else:
                ing1_bcp[i['mes_alta']] = 0
                ing2_bcp[i['mes_alta']] = 0
                ing3_bcp[i['mes_alta']] = 0
                ing4_bcp[i['mes_alta']] = 0
                ing5_bcp[i['mes_alta']] = 0
                ing6_bcp[i['mes_alta']] = 0
                ing7_bcp[i['mes_alta']] = 0
        if j['empresa'] == '2.IBK':
            if i['mes_alta'] == j['mes_alta']:
              if j['rg_ingreso'] == '00 En blanco':
                ing1_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '01 0-1Mil':
                ing2_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '02 1-1.5Mil':
                ing3_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '03 1.5-2.5Mil':
                ing4_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '04 2.5-3.5Mil':
                ing5_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '05 3.5-4.5Mil':
                ing6_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_ingreso'] == '06 +4.5Mil':
                ing7_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              else:
                ing1_ibk[i['mes_alta']] = 0
                ing2_ibk[i['mes_alta']] = 0
                ing3_ibk[i['mes_alta']] = 0
                ing4_ibk[i['mes_alta']] = 0
                ing5_ibk[i['mes_alta']] = 0
                ing6_ibk[i['mes_alta']] = 0
                ing7_ibk[i['mes_alta']] = 0

    edad_bbva= AltasSeguimiento.objects.values('mes_alta','rg_edad','empresa').annotate(cant=Sum('ctas')).order_by('mes_alta')
    edad1_bbva = {}; edad2_bbva = {}; edad3_bbva = {}; edad4_bbva = {}; edad5_bbva = {}; edad6_bbva = {};
    edad1_bcp = {}; edad2_bcp = {}; edad3_bcp = {}; edad4_bcp = {}; edad5_bcp = {}; edad6_bcp = {};  
    edad1_ibk = {}; edad2_ibk = {}; edad3_ibk = {}; edad4_ibk = {}; edad5_ibk = {}; edad6_ibk = {};  
    for i in meses:
      for j in edad_bbva:
        if j['empresa'] == '0.BBVA':
            if i['mes_alta'] == j['mes_alta']:
              if j['rg_edad'] == '00 En blanco':
                edad1_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_edad'] == '01 18-22':
                edad2_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_edad'] == '02 23-24':
                edad3_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_edad'] == '02 25-32':
                edad4_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_edad'] == '03 33-43':
                edad5_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              elif j['rg_edad'] == '04 +43':
                edad6_bbva[i['mes_alta']] = j['cant']*100/burobbva_dict[i['mes_alta']]
              else:
                edad1_bbva[i['mes_alta']] = 0
                edad2_bbva[i['mes_alta']] = 0
                edad3_bbva[i['mes_alta']] = 0
                edad4_bbva[i['mes_alta']] = 0
                edad5_bbva[i['mes_alta']] = 0
                edad6_bbva[i['mes_alta']] = 0
        if j['empresa'] == '1.BCP':
            if i['mes_alta'] == j['mes_alta']:
              if j['rg_edad'] == '00 En blanco':
                edad1_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_edad'] == '01 18-22':
                edad2_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_edad'] == '02 23-24':
                edad3_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_edad'] == '02 25-32':
                edad4_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_edad'] == '03 33-43':
                edad5_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              elif j['rg_edad'] == '04 +43':
                edad6_bcp[i['mes_alta']] = j['cant']*100/burobcp_dict[i['mes_alta']]
              else:
                edad1_bcp[i['mes_alta']] = 0
                edad2_bcp[i['mes_alta']] = 0
                edad3_bcp[i['mes_alta']] = 0
                edad4_bcp[i['mes_alta']] = 0
                edad5_bcp[i['mes_alta']] = 0
                edad6_bcp[i['mes_alta']] = 0
        if j['empresa'] == '2.IBK':
            if i['mes_alta'] == j['mes_alta']:
              if j['rg_edad'] == '00 En blanco':
                edad1_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_edad'] == '01 18-22':
                edad2_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_edad'] == '02 23-24':
                edad3_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_edad'] == '02 25-32':
                edad4_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_edad'] == '03 33-43':
                edad5_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              elif j['rg_edad'] == '04 +43':
                edad6_ibk[i['mes_alta']] = j['cant']*100/buroibk_dict[i['mes_alta']]
              else:
                edad1_ibk[i['mes_alta']] = 0
                edad2_ibk[i['mes_alta']] = 0
                edad3_ibk[i['mes_alta']] = 0
                edad4_ibk[i['mes_alta']] = 0
                edad5_ibk[i['mes_alta']] = 0
                edad6_ibk[i['mes_alta']] = 0
                        
    static_url=settings.STATIC_URL
    #tipo_side = 4
    return render('reports/seguimiento_altas.html', locals(),
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
	fecha='201607'
    elif periodo == '5':
      fecha='201608'
    elif periodo == '6':
      fecha='201609'
    elif periodo == '7':
      fecha='201610'
    meses_mapa = Mapa.objects.values('codmes').order_by('codmes').distinct()
    list_meses=[]; d=0
    for i in meses_mapa:
	list_meses.append(i['codmes'])
    d = len(list_meses)
    ubigeo = Mapa.objects.values('ubigeo').order_by('ubigeo').distinct()
    distrito = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA').annotate(mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    contrato=Mapa.objects.values('ubigeo','codmes').filter(provincia='LIMA', codmes=fecha).annotate(num=Sum('ctas')).order_by('ubigeo')
    dict_ctas = {}
    for i in contrato:
	dict_ctas[i['ubigeo']]=i['num']
    distrito1 = Mapa.objects.values('ubigeo','codmes', 'distrito').filter(provincia='LIMA', codmes=fecha).annotate(contrato=Sum(F('ctas')),inver=Sum(F('inv')),mora=Sum(F('catrasada'))*100/Sum(F('inv'))).order_by('ubigeo')
    dict_contra = {}; dict_contra1 = {}; dict_contra2 = {}; dict_contra3 = {};  
    dict_inv = {}; dict_inv1 = {}; dict_inv2 = {}; dict_inv3 = {};
    dict_morac = {}; dict_morac1 = {}; dict_morac2 = {}; dict_morac3 = {};
    for i in distrito1:
	dict_contra[i['ubigeo']]=i['contrato']
	dict_inv[i['ubigeo']]=i['inver']
	dict_morac[i['ubigeo']]=i['mora']
    vinculo_dep = Mapa.objects.values('ubigeo','codmes').filter(provincia='LIMA', codmes=fecha,vinculo='1. Dependiente').annotate(contrato=Sum(F('ctas'))).order_by('ubigeo')
    dict_vinculo = {}
    for i in vinculo_dep:
	dict_vinculo[i['ubigeo']]=i['contrato']*100/dict_ctas[i['ubigeo']]

    dict_moras = {}; dict_moras1 = {}; 
    dict_moras2 = {}; dict_moras3 = {};dict_moras4 = {};
    dict_moras5 = {}; dict_moras6 = {};
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
          dict_moras[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras[i['ubigeo']]='#A6D974'
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
          dict_moras1[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras1[i['ubigeo']]='#A6D974'
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
          dict_moras2[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras2[i['ubigeo']]='#A6D974'
      if i['codmes']=='201607':
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
          dict_moras3[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras3[i['ubigeo']]='#A6D974'
      if i['codmes']=='201608':
        if i['mora']>3:
          dict_moras4[i['ubigeo']]='#E31A1C'
        if i['mora']>2 and i['mora']<=3:
          dict_moras4[i['ubigeo']]='#FC4E2A'
        if i['mora']>1.5 and i['mora']<=2:
          dict_moras4[i['ubigeo']]='#FB8D29'
        if i['mora']>1.2 and i['mora']<=1.5:
          dict_moras4[i['ubigeo']]='#FEB228'
        if i['mora']>0.9 and i['mora']<=1.2:
          dict_moras4[i['ubigeo']]='#FED976'
        if i['mora']>0.6 and i['mora']<=0.9:
          dict_moras4[i['ubigeo']]='#FBE975'
        if i['mora']>0.3 and i['mora']<=0.6:
          dict_moras4[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras4[i['ubigeo']]='#A6D974'
      if i['codmes']=='201609':
        if i['mora']>3:
          dict_moras5[i['ubigeo']]='#E31A1C'
        if i['mora']>2 and i['mora']<=3:
          dict_moras5[i['ubigeo']]='#FC4E2A'
        if i['mora']>1.5 and i['mora']<=2:
          dict_moras5[i['ubigeo']]='#FB8D29'
        if i['mora']>1.2 and i['mora']<=1.5:
          dict_moras5[i['ubigeo']]='#FEB228'
        if i['mora']>0.9 and i['mora']<=1.2:
          dict_moras5[i['ubigeo']]='#FED976'
        if i['mora']>0.6 and i['mora']<=0.9:
          dict_moras5[i['ubigeo']]='#FBE975'
        if i['mora']>0.3 and i['mora']<=0.6:
          dict_moras5[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras5[i['ubigeo']]='#A6D974'
      if i['codmes']=='201610':
        if i['mora']>3:
          dict_moras6[i['ubigeo']]='#E31A1C'
        if i['mora']>2 and i['mora']<=3:
          dict_moras6[i['ubigeo']]='#FC4E2A'
        if i['mora']>1.5 and i['mora']<=2:
          dict_moras6[i['ubigeo']]='#FB8D29'
        if i['mora']>1.2 and i['mora']<=1.5:
          dict_moras6[i['ubigeo']]='#FEB228'
        if i['mora']>0.9 and i['mora']<=1.2:
          dict_moras6[i['ubigeo']]='#FED976'
        if i['mora']>0.6 and i['mora']<=0.9:
          dict_moras6[i['ubigeo']]='#FBE975'
        if i['mora']>0.3 and i['mora']<=0.6:
          dict_moras6[i['ubigeo']]='#66BD63'
        if i['mora']<=0.3:
          dict_moras6[i['ubigeo']]='#A6D974'

    return HttpResponse(distrito1)

def json_limaprov(request):
    periodo = request.POST['periodo']
    if periodo == '1':
	fecha='201312'
    elif periodo == '2':
	fecha='201412'
    elif periodo == '3':
	fecha='201512'
    elif periodo == '4':
	fecha='201607'
    limaprov = Mapa.objects.values('lima_prov').filter(codmes=fecha).annotate(num=Sum('ctas')).order_by('lima_prov')

    return HttpResponse(limaprov)



# Vistas para carga de csv
def load(request):
    static_url=settings.STATIC_URL
    #Campana2.objects.all().delete()
    #Evaluaciontc.objects.all().delete()
    #Evaluacionpld.objects.all().delete()
    #Seguimiento1.objects.all().delete()
    #HipotecaConce.objects.all().delete()
    #Moras.objects.all().delete()
    #IncreLinea.objects.all().delete()
    #PrestInmediato.objects.all().delete()
    #Lifemiles.objects.all().delete()
    #Mapa.objects.all().delete()
    #DepartamentosWeb.objects.all().delete()
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

def carga_seguimiento(request):
    if request.method == 'POST':
        form = UploadSeguimiento(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['seguimiento']
            SeguimientoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)


def carga_seguimiento1(request):
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
    #Moras.objects.all().delete()
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

def carga_campanaefec(request):
    CampanaEfec.objects.all().delete()
    if request.method == 'POST':
        form = UploadCampanaEfec(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['campanaefec']
            CampanaEfecCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

#def carga_campanalabseg(request):
    #CampanaLabSeg.objects.all().delete()
    #if request.method == 'POST':
        #form = UploadCampanaLabSeg(request.POST, request.FILES)
        #if form.is_valid():
            #csv_file = request.FILES['campanalabseg']
            #CampanaLabSegCsv.import_data(data = csv_file)
            #return campana_resumen(request)
        #else:
            #return load(campana_resumen)
    #else:
        #return load(campana_resumen)

def carga_campanaequifax(request):
    CampanaEquifax.objects.all().delete()
    if request.method == 'POST':
        form = UploadCampanaEquifax(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['campanaequifax']
            CampanaEquifaxCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_comentario(request):
    if request.method == 'POST':
        form = UploadComentario(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['comentario']
            ComentarioCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_efectividadtc(request):
    if request.method == 'POST':
        form = UploadEfectividadTC(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['efectividadtc']
            EfectividadTCCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_altasseguimiento(request):
    #AltasSeguimiento.objects.all().delete()
    if request.method == 'POST':
        form = UploadAltasSeguimiento(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['altasseguimiento']
            AltasSeguimientoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_ofertasproducto(request):
    if request.method == 'POST':
        form = UploadOfertasProducto(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['ofertasproducto']
            OfertasProductoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_stock(request):
    if request.method == 'POST':
        form = UploadStock(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['stock']
            StockCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_dotaciones(request):
    if request.method == 'POST':
        form = UploadDotaciones(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['dotaciones']
            DotacionesCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_costeriesgo(request):
    if request.method == 'POST':
        form = UploadCosteRiesgo(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['costeriesgo']
            CosteRiesgoCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_costeriesgo2(request):
    if request.method == 'POST':
        form = UploadCosteRiesgo2(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['costeriesgo2']
            CosteRiesgo2Csv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_seguimientoter(request):
    if request.method == 'POST':
        form = UploadSeguimientoTer(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['seguimientoter']
            SeguimientoTerCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_stocktelefonica(request):
    if request.method == 'POST':
        form = UploadStockTelefonica(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['stocktelefonica']
            StockTelefonicaCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def carga_formtelefonica(request):
    if request.method == 'POST':
        form = UploadFormTelefonica(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['formtelefonica']
            FormTelefonicaCsv.import_data(data = csv_file)
            return campana_resumen(request)
        else:
            return load(campana_resumen)
    else:
        return load(campana_resumen)

def excel(request):

    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = handle_uploaded_file(request.FILES['file'])
            print newdoc
            print "you in"
            newdoc.save()

            return HttpResponseRedirect(reverse('upload.views.excel'))
    else:
        form = UploadFileForm() # A empty, unbound form
    #documents = Document.objects.all()
    return campana_resumen(request)

def handle_uploaded_file(f):
    destination = open('media/data.xls', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

