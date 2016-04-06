# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-06 16:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0029_adelantosueldo_altasempresa_altassegmento_prestinmediato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adelantosueldo',
            name='fact',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='prestinmediato',
            name='fact',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
