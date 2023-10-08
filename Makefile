IMAGE ?= ghcr.io/seb-schulz/mariadb-operator
VERSION ?= latest

BUILDAH_BIN ?= $(shell which buildah 2> /dev/null)

.PHONY: build
build:
	$(BUILDAH_BIN) bud -t $(IMAGE):$(VERSION)

.PHONY: build-dev
build-dev:
	$(BUILDAH_BIN) bud -f Dockerfile.dev -t $(IMAGE):dev

.PHONY: test-latest
test-latest:
	./scripts/test-apply.sh $(IMAGE) $(VERSION)

.PHONY: test-dev
test-dev:
	./scripts/test-apply.sh $(IMAGE) dev
