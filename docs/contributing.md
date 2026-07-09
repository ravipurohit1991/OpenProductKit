# Contributing

Thanks for helping improve OpenProductKit. The main rule is to keep the template useful as a product starter, not just as a demo app.

## Development loop

```bash
git clone https://github.com/ravipurohit1991/OpenProductKit
cd OpenProductKit
uvx copier copy . ../scratch-product
cd ../scratch-product
uv sync --dev
uv run opk test
uv run opk lint
```

Make template changes in `OpenProductKit`, then regenerate a scratch project to verify that rendered package names, imports and docs still work.

## What to preserve

- Keep business logic out of FastAPI, Typer and React.
- Keep the Resource Vault demo small and clearly fenced with `[demo]`.
- Keep generated projects runnable on day one.
- Keep CLI workflows cross-platform.
- Keep docs close to the generated behavior.

## Before opening a pull request

Run the relevant checks in a generated scratch project:

```bash
uv run opk test
uv run opk lint
uv run opk build web
uv run opk desktop --check
```

For documentation changes in the template repository:

```bash
uvx --with-requirements requirements-docs.txt mkdocs build --strict
```

Use the repository's GitHub issue and pull request templates for the rest of the contribution checklist.
