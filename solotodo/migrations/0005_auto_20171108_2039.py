# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-08 20:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0004_auto_20171102_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entity',
            name='last_pricing_update_user',
        ),
        migrations.RemoveField(
            model_name='entity',
            name='last_staff_change',
        ),
        migrations.RemoveField(
            model_name='entity',
            name='last_staff_change_user',
        ),
    ]
