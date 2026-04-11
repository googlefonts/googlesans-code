SOURCES=$(shell python3 scripts/read-config.py --sources)
FAMILY=$(shell python3 scripts/read-config.py --family)

help:
	@echo "###"
	@echo "# Build targets for $(FAMILY)"
	@echo "###"
	@echo
	@echo "  make build:  Builds the fonts and places them in the fonts/ directory"
	@echo "  make test:   Tests the fonts with fontbakery"
	@echo

build: build.stamp android

venv: venv/touchfile

venv-test: venv-test/touchfile

build.stamp: venv sources/config.yaml $(SOURCES)
	rm -rf fonts
	(for config in sources/config*.yaml; do . venv/bin/activate; gftools builder $$config; done)  && touch build.stamp

android: build.stamp
	mkdir -p fonts/android
	-@rm fonts/android/*.ttf
	cp fonts/variable/GoogleSansCode[wght].ttf fonts/variable/GoogleSansCode-Italic[wght].ttf fonts/android
	venv/bin/python scripts/prune_base.py fonts/android/GoogleSansCode[wght].ttf
	venv/bin/python scripts/prune_base.py fonts/android/GoogleSansCode-Italic[wght].ttf

venv/touchfile: requirements.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/touchfile

venv-test/touchfile: requirements-test.txt
	test -d venv-test || python3 -m venv venv-test
	. venv-test/bin/activate; pip install -Ur requirements-test.txt
	touch venv-test/touchfile

test: venv-test build.stamp
	TOCHECK=$$(find fonts/variable -type f 2>/dev/null); \
	if [ -z "$$TOCHECK" ]; then TOCHECK=$$(find fonts/ttf -type f 2>/dev/null); fi ; \
	. venv-test/bin/activate; \
	mkdir -p out/ out/fontbakery; \
	fontbakery check-profile -l WARN --full-lists --succinct \
		--html out/fontbakery/fontbakery-report.html \
		--ghmarkdown out/fontbakery/fontbakery-report.md \
		qa/check-gscode.py \
		$$TOCHECK

android: build.stamp
	mkdir -p fonts/android
	cp fonts/variable/GoogleSansCode[MONO,wght].ttf fonts/android/
	cp fonts/variable/GoogleSansCode-Italic[MONO,wght].ttf fonts/android/
	. venv/bin/activate; python3 scripts/prune_hvar.py fonts/android/GoogleSansCode[MONO,wght].ttf
	. venv/bin/activate; python3 scripts/prune_hvar.py fonts/android/GoogleSansCode-Italic[MONO,wght].ttf
clean:
	rm -rf venv
	find . -name "*.pyc" -delete

update: venv venv-test
	venv/bin/pip install --upgrade pip-tools
# See https://pip-tools.readthedocs.io/en/latest/#a-note-on-resolvers for
# the `--resolver` flag below.
	venv/bin/pip-compile --upgrade --verbose --resolver=backtracking requirements.in
	venv/bin/pip-sync requirements.txt

	venv-test/bin/pip install --upgrade pip-tools
	venv-test/bin/pip-compile --upgrade --verbose --resolver=backtracking requirements-test.in
	venv-test/bin/pip-sync requirements-test.txt

	git commit -m "Update requirements" requirements.txt requirements-test.txt
	git push

# ---------------------------
# Generate BASE table records
# ---------------------------
autobase: build
	cargo binstall autobase-cli --no-confirm || cargo install --locked autobase-cli
	autobase --min-max --config sources/autobase.toml --words 1000000 fonts/variable/GoogleSansCode*.ttf
