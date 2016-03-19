from django.contrib import admin

from .models import Campana, MoraDistrito, RVGL, Verificaciones, Caida

admin.site.register(Campana)
admin.site.register(MoraDistrito)
admin.site.register(RVGL)
admin.site.register(Verificaciones)
admin.site.register(Caida)

# Register your models here.
