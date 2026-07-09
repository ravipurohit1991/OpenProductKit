# vs Tauri / Electron desktop boilerplates

Desktop boilerplates (Tauri + FastAPI sidecar, Electron + Python, …) get you a desktop shell. OpenProductKit is a product platform where desktop is *one* surface.

| | Desktop boilerplates | OpenProductKit |
| --- | --- | --- |
| Scope | Desktop shell + a bundled backend | Web + CLI + desktop from the same core |
| Backend coupling | Often a bundled HTTP sidecar | Desktop calls the core **in-process** (no sidecar, no port) |
| Web parity | Usually desktop-only | The same web build runs in the browser and in the window |
| Extensibility | Rare | Plugin system across surfaces |
| Licensing | DIY | Signed offline tokens + vendor tooling built in |

!!! note "Why in-process instead of a sidecar"
    The riskiest thing in a desktop template is a bundled-Python HTTP sidecar
    plus code signing / notarization — port races, orphaned processes, firewall
    prompts, two binaries to sign. OpenProductKit's shell dispatches UI requests
    over a JS bridge to the FastAPI app **in the same process**: one binary, no
    socket. That is only possible because the core never assumed HTTP in the
    first place. Signing/notarization remains documented-not-solved — see
    [Desktop](../desktop.md).
