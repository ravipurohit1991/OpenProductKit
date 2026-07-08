import { useEffect, useState, type FormEvent } from "react";

import { APP_NAME } from "./config";

type Note = {
  id: string;
  title: string;
  body: string;
  created_at: string;
};

export function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function load() {
    const res = await fetch("/api/notes");
    setNotes(await res.json());
  }

  useEffect(() => {
    load().catch((e) => setError(String(e)));
  }, []);

  async function addNote(e: FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    const res = await fetch("/api/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    if (!res.ok) {
      setError(`Failed to add note (${res.status})`);
      return;
    }
    setTitle("");
    setError(null);
    await load();
  }

  return (
    <main style={{ fontFamily: "system-ui", maxWidth: 640, margin: "3rem auto", padding: "0 1rem" }}>
      <h1>{APP_NAME}</h1>
      <p style={{ color: "#666" }}>A minimal notes demo wired core → backend → web.</p>

      <form onSubmit={addNote} style={{ display: "flex", gap: 8, margin: "1.5rem 0" }}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New note title…"
          style={{ flex: 1, padding: "0.5rem" }}
        />
        <button type="submit" style={{ padding: "0.5rem 1rem" }}>
          Add
        </button>
      </form>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <ul style={{ paddingLeft: 0, listStyle: "none" }}>
        {notes.map((note) => (
          <li key={note.id} style={{ borderBottom: "1px solid #eee", padding: "0.6rem 0" }}>
            <strong>{note.title}</strong>
            {note.body && <div style={{ color: "#666" }}>{note.body}</div>}
          </li>
        ))}
        {notes.length === 0 && <li style={{ color: "#999" }}>No notes yet.</li>}
      </ul>
    </main>
  );
}
