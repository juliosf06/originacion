from __future__ import unicode_literals

from django.db import models

class Segmento(models.Model):
    nombre = models.CharField(max_length=100)

class Campana(models.Model):
    codigo_campana = models.CharField(max_length=100)
    mes_vigencia = models.CharField(max_length=10)
    segmento = models.CharField(max_length=20)
    ofertas = models.IntegerField()

    def __str__(self):
        return self.codigo_campana+' '+self.segmento
