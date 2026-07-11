// A tiny, fully-typed fetch client. Every path, param, request body and response
// is typed from `schema.d.ts`, which is generated from the backend's OpenAPI
// schema (`opk gen`). Do not hand-edit schema.d.ts.

import createClient from "openapi-fetch";

import type { paths } from "./schema";

// In the desktop shell the UI is loaded from disk (file://) and there is no
// HTTP server at all: requests cross the pywebview JS bridge and are handled
// by the FastAPI app in the same process. The web build path is untouched.
type BridgeResult = { status: number; content_type: string; body: string };

declare global {
  interface Window {
    pywebview?: { api?: { request?: (payload: object) => Promise<BridgeResult> } };
  }
}

const isDesktop =
  typeof window !== "undefined" && window.location.protocol === "file:";

// pywebview injects `window.pywebview.api` as an empty object first and
// attaches the methods a beat later, so testing the object is not enough —
// wait until the method itself exists (or the ready event fires).
function bridgeReady(): Promise<void> {
  if (typeof window.pywebview?.api?.request === "function") return Promise.resolve();
  return new Promise((resolve) =>
    window.addEventListener("pywebviewready", () => resolve(), { once: true }),
  );
}

async function bridgeFetch(input: Request): Promise<Response> {
  await bridgeReady();
  const url = new URL(input.url);
  const body =
    input.method === "GET" || input.method === "HEAD" ? null : await input.text();
  const result = await window.pywebview!.api!.request!({
    method: input.method,
    path: url.pathname + url.search,
    body,
  });
  return new Response(result.body || null, {
    status: result.status,
    headers: { "Content-Type": result.content_type },
  });
}

// Web: baseUrl "/" — Vite proxies /api in dev; same-origin in prod.
// Desktop: a dummy http:// base keeps URL parsing sane on a file:// page (a
// relative "/api/…" would resolve drive-relative to file:///C:/api/…); it is
// never fetched — bridgeFetch only reads the path off it.
export const client = createClient<paths>(
  isDesktop
    ? { baseUrl: "http://desktop.internal", fetch: bridgeFetch }
    : { baseUrl: "/" },
);
