#!make
include .env
export $(shell sed 's/=.*//' .env)


.PHONY: test doc run debug flake8


run:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE)

debug:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE) -v

# linter, but throws some false positives about import order (I201 errors, etc).
# For more discussion see https://stackoverflow.com/a/47236498.
flake8:
	flake8 src --application-import-names appnexus

test:
	python -m unittest discover -s src -p "*_test.py"

doc:
	$(MAKE) -C sphinx html
