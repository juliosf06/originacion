# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0010_prestamo_tarjeta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluacionpld',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=20)),
                ('tip_doc', models.CharField(max_length=5)),
                ('documento', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=100)),
                ('apell_paterno', models.CharField(max_length=100)),
                ('apell_materno', models.CharField(max_length=100)),
                ('edad', models.IntegerField(default=0)),
                ('segmento', models.CharField(max_length=10)),
                ('buro', models.IntegerField(default=0)),
                ('grupo_pr', models.CharField(max_length=10)),
                ('sueldo_final', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('sueldo_final_fuente', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluaciontc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=20)),
                ('tip_doc', models.CharField(max_length=5)),
                ('documento', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=100)),
                ('apell_paterno', models.CharField(max_length=100)),
                ('apell_materno', models.CharField(max_length=100)),
                ('edad', models.IntegerField(default=0)),
                ('segmento', models.CharField(max_length=10)),
                ('buro', models.IntegerField(default=0)),
                ('grupo_pr', models.CharField(max_length=10)),
                ('sueldo_final', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('sueldo_final_fuente', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Prestamo',
        ),
        migrations.DeleteModel(
            name='Tarjeta',
        ),
    ]
