[![Gitignore check](https://github.com/BogdanAIP/aip-runner/actions/workflows/ignore-check.yml/badge.svg)](https://github.com/BogdanAIP/aip-runner/actions/workflows/ignore-check.yml) 
# AIP Runner (CLI) — Agent Interaction Protocol

**AIP Runner** is a small CLI to execute **AIP (Agent Interaction Protocol)** manifests.  
Goal: make multi-agent LLM scenarios **portable, reproducible, and easy to share**.

> Status: **early draft / work in progress**. We’re building this together with the community.

## Why
- Today each framework (CrewAI, AutoGen, LangGraph, etc.) uses its own format.
- Reproducing or migrating scenarios is painful.
- AIP aims to be a **common manifest** (JSON) + a **simple runner** to try scenarios without rewriting code.

## What this CLI will do
- ✅ Validate AIP manifests against JSON Schema
- ✅ Run simple `sequential` workflows in **demo mode** (no LLM required)
- ⏳ Optional LLM mode (OpenAI and others) — planned
- ⏳ Converters (e.g., AIP → CrewAI/AutoGen) — planned
- ⏳ Tools (api/file/custom), logs, artifacts — planned

## Quick start (dev)
```bash
# 1) Create and activate a virtual env
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2) Install in editable mode (package config will be added soon)
pip install -e .

# 3) Validate and run (demo)
aip-runner validate examples/article_pipeline.aip.json
aip-runner run examples/article_pipeline.aip.json --no-llm


