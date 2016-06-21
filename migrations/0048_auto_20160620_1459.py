# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-20 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0047_auto_20160613_1741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departamentosweb',
            name='fecha_envio',
        ),
        migrations.AddField(
            model_name='departamentosweb',
            name='formalizado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='departamentosweb',
            name='ofertas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]