# Deploy recipes

[Deployment](deployment.md) covers *what* ships (the Docker stack, the share
tunnel, SQLite vs PostgreSQL). This page answers *where*: copy-paste starting
points for the hosts people actually use. The template stays host-neutral on
purpose — everything below is plain Docker and static files, so none of it
locks you in.

Commands use the default names (`opk`, `openproductkit`); substitute your
generated CLI and slug.

## Before anything goes public

- **Turn accounts on.** `APP_AUTH_ENABLED=true` — a public URL without it means
  anyone can use the app *and its admin surface*. The first visit creates the
  admin account; see [Auth](auth.md).
- **Keep runtime installs off.** `APP_MARKETPLACE_ALLOW_INSTALL` defaults to
  `false`; leave it that way on shared hosts.
- **Secrets live in the host's env store**, never in the image. The
  `.dockerignore` already refuses `.env` and license keys.
- **TLS at the edge.** Every recipe below terminates TLS for you except the
  bare VPS, where your reverse proxy does it.

## One image for the whole product

The backend serves the built web UI at `/` whenever `apps/frontend/dist`
exists, so a single container can deliver everything. The stack's images split
web and API for nginx; for single-container hosts (Fly, Railway, Cloud Run),
add this `Dockerfile.single` next to the compose file:

```dockerfile
# Dockerfile.single — web build + API in one image.
FROM node:22-alpine AS web
RUN corepack enable
WORKDIR /app
COPY . .
RUN pnpm install && pnpm -C apps/frontend build

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY . .
# The web build is produced in the stage above because .dockerignore
# (correctly) keeps your local apps/frontend/dist out of the build context.
COPY --from=web /app/apps/frontend/dist ./apps/frontend/dist
RUN uv sync --no-dev
ENV APP_DATABASE_URL=sqlite:////app/data/app.db
EXPOSE 8000
CMD ["uv", "run", "--no-sync", "python", "-m", "openproductkit_backend"]
```

Smoke test it locally:

```bash
docker build -f Dockerfile.single -t myapp .
docker run --rm -p 8000:8000 -v myapp-data:/app/data myapp
# http://localhost:8000 serves the UI, /api/health the API
```

!!! note "SQLite needs a disk that survives restarts"
    On any host with an ephemeral filesystem, either mount a volume for
    `/app/data` (Fly, Railway) or use PostgreSQL (`APP_DATABASE_URL`). Cloud
    Run has no volumes — use a managed PostgreSQL there.

## Fly.io

The shortest path from repo to URL with a persistent disk:

```bash
fly launch --no-deploy          # answer the prompts; it writes fly.toml
fly volumes create data --size 1
```

Edit `fly.toml` to use the single-container image and the volume:

```toml
[build]
  dockerfile = "Dockerfile.single"

[http_service]
  internal_port = 8000
  force_https = true

[mounts]
  source = "data"
  destination = "/app/data"
```

Then secrets and ship:

```bash
fly secrets set APP_AUTH_ENABLED=true APP_LICENSE_PUBLIC_KEY=<your key>
fly deploy
```

For PostgreSQL instead of the volume: `fly postgres create`, attach it, and set
`APP_DATABASE_URL` accordingly (the backend image includes `psycopg` when you
generated with the PostgreSQL answer).

## Railway

Point Railway at the repo and tell it which Dockerfile to use:

1. **New Project → Deploy from GitHub repo.**
2. In the service's settings set the variable
   `RAILWAY_DOCKERFILE_PATH=Dockerfile.single`.
3. Add a **volume** mounted at `/app/data` (or provision Railway PostgreSQL and
   set `APP_DATABASE_URL`).
4. Add `APP_AUTH_ENABLED=true` and your `APP_LICENSE_PUBLIC_KEY` under
   Variables, then generate a domain under Networking.

## Google Cloud Run (+ Firebase Hosting)

Cloud Run runs the same single-container image; Firebase Hosting is only
worth adding if you want its CDN in front of the static files.

```bash
gcloud run deploy myapp \
  --source . \
  --set-env-vars APP_AUTH_ENABLED=true,APP_LICENSE_PUBLIC_KEY=<key>,APP_DATABASE_URL=<postgres url>
```

(`--source` builds with your Dockerfile — temporarily name `Dockerfile.single`
as `Dockerfile`, or build/push the image yourself.) Cloud Run's filesystem is
ephemeral: **SQLite does not fit here** — use Cloud SQL or any managed
PostgreSQL.

To put Firebase Hosting in front, rewrite everything to the service and let
the container do the serving:

```json
{
  "hosting": {
    "public": "apps/frontend/dist",
    "rewrites": [
      { "source": "/api/**", "run": { "serviceId": "myapp", "region": "us-central1" } },
      { "source": "**", "destination": "/index.html" }
    ]
  }
}
```

Build the frontend first (`opk build web`), then `firebase deploy`. The static
files come from the CDN; `/api` hits Cloud Run same-origin, so no CORS
configuration is needed.

## Static host for the frontend only (Vercel, Cloudflare Pages, Netlify)

The frontend is a plain Vite build (`opk build web` → `apps/frontend/dist`),
so any static host can serve it — **as long as it proxies `/api` to your
backend** so requests stay same-origin:

=== "Cloudflare Pages"

    `apps/frontend/public/_redirects`:

    ```
    /api/*  https://api.your-domain.com/api/:splat  200
    ```

=== "Vercel"

    `vercel.json` in the frontend root:

    ```json
    { "rewrites": [{ "source": "/api/:path*", "destination": "https://api.your-domain.com/api/:path*" }] }
    ```

=== "Netlify"

    `netlify.toml`:

    ```toml
    [[redirects]]
    from = "/api/*"
    to = "https://api.your-domain.com/api/:splat"
    status = 200
    ```

Host the backend anywhere from the recipes above. Prefer the proxy over CORS:
one origin means the bearer session, cookies-free auth and the generated
client all work unchanged.

## A VPS you own

Already first-class: copy the repo, put your real `.env` next to it, and
`opk stack up` (see [Deployment](deployment.md#going-to-production)). Put
Caddy in front for TLS:

```
your-domain.com {
    reverse_proxy localhost:8080
}
```

## Cloudflare named tunnel (self-host without opening ports)

`opk stack share` gives throwaway URLs; a *named* tunnel is the permanent
version — a stable domain pointed at a box behind NAT, no inbound ports:

```bash
cloudflared tunnel login
cloudflared tunnel create myapp
cloudflared tunnel route dns myapp app.your-domain.com
cloudflared tunnel run --url http://localhost:8080 myapp
```

Run the stack (`opk stack up`), and `app.your-domain.com` serves it with TLS.
Remember: a stable public URL is exactly the case for `APP_AUTH_ENABLED=true`.
