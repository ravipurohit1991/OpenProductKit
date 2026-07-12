// TanStack Query hooks over the generated typed client. These are intentionally
// thin and hand-owned; the *types* (Project, Note, request bodies, query params)
// all come from the generated schema, so the compiler catches API drift for you.

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { client, setAuthToken } from "./client";
import type { components } from "./schema";

// --- [demo] Resource Vault hooks — replace with hooks for your own API --------

export type Project = components["schemas"]["ProjectOut"];
export type Note = components["schemas"]["NoteOut"];

// openapi-typescript marks fields that have a schema `default` (body, tags) as
// required. That is right for responses but clunky for a request body, so we
// derive a friendlier input type from the same schema — still fully generated,
// just with the defaulted fields made optional.
export type CreateNoteInput = Pick<
  components["schemas"]["NoteIn"],
  "project_id" | "title"
> &
  Partial<Pick<components["schemas"]["NoteIn"], "body" | "tags">>;

export type NoteFilters = {
  project_id?: string;
  tag?: string;
  q?: string;
};

export const queryKeys = {
  projects: ["projects"] as const,
  notes: (filters: NoteFilters) => ["notes", filters] as const,
};

export function useProjects() {
  return useQuery({
    queryKey: queryKeys.projects,
    queryFn: async () => {
      const { data, error } = await client.GET("/api/projects");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

export function useCreateProject() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (name: string) => {
      const { data, error } = await client.POST("/api/projects", {
        body: { name },
      });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: queryKeys.projects }),
  });
}

export function useNotes(filters: NoteFilters) {
  return useQuery({
    queryKey: queryKeys.notes(filters),
    enabled: Boolean(filters.project_id),
    queryFn: async () => {
      const { data, error } = await client.GET("/api/notes", {
        params: { query: filters },
      });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

export function useCreateNote() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: CreateNoteInput) => {
      const { data, error } = await client.POST("/api/notes", {
        body: { body: "", tags: [], ...input },
      });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes"] }),
  });
}

// --- plugins (framework — keep) ---------------------------------------------

export type PluginInfo = components["schemas"]["PluginOut"];

export function usePlugins() {
  return useQuery({
    queryKey: ["plugins"],
    queryFn: async () => {
      const { data, error } = await client.GET("/api/plugins");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

// --- auth (framework — keep) ---------------------------------------------------
// Inert until the deployment sets APP_AUTH_ENABLED=true; /api/auth/me then
// drives the AuthGate (login / first-run setup) around the whole app.

export type AuthStatus = components["schemas"]["AuthStatusOut"];
export type AuthUser = components["schemas"]["UserOut"];

export function useAuthStatus() {
  return useQuery({
    queryKey: ["auth", "me"],
    retry: false,
    queryFn: async () => {
      const { data, error } = await client.GET("/api/auth/me");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

function useCredentialMutation(path: "/api/auth/login" | "/api/auth/setup") {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (creds: { email: string; password: string }) => {
      const { data, error } = await client.POST(path, { body: creds });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: (data) => {
      setAuthToken(data.token);
      qc.clear(); // every cached query was fetched unauthenticated — refetch all
    },
  });
}

export function useLogin() {
  return useCredentialMutation("/api/auth/login");
}

// First-run bootstrap: creates the initial admin account, then logs it in.
export function useSetup() {
  return useCredentialMutation("/api/auth/setup");
}

export function useLogout() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const { data, error } = await client.POST("/api/auth/logout");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSettled: () => {
      setAuthToken(null);
      qc.clear();
    },
  });
}

export function useUsers(enabled: boolean) {
  return useQuery({
    queryKey: ["auth", "users"],
    enabled,
    queryFn: async () => {
      const { data, error } = await client.GET("/api/auth/users");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

export function useCreateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: { email: string; password: string; is_admin: boolean }) => {
      const { data, error } = await client.POST("/api/auth/users", { body: input });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["auth", "users"] }),
  });
}

export function useDeleteUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (userId: string) => {
      const { data, error } = await client.DELETE("/api/auth/users/{user_id}", {
        params: { path: { user_id: userId } },
      });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["auth", "users"] }),
  });
}

// --- marketplace (framework — keep) -------------------------------------------

export type MarketplaceItem = components["schemas"]["MarketplaceItemOut"];

export function useMarketplace() {
  return useQuery({
    queryKey: ["marketplace"],
    queryFn: async () => {
      const { data, error } = await client.GET("/api/marketplace");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

// Install a catalog extension into the running app (only offered when the
// server reports it installable). New plugin routes mount live — no restart.
export function useInstallExtension() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data, error } = await client.POST("/api/marketplace/install", {
        body: { id },
      });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["marketplace"] });
      qc.invalidateQueries({ queryKey: ["plugins"] });
    },
  });
}

// Activate a signed license token. On success every gate re-reads entitlements,
// so locked plugins and features unlock without a restart.
export function useUnlockLicense() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (token: string) => {
      const { data, error } = await client.POST("/api/marketplace/unlock", {
        body: { token },
      });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["license"] });
      qc.invalidateQueries({ queryKey: ["plugins"] });
      qc.invalidateQueries({ queryKey: ["marketplace"] });
    },
  });
}

// --- license (framework — keep) ------------------------------------------------

export type LicenseStatus = components["schemas"]["LicenseOut"];

export function useLicense() {
  return useQuery({
    queryKey: ["license"],
    queryFn: async () => {
      const { data, error } = await client.GET("/api/license");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

// Compare the licensed plan against a required plan using the server-provided
// rank map, so no tier ordering is hardcoded client-side. While the license is
// still loading, features report as not entitled (locked-by-default).
export function useEntitlement(requiredPlan?: string | null) {
  const license = useLicense();
  const data = license.data;
  const plan = data && data.valid ? data.plan : "free";
  const entitled = requiredPlan
    ? data != null &&
      (data.plans[plan] ?? 0) >= (data.plans[requiredPlan] ?? Number.POSITIVE_INFINITY)
    : true;
  return { entitled, plan, isLoading: license.isLoading, license: data };
}

// [demo] Gated-feature hook for the sample export route.
export function useExportVault() {
  return useMutation({
    mutationFn: async () => {
      const { data, error } = await client.GET("/api/export");
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
  });
}

export function useSetPluginEnabled() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, enabled }: { id: string; enabled: boolean }) => {
      const params = { path: { plugin_id: id } };
      const { data, error } = enabled
        ? await client.POST("/api/plugins/{plugin_id}/enable", { params })
        : await client.POST("/api/plugins/{plugin_id}/disable", { params });
      if (error) throw new Error(JSON.stringify(error));
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["plugins"] }),
  });
}
