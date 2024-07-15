# Makefile

.PHONY: build

VERSION ?= v1.0.0

build:
	@echo "Building release version $(VERSION)..."
	rm -rf build app/__pycache__
	mkdir -p build/App
	cp -r app build/App/Storii
	cd build && zip -r Storii-$(VERSION).zip App && cd ..
	rm -rf build/App
	@echo "Release build $(VERSION) done."
