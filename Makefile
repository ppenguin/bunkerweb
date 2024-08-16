.ONESHELL:

TAGS ?= $(shell cat src/VERSION)
DUSER ?= ppenguin
DREGISTRY ?= docker.io
# The DOCKERHUBTOKEN is in the env

.PHONY: all help
all: help

##@ Utility
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# We assume our dev host is amd64 and we will build the arm64 arch natively somewhere else and place the resulting tgz in .build/
.PHONY: imgbw-amd64
imgbw-amd64: .build/bunkerweb-amd64.tgz  ## Build plain docker image archive for bunkerweb amd64
.build/bunkerweb-amd64.tgz: | .build/
	podman build --platform=linux/amd64 --no-cache -f src/bw/Dockerfile --force-rm -t $(DUSER)/bunkerweb:amd64 .
	podman save bunkerweb:amd64 | gzip -c >$@

# The reason it didn't work was in fact a system upgrade without reboot, leading to borked binfmt handling
# image-scheduler:  ## Build multiarch image of scheduler (on amd64 with qemu for arm64)
# 	# just in case...
# 	podman run --rm --privileged multiarch/qemu-user-static:latest --reset -p yes
# 	# somehow building with more platforms directly gives us a multiarch manifest but a single image, so we do the 2 step process
# 	podman manifest rm $(DUSER)/bunkerweb-scheduler:$(TAGS)
# 	podman manifest create $(DUSER)/bunkerweb-scheduler:$(TAGS)
# 	for arch in arm64; do
# 		echo "Building $@ for $$arch platform..."
# 		podman build --platform=linux/$$arch --no-cache -f src/scheduler/Dockerfile --force-rm -t $(DUSER)/bunkerweb-scheduler:$$arch .
# 		podman manifest add $(DUSER)/bunkerweb-scheduler:$(TAGS) bunkerweb-scheduler:$$arch
# 	done
# 	# podman manifest push $(DUSER)/bunkerweb-scheduler:$(TAGS)

image-scheduler:  | docker-login  ## Build multiarch image of scheduler (on amd64 with qemu for arm64)
	podman manifest rm $(DUSER)/bunkerweb-scheduler:$(TAGS)
	podman manifest create $(DUSER)/bunkerweb-scheduler:$(TAGS)
	podman build --platform=linux/amd64,linux/arm64 --no-cache -f src/scheduler/Dockerfile --force-rm --manifest $(DUSER)/bunkerweb-scheduler:$(TAGS) .
	podman manifest push $(DUSER)/bunkerweb-scheduler:$(TAGS)

image-bunkerweb: .build/bunkerweb-amd64.tgz .build/bunkerweb-arm64.tgz | docker-login ## Build multiarch docker images for bunkerweb 
	podman manifest rm $(DUSER)/bunkerweb:$(TAGS)
	podman manifest create $(DUSER)/bunkerweb:$(TAGS)
	for img in $^; do 
		podman load -i "$$img" \
			&& podman manifest add $(DUSER)/bunkerweb:$(TAGS) bunkerweb:$$(sed -n -E 's/^.*?-([A-Za-z0-9]*)\..*$$/\1/p' <<<"$$img")
	done
	podman manifest push $(DUSER)/bunkerweb:$(TAGS)

.PHONY: docker-login
docker-login:
	@podman login -u "$(DUSER)" -p "$(DOCKERHUBTOKEN)" "$(DREGISTRY)"

# explicit push is not necessary if we already have done `push manifest ...`
.PHONY: push-% pushall
pushall: pushdh-bunkerweb pushdh-bunkerweb-scheduler
pushdh-%: | docker-login  ## push to remote registry
	podman push $(DUSER)/$*:$(TAGS) $(DREGISTRY)/$(DUSER)/$*:$(TAGS)


%/:
	mkdir -p $@
