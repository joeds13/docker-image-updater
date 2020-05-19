IMAGE := $(shell basename `pwd`)
REGISTRY := ecr.repository
VERSION := $(shell git rev-parse --short=8 HEAD)

all: build tag push

build:
	docker build -t $(PREFIX)/$(IMAGE):$(VERSION) .

run:
	docker run --rm \
		-v /var/run/docker.sock:/var/run/docker.sock:ro \
		-v $(HOME)/.docker/config.json:/.docker/config.json \
		-e DOCKER_REGISTRY=$(REGISTRY) \
		$(IMAGE):$(VERSION)
