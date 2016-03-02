from django import template
from django.conf import settings

register = template.Library()

#Header
@register.inclusion_tag('reports/header.html')
def header():
    return locals()

#Footer
@register.inclusion_tag('reports/footer.html')
def footer():
    return locals()

#Sidebar
@register.inclusion_tag('reports/sidebar.html')
def sidebar():
    return locals()
