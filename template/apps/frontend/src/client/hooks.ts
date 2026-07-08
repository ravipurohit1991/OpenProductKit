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
