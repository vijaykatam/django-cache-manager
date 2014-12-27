.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "dev-requirements - install development dependencies to current environment"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - run tests and generate cobertura coverage reports"
	@echo "dist - package"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	python setup.py flake8

dev-requirements:
	pip install -r requirements-dev.txt	

test: dev-requirements
	DJANGO_SETTINGS_MODULE=tests.settings python setup.py nosetests --with-django-nose $(TESTARGS)

test-all:
	tox

shell: dev-requirements
	pip install -e .
	python tests/shell.py

coverage: dev-requirements
	DJANGO_SETTINGS_MODULE=tests.settings python setup.py nosetests --with-django-nose --with-xcoverage --cover-package=django_cache_manager --cover-inclusive --cover-erase

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
