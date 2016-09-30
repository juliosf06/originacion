# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-10 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0043_mapa'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartamentosWeb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip_doc', models.CharField(max_length=5)),
                ('documento', models.CharField(max_length=15)),
                ('segmento', models.CharField(max_length=15)),
                ('oferta_tc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('plastico_tc', models.CharField(max_length=15)),
                ('oferta_inc', models.DecimalField(decimal_places=2, max_digits=10)),
                ('oferta_pld', models.DecimalField(decimal_places=2, max_digits=10)),
                ('plazo_pld', models.DecimalField(decimal_places=2, max_digits=5)),
                ('verf_lab', models.CharField(max_length=5)),
                ('Verf_dom', models.CharField(max_length=5)),
                ('fuente', models.CharField(max_length=15)),
                ('base', models.CharField(max_length=5)),
                ('departamento', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=50)),
                ('fecha_envio', models.CharField(max_length=15)),
                ('edad', models.IntegerField()),
                ('buro', models.CharField(max_length=5)),
            ],
        ),
    ]
