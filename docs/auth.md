# Auth & users

Hosted deployments need accounts; a desktop app on someone's own machine does
not. OpenProductKit ships auth as a **runtime switch, not a build variant**:

```bash
APP_AUTH_ENABLED=true
```

Off (the default) the app behaves exactly as before — no login, no users, the
desktop/local story stays frictionless. On, the same image/binary becomes a
multi-user deployment. There is no Copier question and no second build
artifact to maintain; dev, Docker and desktop all share one auth-aware app
that simply doesn't enforce until told to.

## What turning it on does

- **Every API route requires a signed-in session** — including plugin routes,
  which inherit enforcement automatically. The public exceptions are
  `/api/health`, `/api/auth/me`, `/api/auth/login` and `/api/auth/setup`
  (without them nobody could log in). `/docs` stays reachable: it exposes the
  schema, never data.
- **Operator actions require an admin**: enabling/disabling plugins, unlocking
  licenses, runtime marketplace installs, and user management. Non-admin users
  get the product, not the controls.
- **First run bootstraps itself.** With no users yet, the web UI shows
  "Create the admin account" instead of a login form (the API equivalent is
  `POST /api/auth/setup`, one-shot). Prefer the CLI? `opk user add
  you@example.com --admin`.

## Sessions

Logging in returns an opaque bearer token; the frontend stores it in
`localStorage` and the generated client sends it as `Authorization: Bearer …`
on every call. Server-side only the token's SHA-256 is stored, so a leaked
database doesn't leak logins. Sessions expire after `APP_AUTH_SESSION_DAYS`
(default 30); logout revokes the token, and resetting a password revokes all
of that user's sessions.

Passwords are hashed with stdlib `scrypt` — no extra dependencies.

## Managing users

In the UI, admins get a **Users** tab (create, delete, admin flag). From the
shell:

```bash
opk user add alice@example.com          # prompts for a password
opk user add ci@example.com --password … --admin
opk user list
opk user passwd alice@example.com
opk user remove alice@example.com
```

These work regardless of `APP_AUTH_ENABLED` — you can seed accounts before
flipping the switch.

## The API

| Endpoint | Auth | Purpose |
| --- | --- | --- |
| `GET /api/auth/me` | public | Is auth on? Does it need setup? Who am I? |
| `POST /api/auth/setup` | public, one-shot | Create the first admin account |
| `POST /api/auth/login` | public | `{email, password}` → `{token, user}` |
| `POST /api/auth/logout` | session | Revoke the presented token |
| `GET/POST /api/auth/users`, `DELETE /api/auth/users/{id}` | admin | User management |

`401` responses carry `{"error": "auth_required"}` and admin failures
`{"error": "admin_required"}` — structured like the licensing gates, so
clients can react without string-matching.

## Honest limits

This is deliberately small, dependency-free session auth — right-sized for
"put my product on a URL for my team/customers". Know what it is not:

- **No rate limiting or lockout.** On the open internet, put your reverse
  proxy's limits in front of `/api/auth/login`.
- **No self-service password reset** (no email pipeline is assumed). Admins
  reset via `opk user passwd` or the Users tab.
- **No SSO/OIDC yet** — on the roadmap; the enforcement seam (`enforce_auth`)
  is where it will plug in.
- **Bearer over TLS only.** Every [deploy recipe](deploy-recipes.md)
  terminates TLS; don't skip it.
