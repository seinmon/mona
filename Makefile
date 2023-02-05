TEST ?= tests/*
SRC ?= *.py mona/*

.PHONY: install
install:
	@echo "Installing..."
	python3 -m pip install .

.PHONY: help
help:
	@echo "make install:		install package"
	@echo "make unittest:		run all integration/unit tests"
	@echo "make test_flake8:	run flake8"
	@echo "make test_pylint:	run pylint"
	@echo "make clean_pyc: 	clean compiled python files"
	@echo "make clean_build:	clean build files"
	@echo "make clean:		clean build, and compiled python files"

.PHONY: test
test: unittest lint

.PHONY: unittest
unittest:
	@echo "Running integration/unittests..."
	-python3 -m unittest $(TEST)

.PHONY: lint
lint: test_flake8 test_pylint

.PHONY: test_flake8
test_flake8:
	@echo "Running flake8..."
	-flake8 --exclude venv $(SRC) $(TEST)

.PHONY: test_pylint
test_pylint:
	@echo "Running pylint..."
	-pylint mona.py $(SRC) $(TEST)

.PHONY: coverage
coverage:
	@echo "Running integration/unittests and calculating code coverage..."
	coverage run -m unittest $(TEST)
	coverage report

.PHONY: clean_pyc
clean_pyc:
	@echo "Deleting compiled python files..."
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

.PHONY: clean_build
clean_build:
	@echo "Deleting build files..."
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean
clean: clean_build clean_pyc

.PHONY: todo
todo:
	@grep --color -Ion '\(TODO\|XXX\).*' *.py -r src
