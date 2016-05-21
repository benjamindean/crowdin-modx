### Crowdin translations parser for MODX

Command-line utility which downloads translations from [Crowdin](https://crowdin.com/) Localization Platform and converts them into MODX lexicon files.

## Getting Started

1. `git clone git@github.com:benjamindean/crowdin-modx.git`
2. `cd crowdin-modx && sudo python setup.py install`
3. Create `projects.json`* file.
4. Create `config.cfg`** file.
5. Run `crowdin-modx` inside the folder where `projects.json` file is.

### * projects.json

```
{
    "project-identifier": "api-key",
    ...
}
```

### ** config.cfg

```
[DEFAULT]
template = <?php{n} {array} {n}?>
item-template = $_lang["{key}"] = "{value}";{n}
```

The script will download and covert all projects mentioned in `projects.json` file into the following folder structure:

```
.
├── project-identifier
    └── lexicon
        └── language
            └── filename.inc.php

```

## Commands

### cleanup   

Delete 'translations_source' folder

### convert [NAMESPACE]

Convert project to MODX lexicon files

### download [NAMESPACE]

Download and extract project

### run

Download and convert all projects

## Notes

The source `.csv` files should have *key-id*, *source*, and *translation* headers.
