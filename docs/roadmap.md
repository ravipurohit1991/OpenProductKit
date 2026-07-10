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

## Milestone 4 — marketplace, desktop choice & one-command deploy (shipped)

- [x] **Marketplace** — a Marketplace tab and `/api/marketplace` that merge installed plugins with a vendor catalog (`marketplace/catalog.json`, or a hosted URL via `APP_MARKETPLACE_URL`); paid extensions unlock by pasting a signed license token, applied **without a restart** (plugin gates are checked per-request now). Ships a demo extension that lives in the repo but installs on demand. See [Marketplace](marketplace.md).
- [x] **Choose your desktop shell** — a Copier question picks **pywebview** (in-process, PyInstaller — the default), **Electron** or **Tauri** (both thin native windows over a *sidecar* backend that serves the API and the web UI on one localhost origin), or none. The CLI keeps a single surface: `opk desktop` and `opk build desktop` do the right thing per framework. See [Desktop](desktop.md).
- [x] **One-command deploy stack** — `opk stack up` runs the product in Docker: nginx serving the built UI and proxying `/api`, the backend, optional **PostgreSQL** (a Copier question), health checks and volumes wired. `opk stack share` adds a Cloudflare quick tunnel and prints a public `trycloudflare.com` URL for demos and device testing. See [Deployment](deployment.md).
- [x] **Backend serves the web build** — when `apps/frontend/dist` exists the FastAPI app serves it at `/`, so a single process (or single container) can deliver the whole product; this is what makes the sidecar desktop shells CORS-free.

## Next

- **Payments hook** — a documented webhook recipe (Stripe/Paddle → `license issue` → email token) so the marketplace unlock flow connects to real checkout.
- **Runtime plugin installation** — installing catalog plugins from the UI (not just `uv add`), with sandboxing/permissions; bundling plugins into frozen desktop builds (`--copy-metadata`).
- **Auth & multi-user** — optional user accounts for the hosted deployment story (the desktop/local story intentionally has none).
- **Desktop auto-update & release CI** — tag-triggered GitHub Actions that build installers per OS; auto-update via the shells' native mechanisms.
- **Generated-client drift gate in CI** — deferred while `openapi-typescript` output can format-drift across minor versions.

## Explicitly out of scope for now

To stay opinionated and avoid a "supports everything, supports nothing" repo, the template does **not** ship multiple databases beyond SQLite/PostgreSQL, multiple payment providers, or Kubernetes manifests. Those arrive as optional recipes.
