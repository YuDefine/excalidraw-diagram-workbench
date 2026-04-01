# Color Palette & Brand Style

**This is the single source of truth for all colors and brand-specific styles.** To customize diagrams for your own brand, edit this file — everything else in the skill is universal.

---

## Shape Colors (Semantic)

Colors encode meaning, not decoration. Each semantic purpose has a fill/stroke pair.

| Semantic Purpose | Fill | Stroke |
|------------------|------|--------|
| Primary/Neutral | `#3b82f6` | `#1e3a5f` |
| Secondary | `#60a5fa` | `#1e3a5f` |
| Tertiary | `#93c5fd` | `#1e3a5f` |
| Start/Trigger | `#fed7aa` | `#c2410c` |
| End/Success | `#a7f3d0` | `#047857` |
| Warning/Reset | `#fee2e2` | `#dc2626` |
| Decision | `#fef3c7` | `#b45309` |
| AI/LLM | `#ddd6fe` | `#6d28d9` |
| Inactive/Disabled | `#dbeafe` | `#1e40af` (use dashed stroke) |
| Error | `#fecaca` | `#b91c1c` |

**Rule**: Always pair a darker stroke with a lighter fill for contrast.

---

## Text Colors (Hierarchy)

Use color on free-floating text to create visual hierarchy without containers.

| Level | Color | Use For |
|-------|-------|---------|
| Title | `#1e40af` | Section headings, major labels |
| Subtitle | `#3b82f6` | Subheadings, secondary labels |
| Body/Detail | `#64748b` | Descriptions, annotations, metadata |
| On light fills | `#374151` | Text inside light-colored shapes |
| On dark fills | `#ffffff` | Text inside dark-colored shapes |

---

## Evidence Artifact Colors

Used for code snippets, data examples, and other concrete evidence inside technical diagrams.

| Artifact | Background | Text Color |
|----------|-----------|------------|
| Code snippet | `#1e293b` | Syntax-colored (language-appropriate) |
| JSON/data example | `#1e293b` | `#22c55e` (green) |

---

## Default Stroke & Line Colors

| Element | Color |
|---------|-------|
| Arrows | Use the stroke color of the source element's semantic purpose |
| Structural lines (dividers, trees, timelines) | Primary stroke (`#1e3a5f`) or Slate (`#64748b`) |
| Marker dots (fill + stroke) | Primary fill (`#3b82f6`), or contextual stroke color when used within a themed section |

---

## Background

| Property | Light | Dark |
|----------|-------|------|
| Canvas background | `#ffffff` | `#1e1e2e` |

---

## Dark Mode Palette

When generating dark-mode diagrams, use these colors instead of the light equivalents above. Based on Catppuccin Mocha.

**Rule (dark)**: Pair a brighter stroke with a darker fill for contrast — the inverse of light mode.

### Shape Colors (Dark)

| Semantic Purpose | Fill | Stroke |
|------------------|------|--------|
| Primary/Neutral | `#313244` | `#89b4fa` |
| Secondary | `#313244` | `#89b4fa` |
| Tertiary | `#45475a` | `#89b4fa` |
| Start/Trigger | `#45475a` | `#fab387` |
| End/Success | `#313244` | `#a6e3a1` |
| Warning/Reset | `#45475a` | `#f38ba8` |
| Decision | `#45475a` | `#fab387` |
| AI/LLM | `#313244` | `#cba6f7` |
| Inactive/Disabled | `#313244` | `#585b70` (use dashed stroke) |
| Error | `#45475a` | `#f38ba8` |

### Text Colors (Dark)

| Level | Color | Use For |
|-------|-------|---------|
| Title | `#89b4fa` | Section headings, major labels |
| Subtitle | `#74c7ec` | Subheadings, secondary labels |
| Body/Detail | `#a6adc8` | Descriptions, annotations, metadata |
| On fills | `#cdd6f4` | Text inside shapes (all fills are dark) |

### Evidence Artifact Colors (Dark)

| Artifact | Background | Text Color |
|----------|-----------|------------|
| Code snippet | `#11111b` | Syntax-colored |
| JSON/data example | `#11111b` | `#a6e3a1` (green) |

### Default Stroke & Line Colors (Dark)

| Element | Color |
|---------|-------|
| Arrows | Use the stroke color of the source element's semantic purpose |
| Structural lines | `#585b70` |
| Marker dots (fill + stroke) | `#89b4fa`, or contextual stroke color when used within a themed section |
