# Concepts

OpenProductKit is easiest to work with when you keep a few boundaries clear.

## Product template

OpenProductKit is a template for creating a product repository. The template repository contains Jinja-rendered files under `template/`; a generated product contains normal Python, TypeScript, Markdown and config files with your names already filled in.

You should usually edit the generated product, not the template, unless you are improving OpenProductKit for every future product.

## One core, many adapters

The core package contains domain models, ports and services. It does not import FastAPI, SQLModel, Typer, React or pywebview.

Adapters deliver the same core through different surfaces:

- FastAPI for HTTP
- Typer for CLI commands
- React for the browser UI
- pywebview for a desktop window
- plugins for extension packages

This is why the same product can run in a browser, terminal and desktop window without duplicating business logic.

## Demo vs framework

Generated projects include a small Resource Vault demo: projects, notes, tags and search. It proves the wiring across every layer.

The demo is intentionally fenced with `[demo]` markers. Replace those parts with your product. Keep the unmarked framework pieces: licensing, plugin discovery, migrations, desktop bridge, generated client pipeline, CI and docs tooling.

## CLI as control plane

The generated CLI is not only a user-facing command. It is also the cross-platform task runner for development:

- run the app
- run migrations
- build web and desktop artifacts
- regenerate API types
- manage plugins
- issue and install licenses
- build and serve docs

This keeps project workflows in Python code instead of scattering them across shell scripts.

## Generated client

The frontend API types come from the backend's OpenAPI schema. After changing API routes, run:

```bash
uv run opk gen
```

TypeScript then catches stale frontend calls before they ship.

## Commercial hooks

Licensing is an entitlement layer. It can run as a development stub, verify signed offline tokens, or call an HTTP license endpoint. Routes, plugins and UI components all read from the same entitlement model.

It is meant for honest-user licensing and product packaging, not impossible-to-break DRM.

## Agent-ready rework

Every generated project includes `AGENTS.md` and `CLAUDE.md` rendered with your package names and CLI name. Those files tell coding agents where the demo lives, which architecture rules matter, and how to replace the sample domain layer by layer.
