#!/usr/bin/env python
import json
import os
import re
import csv
import shutil
import subprocess
import click

BASE_PATH = '.'
KEYS = ""

@click.group()
def cli():
    """Crowdin parser for MODX"""
    pass

def _setKeys():
    try:
       with open('projects.json') as keysFile:
        KEYS = json.load(keysFile)
    except IOError:
       click.secho("projects.json file not found.", fg='red')
       exit()

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

@cli.command()
@click.argument("namespace", nargs=1)
def download(namespace):
    """Download and extract project"""
    _setKeys()
    if namespace in KEYS:
        directory = os.path.join(BASE_PATH, 'translations_source', namespace)
        url = "https://api.crowdin.com/api/project/%s/download/all.zip?key=%s" % (namespace, KEYS[namespace])
        mkdir(directory)
        subprocess.Popen(['wget', url, '-O', namespace + '.zip'], cwd=directory).wait()
        subprocess.Popen(['unzip', '-o', '-q', namespace + '.zip'], cwd=directory).wait()
    else:
        click.secho("%s not found in projects.json file." % namespace, fg='red')
        exit()

def parse(path, namespace, filename):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        pathList = path.split('/')
        directory = os.path.join(BASE_PATH, namespace, 'lexicon', pathList[pathList.index('translations_source') + 2])
        filename = re.sub(r'(\'|&| )', '', filename)
        php = os.path.join(directory, filename.replace('csv', 'inc.php'))
        mkdir(directory)

        file = open(php, 'w')
        file.write('<?php\n')

        for row in reader:
            key = row['key-id'].replace('"', "")
            if '' != row['translation']:
                translated = row['translation']
            else:
                translated = row['source']
            file.write("$_lang[\"%s\"] = \"%s\";\n" % (key, translated.replace('"', "'").splitlines()[0]))

        file.close()

@cli.command()
@click.argument('namespace', nargs=1)
def convert(namespace):
    """Convert project to MODX lexicon files"""
    path = os.path.join(BASE_PATH, 'translations_source', namespace)
    if os.path.isdir(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in [f for f in filenames if f.endswith(".csv")]:
                parse(os.path.join(dirpath, filename), namespace, filename)
        click.secho("%s successfully converted." % namespace, fg='green')
    else:
        click.secho("%s not found in source folder. You need to download in first." % namespace, fg='red')
        exit()

@cli.command()
def cleanup():
    """Delete 'translations_source' folder"""
    SOURCE_DIR = os.path.join(BASE_PATH, 'translations_source')
    if os.path.exists(SOURCE_DIR):
        shutil.rmtree(SOURCE_DIR)

@cli.command()
@click.pass_context
def run(ctx, base=BASE_PATH):
    """Download and convert all projects"""
    _setKeys()
    global BASE_PATH
    BASE_PATH = base
    for namespace in KEYS.iterkeys():
        ctx.invoke(download, namespace=namespace)
        ctx.invoke(convert, namespace=namespace)
        ctx.invoke(cleanup)
    click.secho("All done!", fg='green', bold=True)

if __name__ == '__main__':
    run()
