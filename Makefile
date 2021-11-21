.PHONY: clean_pyc clean_build clean

help:
	@echo "venv_install:	install in a virtual environment"
	@echo "install:	install on system"
	@echo "run_tests:	run all unit/integration tests"
	@echo "clean_pyc: 	clean compiled python files"
	@echo "clean_build:	clean build files"
	@echo "clean:		clean build, and compiled python files"
	@echo "delete_venv: 	delete virtual environment"
	
venv_install:
	(\
		python3 -m venv ./venv; \
		source venv/bin/activate; \
		python3 -m pip install .)

install:
	python3 -m pip install .

run_tests:
	python3 -m unittest

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
