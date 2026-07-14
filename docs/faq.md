# FAQ

## Is OpenProductKit a framework?

It is a Copier template. The generated project is a normal Python and TypeScript repository that you own.

## Should I edit OpenProductKit or the generated project?

Edit the generated project when building your product. Edit OpenProductKit when you want to improve the template for future generated projects.

## Can I keep receiving template updates after replacing the demo?

Yes. Run `copier update` from the generated project. Framework files usually merge cleanly. Files where you removed or rewrote the Resource Vault demo may conflict or reappear; resolve those in favor of your product.

## Why is the demo included?

It proves every layer: core, persistence, API, CLI, frontend, desktop and tests. A blank template hides the hard parts; a small demo makes the replacement path visible.

## Can I delete the desktop app?

Yes. The desktop app is an adapter around the same backend and core. If your product does not need it, remove `apps/desktop` and the related build commands after generation.

## Can I use another billing provider?

Yes. OpenProductKit ships an entitlement abstraction, not a payment provider. You can validate licenses through your own HTTP endpoint backed by Stripe, Lemon Squeezy, Paddle or something custom — [Payments](payments.md) has ready-made recipes for all three.

## Are plugins safe to install at runtime?

Plugins are Python packages: installing one runs its code with the app's privileges — there is no sandbox, by honesty rather than accident. That is why the runtime install path is off by default (`APP_MARKETPLACE_ALLOW_INSTALL`), admin-only under [auth](auth.md), and meant exclusively for vendor-controlled catalogs. See [Marketplace](marketplace.md#runtime-installs-opt-in). A real permission/sandbox model remains a roadmap item.

## Does the template include user accounts?

Yes, as a runtime switch aimed at hosted deployments: set `APP_AUTH_ENABLED=true` and every API route requires a login, with admin-gated operator actions. Desktop and local runs stay accountless by default. See [Auth & users](auth.md).

## Can I start from an existing core or FastAPI backend?

Yes. `APP_PRODUCT_ROUTERS` connects existing FastAPI routers/apps directly, or a thin router factory around a framework-free core. Those endpoints join the generated OpenAPI client, web/desktop transport and deployment stack. See [Bring your own core or backend](bring-your-own-code.md).

## Does the desktop app run a hidden web server?

No. It loads the built web UI in a native window and dispatches API requests to the FastAPI app in the same process through a bridge.

## Can I generate from a private fork?

Yes. Use a Git URL your environment can access:

```bash
uvx copier copy git+ssh://git@github.com/acme/OpenProductKit.git my-product
```

## How do I publish the docs?

The template repository includes `.readthedocs.yaml` for Read the Docs and `.github/workflows/docs.yml` for GitHub Pages. Use whichever host you prefer; both build the same MkDocs site.
