import type { ReactNode } from "react";

import { useEntitlement } from "./client/hooks";

/** Drop-in placeholder rendered where a feature would be if it were licensed. */
export function LockedFeatureCard({
  title,
  requiredPlan,
  children,
}: {
  title: string;
  requiredPlan: string;
  children?: ReactNode;
}) {
  const { plan } = useEntitlement(requiredPlan);
  return (
    <div
      style={{
        border: "1px dashed #bbb",
        borderRadius: 8,
        padding: "0.9rem 1rem",
        background: "#fafafa",
        color: "#555",
      }}
    >
      <strong>
        <span aria-hidden="true">{"\u{1F512}"}</span> {title}
      </strong>
      <p style={{ margin: "0.4rem 0 0", fontSize: 14 }}>
        Requires the <strong>{requiredPlan}</strong> plan; this install is on{" "}
        <strong>{plan}</strong>.{children}
      </p>
    </div>
  );
}
