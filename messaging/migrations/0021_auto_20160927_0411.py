# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-27 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20160927_0348'),
        ('messaging', '0020_auto_20160926_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardmessaging',
            name='copied_recipients',
            field=models.ManyToManyField(related_name='cc_recipients', to='core.Contact'),
        ),
        migrations.AlterField(
            model_name='standardmessaging',
            name='recipients',
            field=models.ManyToManyField(related_name='recipients', to='core.Contact'),
        ),
    ]
