# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-24 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gomez', '0008_auto_20160823_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsreport',
            name='gw_msg_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
