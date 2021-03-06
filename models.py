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

class Campana2(models.Model):
    codigo_campana = models.CharField(max_length=10)
    mes_vigencia = models.CharField(max_length=10)
    segmento = models.CharField(max_length=20)
    tipo_clie = models.CharField(max_length=20)
    verificacion = models.CharField(max_length=50)
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
        return self.codigo_campana+' '+self.segmento+' '+self.tipo_clie

class CampanaWeb(models.Model):
    num_eval = models.IntegerField(default=0)
    mes = models.CharField(max_length=20,default=0)
    semana = models.CharField(max_length=10,default=0)
    fecha_recepcion = models.CharField(max_length=10)
    num_clientes = models.DecimalField(max_digits=12, decimal_places=2)
    form_tdc = models.DecimalField(max_digits=12, decimal_places=2)
    form_pld = models.DecimalField(max_digits=12, decimal_places=2)
    total_filtros = models.DecimalField(max_digits=12, decimal_places=2)
    tdc_moi = models.DecimalField(max_digits=12, decimal_places=2)
    tdc_il = models.DecimalField(max_digits=12, decimal_places=2)
    tdc_nueva = models.DecimalField(max_digits=12, decimal_places=2)
    tdc_total = models.DecimalField(max_digits=12, decimal_places=2)
    tdc_porcentaje = models.DecimalField(max_digits=12, decimal_places=2)
    pld_moi = models.DecimalField(max_digits=12, decimal_places=2)
    pld_nueva = models.DecimalField(max_digits=12, decimal_places=2)
    pld_total = models.DecimalField(max_digits=12, decimal_places=2)
    pld_porcentaje = models.DecimalField(max_digits=12, decimal_places=2)
    tdc = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    tdc_formal = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    pld = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    pld_formal = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.fecha_recepcion+' '+self.num_clientes

class CampanaEfec(models.Model):
    id_efec = models.IntegerField(default=0)
    mes = models.CharField(max_length=20,default=0)
    semana = models.CharField(max_length=10,default=0)
    segmento0 = models.CharField(max_length=50)
    segmento1 = models.CharField(max_length=50)
    form_ambas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    form_solovd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    form_solovl = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    form_req = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    form_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sol_ambas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sol_solovd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sol_solovl = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sol_req = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sol_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_apro = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    form = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.segmento0+' '+self.segmento1

class CampanaEquifax(models.Model):
    id_equifax = models.IntegerField(default=0)
    filtro0 = models.CharField(max_length=40)
    filtro1 = models.CharField(max_length=40)
    ambas = models.CharField(max_length=10)
    solovd = models.CharField(max_length=10)
    solovl = models.CharField(max_length=10)
    req = models.CharField(max_length=10)
    total = models.CharField(max_length=10)

    def __str__(self):
        return self.filtro0+' '+self.filtro1

class CampanaLabSeg(models.Model):
    filtro0 = models.CharField(max_length=40)
    filtro1 = models.CharField(max_length=40)
    filtro2 = models.CharField(max_length=50)
    form = models.CharField(max_length=10)
    total_form = models.CharField(max_length=10)
    porc_form = models.CharField(max_length=10)

    def __str__(self):
        return self.filtro0+' '+self.filtro1+' '+self.filtro2

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

class Exoneracion(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    tipo = models.CharField(max_length=5)
    motivo_exo = models.CharField(max_length=50)
    cat_cliente = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.mes_vigencia+' '+self.tipo+' '+self.motivo_exo

class Caida(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    segmento = models.CharField(max_length=20)
    caida = models.CharField(max_length=150)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.segmento+' '+self.caida

class Evaluaciontc(models.Model):
    fecha = models.CharField(max_length=10,default=0)
    hora_fin = models.CharField(max_length=10,default=0)
    cliente = models.CharField(max_length=20)
    relacion_lab = models.CharField(max_length=20,default=0)
    validado = models.CharField(max_length=5,default=0)
    scoreweb = models.CharField(max_length=20,default=0)
    eval_admi = models.CharField(max_length=20,default=0)
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
        return self.fecha+' '+self.cliente+' '+ self.documento

class Evaluacionpld(models.Model):
    fecha = models.CharField(max_length=10,default=0)
    hora_fin = models.CharField(max_length=10,default=0)
    cliente = models.CharField(max_length=20)
    relacion_lab = models.CharField(max_length=20,default=0)
    validado = models.CharField(max_length=5,default=0)
    scoreweb = models.CharField(max_length=20,default=0)
    eval_admi = models.CharField(max_length=20,default=0)
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
        return self.fecha+' '+self.cliente+' '+ self.documento

class Stock(models.Model):
    codmes = models.CharField(max_length=10,default=0)
    flg_campana = models.CharField(max_length=50,default=0)
    trimestre = models.CharField(max_length=10)
    producto = models.CharField(max_length=20,default=0)    
    subproducto = models.CharField(max_length=40,default=0)
    campana = models.CharField(max_length=50,default=0)
    ctas = models.DecimalField(max_digits=8, decimal_places=2)
    fact = models.DecimalField(max_digits=14, decimal_places=8)
    inv = models.DecimalField(max_digits=14, decimal_places=8)
    atrasada = models.DecimalField(max_digits=14, decimal_places=8)

    def __str__(self):
        return self.codmes+' '+self.producto+' '+ self.subproducto

class Dotaciones(models.Model):
    codmes = models.CharField(max_length=10,default=0)
    producto = models.CharField(max_length=20,default=0)    
    subproducto = models.CharField(max_length=40,default=0)
    campana = models.CharField(max_length=50,default=0)
    riesgo = models.DecimalField(max_digits=20, decimal_places=4)
    dotacion = models.DecimalField(max_digits=20, decimal_places=4)
    mora = models.DecimalField(max_digits=20, decimal_places=4)
    salidas = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return self.codmes+' '+self.producto+' '+ self.subproducto

class CosteRiesgo(models.Model): #mensual
    codmes = models.CharField(max_length=10,default=0)  
    producto = models.CharField(max_length=20,default=0)       
    m6_t = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m9_t = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m12_t = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m6_c = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m9_c = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m12_c = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m6_u = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m9_u = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m12_u = models.DecimalField(max_digits=8, decimal_places=5, default=0)

    def __str__(self):
        return self.producto+' '+self.codmes

class CosteRiesgo2(models.Model): #trimestral
    codmes = models.CharField(max_length=10,default=0) 
    producto = models.CharField(max_length=20,default=0) 
    subproducto = models.CharField(max_length=20,default=0)   
    m1 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m2 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m3 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m4 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m5 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m6 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m7 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m8 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m9 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m10 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m11 = models.DecimalField(max_digits=8, decimal_places=5, default=0)
    m12 = models.DecimalField(max_digits=8, decimal_places=5, default=0)

    def __str__(self):
        return self.codmes+' '+self.producto+' '+self.subproducto

class Seguimiento(models.Model):
    periodo = models.CharField(max_length=10)
    trimestre_form = models.CharField(max_length=10)
    mes_vigencia = models.CharField(max_length=10)
    producto = models.CharField(max_length=50)
    origen = models.CharField(max_length=50)
    riesgos = models.CharField(max_length=20)
    rng_ing = models.CharField(max_length=20)
    segmento = models.CharField(max_length=20)
    cat_persona = models.CharField(max_length=50)
    buro_camp = models.CharField(max_length=20)
    cluster = models.CharField(max_length=50)
    digital = models.CharField(max_length=5)
    canal_digital = models.CharField(max_length=30)    
    flg_lifemiles = models.CharField(max_length=5)
    form = models.DecimalField(max_digits=12, decimal_places=2)
    ctas = models.DecimalField(max_digits=8, decimal_places=2)
    facturacion = models.DecimalField(max_digits=12, decimal_places=8)
    mora4_60 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora6 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora9 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora12 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora18 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora24 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora36 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self):
        return self.mes_vigencia+' '+self.segmento+' '+self.producto

class SeguimientoTer(models.Model):
    periodo = models.CharField(max_length=10)
    trimestre_form = models.CharField(max_length=10)
    mes_vigencia = models.CharField(max_length=10)
    producto = models.CharField(max_length=50)
    origen = models.CharField(max_length=50)
    riesgos = models.CharField(max_length=20)
    territorio = models.CharField(max_length=80)
    rng_ing = models.CharField(max_length=20)
    segmento = models.CharField(max_length=20)
    cat_persona = models.CharField(max_length=50)
    buro_camp = models.CharField(max_length=20)
    cluster = models.CharField(max_length=50)
    digital = models.CharField(max_length=5)
    canal_digital = models.CharField(max_length=30)    
    flg_lifemiles = models.CharField(max_length=5)
    form = models.DecimalField(max_digits=12, decimal_places=2)
    ctas = models.DecimalField(max_digits=8, decimal_places=2)
    facturacion = models.DecimalField(max_digits=12, decimal_places=8)
    mora4_60 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora6 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora9 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora12 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora18 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora24 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora36 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self):
        return self.mes_vigencia+' '+self.segmento+' '+self.producto

class Seguimiento1(models.Model):
    periodo = models.CharField(max_length=10, default=0)
    trimestre_form = models.CharField(max_length=10, default=0)
    mes_vigencia = models.CharField(max_length=10)
    buro_camp = models.CharField(max_length=20)
    buro_uno = models.CharField(max_length=20)
    cat_persona = models.CharField(max_length=50, default=0)
    segmento = models.CharField(max_length=20)
    origen = models.CharField(max_length=50)
    rng_ing = models.CharField(max_length=20)
    producto = models.CharField(max_length=50)
    riesgos = models.CharField(max_length=20)
    cluster = models.CharField(max_length=50, default=0)
    flg_lifemiles = models.IntegerField(default=0)
    digital = models.IntegerField(default=0)
    canal_digital = models.CharField(max_length=30, default=0)
    ltv = models.CharField(max_length=60, default=0)
    plazo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    facturacion = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    form = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ctas = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora4 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora6 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora9 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora12 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora18 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora24 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora36 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora4_60 = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.segmento+' '+self.producto

class Mapa(models.Model):
    cod_ofic = models.CharField(max_length=10)
    ubigeo = models.CharField(max_length=15)
    lima_prov = models.CharField(max_length=15, default=0)
    departamento = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    distrito = models.CharField(max_length=60)
    vinculo = models.CharField(max_length=60, default=0)
    inv = models.DecimalField(max_digits=16, decimal_places=10)
    catrasada = models.DecimalField(max_digits=16, decimal_places=10)
    ctas = models.DecimalField(max_digits=8, decimal_places=2)
    codmes = models.CharField(max_length=10)

    def __str__(self):
        return self.cod_ofic+' '+self.ubigeo+' '+self.departamento

class DepartamentosWeb(models.Model):
    tip_doc = models.CharField(max_length=5)
    documento = models.CharField(max_length=25)
    segmento = models.CharField(max_length=25)
    oferta_tc = models.FloatField(default=0)
    plastico_tc = models.CharField(max_length=25)
    oferta_inc = models.DecimalField(max_digits=10, decimal_places=2)
    oferta_pld = models.FloatField(default=0)
    plazo_pld = models.DecimalField(max_digits=5, decimal_places=2)
    verf_lab = models.CharField(max_length=5)
    Verf_dom = models.CharField(max_length=5)
    fuente = models.CharField(max_length=25)
    base = models.IntegerField()
    departamento = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    edad = models.CharField(max_length=5)
    buro = models.CharField(max_length=5)
    ofertas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    formalizado = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    semana = models.IntegerField(default=0)

    def __str__(self):
        return self.documento+' '+self.segmento+' '+self.departamento

class AdelantoSueldo(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    rng_buro = models.CharField(max_length=15)
    rng_buro_act = models.CharField(max_length=15, default=0)
    tipo_importe = models.CharField(max_length=30)
    rng_suelgo = models.CharField(max_length=40)
    flg_prestamo = models.CharField(max_length=20)
    estado_cred = models.CharField(max_length=50)
    laboral = models.CharField(max_length=50, default=0)
    ctas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fact = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mora = models.IntegerField(default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.rng_buro+' '+self.tipo_importe

class PrestInmediato(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    rng_ingreso = models.CharField(max_length=30)
    segmento = models.CharField(max_length=10)
    rng_buro = models.CharField(max_length=20)
    laboral = models.CharField(max_length=50, default=0)
    subproducto = models.CharField(max_length=60)
    estado_cred = models.CharField(max_length=50)
    ctas = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fact = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora12 = models.IntegerField(default=0)
    mora6 = models.IntegerField(default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.segmento+' '+self.rng_ingreso

class Forzaje(models.Model):
    periodo = models.CharField(max_length=10, default=0)
    trimestre_form = models.CharField(max_length=10, default=0)
    mes_vigencia = models.CharField(max_length=10)
    dic_global = models.CharField(max_length=10)
    producto = models.CharField(max_length=30)
    form = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.mes_vigencia+' '+self.dic_global+' '+self.producto

class Lifemiles(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    buro = models.CharField(max_length=20)
    buro1 = models.CharField(max_length=20)
    rng_ing = models.CharField(max_length=20)
    segmento = models.CharField(max_length=20)
    ctas = models.DecimalField(max_digits=8, decimal_places=2)
    ctas_saldo = models.DecimalField(max_digits=8, decimal_places=2)
    mora6_60 = models.DecimalField(max_digits=4, decimal_places=2)
    mora12_60 = models.DecimalField(max_digits=4, decimal_places=2)
    mora6 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    mora9 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    mora12 = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    imp_sol = models.DecimalField(max_digits=12, decimal_places=8)
    inv = models.DecimalField(max_digits=12, decimal_places=8)

    def __str__(self):
        return self.mes_vigencia+' '+self.buro+' '+self.segmento

class AltasEmpresa(models.Model):
    mes_vigencia = models.CharField(max_length=10,default=0)
    empresa = models.CharField(max_length=20)
    grupo = models.CharField(max_length=30)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.empresa+' '+self.grupo

class IncreLinea(models.Model):
    mes_vigencia = models.CharField(max_length=10, default=0)
    lifemiles = models.IntegerField(default=0)
    empleado = models.IntegerField(default=0)
    buro = models.CharField(max_length=20, default=0)
    buro_act = models.CharField(max_length=20, default=0)
    segmento = models.CharField(max_length=20, default=0)
    rng_sueldo = models.CharField(max_length=30, default=0)
    laboral = models.CharField(max_length=50, default=0)
    flg_uso = models.IntegerField(default=0)
    ctas = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ctas_uso = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora12 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    cantidad = models.DecimalField(max_digits=12, decimal_places=8, default=0)
    

    def __str__(self):
        return self.mes_vigencia+' '+self.buro+' '+self.segmento

class AltasSegmento(models.Model):
    segmento = models.CharField(max_length=20)
    empresa = models.CharField(max_length=20)
    grupo = models.CharField(max_length=30)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return self.empresa+' '+self.segmento+' '+self.grupo

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

class FlujOperativo(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    tipo = models.CharField(max_length=5)
    grupo_exoneracion = models.CharField(max_length=20)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.mes_vigencia+' '+self.tipo+' '+self.grupo_exoneracion

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
    importe_aprob = models.FloatField(default=0)
    oficina = models.CharField(max_length=50, default=0)
    base_sco = models.IntegerField(default=0)
    base_rvgl = models.IntegerField(default=0)

    def __str__(self):
        return self.mes_vigencia+' '+self.rvgl+' '+self.seco

class HipotecaSSFF(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    banco = models.CharField(max_length=15)
    tipo_hipotecario = models.CharField(max_length=15)
    tipo_cuenta = models.CharField(max_length=15)
    clasificacion = models.IntegerField()
    mto_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clientes = models.IntegerField()

    def __str__(self):
        return self.mes_vigencia+' '+self.banco

class HipotecaConce(models.Model):
    mes_form = models.CharField(max_length=10)
    territorio = models.CharField(max_length=30)
    inversion = models.DecimalField(max_digits=18, decimal_places=15, default=0)
    vencida = models.DecimalField(max_digits=18, decimal_places=15, default=0)
    cuotas = models.IntegerField()
    mes = models.CharField(max_length=10)

    def __str__(self):
        return self.mes_form+' '+self.territorio

class Moras(models.Model):
    trimestre_form = models.CharField(max_length=10)
    mes_form = models.CharField(max_length=10)
    flg_camp = models.CharField(max_length=25)
    flg_uso = models.IntegerField()
    buro_camp = models.CharField(max_length=20, default=0)
    buro_uno = models.CharField(max_length=20, default=0)
    cat_persona = models.CharField(max_length=50, default=0)
    segmento = models.CharField(max_length=20, default=0)
    producto = models.CharField(max_length=30)
    ctas = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ctas_uso = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora4 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora6 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora9 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora12 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora18 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora24 = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mora36 = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.mes_form+' '+self.segmento+' '+self.producto

class Comentario(models.Model):
    periodo = models.CharField(max_length=10)
    titulo = models.CharField(max_length=400, default=0)
    comentario = models.CharField(max_length=3500, default=0)
    usuario = models.CharField(max_length=20)
    tiempo = models.CharField(max_length=50, default=0)
    hora = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.periodo+' '+self.usuario

class ComentarioBackup(models.Model):
    periodo = models.CharField(max_length=10)
    titulo = models.CharField(max_length=400, default=0)
    comentario = models.CharField(max_length=3500, default=0)
    usuario = models.CharField(max_length=20)
    tiempo = models.CharField(max_length=50, default=0)
    hora = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.periodo+' '+self.usuario

class EfectividadTC(models.Model):
    codigo_campana = models.CharField(max_length=10)
    trimestre = models.CharField(max_length=10)
    mes_vigencia = models.CharField(max_length=10)
    buro = models.CharField(max_length=10)
    segmento = models.CharField(max_length=20)
    tipo_clie = models.CharField(max_length=30)
    verificacion = models.CharField(max_length=50)
    contratado = models.CharField(max_length=60)
    total_form = models.DecimalField(max_digits=12, decimal_places=2)
    monto_form = models.DecimalField(max_digits=12, decimal_places=2)
    monto_ofer = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.codigo_campana+' '+self.mes_vigencia+' '+self.buro+' '+self.tipo_clie

class AltasSeguimiento(models.Model):
    buro = models.CharField(max_length=10)
    codempresa = models.CharField(max_length=20)
    empresa = models.CharField(max_length=20)
    mes_alta = models.CharField(max_length=10)
    rg_edad = models.CharField(max_length=20)
    cat_cliente = models.CharField(max_length=30)
    rg_ingreso = models.CharField(max_length=30)
    ctas = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.mes_alta+' '+self.empresa+' '+self.buro+' '+self.cat_cliente

class OfertasProducto(models.Model):
    mes_vigencia = models.CharField(max_length=10)
    ofertas_tc = models.DecimalField(max_digits=12, decimal_places=2)
    monto_tc = models.DecimalField(max_digits=16, decimal_places=2)
    ofertas_pld = models.DecimalField(max_digits=12, decimal_places=2)
    monto_pld = models.DecimalField(max_digits=16, decimal_places=2)
    ofertas_veh = models.DecimalField(max_digits=12, decimal_places=2)
    monto_veh = models.DecimalField(max_digits=16, decimal_places=2)
    ofertas_sub = models.DecimalField(max_digits=12, decimal_places=2)
    monto_sub = models.DecimalField(max_digits=16, decimal_places=2)
    ofertas_ep = models.DecimalField(max_digits=12, decimal_places=2)
    monto_ep = models.DecimalField(max_digits=16, decimal_places=2)
    ofertas_il = models.DecimalField(max_digits=12, decimal_places=2)
    monto_il = models.DecimalField(max_digits=16, decimal_places=2)
    ofertas_ads = models.DecimalField(max_digits=12, decimal_places=2)
    monto_ads = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return self.mes_vigencia

class StockTelefonica(models.Model):
    codmes = models.CharField(max_length=10)
    mesform = models.CharField(max_length=10)
    tipo_operacion = models.CharField(max_length=20)
    clasificacion_final = models.DecimalField(max_digits=8, decimal_places=4)
    maduracion = models.DecimalField(max_digits=8, decimal_places=4)
    con_atraso = models.DecimalField(max_digits=8, decimal_places=4)
    ctas = models.DecimalField(max_digits=16, decimal_places=4)
    ctas_atraso = models.DecimalField(max_digits=16, decimal_places=4)
    ctas_30 = models.DecimalField(max_digits=16, decimal_places=4)
    deuda = models.DecimalField(max_digits=16, decimal_places=4)
    mora_30 = models.DecimalField(max_digits=16, decimal_places=4)
    vigente = models.DecimalField(max_digits=16, decimal_places=4)
    vencido = models.DecimalField(max_digits=16, decimal_places=4)
    judicial = models.DecimalField(max_digits=16, decimal_places=4)
    ref_vigente = models.DecimalField(max_digits=16, decimal_places=4)
    ref_vencido = models.DecimalField(max_digits=16, decimal_places=4)
    ref_judicial = models.DecimalField(max_digits=16, decimal_places=4)
    prov_gen = models.DecimalField(max_digits=16, decimal_places=4)
    prov_esp = models.DecimalField(max_digits=16, decimal_places=4)
    prov_pro = models.DecimalField(max_digits=16, decimal_places=4)

    def __str__(self):
        return self.codmes+' '+self.mesform+' '+self.tipo_operacion+' '+self.clasificacion_final

class FormTelefonica(models.Model):
    cosecha = models.CharField(max_length=10)
    rng_edad = models.CharField(max_length=20)
    rng_buro = models.CharField(max_length=20)
    cluster = models.CharField(max_length=50)
    rng_financiar = models.CharField(max_length=20)
    capital_financiar = models.DecimalField(max_digits=16, decimal_places=4)
    form = models.DecimalField(max_digits=16, decimal_places=4)
    m12 = models.DecimalField(max_digits=16, decimal_places=4)
    m6 = models.DecimalField(max_digits=16, decimal_places=4)
    m3 = models.DecimalField(max_digits=16, decimal_places=4)

    def __str__(self):
        return self.cosecha+' '+self.rng_edad+' '+self.rng_buro


class AltasTarjetas(models.Model):
    mes = models.CharField(max_length=50)
    segmento = models.CharField(max_length=50)
    riesgo_cliente = models.CharField(max_length=100)
    tipo_oferta = models.CharField(max_length=100)
    edad = models.CharField(max_length=200)
    sueldo_final = models.CharField(max_length=200)
    buro = models.CharField(max_length=100)
    ofertas = models.DecimalField(max_digits=12, decimal_places=2)
    altas = models.DecimalField(max_digits=12, decimal_places=2)
    altas_dia = models.DecimalField(max_digits=12, decimal_places=2)
    dia_alta = models.CharField(max_length=200)

    def __str__(self):
        return self.mes+' '+self.segmento+' '+self.riesgo_cliente