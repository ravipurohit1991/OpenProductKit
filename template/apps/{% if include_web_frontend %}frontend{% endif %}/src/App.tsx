import { useState } from "react";

import { LicensePanel } from "./LicensePanel";
import { Marketplace } from "./Marketplace";
import { PluginManager } from "./PluginManager";
import { VaultView } from "./VaultView"; // [demo]
import { APP_NAME } from "./config";

type Tab = "vault" | "marketplace" | "plugins" | "license";

export function App() {
  const [tab, setTab] = useState<Tab>("vault");

  const tabButton = (id: Tab, label: string) => (
    <button
      onClick={() => setTab(id)}
      style={{
        padding: "0.4rem 0.9rem",
        border: "1px solid #ddd",
        borderRadius: 6,
        background: tab === id ? "#eef" : "white",
        cursor: "pointer",
        fontWeight: tab === id ? 600 : 400,
      }}
    >
      {label}
    </button>
  );

  return (
    <main style={{ fontFamily: "system-ui", maxWidth: 900, margin: "2.5rem auto", padding: "0 1rem" }}>
      <h1>{APP_NAME}</h1>
      <nav style={{ display: "flex", gap: 8, margin: "1rem 0 1.5rem" }}>
        {tabButton("vault", "Resource Vault")} {/* [demo] */}
        {tabButton("marketplace", "Marketplace")}
        {tabButton("plugins", "Plugins")}
        {tabButton("license", "License")}
      </nav>

      {tab === "vault" && <VaultView />} {/* [demo] */}
      {tab === "marketplace" && <Marketplace />}
      {tab === "plugins" && <PluginManager />}
      {tab === "license" && <LicensePanel />}
    </main>
  );
}
