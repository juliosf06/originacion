
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.conf import settings
from models import *

def index(request):
    campanas = Campana.objects.filter(mes_vigencia='201512')
    static_url=settings.STATIC_URL
    return render('reports/reports.html', locals(),
                  context_instance=RequestContext(request))

def mapa(request):
    distrito = MoraDistrito.objects.filter(provincia='Lima')
    static_url=settings.STATIC_URL
    return render('reports/mapa.html', locals(),
                  context_instance=RequestContext(request))
