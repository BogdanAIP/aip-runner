[![Gitignore check](https://github.com/BogdanAIP/aip-runner/actions/workflows/ignore-check.yml/badge.svg)](https://github.com/BogdanAIP/aip-runner/actions/workflows/ignore-check.yml) 
# AIP Runner — Agent Interaction Protocol (CLI)

A tiny command-line runtime for **AIP (Agent Interaction Protocol)** manifests.  
Goal: make multi-agent LLM scenarios **portable, reproducible, and easy to share**.

> Status: **early draft / work in progress** — contributions welcome!

---

## What is this?

- **AIP manifest (JSON):** describes a scenario — **project**, **agents**, **workflow** steps, and **artifacts**.
- **AIP Runner (CLI):** validates a manifest and can execute simple `sequential` workflows in **demo mode** (no LLM required).
- Designed to be **framework-agnostic** and **easy to migrate** to other stacks later.

Planned features:
- Optional LLM mode (OpenAI and others)
- Converters (e.g. AIP → CrewAI/AutoGen)
- Tools (api/file/custom) and artifacts handling
- **MCP** (Model Context Protocol) integration as a standard tool provider

---

## Quick start

### Requirements
- Python **3.8+**
- Git (optional)

### Clone and run
```bash
git clone https://github.com/<your-username>/aip-runner.git
cd aip-runner

python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -e .              # installs the console script `aip-runner`
