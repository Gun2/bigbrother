# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-19 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigbrother_sniper', '0006_auto_20180319_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='postalertmessagelog',
            name='recordTime',
            field=models.DateTimeField(null=True),
        ),
    ]
