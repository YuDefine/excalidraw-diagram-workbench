---
description: Excalidraw 圖表建立與修改的強制流程
globs: ["**/*.excalidraw", "temp/**", "output/**"]
---

# Excalidraw Diagram Rules

## Skill 調用（強制）

**MUST** 使用 `/excalidraw-diagram` skill 來建立或修改 `.excalidraw` 圖表。
**NEVER** 在主對話中直接手寫完整的 Excalidraw JSON。

唯一例外：對已存在圖表的微調（修正單一座標、調整顏色值），可直接用 Edit tool。

## 結構驗證（強制，先於渲染）

**MUST** 在每次圖表產出 / 修改後、`./render_excalidraw.sh` 之前，先跑結構驗證器：

```bash
./validate_excalidraw.sh                 # 批次驗證 output/ 與 temp/
./validate_excalidraw.sh file.excalidraw # 單一檔案
./validate_excalidraw.sh file.excalidraw --fix  # 自動修綁定（不會改文字 / 容器尺寸）
```

驗證器會抓兩類問題：

1. **Text overflow**：用 headless Chromium 的 canvas measureText 配合 Excalidraw 字體棧（Virgil / Helvetica / Cascadia / Excalifont / Nunito / Lilita One / Comic Shanns）量測每個 text element 的實際 render 寬度，比對其所屬 rectangle / ellipse / diamond 容器（`containerId` 或幾何包覆）的內寬。**精度等同 Excalidraw 自身的渲染寬度**，不是 char count 估算。
2. **Binding consistency**：檢查所有 arrow 的 `startBinding` / `endBinding` 與目標元素的 `boundElements` 反向指標是否一致；箭頭端點貼在 rectangle 邊上但未綁定時提示。

**NEVER** 跳過驗證器直接渲染。validator exit code 非 0 = 圖表有結構性 bug，render 出來的 PNG 可能正常顯示但已是 invariant 破損狀態（例如綁定不對稱、文字溢出容器）。

`--fix` 只動三類安全變更：補缺漏的反向指標、清孤兒 boundElements、把單一明確候選的 unbound 端點綁回去。**不會**改文字、不會改容器尺寸、不會猜模糊綁定。

## 渲染驗證（強制）

**MUST** 在 validator 通過後執行渲染並用 Read tool 目視檢查 PNG。
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
