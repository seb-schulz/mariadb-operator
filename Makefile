IMAGE ?= ghcr.io/seb-schulz/mariadb-operator
VERSION ?= latest

BUILDAH_BIN ?= $(shell which buildah 2> /dev/null)
BUILDAH_ARGS ?= --squash

.PHONY: build
build:
	$(BUILDAH_BIN) bud $(BUILDAH_ARGS) -t $(IMAGE):$(VERSION)

.PHONY: test-latest
test-latest:
	./scripts/test-apply.sh $(IMAGE) $(VERSION)
