### Crowdin translations parser

Command-line utility which downloads translations from [Crowdin](https://crowdin.com/) Localization Platform and converts them into usable translation files.

## Getting Started

1. `git clone git@github.com:benjamindean/crowdin-parse.git`
2. `cd crowdin-parse && sudo python3 setup.py install`
3. Edit `config.cfg`* file.
4. Run `crowdin-parse` inside the folder where `config.cfg` file is.

### * config.cfg

```
[PATHS]
; `base-path` - Base path for converted files.
; `path` - Full path to the converted files. For example:
; /translations/{lang}
base-path = .
path = /translations/{lang}/

[FILE]
; `filename` - if empty - will use original filename exported from Crowdin.
; Otherwise, {lang} placeholder available.
; `extension` - txt, php, etc.
; `only_files` - comma separated list of files to convert.
; For example: page.csv, second page.csv
; Leave it blank if you want to convert all files.
filename =
extension = php
only_files =

[TEMPLATES]
; {n} - new line, {t} - tab.
template = <?php{n}return array({n}{array}); {n}?>
item-template = {t}"{key}" => "{value}",{n}

[KEYS]
; project-name = api-key
; test-project-name = projects_api_key

```

## Commands

### cleanup   

Delete 'translations_source' folder.

### convert [NAMESPACE]

Convert project to language files.

### download [NAMESPACE]

Download and extract project.

### run

Download and convert all projects.

## Notes

The source `.csv` files should have *key-id*, *source*, and *translation* headers.
