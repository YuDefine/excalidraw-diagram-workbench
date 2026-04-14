# Excalidraw Diagram Skill 擴充計畫

參考來源：[Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (1128 ⭐)

---

## 高優先

### 1. Architecture-specific 調色板 ✅
**檔案**: `references/architecture-palette.md`

新增針對系統架構圖的語意化顏色：

| Component Type | Fill (Dark) | Stroke (Dark) |
|----------------|-------------|---------------|
| Frontend | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan) |
| Backend | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) |
| Database | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet) |
| Cloud/AWS | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber) |
| Security | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose) |
| Message Bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange) |
| External | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate) |

---

### 2. Region / Security Group 模板 ✅
**檔案**: `references/element-templates.md` (擴充)

新增 dashed boundary 元素：

- [x] **Security Group** — dashed stroke, rose color, 包圍元件群組
- [x] **Region Boundary** — larger dashed stroke, amber color, 標示 cloud region
- [x] **Cluster Boundary** — 用於 K8s cluster、VPC 等

---

### 3. Legend 模板 ✅
**檔案**: `references/element-templates.md` (擴充)

- [x] 可複製的 Legend 區塊模板
- [x] 放置規則：MUST 放在所有 boundary 外部
- [x] 自動擴展 canvas 以容納 legend

---

## 中優先

### 4. Message Bus / Event Bus Pattern ✅
**檔案**: `references/element-templates.md` (擴充)

- [x] 水平 bus 元件（Kafka, RabbitMQ, EventBridge）
- [x] 連接多個 service 的 fan-out 箭頭模式

---

### 5. Spacing Rules 強化 ✅
**檔案**: `SKILL.md` (擴充)

明確的間距規則，標註 **CRITICAL**：

- [x] 元件最小垂直間距：40px
- [x] Inline connector 必須放在 gap 中間，不可重疊
- [x] Legend 必須在所有 boundary 之下

---

## 低優先

### 6. Arrow Z-order 指南 ✅
**檔案**: `references/element-templates.md` (擴充)

- [x] 說明 Excalidraw 的 z-order 機制
- [x] 半透明填充下的箭頭可見性處理

---

### 7. Architecture Diagram 專用 Skill Variant
**考慮**: 是否要獨立一個 `/architecture-diagram` skill？

優點：
- 專精於 architecture，不混淆通用圖表
- 可以預載 architecture palette

缺點：
- 維護兩套 skill
- 功能重疊

**決定**: 暫不拆分，先用 palette 擴充方式處理

---

## 不採用

| 項目 | 原因 |
|------|------|
| Info Cards / Header / Footer | HTML 頁面結構，Excalidraw 是純 canvas |
| CSS Animations | 靜態圖不適用 |
| Google Fonts | Excalidraw 用內建字體 |

---

## 驗收標準 ✅

- [x] 用新 palette 產出一張 AWS architecture 圖
- [x] 包含 Region Boundary + Security Group
- [x] 包含 Legend
- [x] 渲染 PNG 確認無跑版

**驗收完成**: `output/01-aws-three-tier-architecture.excalidraw` (2026-04-14)
