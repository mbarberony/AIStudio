# Contributing to AIStudio

Thank you for your interest in contributing to AIStudio.

This project is a local-first AI engineering sandbox focused on Retrieval-Augmented Generation (RAG), agentic workflows, observability, guardrails, and clean engineering practices such as testing, CI, and reproducibility.

Even when used as a solo project, this document defines a disciplined workflow and keeps the repository review-ready and maintainable.

---

## Repository Structure

At a high level, the repository is organized as follows:

- AIStudio/  
- local_llm_bot/        Core application (FastAPI, RAG, agents)  
- agentic_lab/          Experimental agent workflows  
- tests/                Unit and integration tests  
- infra/                CI, scripts, automation  
- .github/workflows/    GitHub Actions CI  
- pyproject.toml        Tooling configuration  
- Makefile              Common developer commands  
- README.md             Project overview  

---

## Development Environment

### Python Version

The project targets Python 3.13.

All development should be done inside a local virtual environment located at `.venv`.

### Create and Activate the Virtual Environment

Run the following from the repository root:

python3 -m venv .venv  
source .venv/bin/activate  

### Install Dependencies

Once the virtual environment is active:

make install  

This installs runtime dependencies as well as development tooling such as ruff, pytest, and pre-commit.

---

## Local Quality Gates (Required)

Before committing or pushing any changes, the following commands must pass locally:

```bash
make format  
make lint  
make test  
```

If these fail locally, CI will fail as well.

---

## Testing Strategy

### Test Location

All tests live under the top-level `tests/` directory.

### Test Categories

Tests are explicitly marked using pytest markers:

- unit  
  Fast tests with no external dependencies.

- integration  
  API-level or multi-component tests.  
  Future integration tests may involve LLMs, vector stores, or agents.

### Running Tests

Run all tests:

make test  

Run only unit tests:

pytest -m unit  

Run only integration tests:

pytest -m integration  

---

## Code Style and Linting

Linting is enforced using ruff.  
All configuration lives in `pyproject.toml`.

Formatting, import sorting, and modern Python typing conventions are handled automatically.

To auto-fix lint issues where possible:

make format  

---

## Git Workflow

### Branching Strategy

- Default branch: main
- Use feature branches for non-trivial changes

Create a feature branch:

git checkout -b feature/descriptive-name  

Examples of branch names:

feature/ollama-integration  
feature/vector-store  
feature/agent-tools  

---

### Staging Changes

Recommended defaults:

Stage all changes, including deletions and moves:

git add -A  

Stage selectively for clean commits:

git add -p  

---

### Commit Messages

Commit messages should:

- Start with a verb
- Describe what changed, not how
- Be concise and intentional

Examples:

Add ingestion pipeline skeleton  
Refactor RAG core for model abstraction  
Add integration tests for ask endpoint  

---

## Rebasing and History Hygiene

Before merging into main or opening a pull request, clean up history using interactive rebase:

git rebase -i origin/main  

Use this to:

- squash WIP commits
- clean up commit messages
- ensure a readable, intentional history

Do not rebase main after pushing.

---

## Continuous Integration (CI)

GitHub Actions runs automatically on every push and pull request.

CI enforces:

- linting
- unit tests
- integration tests (on main)

All changes must keep CI green.

---

## Pre-commit Hooks (Recommended)

This repository supports pre-commit hooks to catch issues before commits are created.

Install once:

pre-commit install  

To bypass hooks in exceptional cases:

git commit --no-verify  

Use sparingly.

---

## Scope and Philosophy

AIStudio is intentionally pragmatic, experimental, and architecture-focused.

Clarity, correctness, and reproducibility are preferred over premature abstraction.

When in doubt:

- favor explicit code
- add tests
- document intent

---

## Questions or Suggestions

If something feels unclear or awkward in the workflow, it probably is.  
Improvements to tooling, structure, or documentation are welcome.

---

Happy hacking.

