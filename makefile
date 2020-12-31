.PHONY: init test test-hand-server test-hand-terminal

init:
	pip install -e .

test:
	python -m unittest discover -p '*_test.py'

test-hand-server:
	python tests/hand_run_tests/server.py
	
test-hand-terminal:
	python tests/hand_run_tests/terminal.py