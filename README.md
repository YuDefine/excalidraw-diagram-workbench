# Excalidraw Diagram Workbench

An opinionated starter repo for generating, editing, and exporting Excalidraw diagrams for many different projects.

繁體中文[README.zh-TW.md](./README.zh-TW.md)

## What this repo includes

- A vendored Excalidraw renderer under `.claude/skills/excalidraw-diagram/references/` (also available to Codex via `.codex/skills/excalidraw-diagram`)
- A generic sample renderer in `generate_diagram.js`
- A reusable render script in `render_excalidraw.sh`
- Generated diagram files in `output/`

## Quick start

Recommended editor: VS Code with the `pomdtr.excalidraw-editor` extension for directly editing `.excalidraw` files inside the workspace.

1. Generate or update a diagram JSON file:

```bash
node generate_diagram.js /absolute/path/to/my-diagram.json
```

When a spec path is given, the output `.excalidraw` file is written next to the spec automatically. Without a spec path, `examples/channel-map.example.json` is used as the default spec and the diagram JSON is written to stdout. Use `--dark` for the dark theme.

2. Render the `.excalidraw` file to PNG:

```bash
./render_excalidraw.sh
```

3. Render a different `.excalidraw` file when needed:

```bash
./render_excalidraw.sh /absolute/path/to/your-diagram.excalidraw
```

## Default workflow

- Keep rendering logic in `generate_diagram.js`, and keep diagram content in JSON spec files.
- Edit `.excalidraw` files directly in Excalidraw, or replace the sample renderer with your own generator.
- Run `./render_excalidraw.sh <file>` to render to PNG.
- Add more generators or templates as your diagram library grows.

## Repository structure

```text
.
├── .claude/
│   └── skills/
│       └── excalidraw-diagram/
│           └── references/
├── .codex/
│   └── skills/
│       └── excalidraw-diagram -> ../../.claude/skills/excalidraw-diagram
├── examples/
│   └── channel-map.example.json
├── generate_diagram.js
├── lib/
├── output/
└── render_excalidraw.sh
```

## Notes

- This repo recommends VS Code and includes `.vscode/extensions.json` with `pomdtr.excalidraw-editor`.
- The render script prefers the vendored renderer under `.claude/skills/excalidraw-diagram/references/`, so the project is portable across machines.
- `.codex/skills/excalidraw-diagram` is a symlink to `.claude/skills/excalidraw-diagram`, so Claude/Codex share the same skill source without duplication.
- `generate_diagram.js` is a reusable sample renderer. The repo stays generic by moving concrete diagram content into spec files instead of hardcoding it in the JS source.
