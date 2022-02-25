#!make
include .env
export $(shell sed 's/=.*//' .env)


.PHONY: test doc run debug


run:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE)

debug:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE) -v

test:
	python -m unittest discover -s src -p "*_test.py"

doc:
	$(MAKE) -C sphinx html
