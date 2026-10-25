"""Check a gettext catalog is complete and safe to ship.

usage: python check_po.py path/to/messages.po
Fails on: missing or fuzzy translations, a %(name)s placeholder, an HTML
tag, a "$" (CodeMirror) or a trailing/leading newline that differs from the
English source. Prints every problem, exits 1 if there is any.
"""

import re
import sys

from babel.messages.pofile import read_po

PLACEHOLDER = re.compile(r"%\([a-z_]+\)[sd]|%%")
TAG = re.compile(r"</?([a-zA-Z0-9]+)")


def shape(text):
    return (
        sorted(PLACEHOLDER.findall(text)),
        sorted(TAG.findall(text)),
        text.count("$"),
        text.startswith("\n"),
        text.endswith("\n"),
    )


def check(path):
    catalog = read_po(open(path, "rb"))
    problems = []
    total = 0
    for message in catalog:
        if not message.id:
            continue
        total += 1
        where = f"{message.context + ' | ' if message.context else ''}{message.id!r}"
        if message.fuzzy:
            problems.append(f"fuzzy: {where}")
        sources = (
            list(message.id) if isinstance(message.id, (list, tuple)) else [message.id]
        )
        strings = (
            list(message.string)
            if isinstance(message.string, (list, tuple))
            else [message.string]
        )
        if not all(s and s.strip() for s in strings):
            problems.append(f"missing: {where}")
            continue
        # plural forms: compare with the plural source, except %(num)s may be
        # left out of a singular form (e.g. "one page")
        expected = shape(sources[-1])
        for string in strings:
            got = shape(string)
            if got[1:] != expected[1:]:
                problems.append(f"tags/newlines differ: {where} -> {string!r}")
            missing = set(expected[0]) - set(got[0]) - {"%(num)s"}
            extra = set(got[0]) - set(expected[0])
            if missing or extra:
                problems.append(
                    f"placeholders differ ({sorted(missing)} missing,"
                    f" {sorted(extra)} extra): {where} -> {string!r}"
                )
    for problem in problems:
        print(problem)
    print(f"{path}: {total} messages, {len(problems)} problems")
    return not problems


if __name__ == "__main__":
    sys.exit(0 if all([check(p) for p in sys.argv[1:]]) else 1)
