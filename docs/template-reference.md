# Template reference

This page documents the OpenProductKit template surface: Copier configuration, generated packages and extension points.

## Copier configuration

The template entry point is `copier.yml` at the repository root.

| Setting | Value |
| --- | --- |
| `_subdirectory` | `template` |
| `_templates_suffix` | `.jinja` |
| `_min_copier_version` | `9.0.0` |

All rendered files live under `template/`. Files ending in `.jinja` are rendered and written without the suffix. Files without that suffix are copied as-is unless their path contains Jinja variables.

## Questions

| Name | Type | Notes |
| --- | --- | --- |
| `project_name` | `str` | Display name used in README, docs and UI |
| `project_slug` | `str` | Lowercase dash slug for directories and package metadata |
| `pkg_slug` | `str` | Lowercase underscore slug for Python import names |
| `cli_name` | `str` | Console script name |
| `project_description` | `str` | One-line project description |
| `author_name` | `str` | Package author metadata |
| `author_email` | `str` | Package author metadata |
| `python_version` | choice | `3.12` or `3.13` |

## Generated Python packages

| Package | Purpose |
| --- | --- |
| `<pkg_slug>_core` | Domain models, ports, services and core errors |
| `<pkg_slug>_backend` | FastAPI app, SQLModel persistence, routes, migrations and adapter wiring |
| `<pkg_slug>_cli` | Typer CLI and development control plane |
| `<pkg_slug>_desktop` | pywebview shell and in-process request bridge |
| `<pkg_slug>_plugin_api` | Plugin manifest, contract, health and registry helpers |
| `<pkg_slug>_licensing` | License providers, token signing and plan resolution |

## Frontend package

`apps/frontend` is a React + Vite app. It uses a generated OpenAPI schema in `src/client/schema.d.ts`, a thin client wrapper in `src/client/client.ts`, and hand-written hooks in `src/client/hooks.ts`.

In browser mode, requests go to the backend over HTTP. In desktop mode, the same client dispatches through the pywebview bridge.

## Extension points

| Extension point | Where |
| --- | --- |
| Domain model | `packages/core/src/<pkg_slug>_core/domain/` |
| Core port | `packages/core/src/<pkg_slug>_core/ports/` |
| Core service | `packages/core/src/<pkg_slug>_core/services/` |
| Database row | `apps/backend/src/<pkg_slug>_backend/adapters/db/models.py` |
| Repository adapter | `apps/backend/src/<pkg_slug>_backend/adapters/db/repository.py` |
| API route | `apps/backend/src/<pkg_slug>_backend/api/routes/` |
| CLI command | `apps/cli/src/<pkg_slug>_cli/main.py` |
| Frontend view | `apps/frontend/src/` |
| Plugin | `extensions/*` or a separate package exposing `<pkg_slug>.plugins` entry points |

## Demo markers

The Resource Vault demo is marked with `[demo]` comments in mixed files and described in [Make it yours](replace-the-demo.md). Treat this marker as the removal checklist when your own domain is ready.
