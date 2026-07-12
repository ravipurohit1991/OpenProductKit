import { useState } from "react";

import { CLI_NAME } from "./config";
import {
  useInstallExtension,
  useLicense,
  useMarketplace,
  useSetPluginEnabled,
  useUnlockLicense,
  type MarketplaceItem,
} from "./client/hooks";

function planBadge(item: MarketplaceItem) {
  if (!item.required_plan) return <span style={{ color: "#2a7", fontSize: 12 }}>free</span>;
  return (
    <span style={{ color: item.entitled ? "#2a7" : "#a52", fontSize: 12 }}>
      {item.required_plan} plan {item.entitled ? "· unlocked" : "· locked"}
    </span>
  );
}

function UnlockBox() {
  const license = useLicense();
  const unlock = useUnlockLicense();
  const [token, setToken] = useState("");

  const plan = license.data && license.data.valid ? license.data.plan : "free";

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: 8,
        padding: "0.8rem 1rem",
        marginBottom: 16,
        background: "#fafafa",
      }}
    >
      <strong style={{ fontSize: 14 }}>Unlock with a license token</strong>
      <p style={{ color: "#666", fontSize: 13, margin: "4px 0 8px" }}>
        Current plan: <code>{plan}</code>. Paste the signed token you received after
        purchase; paid extensions and features unlock immediately. Vendors issue
        tokens with <code>{CLI_NAME} license issue</code>.
      </p>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (token.trim()) unlock.mutate(token.trim(), { onSuccess: () => setToken("") });
        }}
        style={{ display: "flex", gap: 8 }}
      >
        <input
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="Paste license token…"
          style={{ flex: 1, padding: "0.4rem 0.6rem", border: "1px solid #ccc", borderRadius: 6 }}
        />
        <button
          type="submit"
          disabled={unlock.isPending || !token.trim()}
          style={{ padding: "0.4rem 0.9rem", borderRadius: 6, border: "1px solid #ccc", cursor: "pointer" }}
        >
          {unlock.isPending ? "Unlocking…" : "Unlock"}
        </button>
      </form>
      {unlock.isSuccess && (
        <p style={{ color: "#2a7", fontSize: 13, marginTop: 8 }}>{unlock.data.message}</p>
      )}
      {unlock.isError && (
        <p style={{ color: "crimson", fontSize: 13, marginTop: 8 }}>
          That token was not accepted. Check it was copied whole and issued for this product.
        </p>
      )}
    </div>
  );
}

function InstallButton({ item }: { item: MarketplaceItem }) {
  const install = useInstallExtension();
  if (!item.entitled) {
    return <span style={{ fontSize: 13, color: "#a52" }}>Unlock a license to install</span>;
  }
  return (
    <span style={{ display: "inline-flex", gap: 8, alignItems: "center" }}>
      {install.isError && (
        <span style={{ color: "crimson", fontSize: 12 }}>Install failed — see the backend log.</span>
      )}
      <button
        onClick={() => install.mutate(item.id)}
        disabled={install.isPending}
        style={{ padding: "0.3rem 0.9rem", borderRadius: 6, border: "1px solid #ccc", cursor: "pointer" }}
      >
        {install.isPending ? "Installing…" : "Install"}
      </button>
    </span>
  );
}

export function Marketplace() {
  const marketplace = useMarketplace();
  const setEnabled = useSetPluginEnabled();

  return (
    <section>
      <h2 style={{ fontSize: "1rem" }}>Marketplace</h2>
      <p style={{ color: "#666" }}>
        Extensions for this product — installed ones can be toggled, paid ones unlock
        with a license token, and catalog items show how to install them.
      </p>
      <UnlockBox />
      <ul style={{ listStyle: "none", padding: 0 }}>
        {(marketplace.data ?? []).map((item) => (
          <li
            key={item.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: "0.8rem",
              marginBottom: 8,
              opacity: item.installed && !item.entitled ? 0.85 : 1,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
              <div>
                <strong>{item.name}</strong>{" "}
                <code style={{ fontSize: 12, color: "#888" }}>
                  {item.id}
                  {item.version ? ` v${item.version}` : ""}
                </code>
                <div style={{ color: "#666", fontSize: 14 }}>{item.description}</div>
                <div style={{ fontSize: 12, marginTop: 4, display: "flex", gap: 12 }}>
                  {planBadge(item)}
                  <span style={{ color: "#888" }}>
                    {item.installed ? (item.enabled ? "installed · enabled" : "installed · disabled") : "not installed"}
                  </span>
                  {item.homepage && (
                    <a href={item.homepage} target="_blank" rel="noreferrer" style={{ fontSize: 12 }}>
                      details
                    </a>
                  )}
                </div>
                {!item.installed && !item.installable && item.install_hint && (
                  <div style={{ marginTop: 6, fontSize: 13 }}>
                    Install it with: <code>{item.install_hint}</code>
                  </div>
                )}
              </div>
              {!item.installed && item.installable && <InstallButton item={item} />}
              {item.installed && (
                <label style={{ display: "flex", gap: 6, alignItems: "center", whiteSpace: "nowrap" }}>
                  <input
                    type="checkbox"
                    checked={item.enabled}
                    disabled={!item.entitled || setEnabled.isPending}
                    onChange={(e) => setEnabled.mutate({ id: item.id, enabled: e.target.checked })}
                  />
                  {item.enabled ? "enabled" : "disabled"}
                </label>
              )}
            </div>
          </li>
        ))}
        {marketplace.data?.length === 0 && (
          <li style={{ color: "#999" }}>Nothing here yet — add items to marketplace/catalog.json.</li>
        )}
      </ul>
    </section>
  );
}
