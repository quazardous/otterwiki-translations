"""Create the language pack of a new language.

usage: python tools/new_language.py <locale> "<English name>"
e.g.   python tools/new_language.py pt_BR "Portuguese (Brazil)"

Writes packages/otterwiki-lang-<locale>/: a plugin for An Otter Wiki whose
only job is to give the wiki the folder of its catalog, and the catalog
itself, made from messages.pot (run `make sync` first).
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PYPROJECT = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{dist}"
version = "{version}"
description = "{name} translation of An Otter Wiki's interface."
readme = "README.md"
license = "MIT"
authors = [{{ name = "An Otter Wiki contributors" }}]
requires-python = ">=3.11"
keywords = ["otterwiki", "wiki", "translation", "i18n", "{locale}"]
classifiers = [
    "Framework :: Flask",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: {name}",
    "Topic :: Software Development :: Localization",
]

[project.urls]
Homepage = "https://github.com/quazardous/otterwiki-translations"
Issues = "https://github.com/quazardous/otterwiki-translations/issues"

[project.entry-points.otterwiki]
lang_{module_suffix} = "{module}"

[tool.hatch.build.targets.wheel]
packages = ["{module}"]
"""

INIT = '''"""{name} translation of An Otter Wiki's interface."""

import os

from otterwiki.plugins import hookimpl, plugin_manager


class LanguagePack:
    @hookimpl
    def translation_directories(self):
        return os.path.join(os.path.dirname(__file__), "translations")


plugin_manager.register(LanguagePack())
'''

README = """\
# {dist}

The {name} translation of [An Otter Wiki](https://otterwiki.com)'s interface,
as a plugin.

```sh
pip install {dist}
```

With the Docker image, put this folder in the `/plugins` volume: the image
installs every plugin it finds there when it starts.

Then pick the language: `SITE_LANG={tag}` for every visitor, or let them
choose with `LANGUAGE_MENU=true` and/or `LANGUAGE_FROM_BROWSER=true`.

Part of [otterwiki-translations](https://github.com/quazardous/otterwiki-translations):
see there to fix or complete the translation.
"""


def main(locale, name):
    module_suffix = locale.lower()
    dist = "otterwiki-lang-" + locale.lower().replace("_", "-")
    module = "otterwiki_lang_" + module_suffix
    base = os.path.join(ROOT, "packages", dist)
    if os.path.exists(base):
        sys.exit(f"{base} exists already")
    os.makedirs(os.path.join(base, module, "translations"))
    version = open(os.path.join(ROOT, "VERSION")).read().strip()
    values = dict(
        dist=dist,
        module=module,
        module_suffix=module_suffix,
        locale=locale,
        tag=locale.replace("_", "-"),
        name=name,
        version=version,
    )
    with open(os.path.join(base, "pyproject.toml"), "w") as f:
        f.write(PYPROJECT.format(**values))
    with open(os.path.join(base, module, "__init__.py"), "w") as f:
        f.write(INIT.format(**values))
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(README.format(**values))
    subprocess.run(
        [
            "pybabel",
            "init",
            "-i",
            os.path.join(ROOT, "messages.pot"),
            "-d",
            os.path.join(base, module, "translations"),
            "-l",
            locale,
        ],
        check=True,
    )
    print(f"created {base}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
