# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-12 01:33
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import randomslugfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160811_0105'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomData',
            fields=[
                ('namespace', randomslugfield.fields.RandomSlugField(blank=True, editable=False, exclude_upper=True, exclude_vowels=True, length=5, max_length=5, primary_key=True, serialize=False, unique=True)),
                ('system_id_field', models.CharField(choices=[('coid', 'Contact ID'), ('doid', 'Domain ID')], max_length=4)),
                ('identity_column_name', models.CharField(max_length=255)),
                ('headers', django.contrib.postgres.fields.jsonb.JSONField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('data_table', django.contrib.postgres.fields.jsonb.JSONField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.KITUser')),
            ],
        ),
        migrations.DeleteModel(
            name='StateMaintainCache',
        ),
    ]