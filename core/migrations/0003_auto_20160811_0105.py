# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-11 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160811_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagetemplate',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
