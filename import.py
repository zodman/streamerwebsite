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
@click.option("--files",default="*")
@click.option("--season",default=None)
@click.option("--episode",default=None)
def entry(slug, files, season, episode):
    media = Media.objects.get(slug=slug)
    click.echo("%s %s type: %s" % (media.name,media.trakt_slug, media.get_type()))
    print (files,)
    for file in formic.FileSet(include=files):

        guessit_result = guessit.guessit(file)
        if media.type == "mov":
            res = gen_api(media.trakt_slug, media.is_anime)
            image  = random.choice(res.get("tmdb").get("posters",[]))
            entry = Entry.objects.create(media=media, image=image)
        elif media.type == "ser":
            if not season:
                season = guessit_result.get("season")
                episode = guessit_result.get("episode")
            res = gen_api(media.trakt_slug, media.is_anime)
            seasons = res.get("tvdb",{}).get("seasons",None)
            if not seasons:
                image  = random.choice(res.get("tmdb").get("posters",[]))
            else:
                for s in seasons:
                    if int(s.get("number",-1)) == season:
                        image = s.get("image")
            entry = Entry.objects.create(media=media, image=image,
                    episode=episode, season=season)

        qua = guessit_result.get("screen_size","720p")
        resource = Resource(entry=entry, quality=qua)
        source , ret = upload(file)
        resource.source = source
        resource.code = ret
        resource.save()

def upload(file):
    # TODO: openload uptobox
    return upload_openload(file)
    # SOLIDFILES
    #return upload_solidfiles(file)
def upload_openload(file):
    res_url = upload_file(file, "openload", "aec7ac76bd33ac48:RtyA9q50")
    res = res_url.split("/")
    res[3] = "embed"
    url = "/".join(res)
    ret_tmp = """
    <iframe src="{}" width="640" height="360" scrolling="no" frameborder="0" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>
    """.format(url)

    return ("openload",ret_tmp.strip())

def upload_solidfiles(file):
    ret = upload_file(file, "solidfiles", "pelana@protonmail.com:zxczxc")
    print ret
    ret = ret.replace("/d/","/e/")
    print ret
    ret_tmp = """
    <iframe src="{}" width="640" height="360" scrolling="no" frameborder="0" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>
    """.format(ret)
    return ("solidfiles", ret_tmp.strip())


def upload_file(file, source, auth ):
    cmd = [
        'plowup',
        '--auth', auth,
        source,
        file,
        '-q',
    ]
    print " ".join(cmd)
    output = proc.call(cmd)
    return output
    



if __name__ == "__main__":
    cli()
>>>>>>> 637f4781a51f39383e2b870f7c506705904009ce
