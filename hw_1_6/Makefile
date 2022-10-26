test:
	python3 -m unittest

lint:
	flake8 --exclude tests .
	mypy --exclude tests .
	black --line-length 79 --skip-string-normalization --check .

.PHONY: test lint