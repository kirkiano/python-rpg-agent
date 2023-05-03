#!make
include .env
export $(shell sed 's/=.*//' .env)


.PHONY: test doc run debug flake8


run:
	python src/main.py $(PORT) $(BOTFILE) \
		--waitleave $(WAITLEAVE) \
		--wait-between-reconnects $(WAIT_BETWEEN_RECONNECTS)

# linter, but decommenting "--application-importnames" below throws false
# positives about import order (I201 errors, etc).
# For more discussion see https://stackoverflow.com/a/47236498.
flake8:
	flake8 src # --application-import-names appnexus

test:
	cd src; python -m unittest get_bots.TestBotfile -v
	cd src; python -m unittest action.blab.TestBlabbingAction -v
	python -m unittest discover -s src -p "test_*.py" -v

doc:
	$(MAKE) -C sphinx html
