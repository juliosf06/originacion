# -*- coding: utf-8 -*-

from django.template import Library, loader, Context
from django.conf import settings

register = Library()

DIC = {'201112':'DIC11','201212':'DIC12','201312':'DIC13','201410':'OCT4', '201411':'NOV14', '201412':'DIC14', '201501':'ENE15','201502':'FEB15', '201503':'MAR15', '201504':'ABR15', '201505':'MAY15', '201506':'JUN15', '201507':'JUL15','201508':'AGO15', '201509':'SET15', '201510':'OCT15', '201511':'NOV15','201512':'DIC15','201601':'ENE16','201602':'FEB16', '201603':'MAR16'}

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


