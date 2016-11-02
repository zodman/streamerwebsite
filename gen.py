import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","streamerwebsite.settings")
django.setup()

import click
from base.models import Media, Entry, Resource
from trakt_tool import gen_api
import slugify
import random
import guessit
import formic
from shelljob import proc
from trakt.movies import get_recommended_movies, trending_movies
from trakt.tv import get_recommended_shows, trending_shows

all_movies = get_recommended_movies() + trending_movies() + get_recommended_shows() + trending_shows()
for i in all_movies:
    print "python import.py media {}".format(i.ids["ids"]["slug"])

