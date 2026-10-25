"""Italian translation of An Otter Wiki's interface."""

import os

from otterwiki.plugins import hookimpl, plugin_manager


class LanguagePack:
    @hookimpl
    def translation_directories(self):
        return os.path.join(os.path.dirname(__file__), "translations")


plugin_manager.register(LanguagePack())
