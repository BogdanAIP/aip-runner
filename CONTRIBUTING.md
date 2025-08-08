# Contributing to AIP Runner

Thanks for taking the time to help! We welcome contributions of all kinds:
docs, examples, bug reports, feature ideas, and code.

## How to get involved
- **Questions / ideas** — open an Issue (English or Russian).
- **Small fixes** — you can edit files in the web UI and submit a Pull Request (PR).
- **New features** — open an Issue first to discuss scope and design.

## What you can work on
- **Docs & README** — improve clarity, fix typos, add examples.
- **Examples** — add new AIP manifests in `examples/`.
- **Schema** — refine `src/aip_runner/schema/aip.schema.json`.
- **CLI UX** — flags, messages, helpful errors.
- **CI** — improve workflows, add checks.

## Pull Request checklist
1. Keep PRs **small and focused**.
2. If changing behavior, update README/docs/examples accordingly.
3. Make sure **CI is green** (Actions → CI).
4. Use clear commit messages (e.g. `feat: ...`, `fix: ...`, `docs: ...`, `ci: ...`).

## How to submit a quick PR via GitHub web
1. Open the file you want to change → click **Edit** (✏️).  
2. Make your change → at the bottom choose **Create a new branch for this commit and start a pull request**.  
3. Describe what you changed and why → **Create Pull Request**.

## Local development (optional)
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
aip-runner validate examples/article_pipeline.aip.json
aip-runner run examples/article_pipeline.aip.json
