# Payments

OpenProductKit deliberately ships **entitlements, not payments** — but the seam
where a payment provider plugs in is already built. This page is the missing
piece: three recipes that turn "customer paid" into "customer's app is
licensed", end to end.

The shape is always the same:

```
customer pays (Stripe / Lemon Squeezy / Paddle)
        │  webhook
        ▼
your license endpoint ──► issue_token(...)  (the same code behind `opk license issue`)
        │  email
        ▼
customer pastes the token → Marketplace “Unlock” (or `opk license install`)
        ▼
every plan/feature gate in the app re-reads entitlements — no restart
```

Commands and module names below use the defaults (`opk`, `openproductkit`);
substitute yours. One-time setup, if you haven't already:

```bash
opk license keygen     # writes license-signing.private / .public
# bake the public key into the app: APP_LICENSE_PUBLIC_KEY=<printed value>
```

!!! warning "The private key signs money"
    Whatever host runs the webhook below holds `license-signing.private`. Keep
    it out of the product repo (`.gitignore` already refuses it), give it to
    exactly one small service, and rotate it if in doubt — the app only ever
    needs the *public* key.

## Recipe 1 — Stripe

Stripe is the raw-payments default: you are the merchant (handle your own VAT /
sales tax, or see Paddle / Lemon Squeezy below). Sell with **Payment Links** —
no storefront code — and let one small webhook service do the licensing.

**Stripe-side setup (dashboard):**

1. Create a Product per plan; on each Payment Link set **metadata**
   `plan=pro` (or `enterprise`).
2. Add a webhook endpoint pointed at your license server, subscribed to
   `checkout.session.completed`; note its signing secret (`whsec_…`).

**The license server** — a single file, `tools/license_server.py` in your
generated repo, so it can import your licensing package directly. Run it
anywhere small (a $5 VPS, Fly machine); it needs `uv add stripe` and three env
vars (`STRIPE_WEBHOOK_SECRET`, `LICENSE_SIGNING_KEY_FILE`, SMTP credentials):

```python
"""Stripe checkout → signed license token → customer email.

Run: uv run uvicorn tools.license_server:app --port 9000
"""

import os
import smtplib
from email.message import EmailMessage

import stripe
from fastapi import FastAPI, Header, HTTPException, Request

from openproductkit_licensing import issue_token

app = FastAPI()
SIGNING_KEY = open(os.environ["LICENSE_SIGNING_KEY_FILE"], encoding="utf-8").read().strip()
WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]
KNOWN_PLANS = {"pro", "enterprise"}


def email_token(to: str, token: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Your license key"
    msg["From"] = os.environ["SMTP_FROM"]
    msg["To"] = to
    msg.set_content(
        "Thanks for your purchase!\n\n"
        "Your license token:\n\n"
        f"{token}\n\n"
        "Activate it in the app under Marketplace → Unlock, "
        "or run: opk license install <token>\n"
    )
    with smtplib.SMTP_SSL(os.environ["SMTP_HOST"]) as smtp:
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        smtp.send_message(msg)


@app.post("/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    try:
        event = stripe.Webhook.construct_event(
            await request.body(), stripe_signature, WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="bad signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session["customer_details"]["email"]
        plan = session.get("metadata", {}).get("plan", "pro")
        if plan not in KNOWN_PLANS:
            raise HTTPException(status_code=400, detail=f"unknown plan: {plan}")
        token = issue_token(
            SIGNING_KEY,
            licensee=email,
            plan=plan,
            valid_days=365,  # or None for perpetual
        )
        email_token(email, token)
    return {"ok": True}
```

That's the whole integration. Test the loop locally with the Stripe CLI:

```bash
stripe listen --forward-to localhost:9000/stripe/webhook
stripe trigger checkout.session.completed
```

**Subscriptions:** issue with `valid_days` slightly longer than the billing
period and re-issue from the `invoice.paid` webhook — lapsed customers
degrade to the free plan when the token expires, which is exactly the offline
behavior the [licensing system](licensing.md) promises. If you need same-day
revocation instead, switch the app to `APP_LICENSE_URL` (below).

## Recipe 2 — Lemon Squeezy (no license server at all)

Lemon Squeezy is a **merchant of record** (they handle global VAT/sales tax —
significant if you sell as a solo developer) and it has a native license-key
API. That means you can skip token signing entirely and validate keys against
their API through the `HttpLicenseProvider` you already have: run one tiny
adapter that speaks the [HTTP license contract](licensing.md#the-http-contract).

Lemon-side: enable **License Keys** on your product's variant (name the
variant after your plan, e.g. "Pro"). Adapter:

```python
"""Adapter: OpenProductKit license contract → Lemon Squeezy key validation.

Run it anywhere; point installs at it with APP_LICENSE_URL=https://…/validate
Customers paste the Lemon Squeezy license key instead of a signed token.
"""

import urllib.parse
import urllib.request
import json

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ValidateIn(BaseModel):
    token: str


@app.post("/validate")
def validate(payload: ValidateIn) -> dict:
    body = urllib.parse.urlencode({"license_key": payload.token}).encode()
    req = urllib.request.Request(
        "https://api.lemonsqueezy.com/v1/licenses/validate",
        data=body,
        headers={"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
    except OSError:
        return {"valid": False, "plan": "free", "message": "validation unreachable"}
    if not data.get("valid"):
        return {"valid": False, "plan": "free", "message": data.get("error") or "invalid key"}
    meta = data.get("meta", {})
    return {
        "valid": True,
        # Variant name is the plan: create variants named "pro" / "enterprise".
        "plan": str(meta.get("variant_name", "pro")).lower(),
        "licensee": meta.get("customer_email", ""),
        "features": [],
        "expires_at": (data.get("license_key") or {}).get("expires_at"),
        "message": "ok",
    }
```

The app side is configuration, not code: `APP_LICENSE_URL=https://…/validate`.
`HttpLicenseProvider` caches responses and keeps the last good one when your
adapter is down, so a Lemon Squeezy outage never locks paying customers out.

## Recipe 3 — Paddle

Paddle is also a merchant of record. The integration is the Stripe recipe with
different names: subscribe to `transaction.completed` in Paddle's developer
dashboard, verify the `Paddle-Signature` header (their SDK:
`uv add paddle-python-sdk`), read your `custom_data` for the plan, then the
same `issue_token(...)` + email as above. Nothing else changes — the token,
unlock flow and gates are provider-agnostic by design.

## Selling marketplace extensions

Paid extensions are the **same tokens**. A purchase of the "Reports" extension
is a token that grants the plan (or feature flag) its manifest requires:

```bash
opk license issue --licensee acme@example.com --plan pro --feature reports
```

So "connect the marketplace to checkout" is nothing new: point the Payment
Link / Lemon product at the same webhook and issue with the right plan or
`--feature`. The customer pastes one token in the Marketplace tab; the
extension unlocks live, [no restart](marketplace.md).

## Which one?

| You want | Pick |
| --- | --- |
| Full control, lowest fees, you handle tax | **Stripe** + the license server |
| Zero infrastructure, tax handled, built-in license keys | **Lemon Squeezy** + the adapter (or even their raw API) |
| Merchant of record with a bigger enterprise footprint | **Paddle** + the Stripe-shaped recipe |

All three degrade gracefully: offline signed tokens keep working with no
server, and `HttpLicenseProvider` grace-caches — pick per business, not per
fear of lock-in.
