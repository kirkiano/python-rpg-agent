#!make
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: test doc run debug \
	docker_build docker_run docker_clean docker_cleanall

IMAGE_NAME=rpg-perscrape
FULL_IMAGE_NAME=$(DOCKER_REGISTRY)/$(IMAGE_NAME)
CONTAINER_NAME=$(IMAGE_NAME)


run:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE)

debug:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE) -v

test:
	python -m unittest test

doc:
	$(MAKE) -C sphinx html

docker_build:
	docker build --tag $(FULL_IMAGE_NAME) .

docker_run: docker_build
	docker run --env-file .env --name $(CONTAINER_NAME) $(FULL_IMAGE_NAME)

docker_logs:
	docker logs $(CONTAINER_NAME) -f

docker_bash:
	docker exec -it $(CONTAINER_NAME) /bin/bash

docker_clean:
	docker rm -f $(CONTAINER_NAME) || true

docker_cleanall: docker_clean
	docker rmi -f $(FULL_IMAGE_NAME) || true
