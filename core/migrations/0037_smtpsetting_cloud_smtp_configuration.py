# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-05 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20161002_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='smtpsetting',
            name='cloud_smtp_configuration',
            field=models.BooleanField(default=False),
        ),
    ]
