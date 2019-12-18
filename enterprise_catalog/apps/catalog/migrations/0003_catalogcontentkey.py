# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-18 18:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_enterprisecatalog_historicalenterprisecatalog'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogContentKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('content_key', models.CharField(help_text='The key that represents a piece of content, such as a course run.', max_length=255)),
                ('catalog_query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_content_keys', to='catalog.CatalogQuery')),
            ],
            options={
                'verbose_name': 'Catalog Content Key',
                'verbose_name_plural': 'Catalog Content Keys',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCatalogContentKey',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('content_key', models.CharField(help_text='The key that represents a piece of content, such as a course run.', max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('catalog_query', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalog.CatalogQuery')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Catalog Content Key',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AlterField(
            model_name='enterprisecatalog',
            name='catalog_query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_catalogs', to='catalog.CatalogQuery'),
        ),
        migrations.AlterField(
            model_name='historicalenterprisecatalog',
            name='enterprise_uuid',
            field=models.UUIDField(),
        ),
        migrations.AlterUniqueTogether(
            name='catalogcontentkey',
            unique_together=set([('catalog_query', 'content_key')]),
        ),
    ]