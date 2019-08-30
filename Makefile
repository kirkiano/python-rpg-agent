
.PHONY: test doc

run:
	python rpg_periodical_scraper/main.py $(PORT) $(BOTFILE)

test:
	python -m unittest test

doc:
	$(MAKE) -C sphinx html

ifndef PORT
	error(PORT is undefined)
endif

ifndef BOTFILE
	error(BOTFILE is undefined)
endif
