# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-14 20:50
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportng', '0005_smsdeliveryreport_kituser_parent_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSDeliveryReportTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received', models.DateTimeField(auto_now_add=True)),
                ('body', django.contrib.postgres.fields.jsonb.JSONField()),
                ('request_meta', django.contrib.postgres.fields.jsonb.JSONField()),
                ('status', models.CharField(choices=[('0', 'Unprocessed'), ('1', 'Processed'), ('2', 'Error')], default='0', max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='smsdeliveryreport',
            old_name='kituser_parent_id',
            new_name='kitu_parent_id',
        ),
    ]
