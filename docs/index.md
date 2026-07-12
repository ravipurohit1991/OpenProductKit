# OpenProductKit

A white-label **product-template** for shipping commercial apps across **web, CLI and desktop** from **one decoupled core** — with plugins, real licensing, a generated typed client, migrations, tests and CI built in.

This is not another FastAPI + React boilerplate. It is a *product-template operating system*: generate it, answer a few questions, and get a runnable, rebrandable, extensible app whose business logic lives in a single framework-free core and whose surfaces are thin adapters around it.

The repository is a [Copier](https://copier.readthedocs.io) template — you generate a fresh project from it and later pull upstream improvements with `copier update`.

## Quick usage

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
cd my-product
uv sync --dev
uv run opk doctor
uv run opk dev
```

See [Quickstart](quickstart.md) for the full first run, including the web UI and desktop app.

## What you get

| Area | Included |
| --- | --- |
| Core | Pure Python domain package with no framework dependencies |
| Backend | FastAPI, SQLModel persistence, Alembic migrations, OpenAPI |
| CLI | Typer command surface for dev, DB, docs, builds, plugins and licensing |
| Frontend | React + Vite over a generated typed client |
| Desktop | pywebview shell that calls the app in-process, with no HTTP sidecar |
| Commercial hooks | Signed offline licenses, HTTP license provider, plan and feature gates, [payment recipes](payments.md) |
| Extensions | Python entry-point plugins with routes, CLI commands, settings and admin UI |
| Hosted mode | Optional [user accounts](auth.md) (runtime switch) and [deploy recipes](deploy-recipes.md) for common hosts |
| Releases | Tag-triggered CI that builds desktop installers per OS onto GitHub Releases |
| Rework path | `[demo]` markers plus generated `AGENTS.md` and `CLAUDE.md` |

## Why it's different

Most templates stop at "web" or "desktop". OpenProductKit's wedge is **breadth + productization + a genuinely decoupled core**.

- **One core, many adapters.** `packages/core` has zero third-party dependencies. FastAPI, Typer and React are delivery mechanisms, not where the logic lives.
- **A desktop app with no HTTP server.** The same web UI runs in a native window, dispatching to the core **in-process**.
- **Real licensing.** Ed25519 signed offline tokens, file/HTTP providers, vendor tooling, route gates and a frontend lock card.
- **A real plugin system.** Python entry-point plugins can contribute backend routes, CLI commands, settings and admin UI.
- **A generated typed client.** The web UI never hand-writes API types; they come from the backend's OpenAPI schema.
- **A CLI that is the control plane.** `opk` runs the app, migrations, builds, client generation, docs, plugin management and licensing.
- **Designed to be reworked.** The demo domain is fenced with grep-able `[demo]` markers and every generated project ships agent instructions rendered with your actual names.

## Where to next

- **[Installation](installation.md)** — prerequisites and docs tooling.
- **[Generate a project](generating.md)** — Copier prompts, tags and generated layout.
- **[Make it yours](replace-the-demo.md)** — replace the demo domain with your product.
- **[Concepts](concepts.md)** — the mental model before you start editing.
- **[Template reference](template-reference.md)** — questions, generated packages and extension points.
