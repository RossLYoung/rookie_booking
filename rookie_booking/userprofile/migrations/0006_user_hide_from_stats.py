# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-30 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20170727_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hide_from_stats',
            field=models.BooleanField(default=False, verbose_name='hide from stats'),
        ),
    ]
