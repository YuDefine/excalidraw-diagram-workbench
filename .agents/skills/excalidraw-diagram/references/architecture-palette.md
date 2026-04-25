# Architecture Diagram Palette

系統架構圖專用的語意化調色板。擴充 `color-palette.md` 的基礎調色板，針對常見架構元件提供一致的視覺語言。

---

## 使用方式

架構圖應優先使用此調色板。當元件不屬於以下分類時，回退到 `color-palette.md` 的通用調色板。

---

## Component Colors (Dark Mode — Catppuccin Mocha)

基於 Catppuccin Mocha 色系，搭配半透明填充讓箭頭在元件內部仍可見。

| Component Type | Fill | Stroke | 用途 |
|----------------|------|--------|------|
| **Frontend** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan) | Web app, Mobile app, SPA, Browser |
| **Backend** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) | API Server, Microservice, Lambda |
| **Database** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet) | PostgreSQL, MySQL, MongoDB, Redis |
| **Cloud/AWS** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber) | AWS, GCP, Azure 服務 |
| **Security** | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose) | Auth, IAM, Firewall, WAF |
| **Message Bus** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange) | Kafka, RabbitMQ, SQS, EventBridge |
| **External** | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate) | 第三方服務、外部 API |
| **Storage** | `rgba(21, 94, 117, 0.4)` | `#06b6d4` (cyan-600) | S3, Blob Storage, CDN |
| **Container** | `rgba(30, 58, 138, 0.4)` | `#3b82f6` (blue) | Docker, K8s Pod, ECS Task |

---

## Boundary Colors (Dark Mode)

用於 Region、Security Group、VPC 等邊界元素。使用 dashed stroke。

| Boundary Type | Fill | Stroke | strokeStyle |
|---------------|------|--------|-------------|
| **Region** | `transparent` | `#fbbf24` (amber) | `dashed` |
| **VPC / Network** | `rgba(30, 41, 59, 0.2)` | `#64748b` (slate) | `dashed` |
| **Security Group** | `transparent` | `#fb7185` (rose) | `dashed` |
| **Availability Zone** | `rgba(30, 58, 138, 0.15)` | `#60a5fa` (blue-400) | `dashed` |
| **Cluster (K8s)** | `rgba(6, 78, 59, 0.15)` | `#34d399` (emerald) | `dashed` |
| **Subnet** | `rgba(76, 29, 149, 0.15)` | `#a78bfa` (violet) | `dashed` |

---

## Component Colors (Light Mode)

| Component Type | Fill | Stroke |
|----------------|------|--------|
| **Frontend** | `rgba(8, 145, 178, 0.15)` | `#0891b2` (cyan-600) |
| **Backend** | `rgba(5, 150, 105, 0.15)` | `#059669` (emerald-600) |
| **Database** | `rgba(124, 58, 237, 0.15)` | `#7c3aed` (violet-600) |
| **Cloud/AWS** | `rgba(217, 119, 6, 0.15)` | `#d97706` (amber-600) |
| **Security** | `rgba(225, 29, 72, 0.15)` | `#e11d48` (rose-600) |
| **Message Bus** | `rgba(234, 88, 12, 0.15)` | `#ea580c` (orange-600) |
| **External** | `rgba(71, 85, 105, 0.15)` | `#475569` (slate-600) |
| **Storage** | `rgba(8, 145, 178, 0.15)` | `#0891b2` (cyan-600) |
| **Container** | `rgba(37, 99, 235, 0.15)` | `#2563eb` (blue-600) |

---

## Boundary Colors (Light Mode)

| Boundary Type | Fill | Stroke | strokeStyle |
|---------------|------|--------|-------------|
| **Region** | `transparent` | `#d97706` (amber-600) | `dashed` |
| **VPC / Network** | `rgba(71, 85, 105, 0.08)` | `#475569` (slate-600) | `dashed` |
| **Security Group** | `transparent` | `#e11d48` (rose-600) | `dashed` |
| **Availability Zone** | `rgba(37, 99, 235, 0.08)` | `#2563eb` (blue-600) | `dashed` |
| **Cluster (K8s)** | `rgba(5, 150, 105, 0.08)` | `#059669` (emerald-600) | `dashed` |
| **Subnet** | `rgba(124, 58, 237, 0.08)` | `#7c3aed` (violet-600) | `dashed` |

---

## Text on Architecture Elements

| Context | Dark Mode | Light Mode |
|---------|-----------|------------|
| 元件內文字 | `#cdd6f4` | `#1e293b` |
| Boundary 標籤 | 與 boundary stroke 同色 | 與 boundary stroke 同色 |
| 外部服務標籤 | `#94a3b8` | `#475569` |

---

## Arrow Colors

箭頭顏色跟隨 **來源元件** 的 stroke 色：

```
Frontend → Backend  ⟹  箭頭用 Frontend 的 cyan (#22d3ee)
Backend → Database  ⟹  箭頭用 Backend 的 emerald (#34d399)
```

跨 boundary 的箭頭使用中性色：
- Dark: `#a6adc8`
- Light: `#64748b`

---

## 使用範例

### AWS 三層架構（Dark Mode）

```
┌─────────────────────────────────────────────────────┐  Region (amber dashed)
│  ┌───────────────────────────────────────────────┐  │
│  │  CloudFront (Storage cyan)                    │  │
│  └───────────────────────────────────────────────┘  │
│                         │                           │
│  ┌─────────────────────────────────────────────┐    │  VPC (slate dashed)
│  │  ┌─────────────┐      ┌─────────────┐       │    │
│  │  │ ALB         │  →   │ ECS Service │       │    │  Security Group (rose)
│  │  │ (Cloud)     │      │ (Backend)   │       │    │
│  │  └─────────────┘      └─────────────┘       │    │
│  │                              │              │    │
│  │                       ┌─────────────┐       │    │
│  │                       │ RDS         │       │    │
│  │                       │ (Database)  │       │    │
│  │                       └─────────────┘       │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```
