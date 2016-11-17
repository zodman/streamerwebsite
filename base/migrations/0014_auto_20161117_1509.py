# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20161026_1402'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='resource',
            name='original_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
