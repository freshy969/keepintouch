# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-10 23:12
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('reportng', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsdeliveryreport',
            name='sms_sender',
            field=models.CharField(blank=True, db_index=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='smsdeliveryreport',
            name='to_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128),
        ),
    ]
