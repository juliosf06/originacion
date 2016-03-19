from django.contrib import admin

from .models import Campana, MoraDistrito, RVGL, Verificaciones, Caida, Evaluaciontc, Evaluacionpld

admin.site.register(Campana)
admin.site.register(MoraDistrito)
admin.site.register(RVGL)
admin.site.register(Verificaciones)
admin.site.register(Caida)
admin.site.register(Evaluaciontc)
admin.site.register(Evaluacionpld)

# Register your models here.
