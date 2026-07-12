// Admin tab: manage user accounts. Only shown (see App.tsx) when the
// deployment runs with APP_AUTH_ENABLED and the signed-in user is an admin.

import { useState } from "react";

import {
  useAuthStatus,
  useCreateUser,
  useDeleteUser,
  useUsers,
} from "./client/hooks";
import { CLI_NAME } from "./config";

export function UsersPanel() {
  const me = useAuthStatus();
  const isAdmin = Boolean(me.data?.user?.is_admin);
  const users = useUsers(isAdmin);
  const createUser = useCreateUser();
  const deleteUser = useDeleteUser();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isNewAdmin, setIsNewAdmin] = useState(false);

  return (
    <section>
      <h2 style={{ fontSize: "1rem" }}>Users</h2>
      <p style={{ color: "#666" }}>
        Accounts for this deployment. Admins manage plugins, licenses and users;
        the CLI equivalent is <code>{CLI_NAME} user add|list|remove|passwd</code>.
      </p>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (!email.trim() || !password) return;
          createUser.mutate(
            { email: email.trim(), password, is_admin: isNewAdmin },
            {
              onSuccess: () => {
                setEmail("");
                setPassword("");
                setIsNewAdmin(false);
              },
            },
          );
        }}
        style={{
          display: "flex",
          gap: 8,
          alignItems: "center",
          border: "1px solid #ddd",
          borderRadius: 8,
          padding: "0.8rem",
          marginBottom: 16,
          background: "#fafafa",
          flexWrap: "wrap",
        }}
      >
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email"
          style={{ flex: 2, minWidth: 160, padding: "0.4rem 0.6rem", border: "1px solid #ccc", borderRadius: 6 }}
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password (min. 8 chars)"
          autoComplete="new-password"
          style={{ flex: 2, minWidth: 160, padding: "0.4rem 0.6rem", border: "1px solid #ccc", borderRadius: 6 }}
        />
        <label style={{ display: "flex", gap: 4, alignItems: "center", fontSize: 13 }}>
          <input type="checkbox" checked={isNewAdmin} onChange={(e) => setIsNewAdmin(e.target.checked)} />
          admin
        </label>
        <button
          type="submit"
          disabled={createUser.isPending || !email.trim() || password.length < 8}
          style={{ padding: "0.4rem 0.9rem", borderRadius: 6, border: "1px solid #ccc", cursor: "pointer" }}
        >
          {createUser.isPending ? "Adding…" : "Add user"}
        </button>
      </form>
      {createUser.isError && (
        <p style={{ color: "crimson", fontSize: 13 }}>
          Could not create the user — the email may already exist, or the password is too short.
        </p>
      )}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {(users.data ?? []).map((user) => (
          <li
            key={user.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: "0.6rem 0.8rem",
              marginBottom: 8,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span>
              {user.email}{" "}
              <span style={{ fontSize: 12, color: user.is_admin ? "#2a7" : "#888" }}>
                {user.is_admin ? "admin" : "user"}
              </span>
            </span>
            <button
              onClick={() => deleteUser.mutate(user.id)}
              disabled={deleteUser.isPending || user.id === me.data?.user?.id}
              title={user.id === me.data?.user?.id ? "You cannot delete your own account" : "Delete this account"}
              style={{ padding: "0.2rem 0.6rem", borderRadius: 6, border: "1px solid #ccc", cursor: "pointer" }}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
