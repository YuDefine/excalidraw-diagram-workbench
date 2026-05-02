# Excalidraw Diagram Workbench

An opinionated starter repo for generating, editing, and exporting Excalidraw diagrams for many different projects.

繁體中文[README.zh-TW.md](./README.zh-TW.md)

## What this repo includes

- A vendored Excalidraw renderer under `.claude/skills/excalidraw-diagram/references/` (also projected for agents under `.agents/skills/excalidraw-diagram`)
- A generic sample renderer in `generate_diagram.js`
- A reusable render script in `render_excalidraw.sh`
- A pre-render structural validator in `validate_excalidraw.sh` (text overflow + arrow-binding consistency)
- Generated diagram files in `output/`

## Quick start

Recommended editor: VS Code with the `pomdtr.excalidraw-editor` extension for directly editing `.excalidraw` files inside the workspace.

1. Generate or update a diagram JSON file:

```bash
node generate_diagram.js /absolute/path/to/my-diagram.json
```

When a spec path is given, the output `.excalidraw` file is written next to the spec automatically. Without a spec path, `examples/channel-map.example.json` is used as the default spec and the diagram JSON is written to stdout. Use `--dark` for the dark theme.

2. Validate structure before rendering (catches text-overflowing-its-box and broken arrow bindings):

```bash
./validate_excalidraw.sh                                  # batch over output/ + temp/
./validate_excalidraw.sh /absolute/path/to/file.excalidraw
./validate_excalidraw.sh /absolute/path/to/file.excalidraw --fix   # auto-fix safe binding issues
```

3. Render the `.excalidraw` file to PNG:

```bash
./render_excalidraw.sh
```

4. Render a different `.excalidraw` file when needed:

```bash
./render_excalidraw.sh /absolute/path/to/your-diagram.excalidraw
```

## Default workflow

- Keep rendering logic in `generate_diagram.js`, and keep diagram content in JSON spec files.
- Edit `.excalidraw` files directly in Excalidraw, or replace the sample renderer with your own generator.
- Run `./validate_excalidraw.sh` first — text overflow and binding issues are cheap to catch before any PNG is rendered.
- Run `./render_excalidraw.sh <file>` to render to PNG.
- Add more generators or templates as your diagram library grows.

## Repository structure

```text
.
├── .claude/
│   └── skills/
│       └── excalidraw-diagram/
│           └── references/
├── .agents/
│   └── skills/
│       └── excalidraw-diagram/
├── examples/
│   └── channel-map.example.json
├── generate_diagram.js
├── lib/
├── output/
├── render_excalidraw.sh
└── validate_excalidraw.sh
```

## Notes

- This repo recommends VS Code and includes `.vscode/extensions.json` with `pomdtr.excalidraw-editor`.
- The render script prefers the vendored renderer under `.claude/skills/excalidraw-diagram/references/`, so the project is portable across machines.
- The vendored renderer loads Excalidraw from a pinned jsdelivr ESM build first, then falls back to the unpkg UMD build. If both fail, it prints browser request/page errors instead of hanging on a generic Playwright timeout.
- The validator measures text width with the same canvas + Excalidraw font stacks the renderer uses, so detected overflows match what would actually appear in the PNG (no character-count estimation).
- `.claude/` is the source of truth. `.agents/skills/excalidraw-diagram` is generated from it by `node ~/.claude/scripts/sync-to-agents.mjs`.
- `generate_diagram.js` is a reusable sample renderer. The repo stays generic by moving concrete diagram content into spec files instead of hardcoding it in the JS source.
