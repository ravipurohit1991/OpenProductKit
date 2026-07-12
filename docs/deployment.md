# Deployment

Generated projects answer "how do I put this in front of someone?" with one
command per situation. All of it is optional — say no to the Docker question
and none of this is generated.

## The Docker stack

```bash
uv run opk stack up      # build + start; open http://localhost:8080
uv run opk stack ps      # services and health
uv run opk stack logs    # follow logs (optionally: stack logs backend)
uv run opk stack down    # stop (add --volumes to wipe data)
```

What runs (see the generated `docker-compose.yml`):

| Service | Role |
| --- | --- |
| `web` | nginx: serves the built React UI, proxies `/api` (and `/docs`) to the backend |
| `backend` | the FastAPI app, health-checked |
| `db` | PostgreSQL 16 with a persistent volume — only if you chose PostgreSQL |
| `tunnel` | Cloudflare quick tunnel — only with `stack share`, profile `share` |

The images build from the repo itself (`apps/backend/Dockerfile`,
`apps/frontend/Dockerfile`); a `.dockerignore` keeps secrets (`.env`,
license keys) and local state out of the build context. Runtime configuration
comes from your `.env` via `env_file`, so licensing and marketplace settings
work in containers the same way they do locally.

## Share a public URL in one command

```bash
uv run opk stack share
# … Public URL: https://<random>.trycloudflare.com
```

This starts the same stack plus [cloudflared](https://github.com/cloudflare/cloudflared)
in *quick tunnel* mode — no Cloudflare account, no DNS setup — and prints the
public URL when the tunnel is up. Use it to test on a phone, demo to a client,
or share a work-in-progress. The URL is temporary and unauthenticated:
**anyone with the link reaches your stack** until `stack down`, so treat it as
a demo tool, not hosting.

## SQLite or PostgreSQL

The Copier `database` question decides what the *deployed stack* runs:

- **SQLite** (default): the backend container keeps its database on a named
  volume. Zero moving parts; right for desktop-first products and small deploys.
- **PostgreSQL**: the stack gains a `db` service (exposed on `localhost:5432`,
  credentials `app`/`app`) and the backend image includes `psycopg`. Local dev
  and tests still use SQLite out of the box; point `APP_DATABASE_URL` at any
  PostgreSQL when you want to develop against it (the `.env.example` shows the
  URL). SQLModel + Alembic migrations run unchanged on both.

## Going to production

The stack is a solid single-server deployment: copy the repo to a VM with
Docker, put your real `.env` next to it, `opk stack up`. From there:

- **TLS / domain**: put your host's nginx/Caddy/Traefik (or a Cloudflare
  *named* tunnel) in front of port 8080, or edit `apps/frontend/nginx.conf` —
  it is a plain nginx site config, also usable outside Docker.
- **Single container**: the backend serves the built web UI at `/` whenever
  `apps/frontend/dist` exists (`APP_WEB_DIST` overrides the path), so the
  backend image alone can deliver the whole product if you prefer one container
  over the nginx split.
- **Secrets**: never bake `.env` into images (the `.dockerignore` already
  refuses); pass it at runtime.
- **Accounts**: anything public wants `APP_AUTH_ENABLED=true` — see
  [Auth & users](auth.md).

Host-specific walkthroughs — Fly.io, Railway, Cloud Run + Firebase Hosting,
static frontend hosts, named Cloudflare tunnels — live in
[Deploy recipes](deploy-recipes.md).
