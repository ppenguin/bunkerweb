.ONESHELL:

TAGS ?= $(shell cat src/VERSION)
DUSER ?= ppenguin
XARCHS ?= linux/amd64,linux/arm64

DBUILD ?= build

.PHONY: all docker dockerpush buildx
all: help

##@ Utility
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

docker: ## Build plain docker images for bunkerweb and bunkerweb-scheduler
	docker $(DBUILD) --no-cache -f src/bw/Dockerfile --force-rm -t $(DUSER)/bunkerweb:$(TAGS)  .
	docker $(DBUILD) --no-cache -f src/scheduler/Dockerfile --force-rm -t $(DUSER)/bunkerweb-scheduler:$(TAGS) .

buildx: ## Build multiarch docker images for bunkerweb and bunkerweb-scheduler
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	docker buildx create --use --name mybuilder --node mybuilder0
	$(MAKE) DBUILD="buildx build --platform=$(XARCHS)" docker

dockerpush: ## Push built docker images (bw and scheduler)
	docker push $(DUSER)/bunkerweb:$(TAGS) 
	docker push $(DUSER)/bunkerweb-scheduler:$(TAGS) 
