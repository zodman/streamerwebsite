#!/usr/bin/env python
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","streamerwebsite.settings")
django.setup()
import yaml
import click
from base.models import Media, Entry, Resource, Subtitle
from django.conf import settings
from trakt_tool import gen_api
import slugify
import random
import guessit
import formic
from shelljob import proc
import json
import opengraph
import requests
from django.core.files import File 

HOME = os.environ.get("HOME")

conf = yaml.load(open(os.path.join(HOME,".gupload")).read())


@click.group()
def cli():
    pass

@cli.command()
@click.argument("name", nargs=-1)
@click.option("--is-anime", is_flag=True, default=False)
def media(name, is_anime):
    """ create movie, serie or anime """
    name = " ".join(name)
    result = gen_api(name, is_anime, name)
    name = result.get("trakt").get("title")
    trakt_slug = result.get("trakt").get("ids").get("slug")
    type = "mov" if result.get("type",False) else 'ser'
    posters = result.get("tmdb", {}).get("posters", [])
    image = result.get("tmdb",{}).get("posters").pop()
    desc = result.get("trakt",{}).get("overview","")
    media,created  = Media.objects.get_or_create(name=name, slug=
            slugify.slugify(name),defaults=dict(is_anime=is_anime,trakt_slug=trakt_slug, 
                                             type=type, desc=desc, image=image,
                                             api =result))
    if not created:
        media.api = result
        media.save()
    else:
        media.api = result
        media.save()


    click.echo(">>>>>>> {} {}".format(media.id, media.slug))


@cli.command()
@click.argument("slug")
@click.option("--files",default="*")
@click.option("--subs",default="*.srt")
@click.option("--season",default=None)
@click.option("--episode",default=None)
def entry(slug, files, season, episode,subs):
    media = Media.objects.get(slug=slug)
    click.echo("%s %s type: %s" % (media.name,media.trakt_slug, media.get_type()))
    for file in formic.FileSet(include=files):
        print file
        guessit_result = guessit.guessit(file)
        if media.type == "mov":
            res = gen_api(media.trakt_slug, media.is_anime, media.trakt_slug)
            image  = random.choice(res.get("tmdb").get("posters",[]))
            entry = Entry.objects.create(media=media, image=image)
        elif media.type == "ser":
            if not season:
                season = guessit_result.get("season")
                episode = guessit_result.get("episode")
            res = gen_api(media.trakt_slug, media.is_anime, media.trakt_slug)
            seasons = res.get("tvdb",{}).get("seasons",None)
            image = False
            if not seasons:
                image  = random.choice(res.get("tmdb").get("posters",[]))
            else:
                for s in seasons:
                    if int(s.get("number",-1)) == int(season):
                        image = s.get("image")
                        break
            if not image:
                click.echo("No pude determinar season ni episode para ponerle una imagen")
                return
            entry = Entry.objects.create(media=media, image=image,
                    episode=episode, season=season)
            click.echo("entry {} creado".format(entry.id))

        qua = guessit_result.get("screen_size","720p")
        resource = Resource(entry=entry, quality=qua)
        source , ret, original_url = upload(file)
        resource.source = source
        resource.code = ret
        resource.original_url = original_url
        resource.save()
        click.echo("Subido!! resource: {}".format(resource.id))

        for file in formic.FileSet(include=subs).qualified_files(absolute=False):
            language = ""
            if ".es.srt" in file:
                language = "es"

            subtitle = Subtitle(language=language)
            fp = File(open(file))
            subtitle.resource = resource
            subtitle.file.save(file,fp)
            subtitle.save()
            # cmd = [
                # 'iconv','-f', 'ISO-8859-1',
                # '-t', 'UTF-8',
                # os.path.join(settings.BASE_DIR,subtitle.file)
            # ]
            # print " ".join(cmd)
            # proc.call(cmd)


def upload(file):
    # TODO: openload uptobox
    #return upload_openload(file)
    # SOLIDFILES
    #return upload_solidfiles(file)
    return upload_googlephoto(file)


def upload_googlephoto(file):
    username, password = conf.get("username"), conf.get("password")
    cmd = [
     'upload-gphotos',
     '-u', username,
     '-p', password,
     file,
    ]
    print " ".join(cmd)
    out = proc.call(cmd)
    source = "googlephoto"
    html_code = """
        <video controls>
            <source src="{}" type="video/mp4">
        </video>
    """ 
    json_str = "".join(out.split("\n")[7:])
    # print json_str
    url = json.loads(json_str)[0].get("id","")
    link="https://photos.google.com/u/1/photo/{}".format(url)
    url_share = click.prompt("ahora es tu chamba abre la liga {} y genera la liga para compartir, cual es?".format(link), type=str)
    resp = requests.get(url_share)
    og = opengraph.OpenGraph(resp.url)
    video_url = og["video"]
    control = html_code.format(video_url)
    return source, control, video_url

def upload_openload(file):
    res_url = upload_file(file, "openload", "aec7ac76bd33ac48:RtyA9q50")
    res = res_url.split("/")
    res[3] = "embed"
    url = "/".join(res)
    ret_tmp = """
    <iframe src="{}" width="640" height="360" scrolling="no" frameborder="0" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>
    """.format(url)

    return ("openload",ret_tmp.strip(), res_url)

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
