import { useState } from "react";

import { AuthGate, UserMenu } from "./AuthGate";
import { LicensePanel } from "./LicensePanel";
import { Marketplace } from "./Marketplace";
import { PluginManager } from "./PluginManager";
import { UsersPanel } from "./UsersPanel";
import { VaultView } from "./VaultView"; // [demo]
import { useAuthStatus } from "./client/hooks";
import { APP_NAME } from "./config";

type Tab = "vault" | "marketplace" | "plugins" | "license" | "users";

export function App() {
  const [tab, setTab] = useState<Tab>("vault");
  const me = useAuthStatus();
  // The Users tab only exists on deployments with accounts, for admins.
  const showUsers = Boolean(me.data?.auth_enabled && me.data.user?.is_admin);

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
    <AuthGate>
      <main style={{ fontFamily: "system-ui", maxWidth: 900, margin: "2.5rem auto", padding: "0 1rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
          <h1>{APP_NAME}</h1>
          <UserMenu />
        </div>
        <nav style={{ display: "flex", gap: 8, margin: "1rem 0 1.5rem" }}>
          {tabButton("vault", "Resource Vault")} {/* [demo] */}
          {tabButton("marketplace", "Marketplace")}
          {tabButton("plugins", "Plugins")}
          {tabButton("license", "License")}
          {showUsers && tabButton("users", "Users")}
        </nav>

        {tab === "vault" && <VaultView />} {/* [demo] */}
        {tab === "marketplace" && <Marketplace />}
        {tab === "plugins" && <PluginManager />}
        {tab === "license" && <LicensePanel />}
        {tab === "users" && showUsers && <UsersPanel />}
      </main>
    </AuthGate>
  );
}
