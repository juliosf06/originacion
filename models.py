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

class MoraDistrito(models.Model):
    departamento = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    distrito = models.CharField(max_length=100)
    saldo_stock = models.DecimalField(max_digits=10, decimal_places=2)
    mora_12 = models.DecimalField(max_digits=4, decimal_places=2)
    mora_24 = models.DecimalField(max_digits=4, decimal_places=2)
    mora_contable = models.DecimalField(max_digits=4, decimal_places=2)
    prima = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.provincia+' '+self.distrito
