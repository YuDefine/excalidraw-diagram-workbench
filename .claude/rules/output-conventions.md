---
description: 圖表輸出路徑與命名規範
globs: ["**/*.excalidraw", "**/*.png"]
---

# Output Conventions

## 目錄用途

| 目錄 | 用途 |
|------|------|
| `temp/` | 開發中的工作檔案、規格文件、草稿圖表 |
| `output/` | 正式交付的圖表 |

## 命名格式

**MUST** 使用語意化命名：`[序號]-[主題].excalidraw`

範例：
- `01-preselection-state-machine.excalidraw`
- `02-billing-er-diagram.excalidraw`

**NEVER** 使用 `diagram.excalidraw`、`test.excalidraw` 等無意義名稱。
