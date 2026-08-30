# Repository Guidelines

## Project Structure & Module Organization

This is a static, asset-heavy Nadia character package. Keep canonical design, narrative, gameplay, voice, and production notes in `docs/`. The public delivery lives in `output/nadia_character/`: `index.html`, `gameplay.html`, `skills.html`, `postcards.html`, `theme.css`, and local `assets/` (PNG and MP3 files, including `acrylic/` and `portraits/`). PDF generators are in `output/nadia_character/print/`; their generated files belong in `output/pdf/`. `tools/nadia_skill_simulator.html` is development-only and must not be added to the public share package. `tmp/` is ignored scratch space. Never commit private source photos in `/xiting/*.jpg`.

## Build, Test, and Development Commands

There is no package manager or project build wrapper. Use a virtual environment with Python 3.10+, `reportlab`, `Pillow`, and `pypdf` installed, then run from the repository root:

```sh
python3 -m http.server 8000
python3 output/nadia_character/print/build_dossier.py
python3 output/nadia_character/print/build_postcards.py
```

Open `http://localhost:8000/output/nadia_character/index.html` for a local browser review. The generators write the A5 dossier and 48-page postcard PDF to `output/pdf/` and expect macOS CJK fonts.

## Coding Style & Naming Conventions

Use two-space indentation in HTML/CSS and four spaces in Python. Python should use typed functions, `snake_case`, and standard-library imports before third-party imports. Keep HTML/CSS lowercase and descriptive. Name new assets with the established pattern, such as `nadia_<subject>_<state>_vN.ext`; update every HTML, documentation, and package reference when changing a canonical asset. No formatter or linter is configured; always run `git diff --check`.

## Testing Guidelines

No automated test suite or CI workflow is present. For HTML changes, inspect all four public pages, navigation, card-flip keyboard behavior, audio playback, and the simulator when relevant. For print changes, run both generators, verify PDF page counts (20 and 48), dimensions, and visual framing. Materialize Git LFS objects before validating tracked ZIP deliverables.

## Commit & Pull Request Guidelines

Follow the recent concise prefixes: `feat:`, `fix:`, `chore:`, `content:`, or `deliver:`, with an optional scope (for example, `feat(nadia): add portrait studies`). Pull requests should describe affected docs, code, and assets; list validation commands; include screenshots for visual changes; and state PDF dimensions/page counts or LFS impact when applicable. Keep generated artifacts synchronized and exclude private or ignored source material.
