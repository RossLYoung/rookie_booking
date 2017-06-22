# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20150928_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='addresses',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_billing_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_shipping_address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
