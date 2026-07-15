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

## Milestone 5 — sell it, host it, ship it (shipped)

- [x] **Payments recipes** — [Payments](payments.md): a complete Stripe webhook → `license issue` → email recipe, a Lemon Squeezy adapter that maps their native license API onto `HttpLicenseProvider` (no license server at all), and the Paddle variant. The app side was already done; now the checkout side is copy-paste.
- [x] **Auth & multi-user** — user accounts as a **runtime switch** (`APP_AUTH_ENABLED`), not a Copier variant: scrypt passwords, hashed bearer sessions, first-run admin setup, a Users admin tab, `user add|list|passwd|remove` CLI, and admin-gated operator actions. The desktop/local story stays accountless. See [Auth](auth.md).
- [x] **Runtime plugin installation** — catalog items with a `package` gain an Install button: `POST /api/marketplace/install` pip-installs, re-scans entry points and mounts routes **live**. Fenced honestly: opt-in (`APP_MARKETPLACE_ALLOW_INSTALL`), admin-only under auth, refused in frozen builds. Frozen desktop builds now bundle installed plugins (`--copy-metadata` + hidden imports) instead of dropping them.
- [x] **Desktop release CI & auto-update story** — a generated `release.yml`: tag push → installers for Windows/macOS/Linux attached to a GitHub Release (dry-run via manual trigger). Electron ships its updater feed (`latest*.yml` + GitHub publish config); Tauri and pywebview update paths are documented with exact steps. See [Releases](releases.md).
- [x] **Generated-client drift gate** — `opk gen --check` in both the generated project's CI and this repo's CI. Unblocked by pinning `openapi-typescript` exactly — the format-drift concern was real, so the pin is the fix, not hope.
- [x] **Deploy recipes** — [copy-paste starts](deploy-recipes.md) for Fly.io, Railway, Cloud Run (+ optional Firebase Hosting front), static hosts with `/api` proxying, VPS + Caddy, and named Cloudflare tunnels — recipes in docs, zero new host lock-in in the template.

## Milestone 6 — adopt existing code (shipped)

- [x] **Bring your own code** — `APP_PRODUCT_ROUTERS` imports existing FastAPI routers/apps or thin factories around an existing core. Routes join OpenAPI, generated clients, auth, desktop and deployment; `opk product check` validates the contract. See [Bring your own core or backend](bring-your-own-code.md).

## Next

- **Plugin permissions & sandboxing** — enforce the manifest's declared `permissions` (today they are informational): restrict network/filesystem where feasible, and explore process isolation for untrusted extensions.
- **Signed catalogs & pinned packages** — sign `catalog.json` with the vendor key and hash-pin `package` requirements, so a hosted catalog compromise cannot push arbitrary code to installs.
- **SSO / OIDC** — enterprise login for the hosted story; `enforce_auth` is the seam it plugs into.
- **Per-user data ownership recipe** — auth provides identity; a documented pattern (and demo) for scoping domain rows to users/teams turns it into multi-tenancy.
- **Turnkey update check for pywebview** — promote the documented check-and-point snippet into a shipped, opt-in helper with UI.

## Explicitly out of scope for now

To stay opinionated and avoid a "supports everything, supports nothing" repo, the template does **not** ship multiple databases beyond SQLite/PostgreSQL, multiple payment providers, or Kubernetes manifests. Payments and hosting arrived as **documented recipes** ([Payments](payments.md), [Deploy recipes](deploy-recipes.md)) rather than template code — that stays the pattern.
