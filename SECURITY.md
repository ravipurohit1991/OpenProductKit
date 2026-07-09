# Security Policy

## Supported versions

OpenProductKit is a project template. Security fixes are made on the `main` branch; regenerate or `copier update` to pick them up.

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Instead, report privately via [GitHub Security Advisories](https://github.com/ravipurohit1991/OpenProductKit/security/advisories/new), or email the maintainer listed in the repository profile. Include:

- a description of the issue and its impact,
- steps to reproduce (a generated project + commands is ideal),
- affected template version / commit.

You can expect an acknowledgement within a few days.

## Scope & honest limits

- The **licensing** system is honest-user entitlement, **not** copy protection. Do not treat it as a security boundary.
- The **plugin** system is dev-time: plugins are installed Python packages and run with full process privileges. Only install plugins you trust. Runtime sandboxing is a roadmap item.
- Generated projects ship with development defaults (e.g. permissive CORS, a local SQLite DB). Harden these before production.
