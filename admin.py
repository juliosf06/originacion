from django.contrib import admin

from .models import Campana, MoraDistrito, RVGL, Verificaciones

admin.site.register(Campana)
admin.site.register(MoraDistrito)
admin.site.register(RVGL)
admin.site.register(Verificaciones)

# Register your models here.
