# Roadmap

## v1 (shipped)

- [x] **P1** Shippable skeleton — hexagonal core, FastAPI backend, Typer CLI, React web UI, CI, one-command dev
- [x] **P2** Resource Vault demo — projects, notes, tags, search through every adapter
- [x] **P3** Generated typed client — OpenAPI → `openapi-typescript` + `openapi-fetch` + TanStack Query
- [x] **P4** CLI as control plane — Alembic migrations, `db`/`build` groups, `info`/`fmt`/`version`
- [x] **P5** Extension manager — dev-time plugins, registry, license gating, admin UI, 3 examples
- [x] **P6** Rebranding & docs — Copier prompts + `copier update`, this docs site, comparisons

## v1.1 (shipped)

- [x] **Real licensing** — Ed25519 signed offline tokens, file + HTTP providers, vendor tooling (`opk license keygen|issue`), `require_plan` / `require_feature` route gates, frontend `useEntitlement()` / `LockedFeatureCard`, a License admin tab and a gated demo feature.
- [x] **Desktop** — pywebview shell calling the core **in-process** over a JS bridge (no HTTP sidecar, no port), per-user app-data storage, `opk build desktop` (PyInstaller); signing/notarization documented, not solved.

## Next

- **Runtime plugin loading** — installing and enabling plugins without a rebuild, with sandboxing/permissions; bundling plugins into frozen desktop builds.
- **Generated-client drift gate in CI** — deferred while `openapi-typescript` output can format-drift across minor versions.

## Explicitly out of scope for v1

To stay opinionated and avoid a "supports everything, supports nothing" repo, v1 does **not** ship Electron + PySide alongside Tauri, multiple databases, or multiple payment providers. Those arrive as optional recipes.
