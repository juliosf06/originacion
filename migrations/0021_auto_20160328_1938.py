# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0020_flujoperativo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento1',
            name='facturacion',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
    ]
