# OpenProductKit

[![CI](https://github.com/ravipurohit1991/OpenProductKit/actions/workflows/ci.yml/badge.svg)](https://github.com/ravipurohit1991/OpenProductKit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![Template: Copier](https://img.shields.io/badge/template-copier-1e90ff.svg)](https://copier.readthedocs.io)

> A white-label **product-template** for shipping commercial apps across web, CLI and desktop from **one decoupled core** — with plugins, real licensing, generated clients, docs, tests and CI built in.

This is a *product-template operating system*: clone it, answer a few questions, and get a runnable, rebrandable, extensible app whose business logic lives in a single framework-free core and whose web/CLI/desktop surfaces are thin adapters around it.

The repository is a [**Copier**](https://copier.readthedocs.io) template. You generate a fresh project from it, and later pull upstream template improvements with `copier update`.

**The intended journey:**

1. **Generate** — `copier copy`, answer a few questions; every package, import and window title carries *your* name.
2. **Run** — a working product on day one: web, CLI and desktop over one core, with licensing, plugins, migrations, typed client, tests and CI.
3. **Rework** — replace the small fenced demo domain with your product, layer by layer, following [the recipe](docs/replace-the-demo.md). Or don't do it by hand: every generated project ships an **`AGENTS.md`** (pre-rendered with your project's names) so you can point Claude Code, Cursor or any coding agent at it and say *"replace the demo with \<my idea\>"*.
4. **Ship** — the packaging, licensing and update story is already built.

**Proof it works:** [Tally](https://github.com/ravipurohit1991/tally-time-tracker), a freelancer time tracker, was generated from this template and reworked by an AI agent following `AGENTS.md` — the first commit is the pristine template output, every commit after is one layer of the rework. [The blog post](docs/blog/introducing-openproductkit.md) walks through it.

📖 **Docs:** [architecture](docs/architecture.md) · [make it yours](docs/replace-the-demo.md) · [plugins](docs/plugins.md) · [licensing](docs/licensing.md) · [desktop](docs/desktop.md) · [rebranding & updates](docs/rebranding.md) · [comparisons](docs/comparisons/vs-fastapi-full-stack-template.md) — the full site is built with MkDocs Material (`uvx --with-requirements requirements-docs.txt mkdocs serve`).

---

## Quickstart

```bash
# 1. Generate a project (Copier is run through uv — no global install needed)
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
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

# 5. Or as a desktop app (same core, no HTTP server)
uv run opk build web && uv run opk desktop

# 6. Make it your product: the demo is fenced — this lists everything to replace
grep -rn "\[demo\]" packages apps
#    …or hand the job to your AI agent: it reads AGENTS.md and knows the recipe.
```

## Architecture — one core, many adapters

```
packages/core        Pure Python. Domain models + Repository "ports". No FastAPI, no DB, no HTTP.
packages/plugin-api  Extension SDK: the Plugin contract + entry-point registry. No runtime deps.
packages/licensing   Entitlement: dev stub, Ed25519 signed offline tokens, file/HTTP providers.
apps/backend         FastAPI HTTP adapter. Owns SQLModel persistence (implements the core ports).
apps/cli             Typer CLI + task runner. Another adapter around the same core.
apps/frontend        React + Vite web UI. Talks to the backend over HTTP — or the desktop bridge.
apps/desktop         pywebview shell: the same UI + core in ONE process. No sidecar, no port.
extensions/          Example plugins: basic (route), cli (command), paid (license-gated).
```

The rule that keeps this template straight forward: **business logic never leaks into FastAPI, Typer, or React.** Those are delivery mechanisms. Swap any of them without touching the core.

## What's here today

> **Version note:** the template and every generated package are at **0.1.0**. A `v1.0` will be tagged only once the surface has proven stable in real projects — the milestones below track scope, not release versions.

**Milestone 1 — foundation (shipped)**

- [x] **P1** Shippable skeleton: hexagonal `core`, FastAPI backend, Typer CLI, React web UI, CI, one-command dev
- [x] **P2** Minimal demo product (Resource Vault: projects, notes, tags, search) — through core, backend, CLI and web
- [x] **P3** Generated typed client (OpenAPI → openapi-typescript + openapi-fetch + TanStack Query hooks)
- [x] **P4** CLI as framework / control plane (Alembic migrations, `db`/`build` groups, `info`/`fmt`/`version`)
- [x] **P5** Extension manager (dev-time Python entry-point plugins: SDK, registry, license gating, backend + CLI + admin UI, 3 example plugins)
- [x] **P6** Rebranding via Copier (`copier update`) + MkDocs docs site, comparisons, SECURITY/CONTRIBUTING

**Milestone 2 — licensing & desktop (shipped)**

- [x] **P7** Real licensing: Ed25519 signed offline tokens, file/HTTP providers, vendor tooling (`opk license keygen|issue`), route gates (`require_plan`/`require_feature`), `useEntitlement()` + `LockedFeatureCard`, License admin tab, gated demo feature
- [x] **P8** Desktop: pywebview shell calling the core **in-process** over a JS bridge (no HTTP sidecar, no port), per-user app data, `opk build desktop` (PyInstaller onedir). Code signing: documented, not solved

**Milestone 3 — agent-ready (shipped)**

- [x] **P9** Agent-ready rework path: every demo line fenced with a grep-able `[demo]` marker, a [replace-the-demo recipe](docs/replace-the-demo.md), and an `AGENTS.md` + `CLAUDE.md` in every generated project — pre-rendered with your project's names — so AI coding agents can do the rework

Next: runtime plugin loading (install/enable without rebuild, sandboxing) — see the [roadmap](docs/roadmap.md).

## License

MIT — see [LICENSE](LICENSE).
