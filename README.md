### Crowdin translations parser for MODX

Command-line utility which downloads translations from Crowdin Localization Platform and converts them into MODX lexicon files.

## Getting Started

1. `git clone git@github.com:benjamindean/crowdin-modx.git`
2. `cd crowdin-modx && sudo python setup.py install`
3. Create `projects.json` file:
```
{
    "project-identifier": "api-key",
    ...
}
```
4. Run `crowdin-modx` inside the folder where `projects.json` file is.

The script will download and covert all projects mentioned in `projects.json` file into the following folder structure:

```
.
├── project-identifier
    └── lexicon
        └── language
            └── filename.inc.php

```

## Notes

The source `.csv` files should have *key-id*, *source*, and *translation* headers.
