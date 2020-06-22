.PHONY: build help deploy

MAJOR_VERSION=0
MINOR_VERSION=0
PATCH_VERSION=1
BUILD_VERSION=$(shell git rev-parse --short HEAD)
VERSION=$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION)-$(BUILD_VERSION)

LOCAL_DOCKER_TAG=carreratrack:$(VERSION)
REMOTE_DOCKER_TAG=localhost:5000/$(LOCAL_DOCKER_TAG)

build:
	docker build -t $(LOCAL_DOCKER_TAG) .
	docker tag $(LOCAL_DOCKER_TAG) $(REMOTE_DOCKER_TAG)

help:
	@echo ''
	@echo 'Usage: make [TARGET] [EXTRA_ARGUMENTS]'
	@echo 'Targets:'
	@echo '  build      build docker image $(LOCAL_DOCKER_TAG)'
	@echo '  deploy     push docker --image-- into local registry $(REMOTE_DOCKER_TAG)'
	@echo '  clean      remove docker --image--'
	@echo ''

deploy:
	docker push $(REMOTE_DOCKER_TAG)

clean:
	docker rmi $(REMOTE_DOCKER_TAG)
	docker rmi $(LOCAL_DOCKER_TAG)