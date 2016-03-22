# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

class Segmento(models.Model):
    nombre = models.CharField(max_length=100)

class Campana(models.Model):
    codigo_campana = models.CharField(max_length=100)
    mes_vigencia = models.CharField(max_length=10)
    segmento = models.CharField(max_length=20)
    ofertas = models.IntegerField(default=0)
    q_tc = models.IntegerField(default=0)
    monto_tc = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_pld = models.IntegerField(default=0)
    monto_pld = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_veh = models.IntegerField(default=0)
    monto_veh = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_subrogacion = models.IntegerField(default=0)
    monto_subrogacion = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_tc_entry_level = models.IntegerField(default=0)
    monto_tc_entry_level = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_renovado = models.IntegerField(default=0)
    monto_renovado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_auto_2da = models.IntegerField(default=0)
    monto_auto_2da = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_adelanto_sueldo = models.IntegerField(default=0)
    monto_adelanto_sueldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_efectivo_plus = models.IntegerField(default=0)
    monto_efectivo_plus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_prestamo_inmediato = models.IntegerField(default=0)
    monto_prestamo_inmediato = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    q_incr_linea = models.IntegerField(default=0)
    monto_incr_linea = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.codigo_campana+' '+self.segmento

class Verificaciones(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    segmento = models.CharField(max_length=20)
    exonera_ambas = models.IntegerField()
    exonera_solo_vl = models.IntegerField()
    exonera_solo_vd = models.IntegerField()
    requiere_ambas = models.IntegerField()
    exonera_vl_tc = models.IntegerField()

    def __str__(self):
        return self.mes_vigencia+' '+self.segmento

class Caida(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    segmento = models.CharField(max_length=20)
    caida = models.CharField(max_length=150)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.segmento+' '+self.caida

class Evaluaciontc(models.Model):
    cliente = models.CharField(max_length=20)
    tip_doc = models.CharField(max_length=5)
    documento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apell_paterno = models.CharField(max_length=100)
    apell_materno = models.CharField(max_length=100)
    edad = models.CharField(max_length=5)
    segmento = models.CharField(max_length=10)
    buro = models.CharField(max_length=5)
    grupo_pr = models.CharField(max_length=10)
    sueldo_final = models.CharField(max_length=20)
    sueldo_final_fuente = models.CharField(max_length=50)

    def __str__(self):
        return self.cliente+' '+self.documento

class Evaluacionpld(models.Model):
    cliente = models.CharField(max_length=20)
    tip_doc = models.CharField(max_length=5)
    documento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apell_paterno = models.CharField(max_length=100)
    apell_materno = models.CharField(max_length=100)
    edad = models.CharField(max_length=5)
    segmento = models.CharField(max_length=10)
    buro = models.CharField(max_length=5)
    grupo_pr = models.CharField(max_length=10)
    sueldo_final = models.CharField(max_length=20)
    sueldo_final_fuente = models.CharField(max_length=50)

    def __str__(self):
        return self.cliente+' '+self.documento

class seguimiento(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    dic_global = models.CharField(max_length=10)
    dic_buro = models.CharField(max_length=5)
    buro_camp = models.CharField(max_length=20)
    buro_uno = models.CharField(max_length=20)
    segmento = models.CharField(max_length=20)
    origen = models.CharField(max_length=50)
    rng_ing = models.CharField(max_length=20)
    producto = models.CharField(max_length=50)
    riesgos = models.CharField(max_length=20)
    soli = models.IntegerField(default=0)
    plazo = models.IntegerField(default=0)
    form = models.IntegerField(default=0)
    facturacion = models.DecimalField(max_digits=4, decimal_places=4, default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.segmento+' '+self.producto

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
    oficina = models.CharField(max_length=50, default=0)

    def __str__(self):
        return self.rvgl
