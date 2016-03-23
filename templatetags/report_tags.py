# -*- coding: utf-8 -*-

from django.template import Library, loader, Context
from django.conf import settings

register = Library()

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
               temp = 'reports/sidebar.html'
    t = loader.get_template(temp)
    return t.render(Context)
