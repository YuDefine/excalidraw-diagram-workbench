@RTK.md

## Language

- 一律使用繁體中文，不要使用簡體中文。

## Source Of Truth

- `.claude/` 是本專案唯一真理。
- 規則 source 在 `.claude/rules/`。
- workflow / skills source 在 `.claude/skills/` 與 `.claude/commands/`。
- hooks / agents / settings source 在 `.claude/` 內對應路徑。
- `AGENTS.md`、`.agents/`、`.codex/` 都是投影；若需調整內容，先改 `.claude/`，再用 `sync-to-agents` 同步。

## Project Focus

- Excalidraw Diagram Workbench，專門用來產生、編修與輸出 Excalidraw 圖表；更多背景與操作方式見 `README.md`。

## Project Rules

- 涉及 `.excalidraw` 的建立、修改或重排時，優先走 `.claude/skills/excalidraw-diagram/`。
- 圖表交付前必須渲染 PNG 驗證畫面沒有跑版。

## Rule Entry Points

- 產圖 workflow：`.claude/rules/excalidraw-diagram.md`
- 輸出與交付約定：`.claude/rules/output-conventions.md`
- diagram skill：`.claude/skills/excalidraw-diagram/`

## Codex Projection

- 定期執行 `node ~/.claude/scripts/sync-to-agents.mjs`，讓 Codex surface 與 `.claude/` 保持一致。
- 專案特化 promotion 規則放在 `.claude/sync-to-agents.config.json`。
- 若 source 與投影不一致，以 `.claude/` 為準，之後再同步生成。
