# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-14 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_rvgl_importe_aprob'),
    ]

    operations = [
        migrations.AddField(
            model_name='rvgl',
            name='oficina',
            field=models.CharField(default=0, max_length=50),
        ),
    ]