.PHONY: help install test unittest test_flake8 test_pylint \
		clean_pyc clean_build clean

help:
	@echo "make install:		install package"
	@echo "make unittest:		run all integration/unit tests"
	@echo "make test_flake8:	run flake8"
	@echo "make test_pylint:	run pylint"
	@echo "make clean_pyc: 	clean compiled python files"
	@echo "make clean_build:	clean build files"
	@echo "make clean:		clean build, and compiled python files"
	
install:
	@echo "Installing..."
	python3 -m pip install .

test: unittest test_flake8 test_pylint

unittest:
	@echo "Running integration/unittests..."
	python3 -m unittest

test_flake8:
	@echo "Running flake8..."
	flake8 --exclude venv

test_pylint:
	@echo "Running pylint..."
	pylint monalyza.py monalyza tests

clean_pyc:
	@echo "Deleting compiled python files..."
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	
clean_build:
	@echo "Deleting build files..."
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean: clean_build clean_pyc
