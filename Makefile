
.PHONY: test doc

run:
	python src/main.py $(PORT) $(BOTFILE)

debug:
	python src/main.py $(PORT) $(BOTFILE) -v

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
