# Architecture

The rule for product code authored in this template: **business logic never leaks into FastAPI, Typer, or React.** Those are delivery mechanisms. Swap any of them without touching the core. Existing backends connected through the product-router boundary may retain their own internal architecture; the host does not copy or reinterpret their logic.

```mermaid
flowchart TD
    subgraph core["packages/core — pure Python, zero deps"]
        D[Domain models<br/>Project, Note]
        P[Ports<br/>Repository protocols]
        S[Services<br/>use-cases]
    end

    subgraph adapters["Adapters"]
        BE[apps/backend<br/>FastAPI + SQLModel]
        CLI[apps/cli<br/>Typer &bull; opk]
        FE[apps/frontend<br/>React + typed client]
        DT[apps/desktop<br/>pywebview shell]
    end

    subgraph ext["Extensions"]
        PA[packages/plugin-api]
        LIC[packages/licensing]
        PL[extensions/*<br/>plugins]
    end

    S --> P
    BE -->|implements| P
    CLI -->|uses| S
    FE -->|HTTP| BE
    DT -->|in-process bridge| BE
    PL -->|entry points| PA
    BE -->|discovers| PA
    BE -->|gates on| LIC
    BYO[Existing core / FastAPI backend] -->|product router| BE
```

## The layers

| Layer | Responsibility | Depends on |
| --- | --- | --- |
| `packages/core` | Domain models, `Repository` ports, services. No I/O. | nothing |
| `packages/plugin-api` | The `Plugin` contract + registry. | nothing (runtime) |
| `packages/licensing` | Entitlement: dev stub, Ed25519 signed tokens, file/HTTP providers. | cryptography |
| `apps/backend` | FastAPI HTTP adapter; owns SQLModel persistence + Alembic. | core, plugin-api, licensing |
| `apps/cli` | Typer CLI, task runner and control plane (`opk`). | core, backend, plugin-api, licensing |
| `apps/frontend` | React + Vite web UI over a generated typed client. | backend (HTTP or desktop bridge) |
| `apps/desktop` | pywebview shell; the same app called in-process (no HTTP). | backend, frontend build |
| `extensions/*` | Example plugins. | plugin-api (+ backend for the paid one) |

Existing first-party code can enter at the backend adapter through a
[product router](bring-your-own-code.md). That seam is intentionally separate
from plugins: it adopts the code that *is* the product without requiring an
extension manifest or copying it into template-owned modules.

## Why hexagonal here

Because the whole selling point is "one product, many faces". `core` is decoupled from **both** HTTP and the database:

- The backend maps domain models to SQLModel rows in `adapters/db` — the core never sees a table.
- The CLI builds the same services against the same repositories.
- Core tests run with an in-memory fake repository — no database, no FastAPI, no network.

If the core weren't decoupled from HTTP *and* persistence, the template wouldn't prove its own thesis.
