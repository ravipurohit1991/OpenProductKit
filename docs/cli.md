# CLI reference

`opk` (the name is configurable at generation time) is a delivery adapter around the core **and** the project's task runner and control plane — so there is no Makefile to maintain across platforms.

## Core

| Command | Description |
| --- | --- |
| `opk hello [name]` | Smoke test. |
| `opk info` | Project + environment summary. |
| `opk doctor` | Check the local toolchain. |
| `opk version` | Print the CLI version. |
| `opk dev [--port] [--reload]` | Run the backend dev server. |

## Quality & build

| Command | Description |
| --- | --- |
| `opk test` | Run the pytest suite. |
| `opk lint` | Run ruff checks. |
| `opk fmt` | Format with ruff. |
| `opk build web` | Build the production web bundle. |
| `opk build desktop` | Package the desktop app into `./dist` (PyInstaller; plus electron-builder or `tauri build` for the sidecar shells). |
| `opk openapi [-o path]` | Export the OpenAPI schema. |
| `opk gen` | Regenerate the typed frontend client from the schema. |
| `opk gen --check` | Drift gate: verify the committed client matches the API (used in CI). |
| `opk product check` | Validate `APP_PRODUCT_ROUTERS` and list the endpoints supplied by existing product code. |

## Desktop

Generated only when a desktop framework was selected; the surface is identical for pywebview, Electron and Tauri.

| Command | Description |
| --- | --- |
| `opk desktop` | Run the desktop app: a native window over the core (in-process or sidecar). |
| `opk desktop --check` | Headless smoke test (boot + `/api/health`, no window). |

## Docker stack

Generated only when Docker was selected.

| Command | Description |
| --- | --- |
| `opk stack up` | Build and start the stack; web UI on `http://localhost:8080`. |
| `opk stack down [--volumes]` | Stop the stack; `--volumes` wipes its data. |
| `opk stack logs [service]` | Follow logs. |
| `opk stack ps` | Services and health. |
| `opk stack share` | Start the stack + Cloudflare quick tunnel; prints the public URL. |

## Database

| Command | Description |
| --- | --- |
| `opk db migrate` | Apply pending migrations. |
| `opk db revision -m "msg"` | Autogenerate a migration from model changes. |
| `opk db downgrade [rev]` | Revert migrations. |
| `opk db reset` | Drop everything and re-apply. |

## Data (demo)

| Command | Description |
| --- | --- |
| `opk project add\|list` | Manage projects. |
| `opk note add\|list` | Manage/search notes. |

## Plugins

| Command | Description |
| --- | --- |
| `opk plugin list` | List installed plugins and state. |
| `opk plugin enable\|disable <id>` | Toggle a plugin. |
| `opk plugin install <path>` | Editable-install a local plugin. |

Installed, licensed plugins can also contribute their own commands — for example the bundled CLI plugin adds `opk example-cli greet`.

## Marketplace

| Command | Description |
| --- | --- |
| `opk marketplace list` | Installed plugins + catalog items, with lock/install state. |
| `opk marketplace unlock <token>` | Activate a license token and show the resulting entitlements. |
| `opk marketplace install <id>` | Install a catalog extension into the current environment. |

## Users

Accounts for hosted deployments (enforced when `APP_AUTH_ENABLED=true` — see [Auth](auth.md)).

| Command | Description |
| --- | --- |
| `opk user add <email> [--admin] [--password …]` | Create an account (prompts for the password if omitted). |
| `opk user list` | List accounts. |
| `opk user passwd <email>` | Reset a password (revokes that user's sessions). |
| `opk user remove <email>` | Delete an account. |

## License

Customer side:

| Command | Description |
| --- | --- |
| `opk license status` | Show the resolved license (plan, licensee, expiry, source). |
| `opk license install <token>` | Activate a license token (writes the license file). |
| `opk license verify <token>` | Verify a token offline and print its contents. |

Vendor side (you, selling your product):

| Command | Description |
| --- | --- |
| `opk license keygen` | Generate the Ed25519 signing keypair (once; keep the private key secret). |
| `opk license issue --licensee X --plan pro [--days N] [--feature F]` | Sign a license token for a customer. |
