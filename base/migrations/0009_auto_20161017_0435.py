# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 04:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_resource_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='media',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='media',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='base.Entry'),
        ),
    ]
