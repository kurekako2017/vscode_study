# SAP Lab

Use this folder to practice and prototype SAP development in isolation from the rest of the repository. Keep SAP-specific tools, scripts, and sample projects here.

Suggested layout:
- `projects/` for small sample apps
- `docs/` for notes and guides
- `scripts/` for setup helpers

Keep dependencies contained (virtualenvs, local SDKs) to avoid affecting other projects in `/workspaces/study`.

Current contents:
- `projects/hello-sap`: starter stub for practice
- `scripts/bootstrap.sh`: optional env bootstrap (creates .venv and installs requirements if present)
- `docs/README.md`: quick notes and links area

Getting started:
1) Run `./scripts/bootstrap.sh` once (inside sap-lab) to prepare a Python venv for quick experiments.
2) Open `projects/hello-sap/main.py` and iterate.
3) Keep SAP-specific dependencies inside this folder to avoid leaking into other projects.
