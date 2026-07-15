# Bring your own core or backend

OpenProductKit's framework should wrap your product code, not force you to
rewrite it in the Resource Vault's shape. There are two supported adoption
paths:

- **Backend-first:** import an existing FastAPI router or app directly.
- **Core-first:** keep the core package unchanged and write one thin router
  factory that constructs its services and translates HTTP at the edge.

Both paths use `APP_PRODUCT_ROUTERS`. Configured endpoints become first-class
routes in the generated backend: they appear in OpenAPI, feed the typed client,
inherit host-level auth, work through the desktop transport, and ship in the
same deployment.

## Backend-first: connect existing FastAPI code

First make the existing package importable from the backend environment. For
an adjacent local package:

```bash
uv add --package <your-pkg>-backend --editable ../my-existing-backend
```

For releases, make that dependency available inside the repository/build
context or publish it to your package index; an editable path outside a Docker
or CI checkout is only a development convenience.

Point the generated product at an `APIRouter`:

```bash
APP_PRODUCT_ROUTERS=my_backend.api:router
uv run opk product check
uv run opk dev
uv run opk gen
```

Multiple routers are comma-separated:

```bash
APP_PRODUCT_ROUTERS=my_backend.api:router,my_backend.admin:create_router
```

A target may be:

- a FastAPI `APIRouter`;
- a zero-argument factory returning an `APIRouter`; or
- an existing `FastAPI` app.

For a `FastAPI` app, OpenProductKit imports its API endpoints but deliberately
does not merge the nested app's middleware, lifespan, docs or static mounts.
Export a router or router factory when those concerns need explicit adaptation.

!!! tip "Keep routes under `/api`"
    The generated Vite and deployment proxies send `/api` to the backend. An
    imported router should therefore use `/api` itself or have a prefix such as
    `APIRouter(prefix="/api/tasks")`.

## Core-first: add only the HTTP adapter

Add the core package as a dependency, then create a small adapter inside the
generated backend. The core stays framework-free and remains the source of
product behavior:

```python
# apps/backend/src/<pkg>_backend/product_adapter.py
from fastapi import APIRouter

from my_core import TaskService


def create_router() -> APIRouter:
    service = TaskService(...)  # construct your existing ports/adapters here
    router = APIRouter(prefix="/api/tasks", tags=["tasks"])

    @router.get("")
    def list_tasks():
        return service.list()

    return router
```

Configure it like any other product router:

```bash
APP_PRODUCT_ROUTERS=<pkg>_backend.product_adapter:create_router
uv run opk product check
uv run opk gen
```

From there, the generated OpenAPI types are the handoff to the React surface.
The desktop shells and deployment stack need no domain-specific changes.

## Product routers vs plugins vs replacing the demo

| Seam | Use it for |
| --- | --- |
| Product routers | First-party core/backend code that defines the product |
| Plugins | Optional or third-party extensions with manifests, enable/disable state and license gates |
| Replace the demo | A native OpenProductKit domain built across core, persistence, API, CLI and frontend |

Product routers are intentionally small. They do not guess persistence or UI
semantics from arbitrary Python code. They establish a stable boundary so an
existing codebase can be adopted incrementally instead of copied into template
files.

Frozen desktop builds include configured product-router modules as dynamic
imports. Run the build with the same `APP_PRODUCT_ROUTERS` value the packaged
app will use, and keep the product package as a backend dependency.

## Validate before running

`opk product check` imports each configured target and prints its contributed
methods and paths. Invalid modules, missing attributes, factory failures and
wrong object types fail with an actionable error. The backend also validates
the same contract at startup, so a broken integration cannot silently ship.
