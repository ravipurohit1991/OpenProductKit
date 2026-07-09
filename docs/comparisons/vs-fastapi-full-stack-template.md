# vs the FastAPI full-stack template

The official [FastAPI full-stack template](https://github.com/fastapi/full-stack-fastapi-template) is excellent and popular. OpenProductKit is aimed at a different job.

| | FastAPI full-stack template | OpenProductKit |
| --- | --- | --- |
| Primary goal | A great web SaaS starter | A *product-template* for web **+ CLI + desktop** from one core |
| Business logic | Lives in the FastAPI app | Lives in a framework-free `core`; web/CLI/desktop are adapters |
| CLI | — | First-class control plane (`opk`) |
| Desktop | — | Native window, core called in-process (no sidecar) |
| Plugins | — | Entry-point plugin system + admin UI |
| Licensing | — | Signed offline tokens, file/HTTP providers, vendor tooling |
| Rebranding | Manual / cookiecutter-style | Copier prompts **+ `copier update`** |
| Typed client | Generated | Generated (`openapi-typescript` + `openapi-fetch`) |

**Choose the FastAPI template** if you want a focused, battle-tested web SaaS starter.

**Choose OpenProductKit** if you want to ship the *same product* as a web app, a CLI and a desktop app, with plugins and commercial hooks, from one decoupled core.
