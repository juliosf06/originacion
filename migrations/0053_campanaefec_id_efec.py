# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-19 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0052_auto_20160719_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='campanaefec',
            name='id_efec',
            field=models.IntegerField(default=0),
        ),
    ]