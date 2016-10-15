# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-15 04:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_resource_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='desc',
            field=models.TextField(default='bla'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='base.Media'),
        ),
    ]