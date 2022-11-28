test:
	python -m unittest

.PHONY: lint
lint: # Lint code
	flake8 --exclude tests .
	mypy --exclude tests .
	black --line-length 79 --skip-string-normalization --check .

.PHONY: test