# Installation

OpenProductKit is a Copier template. You do not install OpenProductKit globally; you use Copier to render a new project from it.

## Requirements

- [uv](https://docs.astral.sh/uv/) for Python environments and `uvx`
- [Node.js](https://nodejs.org) 20+
- [pnpm](https://pnpm.io) 9+
- Git

Generated projects target Python 3.12 by default and can be generated for Python 3.13 from the template prompt.

## Generate from GitHub

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
cd my-product
```

`uvx` downloads and runs Copier for this command only, so there is no global Copier install to keep fresh.

!!! warning "Use templates you trust"
    Copier templates can execute tasks during generation or update. Treat a template like code: read it or use a source you trust before running it on your machine.

## Generate from a local clone

```bash
git clone https://github.com/ravipurohit1991/OpenProductKit
cd OpenProductKit
uvx copier copy . ../my-product
```

This is the best flow when you are developing the template itself or testing unpublished changes.

## Install a generated project

```bash
cd my-product
uv sync --dev
pnpm install
```

Then run the smoke checks:

```bash
uv run opk hello
uv run opk doctor
uv run opk test
```

If you changed `cli_name` during generation, replace `opk` with your generated command name.

## Build these docs

From the OpenProductKit template repository:

```bash
uvx --with-requirements requirements-docs.txt mkdocs serve
uvx --with-requirements requirements-docs.txt mkdocs build --strict
```

The repository also includes `.readthedocs.yaml`, so Read the Docs can build the MkDocs site directly from `mkdocs.yml`.
