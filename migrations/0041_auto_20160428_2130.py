# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0040_forzaje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seguimiento1',
            name='form',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='seguimiento1',
            name='plazo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='seguimiento1',
            name='soli',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
