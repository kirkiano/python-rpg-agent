
.PHONY: test doc

run: port botfile
	python src/main.py $(PORT) $(BOTFILE)

debug: port botfile
	python src/main.py $(PORT) $(BOTFILE) -v

test:
	python -m unittest test

doc:
	$(MAKE) -C sphinx html

port:
ifndef PORT
	error(PORT is undefined)
endif

botfile:
ifndef BOTFILE
	error(BOTFILE is undefined)
endif
