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
    trakt_slug = models.SlugField()
    type = models.CharField(max_length=3, choices = TYPES)
    image = models.URLField()
    desc = models.TextField()
    is_anime = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_type(self):
        return dict(self.TYPES).get(self.type)

    def get_last_entry(self):
        last = self.entries.all().last()
        return last

    #@permalink
    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('detail', args=[self.slug])

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    media = models.ForeignKey("Media", related_name="entries")
    episode = models.PositiveIntegerField(null=True,blank=True)
    season = models.PositiveIntegerField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.media


class Resource(models.Model):
    QUA = (
        ('1080p','1080p'),
        ('720p','720p'),
    )
    entry = models.ForeignKey("Entry", related_name="resources")
    code = models.TextField()
    quality = models.CharField(max_length=5, choices=QUA)
    source = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s %s" % (self.entry, self.quality)

    def get_other_sources(self):
        return self.entry.resources.exclude(pk=self.pk)

    class Meta:
        unique_together  = ("entry","quality")

