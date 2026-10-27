# Security Policy

## Scope

karousel-cli renders local Markdown files to local PNG files. It makes no
network requests, collects no data, and requires no credentials.

## Reporting a vulnerability

Open a GitHub issue with a minimal reproduction. Do not include personal
data, credentials, or exploit code targeting third parties.

## Known posture (v0.1.0)

- Input files are read as UTF-8 text and never executed.
- Output is written only inside the directory passed with `-o`.
- Font files are loaded by Pillow from local paths only.
- Dependencies: Pillow only (see `pyproject.toml` for the pinned minimum).
