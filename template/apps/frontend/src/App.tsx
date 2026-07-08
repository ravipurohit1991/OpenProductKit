import { useCallback, useEffect, useState, type FormEvent } from "react";

import {
  createNote,
  createProject,
  getNotes,
  getProjects,
  type Note,
  type Project,
} from "./api";
import { APP_NAME } from "./config";

export function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [notes, setNotes] = useState<Note[]>([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState<string | null>(null);

  const [newProject, setNewProject] = useState("");
  const [noteTitle, setNoteTitle] = useState("");
  const [noteTags, setNoteTags] = useState("");

  const refreshProjects = useCallback(async () => {
    const list = await getProjects();
    setProjects(list);
    setSelected((cur) => cur ?? list[0]?.id ?? null);
  }, []);

  const refreshNotes = useCallback(async () => {
    if (!selected) {
      setNotes([]);
      return;
    }
    setNotes(await getNotes({ projectId: selected, q: query }));
  }, [selected, query]);

  useEffect(() => {
    refreshProjects().catch((e) => setError(String(e)));
  }, [refreshProjects]);

  useEffect(() => {
    refreshNotes().catch((e) => setError(String(e)));
  }, [refreshNotes]);

  async function addProject(e: FormEvent) {
    e.preventDefault();
    if (!newProject.trim()) return;
    const p = await createProject(newProject.trim());
    setNewProject("");
    setSelected(p.id);
    await refreshProjects();
  }

  async function addNote(e: FormEvent) {
    e.preventDefault();
    if (!selected || !noteTitle.trim()) return;
    try {
      await createNote({
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
      await refreshNotes();
    } catch (err) {
      setError(String(err));
    }
  }

  return (
    <main style={{ fontFamily: "system-ui", maxWidth: 900, margin: "2.5rem auto", padding: "0 1rem" }}>
      <h1>{APP_NAME}</h1>
      <p style={{ color: "#666" }}>
        Resource Vault demo — projects, notes, tags and search, all flowing through one core.
      </p>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <div style={{ display: "grid", gridTemplateColumns: "220px 1fr", gap: 24 }}>
        <section>
          <h2 style={{ fontSize: "1rem" }}>Projects</h2>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {projects.map((p) => (
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
            {projects.length === 0 && <li style={{ color: "#999" }}>No projects yet.</li>}
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
            {notes.map((n) => (
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
            {selected && notes.length === 0 && <li style={{ color: "#999" }}>No matching notes.</li>}
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
    </main>
  );
}
