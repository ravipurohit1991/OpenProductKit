// [demo] Resource Vault sample UI — replace with your product's views (see AGENTS.md).
import { useEffect, useState, type FormEvent } from "react";

import { LockedFeatureCard } from "./LockedFeatureCard";
import {
  useCreateNote,
  useCreateProject,
  useEntitlement,
  useExportVault,
  useNotes,
  useProjects,
} from "./client/hooks";

export function VaultView() {
  const [selected, setSelected] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [newProject, setNewProject] = useState("");
  const [noteTitle, setNoteTitle] = useState("");
  const [noteTags, setNoteTags] = useState("");
  const [error, setError] = useState<string | null>(null);

  const projects = useProjects();
  const notes = useNotes({ project_id: selected ?? undefined, q: query || undefined });
  const createProject = useCreateProject();
  const createNote = useCreateNote();
  const exportEntitlement = useEntitlement("pro");
  const exportVault = useExportVault();

  async function downloadExport() {
    try {
      const data = await exportVault.mutateAsync();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "vault-export.json";
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(String(err));
    }
  }

  useEffect(() => {
    if (selected === null && projects.data && projects.data.length > 0) {
      setSelected(projects.data[0].id);
    }
  }, [projects.data, selected]);

  async function addProject(e: FormEvent) {
    e.preventDefault();
    if (!newProject.trim()) return;
    const created = await createProject.mutateAsync(newProject.trim());
    setNewProject("");
    setSelected(created.id);
  }

  async function addNote(e: FormEvent) {
    e.preventDefault();
    if (!selected || !noteTitle.trim()) return;
    try {
      await createNote.mutateAsync({
        project_id: selected,
        title: noteTitle.trim(),
        tags: noteTags
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      });
      setNoteTitle("");
      setNoteTags("");
      setError(null);
    } catch (err) {
      setError(String(err));
    }
  }

  return (
    <>
      <p style={{ color: "#666" }}>
        Resource Vault demo — projects, notes, tags and search, over a typed client
        generated from the backend OpenAPI schema.
      </p>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ display: "grid", gridTemplateColumns: "220px 1fr", gap: 24 }}>
        <section>
          <h2 style={{ fontSize: "1rem" }}>Projects</h2>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {(projects.data ?? []).map((p) => (
              <li key={p.id}>
                <button
                  onClick={() => setSelected(p.id)}
                  style={{
                    display: "block",
                    width: "100%",
                    textAlign: "left",
                    padding: "0.4rem 0.5rem",
                    marginBottom: 4,
                    border: "1px solid #ddd",
                    borderRadius: 6,
                    background: p.id === selected ? "#eef" : "white",
                    cursor: "pointer",
                  }}
                >
                  {p.name}
                </button>
              </li>
            ))}
            {projects.data?.length === 0 && <li style={{ color: "#999" }}>No projects yet.</li>}
          </ul>
          <form onSubmit={addProject} style={{ display: "flex", gap: 4 }}>
            <input
              value={newProject}
              onChange={(e) => setNewProject(e.target.value)}
              placeholder="New project…"
              style={{ flex: 1, padding: "0.4rem" }}
            />
            <button type="submit">+</button>
          </form>
        </section>

        <section>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2 style={{ fontSize: "1rem" }}>Notes</h2>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search…"
              style={{ padding: "0.4rem", width: 200 }}
            />
          </div>

          <ul style={{ listStyle: "none", padding: 0 }}>
            {(notes.data ?? []).map((n) => (
              <li key={n.id} style={{ borderBottom: "1px solid #eee", padding: "0.6rem 0" }}>
                <strong>{n.title}</strong>
                {n.tags.length > 0 && (
                  <span style={{ marginLeft: 8 }}>
                    {n.tags.map((t) => (
                      <code
                        key={t}
                        style={{ background: "#f2f2f2", borderRadius: 4, padding: "1px 6px", marginRight: 4, fontSize: 12 }}
                      >
                        {t}
                      </code>
                    ))}
                  </span>
                )}
              </li>
            ))}
            {selected && notes.data?.length === 0 && <li style={{ color: "#999" }}>No matching notes.</li>}
            {!selected && <li style={{ color: "#999" }}>Create or select a project.</li>}
          </ul>

          {selected && (
            <form onSubmit={addNote} style={{ display: "flex", gap: 6, marginTop: 8 }}>
              <input
                value={noteTitle}
                onChange={(e) => setNoteTitle(e.target.value)}
                placeholder="Note title…"
                style={{ flex: 2, padding: "0.5rem" }}
              />
              <input
                value={noteTags}
                onChange={(e) => setNoteTags(e.target.value)}
                placeholder="tags, comma, separated"
                style={{ flex: 1, padding: "0.5rem" }}
              />
              <button type="submit" style={{ padding: "0.5rem 1rem" }}>
                Add
              </button>
            </form>
          )}
        </section>
      </div>

      <section style={{ marginTop: 28 }}>
        {exportEntitlement.entitled ? (
          <button
            onClick={downloadExport}
            disabled={exportVault.isPending}
            style={{ padding: "0.5rem 1rem" }}
          >
            {exportVault.isPending ? "Exporting…" : "Export vault (JSON)"}
          </button>
        ) : (
          <LockedFeatureCard title="Export vault" requiredPlan="pro">
            {" "}
            A license-gated feature: install a license to unlock it.
          </LockedFeatureCard>
        )}
      </section>
    </>
  );
}
