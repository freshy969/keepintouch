# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-25 18:29
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMSDeliveryReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('batch_id', models.UUIDField(db_index=True, editable=False, help_text='A.K.A Process ID or Bulk ID')),
                ('origin', models.CharField(choices=[(0, 'Transactional'), (1, 'Bulk SMS')], max_length=1)),
                ('to_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('sms_message', django.contrib.postgres.fields.jsonb.JSONField()),
                ('sms_gateway', django.contrib.postgres.fields.jsonb.JSONField()),
                ('msg_status', models.CharField(choices=[(0, 'ACCEPTED'), (1, 'PENDING'), (2, 'UNDELIVERABLE'), (3, 'DELIVERED'), (4, 'EXPIRED'), (5, 'REJECTED')], max_length=20)),
                ('msg_error', models.CharField(choices=[(0, 'OK'), (1, 'HANDSET_ERROR'), (2, 'USER_ERROR'), (3, 'OPERATOR_ERROR')], max_length=20)),
                ('kituser_id', models.IntegerField(db_index=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMSDeliveryReportHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('message_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportng.SMSDeliveryReport')),
            ],
        ),
    ]
