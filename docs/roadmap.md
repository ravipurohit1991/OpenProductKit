# Roadmap

!!! note "Versioning"
    The template and generated packages are at **0.1.0**. A `v1.0` will be
    tagged once the surface has proven stable in real projects — the milestones
    below track scope, not release versions.

## Milestone 1 — foundation (shipped)

- [x] **P1** Shippable skeleton — hexagonal core, FastAPI backend, Typer CLI, React web UI, CI, one-command dev
- [x] **P2** Resource Vault demo — projects, notes, tags, search through every adapter
- [x] **P3** Generated typed client — OpenAPI → `openapi-typescript` + `openapi-fetch` + TanStack Query
- [x] **P4** CLI as control plane — Alembic migrations, `db`/`build` groups, `info`/`fmt`/`version`
- [x] **P5** Extension manager — dev-time plugins, registry, license gating, admin UI, 3 examples
- [x] **P6** Rebranding & docs — Copier prompts + `copier update`, this docs site, comparisons

## Milestone 2 — licensing & desktop (shipped)

- [x] **Real licensing** — Ed25519 signed offline tokens, file + HTTP providers, vendor tooling (`opk license keygen|issue`), `require_plan` / `require_feature` route gates, frontend `useEntitlement()` / `LockedFeatureCard`, a License admin tab and a gated demo feature.
- [x] **Desktop** — pywebview shell calling the core **in-process** over a JS bridge (no HTTP sidecar, no port), per-user app-data storage, `opk build desktop` (PyInstaller); signing/notarization documented, not solved.

## Milestone 3 — agent-ready (shipped)

- [x] **Agent-ready rework path** — every demo line fenced with a grep-able `[demo]` marker, the [Make it yours](replace-the-demo.md) recipe, and `AGENTS.md` + `CLAUDE.md` shipped in every generated project, pre-rendered with the project's actual names so AI coding agents can replace the demo with the owner's product.

## Next

- **Runtime plugin loading** — installing and enabling plugins without a rebuild, with sandboxing/permissions; bundling plugins into frozen desktop builds.
- **Generated-client drift gate in CI** — deferred while `openapi-typescript` output can format-drift across minor versions.

## Explicitly out of scope for now

To stay opinionated and avoid a "supports everything, supports nothing" repo, the template does **not** ship Electron + PySide alongside Tauri, multiple databases, or multiple payment providers. Those arrive as optional recipes.
