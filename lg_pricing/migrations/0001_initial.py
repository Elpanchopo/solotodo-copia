# Generated by Django 2.0.3 on 2019-07-04 14:43

from django.db import migrations, models
import django_redshift_backend.distkey


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LgRsBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.IntegerField()),
                ('store_name', models.CharField(max_length=255)),
                ('category_id', models.IntegerField()),
                ('category_name', models.CharField(max_length=255)),
                ('banner_id', models.IntegerField()),
                ('asset_id', models.IntegerField()),
                ('content_id', models.IntegerField()),
                ('section_id', models.IntegerField()),
                ('section_name', models.CharField(max_length=255)),
                ('subsection_id', models.IntegerField()),
                ('subsection_name', models.CharField(max_length=255)),
                ('type_id', models.IntegerField()),
                ('type_name', models.CharField(max_length=255)),
                ('brand_id', models.IntegerField()),
                ('brand_name', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('update_id', models.IntegerField()),
                ('picture_url', models.URLField()),
                ('banner_url', models.URLField()),
                ('score', models.IntegerField()),
                ('store_week_updates', models.IntegerField()),
                ('normalized_score', models.FloatField()),
                ('is_active', models.BooleanField()),
            ],
            options={
                'ordering': ('timestamp',),
                'indexes': [django_redshift_backend.distkey.DistKey(fields=['brand_id'], name='lg_pricing__brand_i_fbc4cb_idx')]
            },
        ),
    ]
