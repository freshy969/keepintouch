# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-18 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gomez', '0012_auto_20160908_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitsystem',
            name='sms_unsubscribe_message',
            field=models.TextField(default='To Stop receiving SMS from us, click'),
        ),
    ]
