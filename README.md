# OpenProductKit

> A white-label **product-template** for shipping commercial apps across web, CLI (and soon desktop) from **one decoupled core** — with plugins, licensing hooks, generated clients, docs, tests and CI built in.

This is a *product-template operating system*: clone it, answer a few questions, and get a runnable, rebrandable, extensible app whose business logic lives in a single framework-free core and whose web/CLI/desktop surfaces are thin adapters around it.

The repository is a [**Copier**](https://copier.readthedocs.io) template. You generate a fresh project from it, and later pull upstream template improvements with `copier update`.

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
apps/backend         FastAPI HTTP adapter. Owns SQLModel persistence (implements the core ports).
apps/cli             Typer CLI + task runner. Another adapter around the same core.
apps/frontend        React + Vite web UI. Talks to the backend over HTTP.
```

The rule that keeps this template straight forward: **business logic never leaks into FastAPI, Typer, or React.** Those are delivery mechanisms. Swap any of them without touching the core.

## What's here today (v1 — in progress)

- [x] **P1** Shippable skeleton: hexagonal `core`, FastAPI backend, Typer CLI, React web UI, CI, one-command dev
- [x] **P2** Minimal demo product (Resource Vault: projects, notes, tags, search) — through core, backend, CLI and web
- [ ] **P3** Generated typed clients (OpenAPI → TS + TanStack Query)
- [ ] **P4** CLI as framework / task runner
- [ ] **P5** Extension manager (dev-time Python plugins)
- [ ] **P6** Rebranding via Copier + docs site

Deferred to v1.1: desktop (Tauri, in-process core), real licensing providers, runtime plugin loading.

## License

MIT — see [LICENSE](LICENSE).
