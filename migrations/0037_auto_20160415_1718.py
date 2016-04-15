# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-15 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0036_auto_20160415_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moras',
            name='ctas',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='ctas_uso',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='mora12',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='mora18',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='mora24',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='mora36',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='mora4',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='mora6',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='moras',
            name='mora9',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
