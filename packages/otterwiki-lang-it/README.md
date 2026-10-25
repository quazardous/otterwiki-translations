# otterwiki-lang-it

The Italian translation of [An Otter Wiki](https://otterwiki.com)'s interface,
as a plugin.

```sh
pip install otterwiki-lang-it
```

With the Docker image, put this folder in the `/plugins` volume: the image
installs every plugin it finds there when it starts.

Then pick the language: `SITE_LANG=it` for every visitor, or let them
choose with `LANGUAGE_MENU=true` and/or `LANGUAGE_FROM_BROWSER=true`.

Part of [otterwiki-translations](https://github.com/quazardous/otterwiki-translations):
see there to fix or complete the translation.
