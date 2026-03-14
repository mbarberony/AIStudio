.PHONY: help venv install lint format test test-unit test-integration check coverage run clean

PY := .venv/bin/python
PIP := .venv/bin/pip

help:
	@echo "Targets:"
	@echo "  make venv      - Create local virtualenv (.venv)"
	@echo "  make install   - Install runtime + dev deps"
	@echo "  make lint      - Run ruff checks"
	@echo "  make format    - Auto-fix formatting/imports where possible"
	@echo "  make test      - Run all pytest tests"
	@echo "  make test-unit - Run unit tests only (fast, no server needed)"
	@echo "  make test-integration - Run integration tests"
	@echo "  make check     - Lint + unit tests (mirrors CI)"
	@echo "  make coverage  - Run tests with coverage report"
	@echo "  make run       - Run FastAPI locally (uvicorn)"
	@echo "  make clean     - Remove venv + caches"

venv:
	python3 -m venv .venv

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install ruff pytest pre-commit

lint:
	$(PY) -m ruff check .

format:
	$(PY) -m ruff check . --fix

test:
	$(PY) -m pytest

test-unit:
	$(PY) -m pytest -m unit -v

test-integration:
	$(PY) -m pytest -m integration -v

check: lint test-unit
	@echo "All checks passed — same as CI"

coverage:
	$(PY) -m pytest -m unit --cov=src --cov-report=term-missing --cov-fail-under=20

run:
	$(PY) -m uvicorn local_llm_bot.app.api:app --reload --port 8000

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf **/__pycache__
	rm -rf .ruff_cache
