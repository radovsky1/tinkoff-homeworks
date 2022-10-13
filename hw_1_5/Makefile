PYTHONPATH = D:\projects\tinkoff-homeworks\venv\Scripts\python.exe -m

.PHONY: test
test: # Runs pytest
	$(PYTHONPATH) pytest test.py

.PHONY: lint
lint: # Lint code
	flake8 --exclude test.py .
	mypy .
	black --line-length 79 --skip-string-normalization --check .

.PHONY: check
check: lint test