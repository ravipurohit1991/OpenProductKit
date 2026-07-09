# A product template your AI agent can finish

*Introducing OpenProductKit — a white-label, full-stack template for shipping commercial apps across web, CLI and desktop from one decoupled core. Generate it, point your coding agent at it, ship your product.*

---

## The gap between a boilerplate and a product

Every developer has a folder full of app ideas. Most of them die in the same place: not at the idea, not even at the core feature — at the *product* part. The licensing. The desktop packaging. The plugin story. The typed API client that drifts out of sync. The migrations. The "how do I even rebrand this template without a find-and-replace massacre" problem.

Boilerplates solve day one. Almost none of them solve week four, when you need to sell a license key, ship a Windows build, or pull upstream template fixes into a project you've heavily customized.

And in 2026 there's a new question no classic boilerplate answers: **what does your AI coding agent do with it?** You're probably not going to hand-write the CRUD anymore. You'll generate a project, open Claude Code or Cursor, and say "build my idea into this." Most templates give the agent nothing to work with: no rules, no map, no recipe — so it guesses, and the architecture erodes from the first commit.

[**OpenProductKit**](https://github.com/ravipurohit1991/OpenProductKit) is my attempt to close both gaps.

## What you get on day one

OpenProductKit is a [Copier](https://copier.readthedocs.io) template. You run one command, answer a few questions (product name, package slug, CLI name), and get a monorepo where *everything* — Python packages, imports, the CLI entrypoint, the desktop window title, Docker image names — carries your branding:

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
cd my-product && uv sync --dev
uv run mycli dev        # working API
uv run mycli desktop    # the same app in a native window
```

Inside:

- **One decoupled core.** `packages/core` is pure Python — dataclasses, ports (Protocols), services. Zero third-party dependencies. FastAPI, Typer and React are thin adapters around it.
- **A desktop app with no HTTP server.** The same React UI in a pywebview window, dispatching API calls to the core *in-process* over a JS bridge. No sidecar process, no port, nothing extra to sign. This is only possible because the core never assumed HTTP existed.
- **Real licensing.** Ed25519-signed offline license tokens, vendor tooling (`mycli license keygen|issue`), route gates (`require_plan("pro")`), and a lock-card UI component. You can sell a license key on day one.
- **A plugin system.** Python entry-point plugins that contribute backend routes, CLI commands and admin UI — with license gating, so plugins can be paid features.
- **A generated typed client.** The frontend never hand-writes API types; they're generated from the OpenAPI schema. Change an endpoint and forget a call site, and the TypeScript build fails. Drift is a compile error.
- **The boring essentials.** Alembic migrations (applied automatically in dev), pytest across the workspace, ruff, CI on Linux + Windows, a CLI that doubles as the task runner, and an MkDocs site.

And because the repo *is* a Copier template, `copier update` later pulls upstream improvements into your generated project as a reviewable three-way merge. Rebranding isn't a script that mangles your files — it's the generation step itself.

## The demo is designed to be deleted

The template ships with a deliberately boring demo domain — a "Resource Vault" of projects, notes and tags — threaded through every layer: domain model → port → service → SQL repository → migration → API route → generated client → React view → CLI command. It's not the product; it's the worked example that shows you how one domain flows through the whole system.

Here's the part I think most templates get wrong: they either ship *no* example (an empty skeleton teaches nothing) or an example so entangled you can't tell scaffold from framework.

In OpenProductKit, **every demo line is fenced**:

```bash
grep -rn "\[demo\]" packages apps
```

That one command prints the complete inventory of what to replace. Everything unmarked — licensing, plugins, desktop shell, migrations tooling, the client pipeline — is framework and works unchanged with *any* domain. The docs include a [step-by-step recipe](https://github.com/ravipurohit1991/OpenProductKit/blob/main/docs/replace-the-demo.md) for swapping the demo for your own entities, strangler-style: build yours next to it, keep the tests green, delete the demo last.

## The part built for your AI agent

Every generated project ships an **`AGENTS.md`** (plus a `CLAUDE.md` pointer) — and because it's rendered by the template engine, it's written in terms of *your* project: your actual package names, your CLI command, your paths. Not generic advice. It contains:

- **The one rule** — business logic never leaves the core. Adapters stay thin.
- **The layer map** — what each package is, what's framework, what's demo.
- **The command palette** — how to run, test, lint, migrate, regenerate the client.
- **The recipe** — the exact 12-step, inside-out order for adding a domain entity end-to-end and deleting the demo.
- **The gotchas** — "your frontend type error is a stale generated client, run `mycli gen`", and friends.

So the intended workflow for a new product is genuinely this:

```text
1. uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
2. Open the project with your coding agent, and say:
   "Read AGENTS.md, then replace the demo domain with <your idea>."
3. Review the diff. Ship.
```

The agent doesn't guess the architecture — it's told. It doesn't hunt for the demo — it greps the fence. It doesn't break the client — the recipe says when to regenerate. The hexagonal split that makes the codebase pleasant for humans turns out to be exactly what makes it *legible to a machine*: small layers, one rule, a repeatable pattern per entity.

## Why hexagonal, in one paragraph

"Ports and adapters" sounds like architecture-astronaut talk until you see the payoff: the desktop app. Because the core never imported FastAPI, the desktop shell can call it in the same process — no bundled server, no port conflicts, no second binary to sign. The same discipline is why the CLI is a first-class adapter, why core tests run with zero infrastructure, and why your agent can add an entity by following a template instead of spelunking. The constraint is the feature.

## What it isn't

Honesty section. OpenProductKit is deliberately opinionated and deliberately lean: one database (SQLite/SQLModel + Alembic), one frontend (React + Vite), one desktop approach (pywebview + PyInstaller). No Electron, no multiple payment providers, no Kubernetes charts. Runtime plugin installation (add plugins without a rebuild) is on the [roadmap](https://github.com/ravipurohit1991/OpenProductKit/blob/main/docs/roadmap.md); code signing is documented but not solved for you. If you need a multi-tenant SaaS starter with Stripe wired in, the [comparisons docs](https://github.com/ravipurohit1991/OpenProductKit/blob/main/docs/comparisons/vs-saas-boilerplates.md) point you at better fits.

But if your idea is *a product* — something a customer downloads or logs into, with a license key, plugins, and a web + desktop + CLI surface — this is the fastest honest path from `copier copy` to shipped that I know how to build.

## Try it

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
```

- Repo: [github.com/ravipurohit1991/OpenProductKit](https://github.com/ravipurohit1991/OpenProductKit)
- Start here: the Quickstart, then "Make it yours" in the docs
- MIT licensed

I'd love to hear what you build — and especially what your agent builds. Issues and PRs welcome.
