// TanStack Query hooks over the generated typed client. These are intentionally
// thin and hand-owned; the *types* (Project, Note, request bodies, query params)
// all come from the generated schema, so the compiler catches API drift for you.

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { client } from "./client";
import type { components } from "./schema";

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

// --- plugins ---------------------------------------------------------------

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

// --- license -----------------------------------------------------------------

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
