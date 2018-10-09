import requests
import json
import pprint
import click
import tabulate
import textwrap
import twitter
import time


topten_urls = {
    "overall": "https://docs.google.com/spreadsheets/d/1Y2NsSASb5EGWBhIqf7BGAI1OS0-bECMmR8w9TU_6-jY/gviz/tq?gid=0&tq=select%20A%2CB%2CD%20%20order%20by%20B%20desc%20limit%2010%20offset%200",
    "deutschrap": "https://docs.google.com/spreadsheets/d/1Y2NsSASb5EGWBhIqf7BGAI1OS0-bECMmR8w9TU_6-jY/gviz/tq?gid=0&tq=select%20A%2CB%2CD%20where%20D%20%3D%20%22deutschrap%22%20order%20by%20B%20desc%20limit%2010%20offset%200",
    "iconic-berlin": "https://docs.google.com/spreadsheets/d/1Y2NsSASb5EGWBhIqf7BGAI1OS0-bECMmR8w9TU_6-jY/gviz/tq?gid=0&tq=select%20A%2CB%2CD%20where%20D%20%3D%20%22iconic-berlin%22%20order%20by%20B%20desc%20limit%2010%20offset%200",
    "gitarren": "https://docs.google.com/spreadsheets/d/1Y2NsSASb5EGWBhIqf7BGAI1OS0-bECMmR8w9TU_6-jY/gviz/tq?gid=0&tq=select%20A%2CB%2CD%20where%20D%20%3D%20%22gitarren%22%20order%20by%20B%20desc%20limit%2010%20offset%200",
    "electronic-germany": "https://docs.google.com/spreadsheets/d/1Y2NsSASb5EGWBhIqf7BGAI1OS0-bECMmR8w9TU_6-jY/gviz/tq?gid=0&tq=select%20A%2CB%2CD%20where%20D%20%3D%20%22electronic-germany%22%20order%20by%20B%20desc%20limit%2010%20offset%200"
}

post_url="https://script.google.com/a/folderstudio.com/macros/s/AKfycbyZkkkm00AJM_-6HHRbU9WdTyKYKKh2XcpjC2AEww/exec"

def get_topten(topten_url):
    request = requests.get(topten_url)
    j = json.loads(request.text.replace("/*O_o*/","").replace("google.visualization.Query.setResponse(", "").replace(");", ""))
    topten = []
    for entry in j["table"]["rows"]:
        name = entry["c"][0]["v"]
        score = entry["c"][1]["v"]
        genre = entry["c"][2]["v"]        
        topten.append({
            "name": name,
            "score": score,
            "genre": genre
        })
    return topten

def post_score(name, score, genre):
    request = requests.post(post_url, data= {"Name": name, "Score": score, "Genre": genre})
    j = json.loads(request.text)
    return request.status_code == 200 and j["result"] == "success"

@click.group()
def cli():
    pass

@click.command()
@click.option("--genre", default="overall", help="{overall|deutschrap|iconic-berlin|gitarren|electronic-germany}")
def topten(genre):
    """Shows top 10"""
    tops = get_topten(topten_urls[genre])
    click.echo(tabulate.tabulate(tops, headers={"Name": "Name", "Score": "Score", "Genre": "Genre"}))

@click.command()
@click.argument("name")
@click.argument("score", type=click.INT)
@click.argument("genre", type=click.Choice(["deutschrap", "iconic-berlin", "gitarren", "electronic-germany"]))
def post(name, score, genre):
    """posts a score with a given name"""
    if post_score(name, score, genre):
        click.echo("score posted successfully")
    else:
        click.echo("posting failed", err=True)

@click.command()
@click.argument("where", type=click.Choice(["overall", "deutschrap", "iconic-berlin", "gitarren", "electronic-germany"]), default="iconic-berlin")
@click.argument("text", type=click.STRING)
def write(where, text):
    """Writes text to the Higg Score board"""
    do_write(where, text)

def do_write(where, text):
    for word in text.split(" "):
        if len(word) > 14:
            click.echo(word + " is too long. Max length of a word should be 14")
            return
    
    lines = textwrap.wrap(text, width=14)
    if len(lines) > 10:
        click.echo("Text is too long and would generate more than 10 lines. Please shorten.")
        return
    top = get_topten(topten_urls[where])[0]
    topscore = top["score"]
    topscore += 1
    for line in lines[::-1]:
        click.echo("{}: {}".format(topscore, line))
        post_score(line, topscore, where)
        topscore += 1

@click.command()
@click.option("--consumer-key")
@click.option("--consumer-secret")
@click.option("--access-token-key")
@click.option("--access-token-secret")
@click.option("--screen-name")
def tweet(consumer_key, consumer_secret, access_token_key, access_token_secret, screen_name):
    prevtweet = None
    api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret)    
    while True:
        click.echo("checking for new tweet from {}...".format(screen_name))
        t = api.GetUserTimeline(screen_name=screen_name, count=1)
        tweet = [i.AsDict() for i in t][0]
        if prevtweet != tweet:
            click.echo("found new tweet: {}".format(tweet["text"]))
            do_write("gitarren", tweet["text"])
            prevtweet = tweet
        else:
            click.echo("no new tweet found.")
        time.sleep(30)

cli.add_command(topten)
cli.add_command(post)
cli.add_command(write)
cli.add_command(tweet)

if __name__ == '__main__':
    cli()