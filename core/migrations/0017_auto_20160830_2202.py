# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-30 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20160830_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kituser',
            name='email_validated_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='kituser',
            name='phone_validated_date',
            field=models.DateTimeField(null=True),
        ),
    ]
