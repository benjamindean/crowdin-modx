#!/usr/bin/env python
import json
import os
import re
import csv
import shutil
import subprocess

BASE_PATH = '.'
KEYS = ''

try:
   with open('projects.json', 'r') as keysFile:
    KEYS = keysFile.read().replace('\n', '')
    KEYS = json.loads(KEYS)
except IOError:
   print "Error: projects.json file not found"
   exit()

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def download(namespace):
    directory = os.path.join(BASE_PATH, 'translations_source', namespace)
    url = "https://api.crowdin.com/api/project/%s/download/all.zip?key=%s" % (namespace, KEYS[namespace])
    mkdir(directory)
    subprocess.Popen(['wget', url, '-O', namespace + '.zip'], cwd=directory).wait()
    subprocess.Popen(['unzip', '-o', '-q', namespace + '.zip'], cwd=directory).wait()

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

def convert(namespace):
    path = os.path.join(BASE_PATH, 'translations_source', namespace)
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".csv")]:
            parse(os.path.join(dirpath, filename), namespace, filename)

def cleanup():
    SOURCE_DIR = os.path.join(BASE_PATH, 'translations_source')
    if os.path.exists(SOURCE_DIR):
        shutil.rmtree(SOURCE_DIR)

def run(base=BASE_PATH):
    global BASE_PATH
    BASE_PATH = base
    for (namespace, key) in KEYS.items():
        download(namespace)
        convert(namespace)
        cleanup()

if __name__ == '__main__':
    run()
