#!/usr/bin/env python
# encoding=utf8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# made by zodman
from __future__ import unicode_literals
from django.db import models


class Media(models.Model):
    TYPES = (
            ('mov',u'Película'),
            ("ser","Serie")
    )	
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    type = models.CharField(max_length=3, choices = TYPES)
    image = models.URLField()

    def get_type(self):
            return dict(self.TYPES).get(self.type)

    def __str__(self):
            return self.name


class Entry(models.Model):
    media = models.ForeignKey("Media")
    episode = models.PositiveIntegerField(null=True)
    season = models.PositiveIntegerField(null=True)

    def __str__(self):
            return u"%s"%self.episode

class Resource(models.Model):
    entry = models.ForeignKey("Entry")
    code = models.TextField()
