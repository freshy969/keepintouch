# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-27 03:25
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_kitubalance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedcontact',
            name='file',
        ),
        migrations.AddField(
            model_name='uploadedcontact',
            name='file_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=1),
            preserve_default=False,
        ),
    ]
