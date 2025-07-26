.PHONY: all format lint test tests test_watch integration_tests docker_tests help extended_tests

# Default target executed when no arguments are given to make.
all: help

# Define a variable for the test file path.
TEST_FILE ?= tests/unit_tests/

# Try uv first, fall back to python if uv is not available or fails
PYTHON_CMD := $(shell command -v uv >/dev/null 2>&1 && echo "uv run" || echo "python -m")

test:
	$(PYTHON_CMD) pytest $(TEST_FILE)

integration_tests:
	$(PYTHON_CMD) pytest tests/integration_tests 

test_watch:
	$(PYTHON_CMD) ptw --snapshot-update --now . -- -vv tests/unit_tests

test_profile:
	$(PYTHON_CMD) pytest -vv tests/unit_tests/ --profile-svg

extended_tests:
	$(PYTHON_CMD) pytest --only-extended $(TEST_FILE)


######################
# LINTING AND FORMATTING
######################

# Define a variable for Python and notebook files.
PYTHON_FILES=src/
MYPY_CACHE=.mypy_cache
lint format: PYTHON_FILES=.
lint_diff format_diff: PYTHON_FILES=$(shell git diff --name-only --diff-filter=d main | grep -E '\.py$$|\.ipynb$$')
lint_package: PYTHON_FILES=src
lint_tests: PYTHON_FILES=tests
lint_tests: MYPY_CACHE=.mypy_cache_test

lint lint_diff lint_package lint_tests:
	$(PYTHON_CMD) ruff check .
	[ "$(PYTHON_FILES)" = "" ] || $(PYTHON_CMD) ruff format $(PYTHON_FILES) --diff
	[ "$(PYTHON_FILES)" = "" ] || $(PYTHON_CMD) ruff check --select I $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || $(PYTHON_CMD) mypy --strict $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || mkdir -p $(MYPY_CACHE) && $(PYTHON_CMD) mypy --strict $(PYTHON_FILES) --cache-dir $(MYPY_CACHE)

format format_diff:
	$(PYTHON_CMD) ruff format $(PYTHON_FILES)
	$(PYTHON_CMD) ruff check --select I --fix $(PYTHON_FILES)

spell_check:
	$(PYTHON_CMD) codespell --toml pyproject.toml

spell_fix:
	$(PYTHON_CMD) codespell --toml pyproject.toml -w

######################
# HELP
######################

help:
	@echo '----'
	@echo 'Commands (优先使用 uv，自动回退到 python):'
	@echo 'format                       - run code formatters'
	@echo 'lint                         - run linters'
	@echo 'test                         - run unit tests'
	@echo 'tests                        - run unit tests'
	@echo 'test TEST_FILE=<test_file>   - run all tests in file'
	@echo 'test_watch                   - run unit tests in watch mode'
	@echo 'integration_tests            - run integration tests'

