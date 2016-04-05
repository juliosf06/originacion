# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-30 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0022_auto_20160329_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='HipotecaSSFF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_vigencia', models.CharField(max_length=10)),
                ('banco', models.CharField(max_length=15)),
                ('tipo_hipotecario', models.CharField(max_length=15)),
                ('tipo_cuenta', models.CharField(max_length=15)),
                ('clasificacion', models.IntegerField()),
                ('mto_saldo', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('clientes', models.IntegerField()),
            ],
        ),
    ]