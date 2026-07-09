# Contributing to OpenProductKit

Thanks for your interest! OpenProductKit is a [Copier](https://copier.readthedocs.io) template, so most changes live under `template/` and are only exercised once a project is generated.

## How the repo is laid out

```
copier.yml            Prompts + template configuration
template/             The project that gets generated ({{ ... }} markers, *.jinja files)
docs/                 This documentation site (about the template itself)
.github/workflows/    CI: generates a project and runs its full suite
```

## Local development loop

The template can't be run directly (it contains Jinja markers). Generate a project and work against it:

```bash
# generate into a scratch dir (requires committing your template changes first,
# because Copier reads the committed tree)
git add -A && git commit -m "wip"
uvx copier copy --defaults --trust --vcs-ref HEAD . ../scratch-app

cd ../scratch-app
uv sync --dev
uv run opk test
uv run opk lint
pnpm install && pnpm -C apps/frontend build
```

## Conventions

- **Keep the core pure.** No FastAPI/DB/HTTP imports in `packages/core`.
- **Jinja hygiene.** Only `.jinja` files are rendered; funnel template variables through small config files and never put a literal `{{ ... }}` in a `.jinja` comment.
- **Cross-platform.** CI runs on Linux **and** Windows — avoid Unix-only assumptions (e.g. resolve executables via `shutil.which`, keep CLI output ASCII).
- **Lint & format** with ruff (`opk lint`, `opk fmt`).

## Pull requests

- Keep changes focused; update `docs/` when behavior changes.
- Ensure CI is green (it generates a project and runs the full suite on both OSes).
- By contributing you agree your work is licensed under the repository's [MIT license](LICENSE).

See also the [Code of Conduct](CODE_OF_CONDUCT.md).
