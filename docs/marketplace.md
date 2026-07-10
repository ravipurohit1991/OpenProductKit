# Marketplace

Every generated product ships a **Marketplace tab**: one place where users see
which extensions exist, which are installed, which are locked behind a plan —
and where they paste a license token to unlock the paid ones. It turns the
plugin system + licensing into something you can actually sell with.

```mermaid
flowchart LR
    CAT[marketplace/catalog.json<br/>or APP_MARKETPLACE_URL] --> API["/api/marketplace"]
    EP[Installed plugins<br/>entry points] --> API
    API --> UI[Marketplace tab]
    UI -- "paste license token" --> UNLOCK["/api/marketplace/unlock"]
    UNLOCK -- "verify + persist + re-read gates" --> LIC[license provider]
```

## What the user sees

Each card shows the extension's name, plan requirement and live state:

- **installed · enabled** — running now; toggle on/off instantly.
- **locked** — installed but requires a higher plan; the unlock box at the top
  accepts a signed license token and applies it **immediately, no restart**
  (plugin routes are license-checked per-request).
- **not installed** — offered by the catalog, with the exact install command
  (`uv add <package>`), a homepage link, and its plan requirement.

The same information is available headless: `opk marketplace list` and
`opk marketplace unlock <token>`.

## The catalog

`marketplace/catalog.json` lists what you offer beyond what is installed:

```json
{
  "items": [
    {
      "id": "example.reports",
      "name": "Reports (Pro)",
      "version": "0.1.0",
      "description": "Summary reports over your data.",
      "required_plan": "pro",
      "homepage": "https://example.com/extensions/reports",
      "install_hint": "uv add acme-plugin-reports"
    }
  ]
}
```

Host that file anywhere and set `APP_MARKETPLACE_URL` to manage your catalog
**without shipping app updates**. Installed plugins are always discovered from
entry points regardless of the catalog, so the tab never lies about local state.

The generated project demonstrates the full loop out of the box:
`extensions/example-marketplace-plugin` lives in the repo but is **not**
installed by `uv sync` — it appears as *not installed* in the tab until
`uv add <pkg>-plugin-reports`, and then stays *locked* until a `pro` license
token is activated.

## Unlocking is licensing, not payments

`POST /api/marketplace/unlock` verifies the pasted token offline against your
vendor public key, persists it to the license file, and clears the resolved
provider so every `require_plan` / `require_feature` gate and plugin route sees
the new entitlements on the next request.

You sell however you like (website, email, invoice); your side of the flow is:

```bash
opk license keygen                      # once — keep the private key secret
opk license issue --licensee "Acme" --plan pro --days 365
# send the printed token to the customer; they paste it in the Marketplace tab
```

Connecting a payment provider is a webhook that calls `license issue` and
emails the token — a roadmap recipe, but the app side is already done.
