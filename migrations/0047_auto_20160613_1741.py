# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-13 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0046_auto_20160610_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamentosweb',
            name='base',
            field=models.IntegerField(),
        ),
    ]
