#!/usr/bin/env bash
set -euo pipefail

echo "=== AIStudio bootstrap starting ==="

# Helper: create directory if it doesn't exist
ensure_dir() {
  if [ ! -d "$1" ]; then
    echo "Creating directory: $1"
    mkdir -p "$1"
  else
    echo "Directory already exists: $1"
  fi
}

########################################
# 1. Core directory structure
########################################

# Local LLM bot (RAG)
ensure_dir "local_llm_bot/app"
ensure_dir "local_llm_bot/ingest"
ensure_dir "local_llm_bot/data"
ensure_dir "local_llm_bot/logs"
ensure_dir "local_llm_bot/tests"

# Agentic lab
ensure_dir "agentic_lab/tools"
ensure_dir "agentic_lab/workflows"
ensure_dir "agentic_lab/logs"
ensure_dir "agentic_lab/tests"

# Infra
ensure_dir "infra/cicd"
ensure_dir "infra/docker"
ensure_dir "infra/scripts"
ensure_dir "infra/configs"

# Cloud (Epic 2)
ensure_dir "cloud/aws"
ensure_dir "cloud/azure"
ensure_dir "cloud/docs"

# Docs
ensure_dir "docs"

########################################
# 2. Python package markers
########################################

for pkg in \
  "local_llm_bot" \
  "local_llm_bot/app" \
  "local_llm_bot/ingest" \
  "agentic_lab" \
  "agentic_lab/tools" \
  "agentic_lab/workflows"
do
  if [ ! -f "$pkg/__init__.py" ]; then
    echo "Creating __init__.py in: $pkg"
    touch "$pkg/__init__.py"
  fi
done

########################################
# 3. Documentation placeholders
########################################

if [ ! -f "docs/architecture_overview.md" ]; then
  cat > docs/architecture_overview.md << 'EOF2'
# Architecture Overview

This document describes the high-level architecture of AIStudio:
- Local LLM bot (RAG)
- Agentic lab
- Developer workflow (PyCharm, vibe coding)
- CI/CD and infra
- Cloud extension (Epic 2: AWS, Azure)
EOF2
  echo "Created docs/architecture_overview.md"
else
  echo "docs/architecture_overview.md already exists, skipping."
fi

if [ ! -f "docs/learning_log.md" ]; then
  cat > docs/learning_log.md << 'EOF2'
# Learning Log

Free-form notes on:
- Concepts explored
- Design decisions
- Things to revisit
EOF2
  echo "Created docs/learning_log.md"
else
  echo "docs/learning_log.md already exists, skipping."
fi

if [ ! -f "docs/rag_bot_v1.md" ]; then
  cat > docs/rag_bot_v1.md << 'EOF2'
# RAG Bot v1

Notes and design details for the initial local knowledge engine:
- Ingestion pipeline
- Vector store choice and configuration
- Prompting strategy
- Limitations and next steps
EOF2
  echo "Created docs/rag_bot_v1.md"
else
  echo "docs/rag_bot_v1.md already exists, skipping."
fi

if [ ! -f "docs/agentic_lab_v1.md" ]; then
  cat > docs/agentic_lab_v1.md << 'EOF2'
# Agentic Lab v1

Notes and design details for the initial agentic workflows:
- Framework selection
- Tools exposed to agents
- Example workflows
- Guardrails and observability
EOF2
  echo "Created docs/agentic_lab_v1.md"
else
  echo "docs/agentic_lab_v1.md already exists, skipping."
fi

########################################
# 4. .gitignore (only if it doesn't exist)
########################################

if [ ! -f ".gitignore" ]; then
  echo "Creating .gitignore"
  cat > .gitignore << 'EOF2'
###############################################################################
# AIStudio — Project-Specific .gitignore
# Focused on Python, PyCharm, local LLM development, RAG pipelines,
# agentic workflows, and privacy-preserving experimentation.
###############################################################################

###############
# OS Artifacts
###############
.DS_Store
Thumbs.db

###########################
# PyCharm / JetBrains IDE
###########################
.idea/

###################
# Python Artifacts
###################
__pycache__/
*.py[cod]
*.pyd
*.so
*.dylib
*.egg-info/
.eggs/
build/
dist/
pip-wheel-metadata/
*.egg
*.whl

######################
# Virtual Environments
######################
venv/
.venv/
env/
.python-version

######################
# Package / Tool Cache
######################
.mypy_cache/
.pytest_cache/
.tox/
.coverage
coverage.xml
htmlcov/

###################
# Jupyter
###################
.ipynb_checkpoints/

###################################
# Local Data, Embeddings, & Indexes
###################################
data/raw/
data/raw_samples/
data/private/
data/tmp/

local_llm_bot/data/chroma_db/
local_llm_bot/data/lancedb/
local_llm_bot/data/vector_store/

#############################
# Logs & Observability Output
#############################
local_llm_bot/logs/
agentic_lab/logs/
logs/
*.log
*.tmp

############################
# Secrets / Config Overrides
############################
.env
.env.*
*.env
*.secret
secrets.json
config.local.*
credentials.*

###################################
# Docker, Containers & Build Output
###################################
docker/*-cache/
*.pid
EOF2
else
  echo ".gitignore already exists, skipping."
fi

########################################
# 5. requirements.txt (placeholder)
########################################

if [ ! -f "requirements.txt" ]; then
  echo "Creating requirements.txt (placeholder)"
  cat > requirements.txt << 'EOF2'
# Core web & API
fastapi
uvicorn[standard]

# RAG / LLM tools
chromadb
sentence-transformers
langchain

# Utilities
python-dotenv

# (Adjust and pin versions as the project evolves)
EOF2
else
  echo "requirements.txt already exists, skipping."
fi

echo "=== AIStudio bootstrap complete ==="
