
.PHONY: build run logs login clean cleanall

DOCKER_REGISTRY=docker.kirkiano.org
IMAGE=rpg-perscrapers
FULL_IMAGE=$(DOCKER_REGISTRY)/$(IMAGE):$(IMAGE_TAG)
CONTAINER=$(IMAGE)


build: image_tag
	docker build ../.. \
		-f Dockerfile \
		--tag $(FULL_IMAGE)

run: build image_tag
	docker run --env-file .env --name $(CONTAINER) $(FULL_IMAGE)

logs:
	docker logs $(CONTAINER) -f

login:
	docker exec -it $(CONTAINER) /bin/sh

clean:
	docker rm -f $(CONTAINER) || true

cleanall: clean image_tag
	docker rmi -f $(FULL_IMAGE) || true

############################################################


image_tag:
ifndef IMAGE_TAG
	$(error IMAGE_TAG not defined)
endif
