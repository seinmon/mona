.PHONY: clean_pyc clean_build clean test_flake8 unittest

help:
	@echo "install:	install on system"
	@echo "run_tests:	run all unit/integration tests"
	@echo "test_flake8:	run flake8 on all files"
	@echo "clean_pyc: 	clean compiled python files"
	@echo "clean_build:	clean build files"
	@echo "clean:		clean build, and compiled python files"
	@echo "delete_venv: 	delete virtual environment"
	
install:
	python3 -m pip install .

run_tests: test_flake8 unittest

unittest:
	python3 -m unittest

test_flake8:
	flake8

delete_venv:
	rm -rf ./venv

clean_pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	
clean_build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean: clean_build clean_pyc
