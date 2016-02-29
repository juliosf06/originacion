
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from django.conf import settings
from models import *
from forms import RVGLCsv, UploadRVGL
import csv

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

def load(request):
    static_url=settings.STATIC_URL
    #RVGL.objects.all().delete()
    if request.user.is_authenticated():
        return render('reports/load.html', locals(),
                  context_instance=RequestContext(request))
    else:
        return index(request)

def carga_rvgl(request):
    if request.method == 'POST':
        form = UploadRVGL(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['rvgl']
            RVGLCsv.import_data(data = csv_file)
            return index(request)
        else:
            print "no es valido"
            return load(index)
    else:
        return load(index)

