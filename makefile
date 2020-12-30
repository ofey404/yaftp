.PHONY: init test

init:
	pip install -e .

test:
	python -m unittest discover -p '*_test.py'