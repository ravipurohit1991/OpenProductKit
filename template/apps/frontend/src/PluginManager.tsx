import { usePlugins, useSetPluginEnabled } from "./client/hooks";

export function PluginManager() {
  const plugins = usePlugins();
  const setEnabled = useSetPluginEnabled();

  return (
    <section>
      <h2 style={{ fontSize: "1rem" }}>Installed plugins</h2>
      <p style={{ color: "#666" }}>
        Discovered via Python entry points. Toggling enable/disable takes effect
        immediately for backend routes.
      </p>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {(plugins.data ?? []).map((p) => (
          <li
            key={p.id}
            style={{ border: "1px solid #ddd", borderRadius: 8, padding: "0.8rem", marginBottom: 8 }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
              <div>
                <strong>{p.name}</strong>{" "}
                <code style={{ fontSize: 12, color: "#888" }}>{p.id}</code>
                <div style={{ color: "#666", fontSize: 14 }}>{p.description}</div>
                <div style={{ fontSize: 12, marginTop: 4, color: "#555" }}>
                  <span>health: {p.health}</span>
                  {p.required_plan && (
                    <span style={{ marginLeft: 10 }}>
                      plan: {p.required_plan} — {p.entitled ? "entitled" : "locked"}
                    </span>
                  )}
                  {p.permissions.length > 0 && (
                    <span style={{ marginLeft: 10 }}>perms: {p.permissions.join(", ")}</span>
                  )}
                </div>
              </div>
              <label style={{ display: "flex", gap: 6, alignItems: "center", whiteSpace: "nowrap" }}>
                <input
                  type="checkbox"
                  checked={p.enabled}
                  disabled={!p.entitled || setEnabled.isPending}
                  onChange={(e) => setEnabled.mutate({ id: p.id, enabled: e.target.checked })}
                />
                {p.enabled ? "enabled" : "disabled"}
              </label>
            </div>
          </li>
        ))}
        {plugins.data?.length === 0 && <li style={{ color: "#999" }}>No plugins installed.</li>}
      </ul>
    </section>
  );
}
