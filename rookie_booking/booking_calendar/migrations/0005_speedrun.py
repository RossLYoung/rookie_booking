# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-27 18:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking_calendar', '0004_auto_20170627_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeedRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(default=1, verbose_name=b'Time')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speed_runs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]