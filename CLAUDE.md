# Excalidraw Diagram Workbench

## 強制規則

### 建立圖表必須使用 /excalidraw-diagram skill

當任務涉及建立、修改、或重新生成 `.excalidraw` 圖表時，**必須**透過 `/excalidraw-diagram` skill 執行。禁止在主對話中直接手寫 Excalidraw JSON。

觸發條件（符合任一即適用）：
- 使用者要求畫圖、建立圖表、視覺化任何概念
- 需要產出 `.excalidraw` 檔案
- 需要修改既有 `.excalidraw` 檔案的佈局、元素、或箭頭路由

**唯一例外**：對已渲染圖表的微調（如修正單一座標值、調整顏色），可直接用 Edit tool 修改 JSON，無需重新走 skill。

### 渲染驗證

圖表產出後必須渲染 PNG 並用 Read tool 檢視，確認無跑版再交付。

批次渲染：
```bash
./render_excalidraw.sh ./temp/           # 批次渲染目錄
./render_excalidraw.sh file.excalidraw   # 單一檔案
```

### 主題預設

遵循 memory 中的設定：預設只產 dark 版，除非使用者另有指定。

## 專案結構

- `temp/` — 工作中的圖表與規格文件
- `output/` — 正式交付的圖表
- `.claude/skills/excalidraw-diagram/` — 圖表 skill 與渲染器
- `render_excalidraw.sh` — 批次渲染入口腳本
