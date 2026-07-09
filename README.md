# OpenProductKit

[![CI](https://github.com/ravipurohit1991/OpenProductKit/actions/workflows/ci.yml/badge.svg)](https://github.com/ravipurohit1991/OpenProductKit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![Template: Copier](https://img.shields.io/badge/template-copier-1e90ff.svg)](https://copier.readthedocs.io)

> A white-label **product-template** for shipping commercial apps across web, CLI (and soon desktop) from **one decoupled core** — with plugins, licensing hooks, generated clients, docs, tests and CI built in.

This is a *product-template operating system*: clone it, answer a few questions, and get a runnable, rebrandable, extensible app whose business logic lives in a single framework-free core and whose web/CLI/desktop surfaces are thin adapters around it.

The repository is a [**Copier**](https://copier.readthedocs.io) template. You generate a fresh project from it, and later pull upstream template improvements with `copier update`.

📖 **Docs:** [architecture](docs/architecture.md) · [plugins](docs/plugins.md) · [licensing](docs/licensing.md) · [rebranding & updates](docs/rebranding.md) · [comparisons](docs/comparisons/vs-fastapi-full-stack-template.md) — the full site is built with MkDocs Material (`uvx --with-requirements requirements-docs.txt mkdocs serve`).

---

## Quickstart

```bash
# 1. Generate a project (Copier is run through uv — no global install needed)
uvx copier copy gh:youruser/openproductkit my-product
#   or, from a local clone:
uvx copier copy . ../my-product

cd my-product

# 2. Install the Python workspace (uv provisions the right Python for you)
uv sync --dev

# 3. Smoke test
uv run opk hello
uv run opk doctor

# 4. Run it
uv run opk dev                      # API + web page on http://127.0.0.1:8000
pnpm install && pnpm -C apps/frontend dev   # rich web UI on http://127.0.0.1:5173
```

## Architecture — one core, many adapters

```
packages/core        Pure Python. Domain models + Repository "ports". No FastAPI, no DB, no HTTP.
packages/plugin-api  Extension SDK: the Plugin contract + entry-point registry. No runtime deps.
packages/licensing   Entitlement abstraction (dev stub today; real providers later).
apps/backend         FastAPI HTTP adapter. Owns SQLModel persistence (implements the core ports).
apps/cli             Typer CLI + task runner. Another adapter around the same core.
apps/frontend        React + Vite web UI. Talks to the backend over HTTP.
extensions/          Example plugins: basic (route), cli (command), paid (license-gated).
```

The rule that keeps this template straight forward: **business logic never leaks into FastAPI, Typer, or React.** Those are delivery mechanisms. Swap any of them without touching the core.

## What's here today (v1 — in progress)

- [x] **P1** Shippable skeleton: hexagonal `core`, FastAPI backend, Typer CLI, React web UI, CI, one-command dev
- [x] **P2** Minimal demo product (Resource Vault: projects, notes, tags, search) — through core, backend, CLI and web
- [x] **P3** Generated typed client (OpenAPI → openapi-typescript + openapi-fetch + TanStack Query hooks)
- [x] **P4** CLI as framework / control plane (Alembic migrations, `db`/`build` groups, `info`/`fmt`/`version`)
- [x] **P5** Extension manager (dev-time Python entry-point plugins: SDK, registry, license gating, backend + CLI + admin UI, 3 example plugins)
- [x] **P6** Rebranding via Copier (`copier update`) + MkDocs docs site, comparisons, SECURITY/CONTRIBUTING

Deferred to v1.1: desktop (Tauri, in-process core), real licensing providers, runtime plugin loading.

## License

MIT — see [LICENSE](LICENSE).
