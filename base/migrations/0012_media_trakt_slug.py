# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_media_is_anime'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='trakt_slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
