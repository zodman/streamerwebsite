# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 05:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20161015_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='source',
            field=models.CharField(default='Streaming', max_length=30),
            preserve_default=False,
        ),
    ]
