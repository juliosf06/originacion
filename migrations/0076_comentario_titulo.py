# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-13 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('originacion', '0075_comentariobackup'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='titulo',
            field=models.CharField(default=0, max_length=400),
        ),
    ]
