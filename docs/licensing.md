# Licensing

Licensing is an **abstraction**, not hardcoded DRM.

!!! warning "Honest positioning"
    Desktop and client software can never have perfect license protection. This
    system is honest-user licensing, feature entitlement and commercial-readiness
    hooks — not "unbreakable" protection. Treat it as such.

## The contract

```python
class LicenseProvider(Protocol):
    def current_plan(self) -> str: ...
    def is_entitled(self, required_plan: str | None) -> bool: ...
```

For open-source use it behaves as feature flags. For commercial use, a real provider (signed token, HTTP license server, Stripe / Lemon Squeezy / Paddle / Gumroad) replaces the stub.

## The dev stub

`LocalDevLicenseProvider` resolves a plan locally (default `pro`) and does a real rank check:

```
free  <  pro  <  enterprise
```

So a plugin that declares `required_plan="pro"` is entitled under the dev stub, while one requiring `enterprise` would be locked — the seam a real backend plugs into.

## Where it plugs in

- **Plugins** — the registry marks a plugin `entitled` based on `required_plan`; unlicensed plugin routes are never mounted.
- **Future (P7)** — a `@requires_feature(...)` backend decorator and `useEntitlement()` / `LockedFeatureCard` on the frontend.

## Roadmap

Real providers — `FileLicenseProvider`, `HttpLicenseProvider`, `SignedTokenLicenseProvider` — and the feature-gate decorator land in a later phase. The interface is stable today so you can build against it.
