---
description: Excalidraw 圖表建立與修改的強制流程
globs: ["**/*.excalidraw", "temp/**", "output/**"]
---

# Excalidraw Diagram Rules

## Skill 調用（強制）

**MUST** 使用 `/excalidraw-diagram` skill 來建立或修改 `.excalidraw` 圖表。
**NEVER** 在主對話中直接手寫完整的 Excalidraw JSON。

唯一例外：對已存在圖表的微調（修正單一座標、調整顏色值），可直接用 Edit tool。

## 渲染驗證（強制）

**MUST** 在圖表產出後執行渲染並用 Read tool 目視檢查 PNG。
**NEVER** 僅憑 JSON 內容判斷圖表正確性。

```bash
./render_excalidraw.sh ./temp/           # 批次渲染
./render_excalidraw.sh file.excalidraw   # 單一檔案
```

## 主題預設

**MUST** 預設只產 dark 版（Catppuccin Mocha, `#1e1e2e`）。
**SHOULD** 在使用者明確要求時才額外產 light 版。

## 平行作業

多張圖表 **SHOULD** 使用平行 Agent 同時繪製，每張圖一個 Agent。
