# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-13 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0031_auto_20160406_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='altasempresa',
            name='m1',
        ),
        migrations.RemoveField(
            model_name='altasempresa',
            name='m2',
        ),
        migrations.RemoveField(
            model_name='altasempresa',
            name='m3',
        ),
        migrations.RemoveField(
            model_name='altasempresa',
            name='m4',
        ),
        migrations.RemoveField(
            model_name='altasempresa',
            name='m5',
        ),
        migrations.RemoveField(
            model_name='altasempresa',
            name='m6',
        ),
        migrations.AddField(
            model_name='altasempresa',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='altasempresa',
            name='mes_vigencia',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
