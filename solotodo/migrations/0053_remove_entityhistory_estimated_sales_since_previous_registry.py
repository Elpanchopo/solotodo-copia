# Generated by Django 2.0.3 on 2019-07-08 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0052_auto_20190628_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entityhistory',
            name='estimated_sales_since_previous_registry',
        ),
    ]
