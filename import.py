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

@click.group()
def cli():
    pass

@cli.command()
@click.argument("name", nargs=-1)
@click.option("--is-anime", is_flag=True, default=False)
def media(name, is_anime):
    """ create movie, serie or anime """
    name = " ".join(name)
    result = gen_api(name, is_anime)
    name = result.get("trakt").get("title")
    trakt_slug = result.get("trakt").get("ids").get("slug")
    type = "mov" if result.get("type",False) else 'ser'
    posters = result.get("tmdb", {}).get("posters", [])
    if posters:
        image = random.choice(posters)
    else:
        image = ""
    desc = result.get("trakt",{}).get("overview","")
    media,created  = Media.objects.get_or_create(name=name, slug=
            slugify.slugify(name),defaults=dict(is_anime=is_anime,trakt_slug=trakt_slug, 
                                             type=type, desc=desc, image=image,
                                             api =result))
    if not created:
        media.api = result
        media.save()

    click.echo(">>>>>>> {} {}".format(media.id, media.slug))


@cli.command()
@click.argument("slug")
@click.option("--file_or_pattern",default="*")
def entry(slug, file_or_pattern):
    media = Media.objects.get(slug=slug)
    click.echo("%s %s type: %s" % (media.name,media.trakt_slug, media.get_type()))
    print (file_or_pattern,)
    for file in formic.FileSet(include=file_or_pattern):

        guessit_result = guessit.guessit(file)
        if media.type == "mov":
            res = gen_api(media.trakt_slug, media.is_anime)
            image  = random.choice(res.get("tmdb").get("posters",[]))
            entry = Entry.objects.create(media=media, image=image)
        elif media.type == "ser":
            res = gen_api(media.trakt_slug, media.is_anime)
            image  = random.choice(res.get("tmdb").get("posters",[]))
            entry = Entry.objects.create(media=media, image=image)

        qua = guessit_result.get("screen_size","720p")
        resource = Resource(entry=entry, quality=qua)
        source , ret = upload(file)
        resource.source = source
        resource.code = ret.strip()
        resource.save()

def upload(file):
    # TODO: openload uptobox

    # SOLIDFILES
    ret = upload_file(file, "solidfiles")
    ret = ret.replace("/d/","/e/")
    ret_tmp = """
    <iframe src="{}" width="640" height="360" scrolling="no" frameborder="0" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>
    """.format(ret)
    return ("solidfiles", ret_tmp.strip())


def upload_file(file, source ):
    cmd = [
        'plowup',
        source,
        file,
        '-q',
    ]
    output = proc.call(cmd)
    return output
    



if __name__ == "__main__":
    cli()
