# AI SaaS profile

OpenProductKit can generate an optional, end-to-end AI product runtime: a
tenant-scoped Studio UI, durable generation jobs, uploads, provider adapters,
an atomic credit ledger, Stripe credit packs, webhooks and a worker process.
The default template remains lightweight; enable the profile only for products
that need it.

## Generate it

Choose **yes** for `include_ai_saas`, or pass the answer non-interactively:

```bash
uvx copier copy -d include_ai_saas=true gh:ravipurohit1991/OpenProductKit my-ai-product
cd my-ai-product
uv sync --dev
pnpm install
uv run opk dev
pnpm -C apps/frontend dev
```

The built-in `mock` provider needs no credentials. Open **AI Studio**, submit a
prompt and the complete upload → reserve → process → result flow runs locally.
Each local tenant starts with `APP_AI_TRIAL_CREDITS` credits.

## What is generated

| Layer | Responsibility |
| --- | --- |
| `packages/ai-runtime` | Framework-free job state, provider request/result types and transition rules |
| Backend models + migration | Tenant-owned jobs/assets, credit account, immutable ledger and webhook receipts |
| `ai_runtime.py` | Atomic reserve/grant/refund operations, durable claims, polling and reconciliation |
| Provider adapters | Credential-free mock plus a small HTTP gateway contract |
| Asset stores | Root-confined local files or S3-compatible object storage with presigned reads |
| `/api/ai/*` | Typed generation, upload, credits, health, callback and checkout APIs |
| `opk worker` | Durable queue consumer for hosted deployments |
| AI Studio | Generated-client-backed React flow with uploads, job polling, history and checkout |

Projects and notes also gain an `owner_id`; when hosted auth is enabled, every
repository query is scoped to the signed-in user. Local/desktop mode uses the
single `__local__` tenant.

## Job and credit lifecycle

Creating a generation with an `Idempotency-Key` performs one transaction:

1. validate ownership of the optional input asset;
2. atomically decrement the materialized credit balance only when sufficient;
3. append an immutable `reserve` ledger entry; and
4. create a `queued` job with a tenant-qualified unique request key.

Workers claim only `queued` rows using a conditional update. A successful job
gets a `consume` audit entry. Failure or cancellation appends one idempotent
`refund` entry and restores the balance. Concurrent client retries cannot spend
twice, and repeated provider or Stripe webhooks are stored and ignored.
Claims left without a provider request ID after a worker crash are requeued when
`APP_AI_JOB_LEASE_SECONDS` expires. Provider gateways must therefore use the
stable `job_id` as their own submit idempotency key.

Local development defaults to `APP_AI_INLINE_JOBS=true`, which schedules work
after the API response. Hosted Compose output sets it to `false` and starts the
separate worker automatically. Outside Compose, run:

```bash
uv run opk worker                 # continuous
uv run opk worker --once          # one batch, useful in tests or cron
uv run opk worker --interval 1.0  # polling interval in seconds
```

## HTTP provider contract

Set `APP_AI_PROVIDER=http` and point `APP_AI_PROVIDER_URL` at your provider
gateway. OPK sends:

```json
{
  "job_id": "local-job-id",
  "prompt": "generation prompt",
  "model": "provider-model",
  "input_url": "https://short-lived-private-asset-or-null",
  "callback_url": "https://your-app/api/ai/webhooks/provider/http"
}
```

`POST APP_AI_PROVIDER_URL` and `GET APP_AI_PROVIDER_URL/{request_id}` return:

```json
{
  "request_id": "provider-request-id",
  "status": "pending|running|succeeded|failed",
  "output_url": "https://result.example/image.png",
  "error": null
}
```

Gateways can instead callback with `event_id`, `request_id`, `status`, and
`output_url` or `error`. Sign the exact JSON body with HMAC-SHA256 using
`APP_AI_WEBHOOK_SECRET` and send the hex digest as `X-OPK-Signature` (an
optional `sha256=` prefix is accepted). Callback bodies are capped at 1 MiB.

For a provider-specific SDK, implement the `AIProvider` protocol and return it
from `configured_provider()`; the job, credit and webhook layers do not change.

## Uploads and private assets

Uploads are limited by both declared MIME type and file signature. Configure
the allowed list and byte limit with `APP_AI_ALLOWED_CONTENT_TYPES` and
`APP_AI_MAX_UPLOAD_BYTES`.

`APP_AI_STORAGE_BACKEND=local` stores files below `APP_AI_UPLOAD_DIR` and is
appropriate for desktop or a single server. For multiple workers or replicas,
use `s3` and configure the bucket, region and credentials. `APP_AI_S3_ENDPOINT_URL`
also supports S3-compatible services.

With hosted auth enabled, provider input URLs are short-lived HMAC URLs. Set a
long random `APP_AI_ASSET_SIGNING_SECRET`, a public HTTPS `APP_AI_PUBLIC_URL`,
and rotate the secret if it is exposed. Browser reads still require the owning
user's bearer token. S3 results use short-lived presigned reads.

## Stripe credit packs

Stripe checkout is enabled only for authenticated hosted users. Create one-time
Stripe Prices, then configure the server-owned mapping:

```dotenv
APP_AUTH_ENABLED=true
APP_STRIPE_SECRET_KEY=sk_live_...
APP_STRIPE_WEBHOOK_SECRET=whsec_...
APP_STRIPE_CREDIT_PACKS={"starter":{"price_id":"price_...","credits":100},"pro":{"price_id":"price_...","credits":500}}
APP_STRIPE_SUCCESS_URL=https://app.example.com/?checkout=success
APP_STRIPE_CANCEL_URL=https://app.example.com/?checkout=cancelled
```

Register `https://app.example.com/api/ai/webhooks/stripe` for
`checkout.session.completed`. Credits are granted only after Stripe reports a
paid session, using the signed event and server-created metadata. Both the
event ID and Checkout Session ID are idempotency keys, so webhook retries grant
once. Follow Stripe's guidance to [verify signatures using the raw request
body](https://docs.stripe.com/webhooks/signature) and to [expect duplicate
events](https://docs.stripe.com/webhooks#handle-duplicate-events).

Never expose Stripe or provider secrets through Vite variables or frontend
code. Keep them in the backend/worker environment.

## API surface

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/ai/config` | Safe UI configuration and available credit packs |
| `GET` | `/api/ai/health` | Tenant queue counts and provider/storage readiness |
| `GET` | `/api/ai/credits` | Balance and recent immutable ledger entries |
| `GET/POST` | `/api/ai/generations` | List or create tenant-owned jobs |
| `GET` | `/api/ai/generations/{id}` | Poll a job |
| `POST` | `/api/ai/generations/{id}/cancel` | Cancel and refund unfinished work |
| `POST` | `/api/ai/generations/{id}/sync` | Poll the external provider immediately |
| `POST` | `/api/ai/uploads` | Validate and store a reference image |
| `GET` | `/api/ai/assets/{id}` | Owner-authenticated or expiring signed asset read |
| `POST` | `/api/ai/billing/checkout` | Create an authenticated Stripe Checkout Session |

The generated `schema.d.ts` includes this complete surface, and
`opk gen --check` remains the CI drift gate for both template profiles.

## Production checklist

- Enable auth and create the first admin before sharing the URL.
- Use PostgreSQL plus S3-compatible storage for multiple app/worker replicas.
- Disable inline jobs and run at least one durable worker.
- Use HTTPS for `APP_AI_PUBLIC_URL` and all webhook endpoints.
- Set distinct long random asset and provider webhook secrets.
- Store provider, storage and Stripe credentials in a secret manager.
- Configure Stripe's live webhook secret and retain webhook delivery logs.
- Monitor `/api/ai/health`, failed jobs, queue age, provider latency and credit/refund totals.
- Add provider-specific timeouts, rate limits and moderation at the adapter seam.

Run the full local gate before deployment:

```bash
uv run ruff check .
uv run pytest
uv run opk gen --check
pnpm -C apps/frontend typecheck
pnpm -C apps/frontend build
docker compose config -q
```
