# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-02 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20161201_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagetemplate',
            name='email_reply_to',
            field=models.ManyToManyField(to='core.Contact', verbose_name='Reply To'),
        ),
    ]
