import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","streamerwebsite.settings")
import django
django.setup()

import click
from base.models import Media
from trakt_tool import gen_api
import slugify
import random

@click.command()
@click.argument("name", nargs=-1)
@click.option("--is-anime", is_flag=True, default=False)
def main(name, is_anime):
	result = gen_api(name, is_anime)
	name = result.get("trakt").get("title")
	type = "mov" if result.get("type",False) else 'ser'

	image = random.choice(result.get("tmdb").get("posters"))
	desc = result.get("trakt").get("overview")
	Media.objects.create(name=name, slug= slugify.slugify(name), 
						 type=type, desc=desc, image = image)


if __name__ == "__main__":
	main()