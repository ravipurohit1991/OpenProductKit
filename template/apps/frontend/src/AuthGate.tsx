// Wraps the app when the deployment runs with user accounts. While auth is
// disabled (the default, and always on desktop) it renders children untouched.
// When enabled it shows first-run admin setup, then a login form, and only
// renders the app for a signed-in session.

import { useState } from "react";
import type { ReactNode } from "react";

import { useAuthStatus, useLogin, useLogout, useSetup } from "./client/hooks";
import { APP_NAME } from "./config";

const inputStyle = {
  width: "100%",
  padding: "0.5rem 0.6rem",
  border: "1px solid #ccc",
  borderRadius: 6,
  boxSizing: "border-box",
} as const;

function LoginView({ needsSetup }: { needsSetup: boolean }) {
  const login = useLogin();
  const setup = useSetup();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const action = needsSetup ? setup : login;

  return (
    <main style={{ fontFamily: "system-ui", maxWidth: 380, margin: "6rem auto", padding: "0 1rem" }}>
      <h1 style={{ textAlign: "center" }}>{APP_NAME}</h1>
      <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: "1.2rem", background: "#fafafa" }}>
        <strong>{needsSetup ? "Create the admin account" : "Sign in"}</strong>
        <p style={{ color: "#666", fontSize: 13, margin: "6px 0 12px" }}>
          {needsSetup
            ? "This install has no accounts yet. The first account becomes the administrator."
            : "This deployment requires an account."}
        </p>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (email.trim() && password) action.mutate({ email: email.trim(), password });
          }}
          style={{ display: "flex", flexDirection: "column", gap: 8 }}
        >
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="email"
            autoComplete="username"
            style={inputStyle}
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={needsSetup ? "password (min. 8 characters)" : "password"}
            autoComplete={needsSetup ? "new-password" : "current-password"}
            style={inputStyle}
          />
          <button
            type="submit"
            disabled={action.isPending || !email.trim() || !password}
            style={{ padding: "0.5rem", borderRadius: 6, border: "1px solid #ccc", cursor: "pointer" }}
          >
            {action.isPending ? "…" : needsSetup ? "Create account" : "Sign in"}
          </button>
        </form>
        {action.isError && (
          <p style={{ color: "crimson", fontSize: 13, marginTop: 10 }}>
            {needsSetup
              ? "Could not create the account — check the email and password length."
              : "Invalid email or password."}
          </p>
        )}
      </div>
    </main>
  );
}

// Small header chip: who is signed in + sign out. Renders nothing while auth
// is disabled, so the default (accountless) UI stays exactly as it was.
export function UserMenu() {
  const me = useAuthStatus();
  const logout = useLogout();
  const user = me.data?.user;
  if (!me.data?.auth_enabled || !user) return null;
  return (
    <span style={{ display: "inline-flex", gap: 8, alignItems: "center", fontSize: 13, color: "#666" }}>
      <span>
        {user.email}
        {user.is_admin ? " · admin" : ""}
      </span>
      <button
        onClick={() => logout.mutate()}
        disabled={logout.isPending}
        style={{ padding: "0.2rem 0.6rem", borderRadius: 6, border: "1px solid #ccc", cursor: "pointer" }}
      >
        Sign out
      </button>
    </span>
  );
}

export function AuthGate({ children }: { children: ReactNode }) {
  const me = useAuthStatus();

  if (me.isLoading) {
    return <main style={{ fontFamily: "system-ui", textAlign: "center", marginTop: "6rem", color: "#999" }}>Loading…</main>;
  }
  if (me.isError) {
    return (
      <main style={{ fontFamily: "system-ui", textAlign: "center", marginTop: "6rem", color: "crimson" }}>
        The API is not reachable. Is the backend running?
      </main>
    );
  }
  const status = me.data;
  if (status?.auth_enabled && !status.user) {
    return <LoginView needsSetup={status.needs_setup} />;
  }
  return <>{children}</>;
}
