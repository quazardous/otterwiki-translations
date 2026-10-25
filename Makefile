# otterwiki-translations — make help
# Each language is a package under packages/, made from messages.pot, the
# strings of An Otter Wiki's interface.
.PHONY: help venv sync update check compile build test clean

# where `make sync` takes messages.pot from: a git ref of An Otter Wiki
# (OTTERWIKI_REF), or a local file (POT=../otterwiki/otterwiki/translations/messages.pot)
OTTERWIKI_REPO ?= redimp/otterwiki
OTTERWIKI_REF ?= main
POT ?=
CATALOGS = $(wildcard packages/*/otterwiki_lang_*/translations/*/LC_MESSAGES/messages.po)
VENV = venv/bin

help: ## this help
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-8s %s\n", $$1, $$2}'

venv: ## the tools: Babel, build
	python3 -m venv venv
	$(VENV)/pip install -q -U pip Babel build

sync: ## fetch messages.pot from An Otter Wiki, then update every catalog
ifeq ($(POT),)
	curl -fsSL -o messages.pot https://raw.githubusercontent.com/$(OTTERWIKI_REPO)/$(OTTERWIKI_REF)/otterwiki/translations/messages.pot
else
	cp $(POT) messages.pot
endif
	$(MAKE) update

update: ## merge messages.pot into every catalog (new strings, fuzzy guesses)
	for po in $(CATALOGS); do \
		dir=$$(dirname $$(dirname $$(dirname $$po))); lang=$$(basename $$(dirname $$(dirname $$po))); \
		$(VENV)/pybabel update -i messages.pot -d $$dir -l $$lang --ignore-obsolete || exit 1; \
	done
	$(MAKE) compile

check: ## every catalog complete, no fuzzy, placeholders and tags kept
	$(VENV)/python tools/check_po.py $(CATALOGS)

compile: ## the .mo files the wiki reads (committed)
	for po in $(CATALOGS); do $(VENV)/pybabel compile -i $$po -o $${po%.po}.mo --statistics || exit 1; done

build: ## a wheel per language in dist/
	for p in packages/*/; do $(VENV)/python -m build -q -w -o dist $$p || exit 1; done

test: check ## check, then make sure the .mo files match the .po files
	$(VENV)/python tools/check_compiled.py $(CATALOGS)

clean:
	rm -rf dist packages/*/dist packages/*/build
