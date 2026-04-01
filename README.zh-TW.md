# Excalidraw Diagram Workbench

這是一個偏向實作導向的起始專案，用來產生、編修與匯出各種專案會用到的 Excalidraw 圖。

English README: [README.md](./README.md)

## 專案內容

- vendored 的 Excalidraw renderer：`.claude/skills/excalidraw-diagram/references/`（Codex 也可透過 `.codex/skills/excalidraw-diagram` 使用）
- 通用範例 renderer：`generate_diagram.js`
- 可重複使用的 render 腳本：`render_excalidraw.sh`
- 集中放輸出檔案的 `output/` 目錄

## 快速開始

建議編輯器使用 VS Code，並安裝 `pomdtr.excalidraw-editor`，這樣可以直接在工作區裡編修 `.excalidraw` 檔案。

1. 產生或更新 Excalidraw JSON：

```bash
node generate_diagram.js /absolute/path/to/my-diagram.json
```

給定 spec 路徑時，`.excalidraw` 檔會自動寫在 spec 旁邊。不帶路徑時會使用 `examples/channel-map.example.json` 作為預設 spec，並輸出到 stdout。加 `--dark` 可使用深色主題。

2. 將 `.excalidraw` render 成 PNG：

```bash
./render_excalidraw.sh
```

3. 如果你要 render 其他圖，也可以直接帶入檔案路徑：

```bash
./render_excalidraw.sh /absolute/path/to/your-diagram.excalidraw
```

## 建議工作流程

- 讓 `generate_diagram.js` 專心負責通用繪圖邏輯，把圖的內容放在 JSON spec。
- 直接在 Excalidraw 編修 `.excalidraw` 檔案，或把這個 renderer 換成你自己的產圖程式。
- 改完後執行 `./render_excalidraw.sh <file>` 產出 PNG。
- 後續如果有更多圖種，可以再增加不同的 generator 或 template。

## 專案結構

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

## 備註

- 本專案建議使用 VS Code，並透過 `.vscode/extensions.json` 推薦安裝 `pomdtr.excalidraw-editor`。
- `render_excalidraw.sh` 會優先使用 `.claude/skills/excalidraw-diagram/references/` 下 vendored 的 renderer，所以專案搬到其他機器時也比較容易重現。
- `.codex/skills/excalidraw-diagram` 是指向 `.claude/skills/excalidraw-diagram` 的符號連結，Claude/Codex 可共用同一份 skill，避免重複維護。
- `generate_diagram.js` 是可重複使用的範例 renderer。公開 repo 要維持通用性時，應把具體專案內容放在 spec，而不是硬寫在 JS 原始碼裡。
