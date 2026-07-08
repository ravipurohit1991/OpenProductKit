// Minimal fetch wrapper. In P3 this hand-written client is replaced by one
// generated from the backend's OpenAPI schema.

export type Project = {
  id: string;
  name: string;
  created_at: string;
};

export type Note = {
  id: string;
  project_id: string;
  title: string;
  body: string;
  tags: string[];
  created_at: string;
};

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export function getProjects(): Promise<Project[]> {
  return fetch("/api/projects").then((r) => json<Project[]>(r));
}

export function createProject(name: string): Promise<Project> {
  return fetch("/api/projects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  }).then((r) => json<Project>(r));
}

export function getNotes(params: {
  projectId?: string;
  tag?: string;
  q?: string;
}): Promise<Note[]> {
  const qs = new URLSearchParams();
  if (params.projectId) qs.set("project_id", params.projectId);
  if (params.tag) qs.set("tag", params.tag);
  if (params.q) qs.set("q", params.q);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return fetch(`/api/notes${suffix}`).then((r) => json<Note[]>(r));
}

export function createNote(input: {
  project_id: string;
  title: string;
  body?: string;
  tags?: string[];
}): Promise<Note> {
  return fetch("/api/notes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  }).then((r) => json<Note>(r));
}
