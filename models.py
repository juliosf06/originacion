# -*- coding: utf-8 -*-

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

class RVGL(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    rvgl = models.CharField(max_length=8)
    seco = models.CharField(max_length=8)
    dictamen = models.CharField(max_length=30)
    analista = models.CharField(max_length=100)
    importe_solic = models.DecimalField(max_digits=10, decimal_places=2)
    dias_eval = models.IntegerField()
    producto_esp = models.CharField(max_length=50)
    territorio_nuevo = models.CharField(max_length=50)
    ejecutivo_cuenta = models.CharField(max_length=100)
    cliente = models.CharField(max_length=100)
    seg_prime = models.CharField(max_length=10)
    sco = models.CharField(max_length=10)
    dictamen_sco = models.CharField(max_length=10)
    dic_buro = models.CharField(max_length=10)
    importe_aprob = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.rvgl
