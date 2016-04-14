# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Case, When, IntegerField, F, Q, CharField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response as render
from django.template import RequestContext

from datetime import datetime
from models import *
from forms import *
from django.contrib.auth import authenticate, login, logout

import csv, itertools

fecha_actual = datetime.now().strftime("%Y%m")

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
def campana_resumen(request,fecha=fecha_actual):
    detalles = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'), q_efectivo_plus=Sum('q_efectivo_plus'), q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea'),monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000), monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000), monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000), monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))
    total = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(total_q=Sum(F('q_tc')+F('q_pld')+F('q_veh')+F('q_subrogacion')+F('q_renovado')+F('q_auto_2da')+F('q_adelanto_sueldo')+F('q_efectivo_plus')+F('q_prestamo_inmediato')+F('q_incr_linea')),total_m=Sum(F('monto_tc')/1000000+F('monto_pld')/1000000+F('monto_veh')/1000000+F('monto_subrogacion')/1000000+F('monto_renovado')/1000000+F('monto_auto_2da')/1000000+F('monto_adelanto_sueldo')/1000000+F('monto_efectivo_plus')/1000000+F('monto_prestamo_inmediato')/1000000+F('monto_incr_linea')/1000000))
    detalles2 = zip(detalles,total)

    segmento_fast = Campana2.objects.values('segmento','tipo_clie' ).exclude(segmento__in=['NoCli','EMPLEADO']).filter( mes_vigencia=fecha, tipo_clie='A1' ).annotate(cantidad=Sum('ofertas')).order_by('segmento')
    segmento_cs = Campana2.objects.filter(mes_vigencia=fecha, tipo_clie='1A').exclude(segmento__in=['NoCli','EMPLEADO']).values('segmento','tipo_clie').annotate(cantidad=Sum('ofertas')).order_by('segmento')
    seg_tot = Campana2.objects.filter(mes_vigencia=fecha).values('segmento').exclude(segmento__in=['NoCli','EMPLEADO']).annotate(total=Sum('ofertas')).order_by('segmento')
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
#def campana_ofertas(request):
    #clientes = Verificaciones.objects.values('segmento').annotate(num_clientes=Sum(F('exonera_ambas')+F('exonera_solo_vl')+F('exonera_solo_vd')+F('requiere_ambas'))).filter(mes_vigencia='201604').order_by('segmento')
    #ofertas = Campana.objects.all().filter(mes_vigencia='201604').order_by('segmento')
    #montos = Campana.objects.values('segmento').annotate(monto=Sum(F('monto_tc')+F('monto_pld')+F('monto_veh')+F('monto_subrogacion')+F('monto_tc_entry_level')+F('monto_renovado')+F('monto_auto_2da')+F('monto_adelanto_sueldo')+F('monto_efectivo_plus')+F('monto_prestamo_inmediato')+F('monto_incr_linea'))).filter(mes_vigencia='201604').order_by('segmento')
    #ofer = zip(ofertas, clientes, montos)
    #static_url=settings.STATIC_URL
    #tipo_side = 1
    #return render('reports/campana_ofertas.html', locals(),
                  #context_instance=RequestContext(request))

@login_required
def campana_ofertas(request, fecha=fecha_actual):
    clientes = Campana2.objects.values('segmento').filter(mes_vigencia= fecha).annotate(num_clientes=Sum('ofertas')).order_by('segmento')
    ofertas = Campana2.objects.values('codigo_campana','segmento', 'mes_vigencia').filter(mes_vigencia=fecha).annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_tc_entry_level=Sum('q_tc_entry_level'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea')).order_by('segmento')
    montos = Campana2.objects.values('segmento').filter(mes_vigencia=fecha).annotate(monto=Sum(F('monto_tc')+F('monto_pld')+F('monto_veh')+F('monto_subrogacion')+F('monto_tc_entry_level')+F('monto_renovado')+F('monto_auto_2da')+F('monto_adelanto_sueldo')+F('monto_efectivo_plus')+F('monto_prestamo_inmediato')+F('monto_incr_linea'))).order_by('segmento')
    ofer = zip(ofertas, clientes, montos)
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_ofertas.html', locals(),
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
    if segmento == 'TOTAL':
       detalles = Campana2.objects.filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea')).annotate(monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000),monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000),monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000),monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))
    else:
       detalles = Campana2.objects.filter(segmento=segmento).filter(mes_vigencia=fecha).values('mes_vigencia').annotate(q_tc=Sum('q_tc'), q_pld=Sum('q_pld'), q_veh=Sum('q_veh'),q_subrogacion=Sum('q_subrogacion'), q_renovado=Sum('q_renovado'), q_auto_2da=Sum('q_auto_2da'), q_adelanto_sueldo=Sum('q_adelanto_sueldo'),q_efectivo_plus=Sum('q_efectivo_plus'),q_prestamo_inmediato=Sum('q_prestamo_inmediato'),q_incr_linea=Sum('q_incr_linea')).annotate(monto_tc=Sum(F('monto_tc')/1000000), monto_pld=Sum(F('monto_pld')/1000000), monto_veh=Sum(F('monto_veh')/1000000),monto_subrogacion=Sum(F('monto_subrogacion')/1000000), monto_tc_entry_level=Sum(F('monto_tc_entry_level')/1000000), monto_renovado=Sum(F('monto_renovado')/1000000), monto_auto_2da=Sum(F('monto_auto_2da')/1000000), monto_adelanto_sueldo=Sum(F('monto_adelanto_sueldo')/1000000),monto_efectivo_plus=Sum(F('monto_efectivo_plus')/1000000),monto_prestamo_inmediato=Sum(F('monto_prestamo_inmediato')/1000000), monto_incr_linea=Sum(F('monto_incr_linea')/1000000))
    control_segmentos = Campana2.objects.all().values('segmento').distinct('segmento')
    print detalles
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_detalles.html', locals(),
                  context_instance=RequestContext(request))


@login_required
def campana_caidas(request, fecha=fecha_actual):
    caidas_ms = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='MS').annotate(num_caidaxms=Sum('cantidad')).order_by('caida')
    caidas_ava = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='AVA').annotate(num_caidaxava=Sum('cantidad')).order_by('caida')
    caidas_noph = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='NO PH + PASIVO').annotate(num_caidaxnoph=Sum('cantidad')).order_by('caida')
    caidas_noclie = Caida.objects.values('caida').filter(mes_vigencia=fecha).filter(segmento='NO CLIENTE').annotate(num_caidaxnoclie=Sum('cantidad')).order_by('caida')
    combo_fechas = Caida.objects.values('mes_vigencia').distinct('mes_vigencia').order_by('-mes_vigencia')
    caidas = zip(caidas_ms, caidas_ava, caidas_noph, caidas_noclie)
    static_url=settings.STATIC_URL
    grafica  = Caida.objects.values('caida').filter(mes_vigencia=fecha).exclude(segmento='PNN').annotate(num_caida=Sum('cantidad')).order_by('caida')
    total = Caida.objects.values('mes_vigencia').filter(mes_vigencia=fecha).annotate(total=Sum('cantidad'))
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
def campana_exoneraciones(request, segmento='TOTAL'):
    if segmento == 'TOTAL':
        exo_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
    else:
        exo_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO AMBAS', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
    control_segmentos = Campana2.objects.all().values('segmento').distinct('segmento')
    exoneraciones = itertools.izip_longest(exo_ambas,exo_vl,exo_vd,req_ambas)
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_exoneraciones.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campana_prueba(request, segmento='TOTAL'):
    if segmento == 'TOTAL':
        exo_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS').annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
    else:
        exo_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO AMBAS', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vl = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VL', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        exo_vd = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='EXONERADO SOLO VD', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
        req_ambas = Campana2.objects.values('mes_vigencia','verificacion').filter(verificacion='REQUIERE AMBAS', segmento=segmento).annotate(cantidad=Sum('ofertas')).order_by('mes_vigencia')
    control_segmentos = Campana2.objects.all().values('segmento').distinct('segmento')
    exoneraciones = itertools.izip_longest(exo_ambas,exo_vl,exo_vd,req_ambas)
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_prueba.html', locals(),
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
    flujo1 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='EXONERADO AMBAS').annotate(num_flujo1=Sum('ofertas')).order_by('tipo_clie')
    flujo2 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='EXONERADO SOLO VD').annotate(num_flujo2=Sum('ofertas')).order_by('tipo_clie')
    flujo3 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='EXONERADO SOLO VL').annotate(num_flujo3=Sum('ofertas')).order_by('tipo_clie')
    flujo4 = Campana2.objects.values('tipo_clie','verificacion').filter(mes_vigencia=fecha,verificacion='REQUIERE AMBAS').annotate(num_flujo4=Sum('ofertas')).order_by('tipo_clie')

    flujo = zip(flujo1, flujo2, flujo3, flujo4)
    static_url=settings.STATIC_URL
    tipo_side = 1
    return render('reports/campana2_flujo.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def campana_altasempresa(request):
    alta1_m1 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia='201509').annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m1 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia='201509').annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m1 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia='201509').annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m1 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia='201509').annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m2 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia='201510').annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m2 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia='201510').annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m2 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia='201510').annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m2 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia='201510').annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m3 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia='201511').annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m3 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia='201511').annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m3 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia='201511').annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m3 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia='201511').annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m4 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia='201512').annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m4 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia='201512').annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m4 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia='201512').annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m4 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia='201512').annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m5 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia='201601').annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m5 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia='201601').annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m5 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia='201601').annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m5 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia='201601').annotate(num_alta=Sum('cantidad')).order_by('empresa')

    alta1_m6 = AltasEmpresa.objects.values('empresa', 'grupo').filter(grupo='2.Oferta >= SF',mes_vigencia='201602').annotate(num_alta1=Sum('cantidad')).order_by('empresa')
    alta2_m6 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='1.Oferta < SF',mes_vigencia='201602').annotate(num_alta2=Sum('cantidad')).order_by('empresa')
    alta3_m6 = AltasEmpresa.objects.values('empresa','grupo').filter(grupo='0.Sin Oferta TDC',mes_vigencia='201602').annotate(num_alta3=Sum('cantidad')).order_by('empresa')
    alta_m6 = AltasEmpresa.objects.values('empresa').filter(mes_vigencia='201602').annotate(num_alta=Sum('cantidad')).order_by('empresa')

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
    dictamenxsco_ap = RVGL.objects.values('dictamen').filter(mes_vigencia='201602').filter(dictamen_sco='AP').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco_du = RVGL.objects.values('dictamen').filter(mes_vigencia='201602').filter(dictamen_sco='DU').annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco_re = RVGL.objects.values('dictamen').filter(mes_vigencia='201602').filter(dictamen_sco='RE').annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
    dictamenxsco = zip(dictamenxsco_ap,dictamenxsco_du,dictamenxsco_re)
    print dictamenxsco_ap
    print dictamenxsco_du
    print dictamenxsco_re
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    static_url=settings.STATIC_URL
    tipo_side = 2
    return render('reports/rvgl_dictamenxsco.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def rvgl2_dictamenxsco(request, fecha, analista):
    if analista == 'TODOS':
       dictamenxsco_ap = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='AP').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
       dictamenxsco_du = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='DU').annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
       dictamenxsco_re = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha).filter(dictamen_sco='RE').annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
       dictamenxsco = zip(dictamenxsco_ap,dictamenxsco_du,dictamenxsco_re)
    else:
       dictamenxsco_ap = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha, analista=analista).filter(dictamen_sco='AP').annotate(num_dictamenxsco_ap=Count('dictamen_sco')).order_by('dictamen')
       dictamenxsco_du = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha, analista=analista).filter(dictamen_sco='DU').annotate(num_dictamenxsco_du=Count('dictamen_sco')).order_by('dictamen')
       dictamenxsco_re = RVGL.objects.values('dictamen').filter(mes_vigencia=fecha, analista=analista).filter(dictamen_sco='RE').annotate(num_dictamenxsco_re=Count('dictamen_sco')).order_by('dictamen')
       dictamenxsco = zip(dictamenxsco_ap,dictamenxsco_du,dictamenxsco_re)
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
    print dictamenxsco_ap
    print dictamenxsco_du
    print dictamenxsco_re
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

def rvgl2_top20terr(request, fecha, analista):
    if analista == 'TODOS':
       top20terr1 = RVGL.objects.filter(mes_vigencia=fecha).values('territorio_nuevo').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic')).order_by('-sum_top20terr1')[:20]
       top20terr2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0).values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
       top20terr = zip(top20terr1, top20terr2)
    else:
       top20terr1 = RVGL.objects.filter(mes_vigencia=fecha).filter(analista=analista).values('territorio_nuevo').annotate(num_top20terr1=Count('importe_solic'), sum_top20terr1=Sum('importe_solic')).order_by('-sum_top20terr1')[:20]
       top20terr2 = RVGL.objects.filter(mes_vigencia=fecha).filter(analista=analista).exclude(importe_aprob=0).values('territorio_nuevo').annotate(num_top20terr2=Count('importe_aprob'), sum_top20terr2=Sum('importe_aprob')).order_by('-sum_top20terr2')[:20]
       top20terr = zip(top20terr1, top20terr2)
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
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
def rvgl2_top20gest(request, fecha, analista):
    if analista == 'TODOS':
       top20gest1 = RVGL.objects.filter(mes_vigencia=fecha).values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic'), sum_top20gest1=Sum('importe_solic')).order_by('-sum_top20gest1')[:20]
       top20gest2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest2=Count('importe_aprob'), sum_top20gest2=Sum('importe_aprob')).order_by('-sum_top20gest2')[:20]
       top20gest = zip(top20gest1,top20gest2)
    else:
       top20gest1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('ejecutivo_cuenta').annotate(num_top20gest1=Count('importe_solic'), sum_top20gest1=Sum('importe_solic')).order_by('-sum_top20gest1')[:20]
       top20gest2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).values('ejecutivo_cuenta').annotate(num_top20gest2=Count('importe_aprob'), sum_top20gest2=Sum('importe_aprob')).order_by('-sum_top20gest2')[:20]
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
def rvgl2_top20clie(request, fecha, analista):
    if analista == 'TODOS':
       top20clie1 = RVGL.objects.filter(mes_vigencia=fecha).values('cliente').annotate(num_top20clie1=Count('importe_solic'), sum_top20clie1=Sum('importe_solic')).order_by('cliente').order_by('-sum_top20clie1')[:20]
       top20clie2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0).values('cliente').annotate(num_top20clie2=Count('importe_aprob'), sum_top20clie2=Sum('importe_aprob')).order_by('-sum_top20clie2')[:20]
       top20clie = zip(top20clie1,top20clie2)
    else:
       top20clie1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('cliente').annotate(num_top20clie1=Count('importe_solic'), sum_top20clie1=Sum('importe_solic')).order_by('cliente').order_by('-sum_top20clie1')[:20]
       top20clie2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).values('cliente').annotate(num_top20clie2=Count('importe_aprob'), sum_top20clie2=Sum('importe_aprob')).order_by('-sum_top20clie2')[:20]
       top20clie = zip(top20clie1,top20clie2)
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
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

@login_required
def rvgl2_top20ofic(request, fecha, analista):
    if analista == 'TODOS':
       top20ofic1 = RVGL.objects.filter(mes_vigencia=fecha).values('oficina').annotate(num_top20ofic1=Count('importe_solic'), sum_top20ofic1=Sum('importe_solic')).order_by('-sum_top20ofic1')[:20]
       top20ofic2 = RVGL.objects.filter(mes_vigencia=fecha).exclude(importe_aprob=0).values('oficina').annotate(num_top20ofic2=Count('importe_aprob'), sum_top20ofic2=Sum('importe_aprob')).order_by('-sum_top20ofic2')[:20]
       top20ofic = zip(top20ofic1,top20ofic2)
    else:
       top20ofic1 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).values('oficina').annotate(num_top20ofic1=Count('importe_solic'), sum_top20ofic1=Sum('importe_solic')).order_by('-sum_top20ofic1')[:20]
       top20ofic2 = RVGL.objects.filter(mes_vigencia=fecha, analista=analista).exclude(importe_aprob=0).values('oficina').annotate(num_top20ofic2=Count('importe_aprob'), sum_top20ofic2=Sum('importe_aprob')).order_by('-sum_top20ofic2')[:20]
       top20ofic = zip(top20ofic1,top20ofic2)
    control_analistas = RVGL.objects.all().values('analista').distinct('analista')
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
    total_form = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='03 Tarjeta').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    uno_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='03 Tarjeta', riesgos='UNO A UNO').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='03 Tarjeta', riesgos='CAMP').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_fast = Seguimiento1.objects.values('mes_vigencia','origen').filter(producto='03 Tarjeta', origen='ORIGINACION FAST').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_uno = Seguimiento1.objects.values('mes_vigencia','origen').filter(producto='03 Tarjeta', origen='ORIGINACION MS').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    formalizados = zip(total_form,uno_form,camp_fast,camp_uno)
    fact_uno = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='03 Tarjeta', riesgos='UNO A UNO').annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    fact_camp = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='03 Tarjeta', riesgos='CAMP').annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    ticket = zip(fact_uno, fact_camp, uno_form, camp_form)
    seg_ava = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento__in=['Premium','Vip','Decisores','REFERIDO']).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_ms = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento__in=['MS', 'PLAN CLIENTE']).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_pas = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='Pasivo').annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_noph = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento='No PH').annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_nocli = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='03 Tarjeta', segmento__in=['NoCli','']).annotate(seg=Sum('form')).order_by('mes_vigencia')
    camp_seg = zip(seg_ava, seg_ms, seg_noph, seg_nocli, camp_form)

    mora6 = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte='201410', mes_form__lte ='201508').annotate(sum_mora=Sum('mora6')).order_by('mes_form')
    mora9 = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte='201410', mes_form__lte ='201505').annotate(sum_mora=Sum('mora9')).order_by('mes_form')
    mora12 = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte='201410', mes_form__lte ='201502').annotate(sum_mora=Sum('mora12')).order_by('mes_form')
    total_ctas = Moras.objects.values('mes_form','producto').filter(producto='03 Tarjeta',mes_form__gte='201410', mes_form__lte ='201508').annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    mora_6 = zip(mora6,total_ctas)
    mora_9 = zip(mora9,total_ctas)
    mora_12 = zip(mora12,total_ctas)
    print mora6
    print total_ctas
    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_tarjeta.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_pld(request):
    total_form = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='01 Consumo').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    uno_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='01 Consumo', riesgos='UNO A UNO').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='01 Consumo', riesgos='CAMP').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_fast = Seguimiento1.objects.values('mes_vigencia','origen').filter(producto='01 Consumo', origen='ORIGINACION FAST').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_uno = Seguimiento1.objects.values('mes_vigencia','origen').filter(producto='01 Consumo', origen='ORIGINACION MS').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    formalizados = zip(total_form,uno_form,camp_fast,camp_uno)
    seg_ava = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento__in=['Premium','Vip','Decisores','REFERIDO']).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_ms = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento__in=['MS', 'PLAN CLIENTE']).annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_pas = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='Pasivo').annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_noph = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento='No PH').annotate(seg=Sum('form')).order_by('mes_vigencia')
    seg_nocli = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(riesgos='CAMP', producto='01 Consumo', segmento__in=['NoCli','']).annotate(seg=Sum('form')).order_by('mes_vigencia')
    camp_seg = zip(seg_ava, seg_ms, seg_noph, seg_nocli, camp_form)

    mora6 = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte='201410', mes_form__lte ='201508').annotate(sum_mora=Sum('mora6')).order_by('mes_form')
    mora9 = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte='201410', mes_form__lte ='201505').annotate(sum_mora=Sum('mora9')).order_by('mes_form')
    mora12 = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte='201410', mes_form__lte ='201502').annotate(sum_mora=Sum('mora12')).order_by('mes_form')
    total_ctas = Moras.objects.values('mes_form','producto').filter(producto='01 Consumo',mes_form__gte='201410', mes_form__lte ='201508').annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    mora_6 = zip(mora6,total_ctas)
    mora_9 = zip(mora9,total_ctas)
    mora_12 = zip(mora12,total_ctas)
    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_pld.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_auto(request):
    total_form = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='02 Auto').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    uno_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='02 Auto', riesgos='UNO A UNO').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_form = Seguimiento1.objects.values('mes_vigencia','riesgos').filter(producto='02 Auto', riesgos='CAMP').annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    camp_reg = Seguimiento1.objects.values('mes_vigencia','origen').filter(producto='02 Auto', origen__in=['ORIGINACION FAST','ORIGINACION MS']).annotate(formalizado=Sum('form')).order_by('mes_vigencia')
    formalizados = zip(total_form,uno_form,camp_form)

    fact_uno = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='02 Auto', riesgos='UNO A UNO').annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    fact_camp = Seguimiento1.objects.values('mes_vigencia','producto').filter(producto='02 Auto', riesgos='CAMP').annotate(facturacion=Sum('facturacion')).order_by('mes_vigencia')
    ticket = zip(fact_uno, fact_camp, uno_form, camp_form)

    mora12 = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte='201410', mes_form__lte ='201508').annotate(sum_mora=Sum('mora12')).order_by('mes_form')
    mora18 = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte='201410', mes_form__lte ='201502').annotate(sum_mora=Sum('mora18')).order_by('mes_form')
    mora24 = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte='201410', mes_form__lte ='201502').annotate(sum_mora=Sum('mora24')).order_by('mes_form')
    total_ctas = Moras.objects.values('mes_form','producto').filter(producto='02 Auto',mes_form__gte='201410', mes_form__lte ='201508').annotate(sum_mora=Sum('ctas')).order_by('mes_form')
    moras12 = zip(mora12,total_ctas)
    moras18 = zip(mora18,total_ctas)
    moras24 = zip(mora24,total_ctas)
    print mora12
    static_url=settings.STATIC_URL
    tipo_side = 4

    return render('reports/seguimiento_auto.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def seguimiento_adelanto(request):
    total_form = AdelantoSueldo.objects.values('mes_vigencia').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    ticket = AdelantoSueldo.objects.values('mes_vigencia').annotate(formalizado=Sum('fact')).order_by('mes_vigencia')
    formalizados = zip(total_form,ticket)
    
    meses = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte='201602').distinct('mes_vigencia').order_by('mes_vigencia')
    total_rango = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte='201602').exclude(rng_suelgo='00 Sin Inf').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango_tot = {}
    for i in total_rango:
	rango_tot[i['mes_vigencia']]=i['formalizado']
    rango1 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo__in=['01 [0 - 700>','02 [700 - 1000]'], mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    print rango1_dict
    rango2 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='03 [1001 - 1500]',mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='04 [1501 - 2000]',mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='05 [2001 - 2500]',mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='06 [2501 - 3500]',mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
	     break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    rango6 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_suelgo='07 [3501 - Mas>',mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= 0

    buro1 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='[G1-G4]',mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='G5',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='[G6-G8]',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = AdelantoSueldo.objects.values('mes_vigencia').filter(rng_buro='NB',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(formalizado=Sum('ctas')).order_by('mes_vigencia')
    buro4_dict = {}
    for i in meses:
       for j in buro4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro4_dict[i['mes_vigencia']]=j['formalizado']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             buro4_dict[i['mes_vigencia']]= 0

    mora30 = AdelantoSueldo.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(formalizado=Sum('mora')).order_by('mes_vigencia')
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
    form = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    fact = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('fact')).order_by('mes_vigencia')
    ticket_ava = PrestInmediato.objects.values('mes_vigencia').filter(segmento='Vip',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas'), cantidad2=Sum('fact')).order_by('mes_vigencia')
    ticket_ms = PrestInmediato.objects.values('mes_vigencia').filter(segmento='MS',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas'), cantidad2=Sum('fact')).order_by('mes_vigencia')

    meses = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602').order_by('mes_vigencia')
    total_rango = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas')).exclude(rng_ingreso='').order_by('mes_vigencia')
    rango_tot = {}
    for i in total_rango:
	rango_tot[i['mes_vigencia']]=i['cantidad']
    rango1 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602',rng_ingreso='05 [1K - 1.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602',rng_ingreso='04 [1.5K - 2K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602',rng_ingreso='03 [2K - 2.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602',rng_ingreso='02 [2.5K - 3.5K]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602',rng_ingreso='01 [3.5K - ...]').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    total_rango2 = PrestInmediato.objects.values('mes_vigencia').filter(mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango_tot2 = {}
    for i in total_rango2:
	rango_tot2[i['mes_vigencia']]=i['cantidad']
    buro1 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='[G1-G4]',mes_vigencia__gte='201503', mes_vigencia__lte='201602').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='G5',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='[G6-G8]',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/rango_tot2[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = PrestInmediato.objects.values('mes_vigencia').filter(rng_buro='NB',mes_vigencia__gte='201503', mes_vigencia__lte ='201602').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
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
    meses = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601').order_by('mes_vigencia')
    form = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form_dict = {}
    for i in form:
	form_dict[i['mes_vigencia']]=i['cantidad']
    ticket = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601').annotate(cantidad=Sum('cantidad')).order_by('mes_vigencia')
    ticket_dict = {}
    for i in meses:
       for j in ticket:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ticket_dict[i['mes_vigencia']]=j['cantidad']*1000000/form_dict[i['mes_vigencia']]
             break
       	  else:
             ticket_dict[i['mes_vigencia']]= 0
    form2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601').exclude(segmento='').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    form2_dict = {}
    for i in form2:
	form2_dict[i['mes_vigencia']]=i['cantidad']
    ava = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= '201502', mes_vigencia__lte ='201601',segmento__in=['Vip','Premium']).annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ava_dict = {}
    for i in meses:
       for j in ava:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ava_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ava_dict[i['mes_vigencia']]= 0
    ms = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= '201502', mes_vigencia__lte ='201601',segmento='MS').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    ms_dict = {}
    for i in meses:
       for j in ms:
          if i['mes_vigencia'] == j['mes_vigencia']:
             ms_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             ms_dict[i['mes_vigencia']]= 0
    pasivo = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= '201502', mes_vigencia__lte ='201601',segmento='Pasivo').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    pasivo_dict = {}
    for i in meses:
       for j in pasivo:
          if i['mes_vigencia'] == j['mes_vigencia']:
             pasivo_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             pasivo_dict[i['mes_vigencia']]= 0
    noph = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= '201502', mes_vigencia__lte ='201601',segmento='No PH').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noph_dict = {}
    for i in meses:
       for j in noph:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noph_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noph_dict[i['mes_vigencia']]= 0
    noclie = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte= '201502', mes_vigencia__lte ='201601',segmento='NoCli').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    noclie_dict = {}
    for i in meses:
       for j in noclie:
          if i['mes_vigencia'] == j['mes_vigencia']:
             noclie_dict[i['mes_vigencia']]=j['cantidad']*100/form2_dict[i['mes_vigencia']]
             break
       	  else:
             noclie_dict[i['mes_vigencia']]= 0
    rango1 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601',rng_sueldo='01 [-1000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango1_dict = {}
    for i in meses:
       for j in rango1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango1_dict[i['mes_vigencia']]= 0
    rango2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601',rng_sueldo='02 [1000-1500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango2_dict = {}
    for i in meses:
       for j in rango2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango2_dict[i['mes_vigencia']]= 0
    rango3 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601',rng_sueldo='03 [1500-2000>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango3_dict = {}
    for i in meses:
       for j in rango3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango3_dict[i['mes_vigencia']]= 0
    rango4 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601',rng_sueldo='04 [2000-2500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango4_dict = {}
    for i in meses:
       for j in rango4:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango4_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango4_dict[i['mes_vigencia']]= 0
    rango5 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601',rng_sueldo='05 [2500-3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango5_dict = {}
    for i in meses:
       for j in rango5:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango5_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango5_dict[i['mes_vigencia']]= 0
    rango6 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601',rng_sueldo='06 [+3500>').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    rango6_dict = {}
    for i in meses:
       for j in rango6:
          if i['mes_vigencia'] == j['mes_vigencia']:
             rango6_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             rango6_dict[i['mes_vigencia']]= 0
    buro1 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601', buro='01 G1-G4').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    print buro1
    buro1_dict = {}
    for i in meses:
       for j in buro1:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro1_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro1_dict[i['mes_vigencia']]= 0
    buro2 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601', buro='02 G5').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    print buro2
    buro2_dict = {}
    for i in meses:
       for j in buro2:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro2_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro2_dict[i['mes_vigencia']]= 0
    buro3 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601', buro='03 G6-G8').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    print buro3
    buro3_dict = {}
    for i in meses:
       for j in buro3:
          if i['mes_vigencia'] == j['mes_vigencia']:
             buro3_dict[i['mes_vigencia']]=j['cantidad']*100/form_dict[i['mes_vigencia']]
             break
       	  else:
             buro3_dict[i['mes_vigencia']]= 0
    buro4 = IncreLinea.objects.values('mes_vigencia').filter(mes_vigencia__gte='201502', mes_vigencia__lte ='201601', buro='NB').annotate(cantidad=Sum('ctas')).order_by('mes_vigencia')
    print buro4
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


# 6.- Vistas para reportes de HIPOTECARIO
@login_required
def hipoteca_ssff(request):
    saldo_bcp = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco='BCP',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo_bbva = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco='BBVA',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo_sco = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco='SCO',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo_ibk = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco='IBK',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo2_bcp = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='BCP',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo2_bbva = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='BBVA',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo2_sco = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='SCO',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    saldo2_ibk = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(tipo_cuenta__in=['JUD_HIPO','VEN_HIPO'], banco='IBK',mes_vigencia__in=['201112', '201212', '201312', '201412', '201503', '201506', '201509', '201512']).annotate(sum_saldo=Sum('mto_saldo')).order_by('mes_vigencia')
    bcp = zip(saldo_bcp, saldo2_bcp)
    bbva = zip(saldo_bbva, saldo2_bbva)
    sco = zip(saldo_sco, saldo2_sco)
    ibk = zip(saldo_ibk, saldo2_ibk)
    saldo_jud = HipotecaSSFF.objects.values('mes_vigencia', 'banco', 'tipo_cuenta' ).filter(tipo_cuenta='JUD_HIPO', banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia='201512' ).annotate(sum_jud=Sum('mto_saldo')).order_by('banco')
    saldo_ven = HipotecaSSFF.objects.values('mes_vigencia', 'banco', 'tipo_cuenta' ).filter(tipo_cuenta='VEN_HIPO', banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia='201512' ).annotate(sum_ven=Sum('mto_saldo')).order_by('banco')
    saldo_ref = HipotecaSSFF.objects.values('mes_vigencia', 'banco', 'tipo_cuenta' ).filter(tipo_cuenta='REF_HIPO', banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia='201512' ).annotate(sum_ref=Sum('mto_saldo')).order_by('banco')
    totales = HipotecaSSFF.objects.values('mes_vigencia','banco').filter(banco__in=['BCP','SCO','BBVA','IBK'], mes_vigencia='201512').annotate(total=Sum('mto_saldo')).order_by('banco')
    grafica2 = zip(saldo_jud,saldo_ven,saldo_ref,totales)

    static_url=settings.STATIC_URL
    tipo_side = 5
    return render('reports/hipoteca_ssff.html', locals(),
                  context_instance=RequestContext(request))

@login_required
def hipoteca_conce(request):
    conce = HipotecaConce.objects.values('mes','territorio').filter(mes='201512').annotate(sum_inv=Sum('inversion')).order_by('territorio')
    print conce
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
    print evo_mora12
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



# Vistas para carga de csv
def load(request):
    static_url=settings.STATIC_URL
    #Campana2.objects.all().delete()
    #RVGL.objects.all().delete()
    #Evaluaciontc.objects.all().delete()
    #Evaluacionpld.objects.all().delete()
    #Seguimiento1.objects.all().delete()
    #HipotecaConce.objects.all().delete()
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


#def carga_campana(request):
    #if request.method == 'POST':
        #form = UploadCampana(request.POST, request.FILES)
        #if form.is_valid():
            #csv_file = request.FILES['campana']
            #CampanaCsv.import_data(data = csv_file)
            #return campana_ofertas(request)
        #else:
            #print "no es valido"
            #return load(campana_ofertas)
    #else:
        #return load(campana_ofertas)

def carga_campana2(request):
    if request.method == 'POST':
        form = UploadCampana2(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['campana2']
            Campana2Csv.import_data(data = csv_file)
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
        form = UploadSeguimiento1(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['seguimiento1']
            Seguimiento1Csv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_flujoperativo(request):
    if request.method == 'POST':
        form = UploadFlujOperativo(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['flujoperativo']
            FlujOperativoCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_hipotecassff(request):
    if request.method == 'POST':
        form = UploadHipotecaSSFF(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['hipotecassff']
            HipotecaSSFFCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_hipotecaconce(request):
    if request.method == 'POST':
        form = UploadHipotecaConce(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['hipotecaconce']
            HipotecaConceCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_moras(request):
    if request.method == 'POST':
        form = UploadMoras(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['moras']
            MorasCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_adelantosueldo(request):
    if request.method == 'POST':
        form = UploadAdelantoSueldo(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['adelantosueldo']
            AdelantoSueldoCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_prestinmediato(request):
    if request.method == 'POST':
        form = UploadPrestInmediato(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['prestinmediato']
            PrestInmediatoCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_altasempresa(request):
    if request.method == 'POST':
        form = UploadAltasEmpresa(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['altasempresa']
            AltasEmpresaCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_altassegmento(request):
    if request.method == 'POST':
        form = UploadAltasSegmento(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['altassegmento']
            AltasSegmentoCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

def carga_increlinea(request):
    if request.method == 'POST':
        form = UploadIncreLinea(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['increlinea']
            IncreLineaCsv.import_data(data = csv_file)
            return campana_ofertas(request)
        else:
            return load(campana_ofertas)
    else:
        return load(campana_ofertas)

