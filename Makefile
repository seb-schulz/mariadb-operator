IMAGE ?= ghcr.io/seb-schulz/mariadb-operator
VERSION ?= latest

BUILDAH_BIN ?= $(shell which buildah 2> /dev/null)

.PHONY:
build:
	$(BUILDAH_BIN) bud -t $(IMAGE):$(VERSION)

.PHONY:
test-apply:
	./scripts/$@.sh $(IMAGE) $(VERSION)
