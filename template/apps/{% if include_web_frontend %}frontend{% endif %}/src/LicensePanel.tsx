import { useLicense } from "./client/hooks";
import { CLI_NAME } from "./config";

export function LicensePanel() {
  const license = useLicense();
  const data = license.data;

  if (license.isLoading) return <p style={{ color: "#999" }}>Loading license…</p>;
  if (!data) return <p style={{ color: "crimson" }}>Could not load license status.</p>;

  const row = (label: string, value: string) => (
    <tr>
      <td style={{ padding: "0.3rem 1.2rem 0.3rem 0", color: "#666" }}>{label}</td>
      <td style={{ padding: "0.3rem 0" }}>{value}</td>
    </tr>
  );

  return (
    <section>
      <h2 style={{ fontSize: "1rem" }}>License</h2>
      <table style={{ borderCollapse: "collapse", fontSize: 14 }}>
        <tbody>
          {row("Plan", data.valid ? data.plan : "free")}
          {row("Valid", data.valid ? "yes" : "no")}
          {row("Licensee", data.licensee || "—")}
          {row("Features", data.features.length > 0 ? data.features.join(", ") : "—")}
          {row("Expires", data.expires_at ? data.expires_at.slice(0, 10) : "never")}
          {row("Source", data.source)}
        </tbody>
      </table>
      {data.message && (
        <p style={{ color: "#666", fontSize: 14, marginTop: 8 }}>{data.message}</p>
      )}
      {data.source === "dev" && (
        <div
          style={{
            border: "1px solid #e5d9a8",
            background: "#fdf8e3",
            borderRadius: 8,
            padding: "0.8rem 1rem",
            marginTop: 12,
            fontSize: 14,
            color: "#665c2e",
          }}
        >
          This is the development stub. To license a real install, issue a token with{" "}
          <code>{CLI_NAME} license issue</code> and activate it with{" "}
          <code>{CLI_NAME} license install &lt;token&gt;</code>.
        </div>
      )}
    </section>
  );
}
