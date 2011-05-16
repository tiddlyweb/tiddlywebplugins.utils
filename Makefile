
# Simple Makefile for some common tasks. This will get
# fleshed out with time to make things easier on developer
# and tester types.
.PHONY: test dist upload

clean:
	find . -name "*.pyc" |xargs rm || true
	rm -r dist || true
	rm -r tiddlyweb_plugins.egg-info || true

test:
	py.test -svx test

dist: test
	python setup.py sdist

release: test
	python setup.py sdist upload
