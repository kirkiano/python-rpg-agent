#!make
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: test doc run debug

image_name=rpg-periodical-scrapers
image_name_debug=$(image_name)-debug


run:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE)

debug:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE) -v

test:
	python -m unittest test

doc:
	$(MAKE) -C sphinx html

docker_build:
	docker build \
		--tag $(DOCKER_REGISTRY)/$(image_name) \
		-f Dockerfile/Dockerfile.prod \
		.

docker_run: docker_build
	docker run --env-file .env $(DOCKER_REGISTRY)/$(image_name)

docker_build_debug:
	docker build \
		--tag $(DOCKER_REGISTRY)/$(image_name_debug) \
		-f Dockerfile/Dockerfile.dev \
		.

docker_run_debug: docker_build_debug
	docker run --env-file .env $(DOCKER_REGISTRY)/$(image_name_debug)
