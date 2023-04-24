# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-24 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_columns', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorycolumn',
            options={'ordering': ('field__category', 'ordering')},
        ),
        migrations.AddField(
            model_name='categorycolumn',
            name='ordering',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
