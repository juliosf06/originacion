# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-23 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0062_auto_20160921_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='forzaje',
            name='trimestre',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='seguimiento1',
            name='trimestre',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
