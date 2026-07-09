# OpenProductKit

A white-label **product-template** for shipping commercial apps across **web, CLI and desktop** from **one decoupled core** — with plugins, real licensing, a generated typed client, migrations, tests and CI built in.

This is not another FastAPI + React boilerplate. It is a *product-template operating system*: clone it, answer a few questions, and get a runnable, rebrandable, extensible app whose business logic lives in a single framework-free core and whose surfaces are thin adapters around it.

The repository is a [Copier](https://copier.readthedocs.io) template — you generate a fresh project from it and later pull upstream improvements with `copier update`.

## Why it's different

Most templates stop at "web" or "desktop". OpenProductKit's wedge is **breadth + productization + a genuinely decoupled core**:

- **One core, many adapters.** `packages/core` has zero third-party dependencies. FastAPI, Typer and React are delivery mechanisms, not where the logic lives.
- **A desktop app with no HTTP server.** The same web UI in a native window, dispatching to the core **in-process** — no sidecar, no port. Only possible because the core never assumed HTTP.
- **Real licensing.** Ed25519 signed offline tokens, file/HTTP providers, vendor tooling (`opk license keygen|issue`), route gates and a frontend lock card.
- **A real plugin system.** Python entry-point plugins can contribute backend routes, CLI commands, settings and admin UI — with license gating.
- **A generated typed client.** The web UI never hand-writes API types; they come from the backend's OpenAPI schema.
- **A CLI that is the control plane.** `opk` runs the app, migrations, builds, client generation, plugin management and licensing.
- **Designed to be reworked — by you or your AI agent.** The demo domain is fenced with grep-able `[demo]` markers, there is a step-by-step [replacement recipe](replace-the-demo.md), and every generated project ships an `AGENTS.md` (pre-rendered with *your* names) so Claude Code, Cursor or Codex can turn the template into your product.

## Where to next

- **[Quickstart](quickstart.md)** — generate and run a project in a minute.
- **[Make it yours](replace-the-demo.md)** — replace the demo domain with your product.
- **[Architecture](architecture.md)** — the one-core-many-adapters design.
- **[Plugins](plugins.md)** — the extension system.
- **[Licensing](licensing.md)** — sell licenses in three commands.
- **[Desktop](desktop.md)** — the in-process desktop shell.
- **[Rebranding & updates](rebranding.md)** — `copier copy` and `copier update`.
