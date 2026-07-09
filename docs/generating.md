# Generate a project

OpenProductKit's first job is to render a named product, not to be cloned and edited in place.

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
```

The destination directory is created if it does not exist. If it does exist, it must be writable.

## Template sources

| Source | Command |
| --- | --- |
| GitHub shortcut | `uvx copier copy gh:ravipurohit1991/OpenProductKit my-product` |
| Full Git URL | `uvx copier copy https://github.com/ravipurohit1991/OpenProductKit.git my-product` |
| Local clone | `uvx copier copy . ../my-product` |
| Specific ref | `uvx copier copy --vcs-ref v0.1.0 gh:ravipurohit1991/OpenProductKit my-product` |

For released tags, prefer stable semantic-version tags. Copier uses Git metadata when it later computes template updates.

## Questions

| Question | Default | Used for |
| --- | --- | --- |
| `project_name` | `OpenProductKit` | Human-readable product name in docs and UI |
| `project_slug` | Derived from `project_name` | Directory names, npm package names, Docker names |
| `pkg_slug` | Derived from `project_slug` | Python import packages such as `<pkg>_core` |
| `cli_name` | `opk` | Generated command-line entry point |
| `project_description` | Product one-liner | README and package metadata |
| `author_name` | `Your Name` | Package metadata |
| `author_email` | `you@example.com` | Package metadata |
| `python_version` | `3.12` | Python package metadata and generated targets |

## Generated layout

```text
my-product/
  apps/
    backend/      FastAPI adapter, SQLModel persistence, Alembic
    cli/          Typer command surface and project task runner
    frontend/     React + Vite UI over generated API types
    desktop/      pywebview shell and in-process bridge
  packages/
    core/         Framework-free domain, ports and services
    plugin-api/   Extension contract and registry
    licensing/    License providers and signed token support
  extensions/     Example plugins
  docs/           Generated product docs
  AGENTS.md       Agent instructions rendered with your project names
  CLAUDE.md       Companion agent instructions
```

## First run

```bash
cd my-product
uv sync --dev
uv run opk doctor
uv run opk dev
```

In another terminal:

```bash
pnpm install
pnpm -C apps/frontend dev
```

The backend serves API routes on `http://127.0.0.1:8000`; the richer web UI runs on `http://127.0.0.1:5173`.

## Regenerating during template development

When you are editing OpenProductKit itself, generate from the local checkout:

```bash
uvx copier copy . ../scratch-product
```

Use this to smoke-test prompt changes, newly added files, and Jinja-rendered package names before publishing a tag.
