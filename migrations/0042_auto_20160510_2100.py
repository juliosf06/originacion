# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-10 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0041_auto_20160428_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampanaWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_desde', models.CharField(max_length=10)),
                ('fecha_hasta', models.CharField(max_length=10)),
                ('fecha_recepcion', models.CharField(max_length=10)),
                ('num_clientes', models.DecimalField(decimal_places=2, max_digits=12)),
                ('form_tdc', models.DecimalField(decimal_places=2, max_digits=12)),
                ('form_pld', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_filtros', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tdc_moi', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tdc_il', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tdc_nueva', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tdc_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tdc_porcentaje', models.DecimalField(decimal_places=2, max_digits=12)),
                ('pld_moi', models.DecimalField(decimal_places=2, max_digits=12)),
                ('pld_nueva', models.DecimalField(decimal_places=2, max_digits=12)),
                ('pld_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('pld_porcentaje', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.AlterField(
            model_name='adelantosueldo',
            name='ctas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='adelantosueldo',
            name='fact',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
