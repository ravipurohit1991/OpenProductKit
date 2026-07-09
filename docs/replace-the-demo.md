# Make it yours: replace the demo

The **Resource Vault** demo (projects, notes, tags, search) is not the product — it is a *worked example* that threads one small domain through every layer so you can see how the pieces connect. It exists to be replaced.

Every line of demo code is fenced with a `[demo]` marker. From a generated project:

```bash
grep -rn "\[demo\]" packages apps
```

That is the complete list of code to replace or trim. Everything unmarked — licensing, plugins, the desktop bridge, the CLI control plane, migrations tooling, the typed-client pipeline — is framework and works unchanged with *any* domain.

Generated projects also ship an **`AGENTS.md`** with a condensed version of this recipe, pre-rendered with your project's actual package and CLI names, so an AI coding agent (Claude Code, Cursor, Codex, …) can do the rework for you. "Generate the project, describe your product to your agent, review the diff" is the intended workflow.

## What is demo, what is framework

| Area | Demo (replace) | Framework (keep) |
| --- | --- | --- |
| `packages/core` | `domain/note.py`, `domain/project.py`, `services/notes.py`, `services/projects.py`, the two Protocols in `ports/repository.py`, the two errors in `errors.py`, the demo re-exports in `__init__.py`, `tests/test_notes_service.py` | The package layout itself: `domain/` + `ports/` + `services/`, `CoreError` |
| `apps/backend` | `api/routes/notes.py`, `api/routes/projects.py`, `api/routes/export.py`, the service wiring in `api/deps.py`, `adapters/db/repository.py`, the three Vault rows in `adapters/db/models.py`, `migrations/versions/0001_initial.py`, the Vault tests in `tests/test_api.py` | `app.py` scaffolding, `settings.py`, `db.py`, `licensing.py`, `plugins.py`, `adapters/db/engine.py`, `plugin_state.py`, `0002_plugin_states.py`, license/plugin routes and tests |
| `apps/cli` | The `project` and `note` command groups | Everything else: `dev`, `db`, `build`, `gen`, `license`, `plugin`, `docs`, … |
| `apps/frontend` | `VaultView.tsx`, the Vault hooks in `client/hooks.ts`, the Vault tab in `App.tsx` | `client/client.ts`, the generated `schema.d.ts` (regenerates from *your* API), `PluginManager.tsx`, `LicensePanel.tsx`, `LockedFeatureCard.tsx` |
| `apps/desktop` | Nothing — the bridge is domain-agnostic | All of it (the demo routes in `tests/test_bridge.py` are just sample payloads) |
| `extensions/` | The three example plugins are removable examples too | `packages/plugin-api` is the SDK — keep |

## The recipe: build yours first, delete the demo second

Work strangler-style: add your domain *next to* the demo, keep the test suite green, then delete the demo last. That way you always have a working example to crib from.

The steps below add a `Ticket` entity to an imagined support-desk product generated with `pkg_slug=helpdesk` and `cli_name=hd`. Substitute your own names.

### 1. Domain model — `packages/core/src/helpdesk_core/domain/ticket.py`

A plain frozen dataclass. No Pydantic, no SQLModel, no imports from outside the core — validation lives in `__post_init__`, behavior in methods.

```python
@dataclass(frozen=True, slots=True)
class Ticket:
    title: str
    status: str = "open"          # open | closed
    id: str = field(default_factory=_new_id)
    created_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Ticket title must not be empty")
```

### 2. Error — `packages/core/src/helpdesk_core/errors.py`

```python
class TicketNotFoundError(CoreError): ...
```

Adapters translate `CoreError` subclasses into HTTP codes / exit codes; the core never imports HTTP anything.

### 3. Port — `packages/core/src/helpdesk_core/ports/repository.py`

The interface the core *needs*, not what a database *offers*:

```python
class TicketRepository(Protocol):
    def add(self, ticket: Ticket) -> None: ...
    def get(self, ticket_id: str) -> Ticket | None: ...
    def list(self, *, status: str | None = None) -> list[Ticket]: ...
```

### 4. Service — `packages/core/src/helpdesk_core/services/tickets.py`

Use-cases against the port only. Re-export the new names from `helpdesk_core/__init__.py`.

### 5. Core test — `packages/core/tests/test_tickets_service.py`

Copy the style of the demo's test: an in-memory fake repository, zero infrastructure. This is the fastest feedback loop you have — get the domain right here before touching SQL or HTTP.

```bash
uv run pytest packages/core
```

### 6. Persistence — `apps/backend`

1. Add `TicketRow` to `adapters/db/models.py` (storage shape, not domain shape).
2. Add `SqlTicketRepository` to `adapters/db/repository.py` implementing the port, mapping Row ↔ dataclass.
3. Autogenerate and apply the migration:

```bash
uv run hd db revision -m "add tickets"   # writes apps/backend/migrations/versions/XXXX_add_tickets.py — review it
uv run hd db migrate
```

### 7. API — `apps/backend`

1. `api/routes/tickets.py`: Pydantic `TicketIn`/`TicketOut` at the edge, thin handlers that delegate to the service and translate `CoreError` → `HTTPException`.
2. Wire the service in `api/deps.py` (`TicketServiceDep`).
3. `app.include_router(tickets_router)` in `app.py`.
4. API tests in `apps/backend/tests/`.

### 8. Frontend — `apps/frontend`

```bash
uv run hd gen    # regenerate src/client/schema.d.ts from your new OpenAPI schema
```

Then hand-write the thin parts: TanStack Query hooks in `client/hooks.ts` (types come from the generated schema — `components["schemas"]["TicketOut"]`), a `TicketsView.tsx`, and a tab in `App.tsx`. If you change an endpoint and miss a call site, the TypeScript build fails — that is the drift protection working.

### 9. CLI adapter (optional but cheap)

Add a `ticket` Typer group in `apps/cli` following the demo's `project`/`note` groups: build the service from the SQL repositories, call it, print. Ten minutes, and your domain is scriptable.

### 10. Desktop, plugins, licensing — nothing to do

The desktop shell dispatches *any* route over its bridge; your tickets API works in the native window with zero desktop changes. That is the payoff of the hexagonal split. If some feature should be paid, gate its route with `Depends(require_plan("pro"))` and its UI with `useEntitlement()` — the demo's `export.py` shows the pattern.

### 11. Delete the demo

With your domain green, remove the Vault:

```bash
grep -rn "\[demo\]" packages apps    # your checklist
```

- **Delete** the pure-demo files: `domain/note.py`, `domain/project.py`, `services/notes.py`, `services/projects.py`, `test_notes_service.py`, `routes/notes.py`, `routes/projects.py`, `routes/export.py`, `adapters/db/repository.py`'s Vault classes, `VaultView.tsx`, the Vault API tests.
- **Trim** the marked sections from the mixed files: `ports/repository.py`, `errors.py`, `core/__init__.py`, `models.py`, `deps.py`, `app.py`, `cli/main.py`, `client/hooks.ts`, `App.tsx`, `test_bridge.py`'s sample paths.
- **Migrations:** keep the chain intact. Before you have shipped anything, the simplest move is to rewrite `0001_initial.py` to create *your* tables (it carries a `[demo]` note about this). After any release, write a new revision that drops the Vault tables instead.
- Finish with `uv run hd gen`, `uv run hd test`, `uv run hd lint`, and a frontend build.

## What `copier update` means after you've done this

`copier update` performs a three-way merge between the template version you generated from, the latest template, and your local changes.

- **Framework files you didn't touch** (licensing, plugin system, desktop shell, CI, CLI control plane) merge cleanly — you keep getting upstream improvements for free.
- **Demo files you rewrote or deleted** will conflict or resurrect — that is *expected and fine*. You replaced them on purpose; resolve in favor of your version (delete resurrected demo files, keep your conflicting ones). The demo is a scaffold, not a maintained surface.

Commit before running `copier update` so the merge is a reviewable diff.
