# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-13 05:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode', models.PositiveIntegerField(null=True)),
                ('season', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Entry')),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='image',
            field=models.URLField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Media'),
        ),
    ]
