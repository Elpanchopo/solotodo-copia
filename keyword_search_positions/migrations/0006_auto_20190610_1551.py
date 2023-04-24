# Generated by Django 2.0.3 on 2019-06-10 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_search_positions', '0005_keywordsearch_active_update'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keywordsearchentityposition',
            options={'ordering': ('update', 'value')},
        ),
        migrations.AlterField(
            model_name='keywordsearchentityposition',
            name='update',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='keyword_search_positions.KeywordSearchUpdate'),
        ),
    ]
