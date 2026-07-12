# Changelog

OpenProductKit is currently pre-1.0. The template and generated packages are versioned as `0.1.0` while the surface is proven in real projects.

## Unreleased — Milestone 5

- Optional user accounts as a runtime switch (`APP_AUTH_ENABLED`): scrypt passwords, hashed bearer sessions, first-run admin setup, a Users admin tab, a `user` CLI group, and admin-gated operator actions
- Runtime marketplace installs (`POST /api/marketplace/install`, `marketplace install` CLI): opt-in via `APP_MARKETPLACE_ALLOW_INSTALL`, live route mounting without a restart
- Frozen desktop builds bundle installed plugins (`--copy-metadata` + hidden imports)
- Generated `release.yml`: tag-triggered installers for Windows/macOS/Linux attached to a GitHub Release; Electron updater feed published alongside
- Typed-client drift gate: `gen --check` wired into the generated project's CI and the template's CI; `openapi-typescript` pinned exactly
- New docs: [Payments](payments.md) (Stripe / Lemon Squeezy / Paddle recipes), [Deploy recipes](deploy-recipes.md), [Auth & users](auth.md) and [Releases & auto-update](releases.md)

## 0.1.0

Initial public template surface:

- Hexagonal Python core with FastAPI, Typer, React and pywebview adapters
- Resource Vault demo spanning core, backend, CLI, frontend and desktop
- SQLModel persistence with Alembic migrations
- Generated OpenAPI TypeScript client
- CLI control plane for dev, tests, linting, builds, docs, database tasks, plugins and licensing
- Python entry-point plugin system with backend routes, CLI commands, settings, health and license gating
- Signed offline license tokens, file provider, HTTP provider and frontend entitlement UI
- Desktop app using an in-process bridge instead of an HTTP sidecar
- Copier rebranding and `copier update` support
- Agent-ready replacement path with `[demo]` markers, `AGENTS.md` and `CLAUDE.md`
- MkDocs Material documentation site with Read the Docs configuration

## Next

See the [roadmap](roadmap.md) for what's planned: plugin permissions and sandboxing, signed catalogs, SSO/OIDC, and per-user data ownership.
