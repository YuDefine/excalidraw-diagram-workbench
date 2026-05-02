<!-- AUTO-GENERATED from .claude/ — 請勿手動編輯 -->


## Language

- 一律使用繁體中文，不要使用簡體中文。

## Source Of Truth

- `.claude/` 是本專案唯一真理。
- 規則 source 在 `.claude/rules/`。
- workflow / skills source 在 `.agents/skills/` 與 `.agents/commands/`。
- hooks / agents / settings source 在 `.claude/` 內對應路徑。
- `AGENTS.md`、`.agents/`、`.codex/` 都是投影；若需調整內容，先改 `.claude/`，再用 `sync-to-agents` 同步。

## Project Focus

- Excalidraw Diagram Workbench，專門用來產生、編修與輸出 Excalidraw 圖表；更多背景與操作方式見 `README.md`。

## Project Rules

- 涉及 `.excalidraw` 的建立、修改或重排時，優先走 `.agents/skills/excalidraw-diagram/`。
- 圖表交付前必須渲染 PNG 驗證畫面沒有跑版。

## Rule Entry Points

- 產圖 workflow：`.claude/rules/excalidraw-diagram.md`
- 輸出與交付約定：`.claude/rules/output-conventions.md`
- diagram skill：`.agents/skills/excalidraw-diagram/`

## Codex Projection

- 定期執行 `node ~/.claude/scripts/sync-to-agents.mjs`，讓 Codex surface 與 `.claude/` 保持一致。
- 專案特化 promotion 規則放在 `.claude/sync-to-agents.config.json`。
- 若 source 與投影不一致，以 `.claude/` 為準，之後再同步生成。

# RTK Instructions

Use RTK (Rust Token Killer) to reduce token-heavy shell output when running commands through an AI coding assistant.

## Command Routing

- Prefer `rtk git status`, `rtk git diff`, `rtk git log`, `rtk gh ...` for Git and GitHub CLI output.
- Prefer `rtk pnpm ...`, `rtk npm ...`, `rtk vitest`, `rtk playwright test`, `rtk lint`, and `rtk tsc` for package manager, test, lint, and typecheck output.
- Prefer `rtk grep`, `rtk find`, `rtk read`, and `rtk ls` when the expected output is large.
- Use raw shell commands for small, structural, or shell-native operations such as `pwd`, `cd`, `mkdir`, `test`, `[ ... ]`, `[[ ... ]]`, `true`, `false`, `export`, `printf`, and `echo`.
- Do not rewrite shell builtins as RTK subcommands. For example, use `test -d path`, not `rtk test -d path`.
- For shell syntax, compound commands, heredocs, or commands RTK does not understand, use the raw command or `rtk proxy <command>` only when compact tracking is still useful.

## Sandbox Database

RTK tracking must use a Codex-writable database path:

```toml
[tracking]
database_path = "/Users/charles/.codex/memories/rtk/history.db"
```
