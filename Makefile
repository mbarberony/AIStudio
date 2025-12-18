.PHONY: help venv install lint format test run clean

PY := .venv/bin/python
PIP := .venv/bin/pip

help:
	@echo "Targets:"
	@echo "  make venv      - Create local virtualenv (.venv)"
	@echo "  make install   - Install runtime + dev deps"
	@echo "  make lint      - Run ruff checks"
	@echo "  make format    - Auto-fix formatting/imports where possible"
	@echo "  make test      - Run pytest"
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

run:
	$(PY) -m uvicorn local_llm_bot.app.api:app --reload --port 8000

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf **/__pycache__
	rm -rf .ruff_cache
