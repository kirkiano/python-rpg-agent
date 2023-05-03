
.PHONY: build image_tag

DOCKER_REGISTRY=docker.kirkiano.org
IMAGE=rpg-perscrapers
FULL_IMAGE=$(DOCKER_REGISTRY)/$(IMAGE):$(IMAGE_TAG)
CONTAINER=$(IMAGE)


build: image_tag
	docker build ../.. \
		-f Dockerfile \
		--tag $(FULL_IMAGE)


image_tag:
ifndef IMAGE_TAG
	$(error IMAGE_TAG not defined)
endif
