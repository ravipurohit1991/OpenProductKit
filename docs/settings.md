# Settings

Generated OpenProductKit projects use environment variables prefixed with `APP_`. The backend settings class also reads a local `.env` file.

## Common variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_DATABASE_URL` | SQLAlchemy database URL | Local SQLite database |
| `APP_LICENSE_DEV_PLAN` | Development stub plan | `pro` |
| `APP_LICENSE_PUBLIC_KEY` | Ed25519 public key used to verify signed license tokens | unset |
| `APP_LICENSE_TOKEN` | Signed license token supplied directly | unset |
| `APP_LICENSE_FILE` | Path to a signed license token file | `license.key` |
| `APP_LICENSE_URL` | HTTP license validation endpoint | unset |
| `APP_WEB_DIST` | Directory with the built web UI; served at `/` when it exists | `apps/frontend/dist` |
| `APP_MARKETPLACE_CATALOG` | Local marketplace catalog file | `marketplace/catalog.json` |
| `APP_MARKETPLACE_URL` | Hosted catalog URL (replaces the local file when set) | unset |
| `APP_MARKETPLACE_ALLOW_INSTALL` | Allow installing catalog extensions from the running app ([details](marketplace.md#runtime-installs-opt-in)) | `false` |
| `APP_AUTH_ENABLED` | Require user accounts on every API route ([details](auth.md)) | `false` |
| `APP_AUTH_SESSION_DAYS` | Login session lifetime in days | `30` |

## AI SaaS variables

These variables are used only when the project was generated with
`include_ai_saas=true`. See [AI SaaS](ai-saas.md) for the provider contract,
Stripe setup and production checklist.

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_AI_PROVIDER` | `mock` or the built-in `http` gateway adapter | `mock` |
| `APP_AI_PROVIDER_URL` | Submit URL for the HTTP adapter | unset |
| `APP_AI_API_KEY` | Bearer key sent only to the provider gateway | unset |
| `APP_AI_WEBHOOK_SECRET` | HMAC secret for provider callbacks | unset |
| `APP_AI_DEFAULT_MODEL` | Initial model sent by the Studio | `default` |
| `APP_AI_GENERATION_COST` | Credits reserved per job | `1` |
| `APP_AI_TRIAL_CREDITS` | One-time credits granted per tenant | `10` |
| `APP_AI_INLINE_JOBS` | Process after API response instead of a separate worker | `true` |
| `APP_AI_JOB_LEASE_SECONDS` | Reclaim a claim left without a provider request ID after worker failure | `300` |
| `APP_AI_PUBLIC_URL` | Public origin used in callback and signed asset URLs | `http://127.0.0.1:8000` |
| `APP_AI_MAX_UPLOAD_BYTES` | Maximum reference upload size | `10485760` |
| `APP_AI_ALLOWED_CONTENT_TYPES` | Comma-separated validated image MIME types | PNG, JPEG, WebP |
| `APP_AI_ASSET_SIGNING_SECRET` | HMAC secret for short-lived private provider reads | unset |
| `APP_AI_STORAGE_BACKEND` | `local` or `s3` | `local` |
| `APP_AI_UPLOAD_DIR` | Root for local asset data | `data/uploads` |
| `APP_AI_S3_*` | S3-compatible bucket, endpoint, region and credentials | unset |
| `APP_STRIPE_SECRET_KEY` | Backend Stripe API key | unset |
| `APP_STRIPE_WEBHOOK_SECRET` | Stripe endpoint signing secret | unset |
| `APP_STRIPE_CREDIT_PACKS` | JSON map of pack names to Stripe Price IDs and credit amounts | `{}` |

Desktop mode sets `APP_DATABASE_URL` and `APP_LICENSE_FILE` to platform-specific app-data paths when they are not already set (the sidecar shells also set `APP_WEB_DIST`).

## License resolution

License providers are resolved in this order:

1. `APP_LICENSE_URL`
2. `APP_LICENSE_TOKEN`
3. `APP_LICENSE_FILE`
4. development stub

Invalid or expired licenses degrade to the free plan with a readable status message.

## Frontend settings

The frontend's product name is generated into `apps/frontend/src/config.ts`.

The API client chooses its transport at runtime:

- browser mode uses HTTP (same origin, or the Vite dev proxy)
- the pywebview desktop shell uses the in-process JS bridge
- the Electron/Tauri shells load the UI *from* the sidecar backend, so plain
  same-origin HTTP applies with no special casing

## Copier answers

Generated projects store template answers in `.copier-answers.yml`. Copier uses this file during `copier update` to re-render the project with the same names and metadata.

Commit `.copier-answers.yml` so updates are reproducible for every developer on the project.
