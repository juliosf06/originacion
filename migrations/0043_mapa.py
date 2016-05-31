# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-31 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0042_auto_20160510_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_ofic', models.CharField(max_length=10)),
                ('ubigeo', models.CharField(max_length=15)),
                ('lima_prov', models.CharField(default=0, max_length=15)),
                ('departamento', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=50)),
                ('distrito', models.CharField(max_length=60)),
                ('inv', models.DecimalField(decimal_places=10, max_digits=16)),
                ('catrasada', models.DecimalField(decimal_places=10, max_digits=16)),
                ('ctas', models.DecimalField(decimal_places=2, max_digits=8)),
                ('codmes', models.CharField(max_length=10)),
            ],
        ),
    ]