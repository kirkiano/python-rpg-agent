#!make
include .env
export $(shell sed 's/=.*//' .env)

.PHONY: test doc run debug \
	docker_build docker_run docker_clean docker_cleanall

DOCKER_REGISTRY=docker.kirkiano.org
IMAGE=rpg-perscrape
FULL_IMAGE=$(DOCKER_REGISTRY)/$(IMAGE)
CONTAINER=$(IMAGE)


run:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE)

debug:
	python src/main.py $(PORT) $(BOTFILE) --waitleave $(WAITLEAVE) -v

test:
	python -m unittest test

doc:
	$(MAKE) -C sphinx html

###########################################################

docker_build:
	docker build --tag $(FULL_IMAGE) .

docker_run: docker_build
	docker run --env-file .env --name $(CONTAINER) $(FULL_IMAGE)

docker_logs:
	docker logs $(CONTAINER) -f

docker_login:
	docker exec -it $(CONTAINER) /bin/sh

docker_clean:
	docker rm -f $(CONTAINER) || true

docker_cleanall: docker_clean
	docker rmi -f $(FULL_IMAGE) || true
