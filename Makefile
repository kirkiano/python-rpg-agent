
.PHONY: test doc

test:
	python -m unittest test

doc:
	$(MAKE) -C sphinx html
