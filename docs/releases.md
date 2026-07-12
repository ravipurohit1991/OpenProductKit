# Releases & auto-update

Generated projects with a desktop shell ship `.github/workflows/release.yml`:
push a version tag and GitHub Actions builds the desktop app on **Windows,
macOS and Linux** and attaches the installers to a GitHub Release.

```bash
git tag v0.2.0 && git push origin v0.2.0
```

Want a dry run first? Trigger the workflow manually (*workflow_dispatch*) —
the same builds land as workflow artifacts instead of a release.

## What each shell produces

| Shell | Attached to the release |
| --- | --- |
| pywebview | `<slug>-windows.zip`, `<slug>-macos.tar.gz`, `<slug>-linux.tar.gz` (PyInstaller onedir; tar keeps executable bits) |
| Electron | NSIS `.exe`, `.dmg`, `.AppImage`/`.zip` — plus `latest*.yml`, the electron-updater feed |
| Tauri | `.msi` + NSIS `.exe`, `.dmg`, `.AppImage`, `.deb` |

!!! tip "Plugins ride along"
    `opk build desktop` bundles every plugin installed in the build
    environment — their modules *and* their dist-info metadata
    (`--copy-metadata`), so entry-point discovery works inside the frozen
    build. Install the extensions you want to ship (e.g. `uv add
    <slug>-plugin-reports`) before tagging.

## Code signing (yours to wire)

The workflow builds **unsigned** on purpose: signing needs your certificates,
your Apple/Microsoft accounts and your judgment. When you're ready:

- **Windows**: an OV/EV code-signing cert or Azure Trusted Signing;
  `signtool` for PyInstaller output, `win.certificateSubjectName` &
  friends for electron-builder, `bundle.windows` config for Tauri.
- **macOS**: a Developer ID certificate + notarization (`notarytool`).
  Unsigned apps trip Gatekeeper — treat signing as required for macOS
  distribution. electron-builder and Tauri both automate the notarize step
  once credentials are in CI secrets.

Store secrets in the repo's Actions secrets; never in the workflow file.

## Auto-update

Each shell updates by its own native mechanism — here is the wiring per
framework, in increasing order of effort:

### Electron (mostly wired)

`electron-builder` is already configured with `publish: {"provider":
"github"}`, so builds produce `latest*.yml` and the release workflow uploads
them next to the installers — that *is* the update feed. To consume it:

```bash
pnpm -C apps/desktop-electron add electron-updater
```

```js
// main.js, after app.whenReady()
const { autoUpdater } = require("electron-updater");
autoUpdater.checkForUpdatesAndNotify();
```

Notes: updates only apply to packaged builds; macOS requires the app to be
signed; private repos need a token at runtime (prefer public releases).

### Tauri

Tauri v2's updater is a plugin with its own signing keypair:

1. `pnpm -C apps/desktop-tauri tauri signer generate` — keep the private key
   in CI secrets, put the public key in `tauri.conf.json` under
   `plugins.updater.pubkey`.
2. Add `@tauri-apps/plugin-updater` and set `createUpdaterArtifacts: true` in
   the bundle config so builds emit `.sig` files and `latest.json`.
3. Point `plugins.updater.endpoints` at your release's `latest.json` URL.

The [Tauri updater guide](https://v2.tauri.app/plugin/updater/) covers the
details; the release workflow needs no changes beyond uploading the extra
artifacts.

### pywebview (check, don't self-patch)

PyInstaller apps have no native updater. The honest pattern is
**check-and-point**: compare the running version against the latest GitHub
release and open the download page —

```python
import json, urllib.request, webbrowser

def check_for_update(current: str, repo: str = "you/your-product") -> None:
    with urllib.request.urlopen(
        f"https://api.github.com/repos/{repo}/releases/latest", timeout=5
    ) as resp:
        latest = json.load(resp)["tag_name"].lstrip("v")
    if latest != current:
        webbrowser.open(f"https://github.com/{repo}/releases/latest")
```

For true in-place updates, distribute through a package manager instead
(winget / Homebrew / your MSI infrastructure) — self-patching executables
are a support burden and an antivirus magnet.

## Versioning

The tag is the release version. Keep the app's own versions
(`pyproject.toml`, `apps/desktop-*/package.json`, `tauri.conf.json`) in step
when you bump — CI won't stop you from tagging `v2.0.0` around a `0.1.0`
binary, but your users will notice.
