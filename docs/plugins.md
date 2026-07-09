# Plugins

Plugins are ordinary Python packages that advertise a `Plugin` through the `<pkg>.plugins` entry-point group. The host discovers them with `importlib.metadata`.

!!! note "This is a dev-time model"
    Plugins are installed Python packages discovered via entry points — there is
    no arbitrary runtime code loading. Runtime / end-user plugin installation is a
    roadmap item, kept off the v1 surface on purpose. This is the honest model,
    which matters more than an impressive-but-insecure one.

## What a plugin can contribute

- **Backend routes** — a FastAPI `APIRouter`
- **CLI commands** — a Typer app, auto-attached to `opk`
- **A settings schema** — JSON schema surfaced in the admin UI
- **Nav items** and a **health** probe
- A **`required_plan`** that the license provider gates on

## Minimal plugin

```python
from fastapi import APIRouter
from myapp_plugin_api import Plugin, PluginManifest


class HelloPlugin(Plugin):
    manifest = PluginManifest(
        id="acme.hello",
        name="Hello",
        description="Adds /api/ext/hello.",
        required_plan=None,  # free
    )

    def backend_router(self) -> APIRouter:
        router = APIRouter(prefix="/api/ext/hello")

        @router.get("")
        def hello() -> dict[str, str]:
            return {"hello": "world"}

        return router


PLUGIN = HelloPlugin()
```

```toml
# pyproject.toml
[project.entry-points."myapp.plugins"]
hello = "myapp_plugin_hello:PLUGIN"
```

## Lifecycle

- **Discovery** happens at startup via entry points — no database needed.
- The **license gate** is applied once: an unlicensed plugin's routes are never mounted.
- **Enable/disable** is persisted in the `plugin_states` table and checked *per request*, so toggling a plugin in the admin UI takes effect immediately, no restart.

## The bundled examples

| Plugin | Contributes | Plan |
| --- | --- | --- |
| `example.basic` | `GET /api/ext/basic/ping` + a settings schema | free |
| `example.cli` | `opk example-cli greet` | free |
| `example.paid` | `GET /api/ext/paid/summary` (queries the host DB) | `pro` |

Manage them from the **Plugins** tab in the web UI or via `opk plugin …`.
