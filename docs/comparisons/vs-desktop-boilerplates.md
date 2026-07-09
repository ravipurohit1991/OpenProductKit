# vs Tauri / Electron desktop boilerplates

Desktop boilerplates (Tauri + FastAPI sidecar, Electron + Python, …) get you a desktop shell. OpenProductKit is a product platform where desktop is *one* surface.

| | Desktop boilerplates | OpenProductKit |
| --- | --- | --- |
| Scope | Desktop shell + a bundled backend | Web + CLI now; desktop as a v1.1 surface on the same core |
| Backend coupling | Often a bundled HTTP sidecar | Desktop will call the core **in-process** (no sidecar, no port) |
| Web parity | Usually desktop-only | The web build is first-class today |
| Extensibility | Rare | Plugin system across surfaces |

!!! note "Why desktop is deferred to v1.1"
    The riskiest thing in a desktop template is a bundled-Python HTTP sidecar plus
    code signing / notarization — the classic "works on my machine" failure. v1
    ships the surfaces that are solid today (web + CLI) rather than a desktop leg
    that crashes for half of users. When desktop lands it calls the core
    in-process, which is smaller and far less fragile.
