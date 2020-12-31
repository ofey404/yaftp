.PHONY: init test test-hand-server test-hand-terminal test-hand-recevefile test-hand-sendfile

init:
	pip install -e .

test:
	python -m unittest discover -p '*_test.py'

test-hand-server:
	python tests/hand_run_tests/server.py
	
test-hand-terminal:
	python tests/hand_run_tests/terminal.py

test-hand-recevefile:
	python tests/hand_run_tests/recevefile.py

test-hand-sendfile:
	python tests/hand_run_tests/sendfile.py
