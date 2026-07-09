# CLI reference

`opk` (the name is configurable at generation time) is a delivery adapter around the core **and** the project's task runner and control plane — so there is no Makefile to maintain across platforms.

## Core

| Command | Description |
| --- | --- |
| `opk hello [name]` | Smoke test. |
| `opk info` | Project + environment summary. |
| `opk doctor` | Check the local toolchain. |
| `opk version` | Print the CLI version. |
| `opk dev [--port] [--reload]` | Run the backend dev server. |

## Quality & build

| Command | Description |
| --- | --- |
| `opk test` | Run the pytest suite. |
| `opk lint` | Run ruff checks. |
| `opk fmt` | Format with ruff. |
| `opk build web` | Build the production web bundle. |
| `opk openapi [-o path]` | Export the OpenAPI schema. |
| `opk gen` | Regenerate the typed frontend client from the schema. |

## Database

| Command | Description |
| --- | --- |
| `opk db migrate` | Apply pending migrations. |
| `opk db revision -m "msg"` | Autogenerate a migration from model changes. |
| `opk db downgrade [rev]` | Revert migrations. |
| `opk db reset` | Drop everything and re-apply. |

## Data (demo)

| Command | Description |
| --- | --- |
| `opk project add\|list` | Manage projects. |
| `opk note add\|list` | Manage/search notes. |

## Plugins

| Command | Description |
| --- | --- |
| `opk plugin list` | List installed plugins and state. |
| `opk plugin enable\|disable <id>` | Toggle a plugin. |
| `opk plugin install <path>` | Editable-install a local plugin. |

Installed, licensed plugins can also contribute their own commands — for example the bundled CLI plugin adds `opk example-cli greet`.
