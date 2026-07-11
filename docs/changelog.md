# Changelog

OpenProductKit is currently pre-1.0. The template and generated packages are versioned as `0.1.0` while the surface is proven in real projects.

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

## Unreleased

Native-desktop and commercial-licensing surface (driven by porting a real
PySide6 scientific product onto the template):

- `desktop_framework=pyside6`: `apps/desktop-qt` with native Qt widgets over the core, an in-process demo window, PyInstaller packaging and a Qt-free `--check` smoke test
- Core event bus (`<pkg_slug>_core.events`): headless-safe `Event` pub/sub with a pluggable dispatcher; the Qt shell installs `QtEventDispatcher` to marshal emissions onto the GUI thread
- `include_web_frontend=false`: generate without React/pnpm for Qt- or CLI-only products (frontend, CI job, Docker web service and `gen`/`build web` commands all drop out)
- `ExternalLicenseProvider` + entry-point discovery (`<pkg_slug>.license_provider`): bridge vendor-native license managers (ElecKey, Sentinel, …) ahead of the built-in providers

## Next

See the [roadmap](roadmap.md) for planned runtime plugin loading, desktop plugin packaging and generated-client drift checks.
