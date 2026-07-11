# Licensing

Licensing is an **abstraction with real providers**, not hardcoded DRM.

!!! warning "Honest positioning"
    Desktop and client software can never have perfect license protection. This
    system is honest-user licensing, feature entitlement and commercial-readiness
    hooks — not "unbreakable" protection. Treat it as such.

## The contract

```python
class LicenseProvider(Protocol):
    def current_plan(self) -> str: ...
    def is_entitled(self, required_plan: str | None) -> bool: ...
    def has_feature(self, feature: str) -> bool: ...
    def info(self) -> LicenseInfo: ...   # plan, licensee, expiry, features, source
```

Plans are ranked (`free < pro < enterprise`); features are explicit named grants
in the license. Every adapter — API, CLI, desktop — resolves the **same**
provider from the same settings, so an install is licensed once, everywhere.

## The providers

| Provider | Source of truth | Use case |
| --- | --- | --- |
| `LocalDevLicenseProvider` | Local config (`APP_LICENSE_DEV_PLAN`) | Development, open-source "feature flags" mode |
| `SignedLicenseProvider` | An **Ed25519-signed offline token** (env var or file) | Selling licenses with no server at all |
| `HttpLicenseProvider` | A vendor-run validation endpoint | Central control, revocation, seat counting |
| `ExternalLicenseProvider` | A **vendor-native license manager** (ElecKey, Sentinel, Wibu, …) behind a `fetch()` adapter | Products that already own a commercial license stack |

Resolution order: an installed **entry-point provider** (see below) →
`APP_LICENSE_URL` → `APP_LICENSE_TOKEN` → `APP_LICENSE_FILE` (default
`license.key`) → the dev stub. Invalid or expired licenses **degrade to the
free plan** with a human-readable message — they never crash the app.

### Bridging a native license manager

Many commercial desktop products already run a native licensing SDK (a DLL
with its own activation, dongles, or a license server). Wrap it once and the
whole app — route gates, CLI status, desktop dialogs — sees a normal provider:

```python
# my_product_license_eleckey/__init__.py
from my_product_licensing import ExternalLicenseProvider, LicenseInfo

def _fetch() -> LicenseInfo:
    modules = native_sdk.query_modules()          # your SDK call
    return LicenseInfo(
        plan="pro" if 3 in modules else "free",
        features=tuple(MODULE_FEATURES[m] for m in modules),
        valid=bool(modules),
    )

provider = ExternalLicenseProvider(_fetch, name="eleckey")
```

```toml
# the adapter package's pyproject.toml
[project.entry-points."my_product.license_provider"]
eleckey = "my_product_license_eleckey:provider"
```

Installing the adapter package is the whole activation: the entry point takes
precedence over every built-in provider. A crashing SDK yields an *invalid*
license (locked, with a message) — never a crashed app. Source protection
(Cython/obfuscation) stays a build-pipeline concern in your product repo; the
provider seam is deliberately independent of it.

## Selling licenses in three commands (no server)

You are the vendor. Once:

```bash
opk license keygen        # writes license-signing.private / .public
# bake the public key into the app: APP_LICENSE_PUBLIC_KEY=<printed value>
```

Per customer:

```bash
opk license issue --licensee "Acme Corp" --plan pro --days 365 --feature export
# -> LIC1.eyJ...  (send this token to the customer)
```

The customer activates it:

```bash
opk license install LIC1.eyJ...   # writes license.key
opk license status                # plan: pro, licensee: Acme Corp, ...
```

The token is a signed JSON payload (`licensee`, `plan`, `features`,
`expires_at`). The app verifies it **offline** with only your public key;
tampering or the wrong key degrades it to `free`. Expiry is checked on every
read, so it takes effect without a restart — as does replacing the license file.

## The HTTP contract

`HttpLicenseProvider` POSTs `{"token": "..."}` to your endpoint and expects:

```json
{"valid": true, "plan": "pro", "licensee": "Acme Corp",
 "features": ["export"], "expires_at": null, "message": "ok"}
```

Responses are cached (default 5 min). If your server is unreachable, the **last
good response keeps working** (offline grace) instead of locking paying
customers out; a fresh install that has never validated stays `free`. Implement
the endpoint in anything — including a few lines of FastAPI in your own
license-server project, or a webhook layer over Stripe / Lemon Squeezy / Paddle.

## Gating things

**Plugins** declare `required_plan` in their manifest; unlicensed plugin routes
are never mounted and their CLI commands never attach.

**Backend routes** use FastAPI dependencies (the idiomatic decorator form):

```python
from .licensing import require_feature, require_plan

@router.get("/export", dependencies=[Depends(require_plan("pro"))])
def export(): ...

@router.get("/report", dependencies=[Depends(require_feature("reports"))])
def report(): ...
```

A failed gate returns `403` with a structured detail
(`{"error": "license_required", "required_plan": "pro", "current_plan": "free"}`).

**Frontend** components use the entitlement hook and lock card:

```tsx
const { entitled } = useEntitlement("pro");
return entitled
  ? <ExportButton />
  : <LockedFeatureCard title="Export vault" requiredPlan="pro" />;
```

Plan ranks come from the `/api/license` response, so the client never hardcodes
tiers. The demo app gates its **Export vault** feature exactly this way — run
with `APP_LICENSE_DEV_PLAN=free` to see the locked state.

## Where the pieces live

- `packages/licensing` — providers, token signing/verification, `LicenseInfo`
- `packages/licensing/src/…/external.py` — the native-manager bridge (`ExternalLicenseProvider`, entry-point discovery)
- `apps/backend/src/…/licensing.py` — resolved provider + `require_plan` / `require_feature`
- `GET /api/license` — status for the UI (License tab in the admin)
- `opk license …` — status/install (customer) and keygen/issue/verify (vendor)
