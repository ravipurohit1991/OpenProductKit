# A product template your AI agent can finish — proven, commit by commit

*OpenProductKit is a white-label, full-stack template for shipping commercial apps across web, CLI and desktop from one decoupled core. To prove the pitch, an AI coding agent generated a project from it and reworked it into [**Tally**](https://github.com/ravipurohit1991/tally-time-tracker), a real freelancer time tracker — following nothing but the project's own `AGENTS.md`. This post walks through that build. The repo's git history is the tutorial.*

---

## The gap between a boilerplate and a product

Every developer has a folder full of app ideas. Most die in the same place: not at the idea — at the *product* part. The licensing. The desktop packaging. The typed API client that drifts out of sync. The migrations. The "how do I rebrand this template without a find-and-replace massacre" problem.

Boilerplates solve day one. Almost none solve week four, when you need to sell a license key, ship a Windows build, or pull upstream template fixes into a project you've heavily customized.

And in 2026 there's a question no classic boilerplate answers: **what does your AI coding agent do with it?** You're probably not hand-writing the CRUD anymore. You generate a project, open Claude Code or Cursor, and say "build my idea into this." Most templates give the agent nothing: no rules, no map, no recipe — so it guesses, and the architecture erodes from the first commit.

[**OpenProductKit**](https://github.com/ravipurohit1991/OpenProductKit) closes both gaps. Instead of just claiming that, let me show you.

## What you start from

OpenProductKit is a [Copier](https://copier.readthedocs.io) template. One command, a few questions (product name, package slug, CLI name), and you get a monorepo where everything carries your branding:

- **One decoupled core** — `packages/core` is pure Python: dataclasses, ports, services. Zero third-party dependencies. FastAPI, Typer and React are thin adapters around it.
- **A desktop app with no HTTP server** — the same React UI in a native window, calling the core *in-process* over a JS bridge. No sidecar, no port, nothing extra to sign.
- **Real licensing** — Ed25519-signed offline tokens, vendor tooling (`keygen`/`issue`), route gates, a lock-card UI component.
- **A plugin system** with license-gated plugins, a **generated typed client** (API drift = compile error), **Alembic migrations**, tests, ruff, CI, docs.
- **`AGENTS.md` + `CLAUDE.md`** in every generated project — rendered with *your* actual package and CLI names: the architecture rule, the layer map, the command palette, and the recipe for replacing the demo domain.

The template ships a deliberately boring demo domain (a notes-and-tags "Resource Vault") threaded through every layer, and **every demo line is fenced with a grep-able `[demo]` marker**. It exists to be deleted.

## The proof: building Tally

Tally is a local-first time tracker for freelancers: clients with hourly rates, one running timer at a time, weekly billable reports, CSV export as a paid feature. Web UI, CLI and desktop app — same core, same data.

Here's the thing: **an AI coding agent built it, and its only instructions about the codebase came from the generated `AGENTS.md`.** Every step below links to the actual commit.

### Step 0 — generate ([`dc9247c`](https://github.com/ravipurohit1991/tally-time-tracker/commit/dc9247c))

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit tally
# project_name=Tally, cli_name=tally, pkg_slug=tally
```

The first commit is the pristine template output — no hand edits. It already runs: 37 passing tests, a working web UI, CLI, desktop shell, licensing and plugins. That's the floor you start from, and it makes the rest of the history an honest diff: everything after this commit is the rework.

### Step 1 — the agent reads AGENTS.md

The generated `AGENTS.md` opens with the one rule:

> **Business logic never leaves `packages/core`.** FastAPI, Typer, React and pywebview are delivery mechanisms. If you are writing an `if` that encodes a product decision inside a route, a CLI command or a React component, stop and move it into a core service.

…then gives the agent a 12-step, inside-out recipe for adding a domain. The agent followed it literally, strangler-style: build Tally *next to* the demo, keep tests green, delete the demo last.

### Step 2 — the core domain ([`9062d14`](https://github.com/ravipurohit1991/tally-time-tracker/commit/9062d14))

`Client` and `TimeEntry` as frozen dataclasses; a `TimerService` that owns the product's central rule — **at most one entry runs at a time** — and a `ReportService` that turns completed entries into billable totals. 18 tests against in-memory fakes: no database, no HTTP, sub-second feedback. This is where the hexagonal split earns its keep — the most important logic in the product was written and tested before any framework got involved.

### Step 3 — persistence and API ([`fcc3cb6`](https://github.com/ravipurohit1991/tally-time-tracker/commit/fcc3cb6))

SQLModel rows, repositories implementing the core's ports, and a migration the agent didn't write by hand:

```bash
uv run tally db revision -m "add clients and time entries"   # Alembic autogen, reviewed
uv run tally db migrate
```

Thin routes over the services — and the paid feature is one line:

```python
@router.get("/export", dependencies=[Depends(require_plan("pro"))])
def export_report_csv(...) -> Response:   # CSV of billable hours
```

Tests cover the gate both ways: the dev license stub grants `pro` (200); monkeypatching a `free` plan returns a structured 403.

### Step 4 — the frontend ([`e12c6ec`](https://github.com/ravipurohit1991/tally-time-tracker/commit/e12c6ec))

```bash
uv run tally gen   # regenerate the typed client from the new OpenAPI schema
```

Every hook derives its types from the generated schema — `components["schemas"]["EntryOut"]` — so a backend change that misses a call site fails the TypeScript build. A `TimerView` with a live elapsed clock, a `ReportView` with the billable table and a **CSV export button that renders as a lock card on the free plan** (`useEntitlement("pro")` + `<LockedFeatureCard/>`).

### Step 5 — the CLI ([`042707d`](https://github.com/ravipurohit1991/tally-time-tracker/commit/042707d))

The CLI is a first-class adapter over the same core, so this is the actual product experience:

```text
$ tally client add "Acme Corp" --rate 100
$ tally start "acme corp" "api integration"
Timer started for Acme Corp.  api integration
$ tally status
Running: Acme Corp  0:03  api integration
$ tally stop
Stopped: Acme Corp  0:09
$ tally report --week
Client                      Hours     Rate     Amount
Acme Corp                    0.00   100.00       0.25
TOTAL                        0.00                0.25
```

One-running-timer is enforced here too — same `TimerService`, so the CLI and the web UI *can't* disagree.

### Step 6 — delete the demo ([`d776fec`](https://github.com/ravipurohit1991/tally-time-tracker/commit/d776fec))

```bash
grep -rn "\[demo\]" packages apps   # the complete checklist
```

Pure-demo files deleted, marked sections trimmed from the mixed files, the initial migration rewritten to Tally's schema (the recipe's pre-release path), the typed client regenerated. After the purge: **45 tests, zero `[demo]` markers, and not one line of dead scaffold.** Even the license-gated example plugin got reworked to summarize clients and entries instead of notes.

### The desktop app — zero changes

This deserves its own headline: **the desktop app required no work at all.** The pywebview shell dispatches any route over its in-process bridge, so `tally desktop` just… shows Tally, timer and lock cards included. `tally build desktop` packages it with PyInstaller. That's not luck — it's what "the core never assumed HTTP" buys you.

## What dogfooding caught

Full honesty: the first CI run of the generated project failed. The generated workflow file is copied verbatim (it can't be a Jinja template — GitHub Actions' own `${{ }}` syntax would collide), and its desktop smoke-test step shipped a literal, unrendered `{{ pkg_slug }}_desktop`. Tally was the first generated project to run its own CI, it caught the bug within 19 seconds, and the fix landed upstream the same day ([`8b3dea8`](https://github.com/ravipurohit1991/tally-time-tracker/commit/8b3dea8) in Tally). Building a real product from your own template is the only review that finds this class of bug — which is rather the point of this whole exercise.

## Do this with your idea

The workflow Tally validated is three steps:

```text
1. uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
2. Open it with your coding agent:
   "Read AGENTS.md, then replace the demo with <your idea>."
3. Review the diffs, commit layer by layer, ship.
```

The agent doesn't guess the architecture — it's told. It doesn't hunt for the demo — it greps the fence. It doesn't break the client — the recipe says when to regenerate. And you review commits shaped like the ones above, not a 5,000-line blob. Prefer to do it by hand? The same recipe is written for humans in the docs as [Make it yours](https://github.com/ravipurohit1991/OpenProductKit/blob/main/docs/replace-the-demo.md).

## What it isn't

OpenProductKit is deliberately lean and opinionated: one database (SQLite/SQLModel + Alembic), one frontend (React + Vite), one desktop approach (pywebview + PyInstaller). No Electron, no payment providers, no Kubernetes. Runtime plugin installation is on the [roadmap](https://github.com/ravipurohit1991/OpenProductKit/blob/main/docs/roadmap.md); code signing is documented, not solved. If you need a multi-tenant SaaS starter with Stripe, the [comparisons docs](https://github.com/ravipurohit1991/OpenProductKit/blob/main/docs/comparisons/vs-saas-boilerplates.md) will point you somewhere better.

But if your idea is *a product* — something a customer downloads or logs into, with a license key, plugins, and web + CLI + desktop surfaces — this is the fastest honest path from `copier copy` to shipped that I know how to build. And now there's a repo to prove it.

## Try it

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
```

- The template: [github.com/ravipurohit1991/OpenProductKit](https://github.com/ravipurohit1991/OpenProductKit)
- The proof: [github.com/ravipurohit1991/tally-time-tracker](https://github.com/ravipurohit1991/tally-time-tracker) — read it commit by commit
- MIT licensed, both of them

I'd love to hear what you build — and especially what your agent builds. Issues and PRs welcome.
