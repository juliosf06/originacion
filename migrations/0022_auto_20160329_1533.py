# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-29 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0021_auto_20160328_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento1',
            name='facturacion',
            field=models.DecimalField(decimal_places=8, default=0, max_digits=12),
        ),
    ]
