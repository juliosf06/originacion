# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-19 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0038_auto_20160415_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exoneracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_vigencia', models.CharField(max_length=10)),
                ('tipo', models.CharField(max_length=5)),
                ('motivo_exo', models.CharField(max_length=50)),
                ('cat_cliente', models.CharField(max_length=50)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]