# Generated by Django 4.2.13 on 2024-07-12 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_catalog', '0004_videoskill_historicalvideoskill'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoshortlist',
            name='is_processed',
            field=models.BooleanField(default=False, help_text='Flag for row level filtering of processed rows.'),
        ),
    ]