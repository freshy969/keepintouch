# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-27 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160827_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedcontact',
            name='file_extension',
            field=models.CharField(default='csv', max_length=4),
            preserve_default=False,
        ),
    ]
