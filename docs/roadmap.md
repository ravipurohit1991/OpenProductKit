# Roadmap

## v1 (shipped)

- [x] **P1** Shippable skeleton — hexagonal core, FastAPI backend, Typer CLI, React web UI, CI, one-command dev
- [x] **P2** Resource Vault demo — projects, notes, tags, search through every adapter
- [x] **P3** Generated typed client — OpenAPI → `openapi-typescript` + `openapi-fetch` + TanStack Query
- [x] **P4** CLI as control plane — Alembic migrations, `db`/`build` groups, `info`/`fmt`/`version`
- [x] **P5** Extension manager — dev-time plugins, registry, license gating, admin UI, 3 examples
- [x] **P6** Rebranding & docs — Copier prompts + `copier update`, this docs site, comparisons

## v1.1 (planned)

- **Desktop** — Tauri shell calling the core **in-process** (no HTTP sidecar); signing/notarization documented.
- **Real licensing providers** — file / HTTP / signed-token, plus a `@requires_feature` decorator and frontend `useEntitlement()` / `LockedFeatureCard`.
- **Runtime plugin loading** — installing and enabling plugins without a rebuild, with sandboxing/permissions.

## Explicitly out of scope for v1

To stay opinionated and avoid a "supports everything, supports nothing" repo, v1 does **not** ship Electron + PySide alongside Tauri, multiple databases, or multiple payment providers. Those arrive as optional recipes.
