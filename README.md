# otterwiki-translations

Translations of [An Otter Wiki](https://otterwiki.com)'s interface. Each
language is a small plugin, released on its own schedule:

| Language | Package |
|---|---|
| Chinese (Simplified) | `otterwiki-lang-zh-hans-cn` |
| French | `otterwiki-lang-fr` |
| German | `otterwiki-lang-de` |
| Italian | `otterwiki-lang-it` |
| Spanish | `otterwiki-lang-es` |

## Use a language

```sh
pip install otterwiki-lang-fr
```

With the Docker image, copy the package folder (`packages/otterwiki-lang-fr`)
into the `/plugins` volume: the image installs every plugin there when it
starts.

Then choose how the language is picked, in the admin preferences or the
environment:

- `SITE_LANG=fr`: the language of the wiki, for every visitor;
- `LANGUAGE_FROM_BROWSER=true`: the language the visitor's browser prefers,
  when it is installed;
- `LANGUAGE_MENU=true`: a menu to pick one of the installed languages.

A string a language pack doesn't translate yet is shown in English.

## Translate

The strings come from An Otter Wiki: `otterwiki/translations/messages.pot`,
copied here as `messages.pot`. A catalog is
`packages/otterwiki-lang-<lang>/otterwiki_lang_<lang>/translations/<lang>/LC_MESSAGES/messages.po`:
edit it with any gettext editor (Poedit, Lokalize, a text editor).

```sh
make venv      # Babel and build, once
make sync      # take messages.pot from An Otter Wiki (OTTERWIKI_REF=main, or POT=<file>)
               # and merge the new strings into every catalog
make compile   # after editing a .po: the .mo files are committed
make test      # complete, no fuzzy, %(placeholders)s and <tags> kept, .mo up to date
make build     # a wheel per language in dist/
```

Rules for translators:

- keep `%(name)s` placeholders (their order may change), HTML tags, URLs,
  `$` in the editor messages (context `editor`), and names (An Otter Wiki,
  Markdown, Git…);
- fill every plural form of the language;
- commit messages and page names are content, not interface: they are not
  in the catalogs.

## A new language

```sh
python tools/new_language.py pt_BR "Portuguese (Brazil)"
```

creates `packages/otterwiki-lang-pt-br/`, with an empty catalog. Add it to
the table above.

## License

[MIT](LICENSE), like An Otter Wiki.
