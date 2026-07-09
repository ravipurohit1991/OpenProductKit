# Rebranding & updates

Because the repository *is* a Copier template, rebranding is not a fragile find-and-replace script — it is the generation step itself. And you can pull upstream template improvements into an already-generated project.

## Generate (rebrand)

```bash
uvx copier copy gh:ravipurohit1991/OpenProductKit my-product
```

You are prompted for:

| Question | Used for |
| --- | --- |
| `project_name` | Titles, docs, UI heading |
| `project_slug` | Directories, npm/docker names |
| `pkg_slug` | Python package names (`<pkg>_core`, …) |
| `cli_name` | The CLI entrypoint (default `opk`) |
| `project_description`, `author_name`, `author_email` | Metadata |
| `python_version` | `requires-python` and targets |

Everything — package names, imports, the desktop bundle id (later), README, `.env.example`, Docker image names — is rendered from these answers.

## Update

Copier records your answers in `.copier-answers.yml`. To pull in later template improvements:

```bash
copier update
```

Copier performs a three-way merge between the template version you generated from, the latest template, and your local changes — so your customizations survive. This is the entire "keep generated projects up to date" story, for free.

!!! tip
    Commit your generated project to git before running `copier update` so the
    merge is reviewable as a normal diff.
