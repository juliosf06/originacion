# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-03 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0073_auto_20161024_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='hora',
            field=models.CharField(default=0, max_length=20),
        ),
    ]