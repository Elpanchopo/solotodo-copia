# Generated by Django 2.0.3 on 2019-08-21 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0060_entitylog_scraped_condition'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP MATERIALIZED VIEW solotodo_materializedentity
            """)
    ]
