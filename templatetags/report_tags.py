# -*- coding: utf-8 -*-

from django.template import Library, loader, Context
from django.conf import settings

register = Library()


MESES = {'01':'ENE','02':'FEB', '03':'MAR', '04':'ABR', '05':'MAY', '06':'JUN', '07':'JUL','08':'AGO', '09':'SET', '10':'OCT', '11':'NOV','12':'DIC'}

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
    MES = value[4:]
    ANO = value[2:-2]
    codmes = MESES[MES] + ANO
    return codmes 

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
def to_round(value):
    return 0 if value=='' else round(value, 0)

@register.filter
def to_un_decimal(value):
    return 0 if value=='' else round(value, 1)

@register.filter
def to_dos_decimal(value):
    return 0 if value=='' else round(value, 2)

@register.filter
def to_str(value):
    return 0 if value=='' else str(value)

@register.filter
def x_cien(value):
    return value*100

@register.filter
def convert_time(value):
    value1 = value.replace("/","")
    value = value1.replace(":","")
    return value

@register.filter
def convert_time2(value):
    value1 = value.replace("/","_")
    value = value1.replace(":","_")
    return value


