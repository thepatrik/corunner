.DEFAULT_GOAL := install

.PHONY: install
install: install-poetry
	poetry env use python3.8
	poetry install

.PHONY: install-ci
install-ci: install-pip-poetry
	poetry config virtualenvs.create false
	poetry install

.PHONY: install-poetry
install-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

.PHONY: install-pip-poetry
install-pip-poetry:
	pip install poetry

.PHONY: fmt
fmt:
	poetry run importanize corunner tests
	poetry run autopep8 --in-place --aggressive --aggressive --recursive corunner tests

.PHONY: lint
lint:
	poetry run mypy corunner tests

.PHONY: test
test:
	poetry run pytest -s
