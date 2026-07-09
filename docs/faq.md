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

Yes. OpenProductKit ships an entitlement abstraction, not a payment provider. You can validate licenses through your own HTTP endpoint backed by Stripe, Lemon Squeezy, Paddle or something custom.

## Are plugins safe to install at runtime?

Not yet. The current plugin model is dev-time Python package discovery through entry points. Runtime plugin installation and sandboxing are roadmap items.

## Does the desktop app run a hidden web server?

No. It loads the built web UI in a native window and dispatches API requests to the FastAPI app in the same process through a bridge.

## Can I generate from a private fork?

Yes. Use a Git URL your environment can access:

```bash
uvx copier copy git+ssh://git@github.com/acme/OpenProductKit.git my-product
```

## How do I publish the docs?

The template repository includes `.readthedocs.yaml` for Read the Docs and `.github/workflows/docs.yml` for GitHub Pages. Use whichever host you prefer; both build the same MkDocs site.
