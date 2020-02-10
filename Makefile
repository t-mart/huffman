.PHONY : compile-deps upgrade-deps sync-deps compile-and-sync-deps upgrade-and-sync-deps

all: deps

compile-deps:
	pip-compile --generate-hashes --build-isolation requirements.in
	pip-compile --generate-hashes --build-isolation requirements-dev.in

upgrade-deps:
	pip-compile --generate-hashes --build-isolation --upgrade requirements.in
	pip-compile --generate-hashes --build-isolation --upgrade requirements-dev.in

sync-deps:
	pip-sync requirements.txt requirements-dev.txt

compile-and-sync-deps: compile-deps sync-deps

upgrade-and-sync-deps: upgrade-deps sync-deps

deps: compile-and-sync-deps
