# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-10 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0044_departamentosweb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamentosweb',
            name='edad',
            field=models.CharField(max_length=5),
        ),
    ]
