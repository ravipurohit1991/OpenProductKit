// A tiny, fully-typed fetch client. Every path, param, request body and response
// is typed from `schema.d.ts`, which is generated from the backend's OpenAPI
// schema (`opk gen`). Do not hand-edit schema.d.ts.

import createClient from "openapi-fetch";

import type { paths } from "./schema";

// baseUrl "/" — Vite proxies /api to the backend in dev; same-origin in prod.
export const client = createClient<paths>({ baseUrl: "/" });
