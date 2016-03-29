from django.contrib import admin

from .models import Campana, MoraDistrito, RVGL, Verificaciones, Caida, Evaluaciontc, Evaluacionpld, Seguimiento1, FlujOperativo

admin.site.register(Campana)
admin.site.register(MoraDistrito)
admin.site.register(RVGL)
admin.site.register(Verificaciones)
admin.site.register(Caida)
admin.site.register(Evaluaciontc)
admin.site.register(Evaluacionpld)
admin.site.register(Seguimiento1)
admin.site.register(FlujOperativo)

# Register your models here.
