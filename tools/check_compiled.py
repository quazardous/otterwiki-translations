"""Check each compiled catalog (.mo) matches its source (.po).

usage: python tools/check_compiled.py path/to/messages.po ...
The .mo files are committed so that a plain `pip install` works: this
catches a .po edited without `make compile`.
"""

import sys

from babel.messages.mofile import read_mo
from babel.messages.pofile import read_po


def entries(catalog):
    result = {}
    for message in catalog:
        if not message.id or not message.string or message.fuzzy:
            continue
        context = message.context
        if isinstance(context, bytes):  # read_mo does not decode it
            context = context.decode()
        ids = message.id if isinstance(message.id, (list, tuple)) else [message.id]
        strings = message.string
        strings = (
            tuple(strings) if isinstance(strings, (list, tuple)) else (strings,)
        )
        result[(context, tuple(ids))] = strings
    return result


ok = True
for po in sys.argv[1:]:
    mo = po[: -len(".po")] + ".mo"
    with open(po, "rb") as f:
        source = entries(read_po(f))
    with open(mo, "rb") as f:
        compiled = entries(read_mo(f))
    if source != compiled:
        ok = False
        print(f"{mo} is out of date: run make compile")
    else:
        print(f"{mo}: up to date")
sys.exit(0 if ok else 1)
