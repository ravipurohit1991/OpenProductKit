# Quickstart

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (manages Python for you)
- [Node.js](https://nodejs.org) 20+ and [pnpm](https://pnpm.io) 9+

## Generate a project

Copier runs through `uv` — no global install needed:

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
cd my-product
```

Answer the prompts (project name, slug, CLI name, …) and you get a full, runnable project.

## Install and run

```bash
uv sync --dev                 # install the Python workspace (uv provisions Python)
uv run opk hello              # smoke test
uv run opk doctor             # check your toolchain
uv run opk dev                # API + a basic page on http://127.0.0.1:8000

# rich web UI, separate terminal:
pnpm install
pnpm -C apps/frontend dev     # http://127.0.0.1:5173
```

## What you get on day one

- A decoupled core with a small **Resource Vault** demo (projects, notes, tags, search)
- A FastAPI backend with **Alembic migrations** applied automatically
- A **Typer CLI** (`opk`) that runs the app, migrations, builds and plugins
- A React web UI over a **generated typed client**
- A **plugin system** with three example plugins and an admin UI
- **CI** (Linux + Windows), tests, ruff, and Docker Compose

See the [CLI reference](cli.md) for the full `opk` command surface.
