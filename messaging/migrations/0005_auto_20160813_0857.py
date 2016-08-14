# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-13 07:57
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160812_0233'),
        ('messaging', '0004_remindermessaging_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunningMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', django.contrib.postgres.fields.jsonb.JSONField()),
                ('contact_dsoi', django.contrib.postgres.fields.jsonb.JSONField()),
                ('reminders', django.contrib.postgres.fields.jsonb.JSONField()),
                ('job', django.contrib.postgres.fields.jsonb.JSONField()),
                ('completed', models.BooleanField(default=False)),
                ('first_run_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.KITUser')),
            ],
        ),
        migrations.AlterField(
            model_name='reminder',
            name='delta_direction',
            field=models.CharField(choices=[('before', 'Before'), ('after', 'After')], default='before', max_length=10),
        ),
    ]
