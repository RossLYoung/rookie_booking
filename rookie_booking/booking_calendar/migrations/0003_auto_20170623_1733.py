# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 16:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking_calendar', '0002_auto_20170623_0232'),
    ]

    operations = [
        migrations.CreateModel(
            name='PoolResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balls_left', models.PositiveSmallIntegerField(default=1, verbose_name=b'Balls Left')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('loser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='losing_games', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winning_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='description',
            field=models.CharField(blank=True, default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.CharField(blank=True, default=b'', max_length=100),
        ),
    ]