
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response as render
from models import *

def index(request):
    campanas = Campana.objects.filter(mes_vigencia='201512')
    print campanas
    return render('reports/reports.html', locals(),
                  context_instance=RequestContext(request))
