from django.contrib import admin

from .models import Campana2, MoraDistrito, RVGL, Verificaciones, Caida, Evaluaciontc, Evaluacionpld, Seguimiento1, FlujOperativo, HipotecaSSFF, HipotecaConce, Moras

#admin.site.register(Campana) importar model para uso
admin.site.register(Campana2)
admin.site.register(MoraDistrito)
admin.site.register(RVGL)
admin.site.register(Verificaciones)
admin.site.register(Caida)
admin.site.register(Evaluaciontc)
admin.site.register(Evaluacionpld)
admin.site.register(Seguimiento1)
admin.site.register(FlujOperativo)
admin.site.register(HipotecaSSFF)
admin.site.register(HipotecaConce)
admin.site.register(Moras)

# Register your models here.
