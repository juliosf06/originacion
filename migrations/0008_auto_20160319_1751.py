# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_auto_20160319_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campana',
            name='monto_adelanto_sueldo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_auto_2da',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_efectivo_plus',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_incr_linea',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_pld',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_prestamo_inmediato',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_renovado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_subrogacion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_tc',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_tc_entry_level',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='campana',
            name='monto_veh',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
