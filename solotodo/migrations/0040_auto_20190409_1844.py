# Generated by Django 2.0.3 on 2019-04-09 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solotodo', '0039_auto_20190408_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='active_banner_update',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='banners.BannerUpdate'),
        ),
    ]
