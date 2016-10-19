# -*- coding: utf-8 -*-

from django.template import Library, loader, Context
from django.conf import settings

register = Library()

DIC = {'201101':'ENE11','201102':'FEB11','201103':'MAR11','201104':'ABR11'
,'201105':'MAY11','201106':'JUN11','201107':'JUL11','201108':'AGO11',
'201109':'SET11','201110':'OCT11','201111':'NOV11','201112':'DIC11','201212':'DIC12',
'201201':'ENE12','201202':'FEB12','201203':'MAR12','201204':'ABR12'
,'201205':'MAY12','201206':'JUN12','201207':'JUL12','201208':'AGO12',
'201209':'SET12','201210':'OCT2','201211':'NOV12','201212':'DIC12',
'201301':'ENE13','201302':'FEB13','201303':'MAR13','201304':'ABR13'
,'201305':'MAY13','201306':'JUN13','201307':'JUL13','201308':'AGO13',
'201309':'SET13','201310':'OCT3','201311':'NOV13','201312':'DIC13',
'201401':'ENE14','201402':'FEB14','201403':'MAR14','201404':'ABR14','201405':'MAY14',
'201406':'JUN14','201407':'JUL14','201408':'AGO14','201409':'SET14',
'201410':'OCT4','201411':'NOV14','201412':'DIC14','201501':'ENE15',
'201502':'FEB15', '201503':'MAR15', '201504':'ABR15', '201505':'MAY15', '201506':'JUN15', '201507':'JUL15','201508':'AGO15', '201509':'SET15', '201510':'OCT15','201511':'NOV15','201512':'DIC15','201601':'ENE16',
'201602':'FEB16', '201603':'MAR16', '201604':'ABR16', '201605':'MAY16', '201606':'JUN16', '201607':'JUL16', '201608':'AGO16', '201609':'SET16',
'201610':'OCT16', '201611':'NOV16', '201612':'DIC16'}

FECHAS_NOMBRES = {'01':'Enero','02':'Febrero', '03':'Marzo', '04':'Abril', '05':'Mayo', '06':'Junio', '07':'Julio','08':'Agosto', '09':'Septiembre', '10':'Octubre', '11':'Noviembre','12':'Diciembre'}

#Header
@register.inclusion_tag('reports/header.html')
def header(user):
    return locals()

#Footer
@register.inclusion_tag('reports/footer.html')
def footer():
    return locals()

#Sidebar
@register.simple_tag()
def sidebar(tipo=1):
    if tipo == 2:
        temp = 'reports/sidebar_rvgl.html'
    else:
	if tipo == 3:
           temp = 'reports/sidebar_evaluacion.html'
	else:
	    if tipo == 4:
               temp = 'reports/sidebar_seguimiento.html'
	    else:
		if tipo == 5:
               	   temp = 'reports/sidebar_hipotecario.html'
		else:
                   temp = 'reports/sidebar.html'
    t = loader.get_template(temp)
    return t.render(Context)

@register.filter
def convert_date(value):
    return DIC[value] 

@register.filter
def format_date(value):
    return FECHAS_NOMBRES[value[4:6]]+' '+value[0:4]

@register.filter(name='sort')
def listsort(value):
    if isinstance(value, list):
	return sorted(value, key=lambda k:k[0])
    else:
	return value

@register.filter
def to_int(value):
    return 0 if value=='' else int(value)

@register.filter
def to_str(value):
    return 0 if value=='' else str(value)

@register.filter
def x_cien(value):
    return value*100



