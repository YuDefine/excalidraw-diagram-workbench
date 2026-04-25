# Element Templates

Copy-paste JSON templates for each Excalidraw element type. The `strokeColor` and `backgroundColor` values are placeholders — always pull actual colors from `color-palette.md` based on the element's semantic purpose.

## Free-Floating Text (no container)
```json
{
  "type": "text",
  "id": "label1",
  "x": 100, "y": 100,
  "width": 200, "height": 25,
  "text": "Section Title",
  "originalText": "Section Title",
  "fontSize": 28,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "<title color from palette>",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 11111,
  "version": 1,
  "versionNonce": 22222,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": null,
  "lineHeight": 1.25,
  "autoResize": true
}
```

## Line (structural, not arrow)
```json
{
  "type": "line",
  "id": "line1",
  "x": 100, "y": 100,
  "width": 0, "height": 200,
  "strokeColor": "<structural line color from palette>",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 44444,
  "version": 1,
  "versionNonce": 55555,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "points": [[0, 0], [0, 200]]
}
```

## Small Marker Dot
```json
{
  "type": "ellipse",
  "id": "dot1",
  "x": 94, "y": 94,
  "width": 12, "height": 12,
  "strokeColor": "<marker dot color from palette>",
  "backgroundColor": "<marker dot color from palette>",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 66666,
  "version": 1,
  "versionNonce": 77777,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false
}
```

## Rectangle
```json
{
  "type": "rectangle",
  "id": "elem1",
  "x": 100, "y": 100, "width": 180, "height": 90,
  "strokeColor": "<stroke from palette based on semantic purpose>",
  "backgroundColor": "<fill from palette based on semantic purpose>",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 12345,
  "version": 1,
  "versionNonce": 67890,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [{"id": "text1", "type": "text"}],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

## Text (centered in shape)

**Position calculation** — Excalidraw caches `x`/`y`/`width`/`height` and uses them for initial rendering. If these values are wrong, text appears mispositioned until the user double-clicks to trigger recalculation. Always compute accurate values:

```
textHeight = numLines × fontSize × lineHeight
textWidth  = maxLineChars × fontSize × 0.6    (monospace approx for fontFamily 3)
text.x     = container.x + (container.width  - textWidth)  / 2
text.y     = container.y + (container.height - textHeight) / 2
```

Example: container at `(100, 100, 180×90)`, text "Process" (1 line, fontSize 20, lineHeight 1.25):
- `textHeight = 1 × 20 × 1.25 = 25`
- `textWidth  = 7 × 20 × 0.6 = 84`
- `text.x = 100 + (180 - 84) / 2 = 148`
- `text.y = 100 + (90 - 25) / 2 = 132.5`

```json
{
  "type": "text",
  "id": "text1",
  "x": 148, "y": 132.5,
  "width": 84, "height": 25,
  "text": "Process",
  "originalText": "Process",
  "fontSize": 20,
  "fontFamily": 3,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "<text color — match parent shape's stroke or use 'on light/dark fills' from palette>",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 11111,
  "version": 1,
  "versionNonce": 22222,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": "elem1",
  "lineHeight": 1.25,
  "autoResize": true
}
```

## Arrow
```json
{
  "type": "arrow",
  "id": "arrow1",
  "x": 282, "y": 145, "width": 118, "height": 0,
  "strokeColor": "<arrow color — typically matches source element's stroke from palette>",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 33333,
  "version": 1,
  "versionNonce": 44444,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "points": [[0, 0], [118, 0]],
  "startBinding": {"elementId": "elem1", "fixedPoint": [1, 0.5001], "focus": 0},
  "endBinding": {"elementId": "elem2", "fixedPoint": [0, 0.5001], "focus": 0},
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": true
}
```

**Arrow routing modes** (choose one per arrow):
- `"elbowed": true` — Orthogonal (right-angle) routing. Best for state machines, structured diagrams, channel maps.
- `"elbowed": false` + `"roundness": {"type": 2}` — Smooth curves. Best for ER diagrams, organic flows.

**Binding format**: Include both `fixedPoint` and `focus` for maximum compatibility:
- `fixedPoint: [x, y]` — Position on shape edge. `[0, 0.5]` = left center, `[1, 0.5]` = right center, `[0.5, 0]` = top center, `[0.5, 1]` = bottom center. Use `0.5001` instead of `0.5` to avoid ambiguity.
- `focus: 0` — Curvature bias. Set to `0` for straight routing; use non-zero values (`-0.7`, `0.6`) in ER diagrams to spread fan-out arrows.
- `gap: 1` — Alternative to `fixedPoint`. Used with `focus` only (no `fixedPoint`) when you want Excalidraw to auto-determine the edge.

For curves: use 3+ points in `points` array.

## Arrow with Bound Label

Attach a text label **directly to an arrow** so it renders at the path midpoint and follows the arrow when moved. This is the correct approach for all relationship labels — do NOT use free-floating text near arrows.

**How it works**: arrow `boundElements` references the text; text `containerId` points back to the arrow. Excalidraw positions the text at the geometric midpoint of the arrow path automatically.

```json
// ARROW — add text id to boundElements
{
  "type": "arrow",
  "id": "arrow1",
  "x": 260, "y": 150, "width": 180, "height": 0,
  "strokeColor": "#89b4fa",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 33333,
  "version": 1,
  "versionNonce": 44444,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [{"type": "text", "id": "arrow1_label"}],
  "link": null,
  "locked": false,
  "points": [[0, 0], [180, 0]],
  "startBinding": {"elementId": "elem1", "fixedPoint": [1, 0.5001], "focus": 0},
  "endBinding": {"elementId": "elem2", "fixedPoint": [0, 0.5001], "focus": 0},
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": true
}
```

```json
// TEXT LABEL — containerId points to arrow
{
  "type": "text",
  "id": "arrow1_label",
  "x": 326,
  "y": 130,
  "width": 108,
  "height": 27,
  "text": "OAuth 認證",
  "originalText": "OAuth 認證",
  "fontSize": 16,
  "fontFamily": 6,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#a6adc8",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 33334,
  "version": 1,
  "versionNonce": 33335,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": "arrow1",
  "lineHeight": 1.35,
  "autoResize": true
}
```

**Position calculation** — text x/y = arrow path midpoint − half text dimensions:
- For a straight arrow from `(x, y)` to `(x+dx, y+dy)`: midpoint = `(x+dx/2, y+dy/2)`
- For multi-segment paths: walk cumulative segment lengths, interpolate at 50%
- `text.x = midX − textWidth/2`, `text.y = midY − textHeight/2`

**Key rules**:
- Arrow `boundElements`: use `[]` (empty array) when no label; `[{"type":"text","id":"..."}]` when labelled
- Text `boundElements`: always `[]` (empty array, never `null`)
- Text `lineHeight`: `1.35` (matches Excalidraw's native behaviour)
- Text `autoResize`: `true`
- Arrow-bound labels MUST use `fontFamily: 6` (not `3`) and `lineHeight: 1.35` — this matches the Excalidraw editor's native behavior and prevents JSON drift when users edit the file

## ER Relationship Arrow (Crowfoot Notation)

For ER diagrams, use crowfoot arrowheads instead of generic arrows. Use `focus`/`gap` binding for natural curve behavior and `roundness: {"type": 2}` for smooth curves.

### Structural Relationship (1:N with crowfoot)
```json
{
  "type": "arrow",
  "id": "er_arrow1",
  "x": 280, "y": 285, "width": 120, "height": 0,
  "strokeColor": "<source entity's stroke color from palette>",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 33333,
  "version": 1,
  "versionNonce": 44444,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "points": [[0, 0], [120, 0]],
  "startBinding": {"elementId": "tbl_parent", "focus": 0.0, "gap": 1},
  "endBinding": {"elementId": "tbl_child", "focus": 0.0, "gap": 1},
  "startArrowhead": null,
  "endArrowhead": "crowfoot_many",
  "roundness": {"type": 2},
  "elbowed": false
}
```

### Reference/FK Arrow (same crowfoot notation, thinner + neutral color)
```json
{
  "type": "arrow",
  "id": "fk_arrow1",
  "x": 500, "y": 130, "width": 50, "height": 130,
  "strokeColor": "#ffffff",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 55555,
  "version": 1,
  "versionNonce": 66666,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": null,
  "link": null,
  "locked": false,
  "points": [[0, 0], [-50, 130]],
  "startBinding": {"elementId": "tbl_source", "focus": 0.0, "gap": 1},
  "endBinding": {"elementId": "tbl_target", "focus": 0.0, "gap": 1},
  "startArrowhead": null,
  "endArrowhead": "crowfoot_many",
  "roundness": {"type": 2},
  "elbowed": false
}
```

### Available Arrowhead Values

| Value | Visual | Typical Use |
|-------|--------|-------------|
| `"arrow"` | → | Default flow arrow |
| `"crowfoot_one"` | ─\|─ | "Exactly one" side of relationship |
| `"crowfoot_many"` | ─<─ | "Many" side of relationship |
| `"crowfoot_one_or_many"` | ─\|<─ | "One or many" |
| `"circle"` | ─●─ | Filled circle (FK reference) |
| `"circle_outline"` | ─○─ | "Optional / zero" |
| `"diamond"` | ─◆─ | Aggregation |
| `"diamond_outline"` | ─◇─ | Composition |
| `"bar"` | ─\|─ | Bar / tick |
| `null` | ─── | No arrowhead |

### Binding Format: `focus` + `gap`

For ER arrows, prefer `focus`/`gap` binding over `fixedPoint`:

```json
"startBinding": {"elementId": "entity_id", "focus": 0.0, "gap": 1}
```

- **`focus`**: Position along the shape edge. Range: -1.0 (left/top) → 0.0 (center) → 1.0 (right/bottom)
- **`gap`**: Pixel distance from the shape edge (typically `1`)

---

## Boundary Elements (Region / Security Group / Cluster)

Dashed boundary rectangles for grouping architecture components. Use `strokeStyle: "dashed"` and transparent or semi-transparent fills.

### Region Boundary (AWS Region, GCP Region)

Large outer boundary, amber stroke, no fill.

```json
{
  "type": "rectangle",
  "id": "region_boundary",
  "x": 50, "y": 50, "width": 800, "height": 600,
  "strokeColor": "#fbbf24",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "dashed",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 90001,
  "version": 1,
  "versionNonce": 90002,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [{"id": "region_label", "type": "text"}],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

```json
// Region label — positioned at top-left inside boundary
{
  "type": "text",
  "id": "region_label",
  "x": 60, "y": 58,
  "width": 120, "height": 20,
  "text": "ap-northeast-1",
  "originalText": "ap-northeast-1",
  "fontSize": 14,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#fbbf24",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 90003,
  "version": 1,
  "versionNonce": 90004,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": null,
  "lineHeight": 1.25,
  "autoResize": true
}
```

### Security Group Boundary

Rose-colored dashed stroke, wraps a group of related services.

```json
{
  "type": "rectangle",
  "id": "sg_boundary",
  "x": 100, "y": 150, "width": 400, "height": 300,
  "strokeColor": "#fb7185",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "dashed",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 90010,
  "version": 1,
  "versionNonce": 90011,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

```json
// Security Group label — top-left corner
{
  "type": "text",
  "id": "sg_label",
  "x": 110, "y": 158,
  "width": 180, "height": 20,
  "text": "sg-web-tier",
  "originalText": "sg-web-tier",
  "fontSize": 12,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#fb7185",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 90012,
  "version": 1,
  "versionNonce": 90013,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": null,
  "lineHeight": 1.25,
  "autoResize": true
}
```

### VPC / Cluster Boundary

Slate or emerald dashed stroke with subtle semi-transparent fill for visual layering.

```json
{
  "type": "rectangle",
  "id": "vpc_boundary",
  "x": 80, "y": 100, "width": 700, "height": 500,
  "strokeColor": "#64748b",
  "backgroundColor": "rgba(30, 41, 59, 0.2)",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "dashed",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 90020,
  "version": 1,
  "versionNonce": 90021,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

### Boundary Nesting Order (Z-order)

When nesting boundaries, ensure correct layering in the `elements` array:

1. **Outermost boundary first** (Region) — lowest z-index
2. **Middle boundaries** (VPC, Cluster)
3. **Inner boundaries** (Security Group, Subnet)
4. **Components inside boundaries**
5. **Arrows last** — highest z-index, renders on top

---

## Legend Template

A reusable legend block explaining the color coding in architecture diagrams.

### Placement Rules (CRITICAL)

- **MUST** place legend **outside** all boundary elements
- **MUST** position at bottom-right or bottom-left of canvas
- **MUST** expand canvas size if needed to accommodate legend without overlapping content
- Typical position: `x = rightmost_element.x + 60`, `y = bottommost_element.y - legend_height`

### Legend Structure

```json
// Legend container (background)
{
  "type": "rectangle",
  "id": "legend_bg",
  "x": 900, "y": 500, "width": 200, "height": 280,
  "strokeColor": "#585b70",
  "backgroundColor": "#1e1e2e",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 95001,
  "version": 1,
  "versionNonce": 95002,
  "isDeleted": false,
  "groupIds": ["legend_group"],
  "boundElements": [],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

```json
// Legend title
{
  "type": "text",
  "id": "legend_title",
  "x": 920, "y": 510,
  "width": 60, "height": 25,
  "text": "Legend",
  "originalText": "Legend",
  "fontSize": 16,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#cdd6f4",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 95003,
  "version": 1,
  "versionNonce": 95004,
  "isDeleted": false,
  "groupIds": ["legend_group"],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": null,
  "lineHeight": 1.25,
  "autoResize": true
}
```

### Legend Item Pattern

Each legend item = color swatch (small rectangle) + label text.

```json
// Color swatch
{
  "type": "rectangle",
  "id": "legend_swatch_frontend",
  "x": 920, "y": 545, "width": 24, "height": 24,
  "strokeColor": "#22d3ee",
  "backgroundColor": "rgba(8, 51, 68, 0.4)",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 95010,
  "version": 1,
  "versionNonce": 95011,
  "isDeleted": false,
  "groupIds": ["legend_group"],
  "boundElements": [],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

```json
// Swatch label
{
  "type": "text",
  "id": "legend_label_frontend",
  "x": 954, "y": 548,
  "width": 80, "height": 20,
  "text": "Frontend",
  "originalText": "Frontend",
  "fontSize": 14,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#a6adc8",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 95012,
  "version": 1,
  "versionNonce": 95013,
  "isDeleted": false,
  "groupIds": ["legend_group"],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": null,
  "lineHeight": 1.25,
  "autoResize": true
}
```

### Legend Spacing

- Swatch size: 24×24 px
- Gap between swatch and label: 10 px
- Vertical spacing between items: 32 px (swatch height + 8px gap)
- Padding inside legend container: 20 px

---

## Message Bus / Event Bus Pattern

Horizontal bus element connecting multiple services via fan-out arrows.

### Bus Element (Horizontal Bar)

```json
{
  "type": "rectangle",
  "id": "message_bus",
  "x": 200, "y": 300, "width": 500, "height": 40,
  "strokeColor": "#fb923c",
  "backgroundColor": "rgba(251, 146, 60, 0.3)",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 80001,
  "version": 1,
  "versionNonce": 80002,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [
    {"id": "bus_label", "type": "text"},
    {"id": "arrow_to_service1", "type": "arrow"},
    {"id": "arrow_to_service2", "type": "arrow"},
    {"id": "arrow_to_service3", "type": "arrow"}
  ],
  "link": null,
  "locked": false,
  "roundness": {"type": 3}
}
```

```json
// Bus label (centered)
{
  "type": "text",
  "id": "bus_label",
  "x": 380, "y": 308,
  "width": 140, "height": 25,
  "text": "Amazon EventBridge",
  "originalText": "Amazon EventBridge",
  "fontSize": 14,
  "fontFamily": 3,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#cdd6f4",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 80003,
  "version": 1,
  "versionNonce": 80004,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "containerId": "message_bus",
  "lineHeight": 1.25,
  "autoResize": true
}
```

### Fan-Out Arrow Pattern

Multiple arrows from bus to consuming services. Use `fixedPoint` to space arrows evenly along the bus bottom edge.

```json
// Arrow 1 — left consumer
{
  "type": "arrow",
  "id": "arrow_to_service1",
  "x": 300, "y": 340, "width": 0, "height": 60,
  "strokeColor": "#fb923c",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 80010,
  "version": 1,
  "versionNonce": 80011,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "points": [[0, 0], [0, 60]],
  "startBinding": {"elementId": "message_bus", "fixedPoint": [0.2, 1], "focus": 0},
  "endBinding": {"elementId": "service1", "fixedPoint": [0.5, 0], "focus": 0},
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": true
}
```

```json
// Arrow 2 — center consumer
{
  "type": "arrow",
  "id": "arrow_to_service2",
  "x": 450, "y": 340, "width": 0, "height": 60,
  "strokeColor": "#fb923c",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 80012,
  "version": 1,
  "versionNonce": 80013,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "points": [[0, 0], [0, 60]],
  "startBinding": {"elementId": "message_bus", "fixedPoint": [0.5, 1], "focus": 0},
  "endBinding": {"elementId": "service2", "fixedPoint": [0.5, 0], "focus": 0},
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": true
}
```

```json
// Arrow 3 — right consumer
{
  "type": "arrow",
  "id": "arrow_to_service3",
  "x": 600, "y": 340, "width": 0, "height": 60,
  "strokeColor": "#fb923c",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 80014,
  "version": 1,
  "versionNonce": 80015,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "link": null,
  "locked": false,
  "points": [[0, 0], [0, 60]],
  "startBinding": {"elementId": "message_bus", "fixedPoint": [0.8, 1], "focus": 0},
  "endBinding": {"elementId": "service3", "fixedPoint": [0.5, 0], "focus": 0},
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": true
}
```

### Fan-Out `fixedPoint` Calculation

For N consumers, distribute arrows evenly:
```
fixedPoint.x = (i + 1) / (N + 1)   where i = 0, 1, ..., N-1
```

Example for 3 consumers:
- Arrow 1: `fixedPoint: [0.25, 1]` (or `[0.2, 1]` for visual balance)
- Arrow 2: `fixedPoint: [0.5, 1]`
- Arrow 3: `fixedPoint: [0.75, 1]` (or `[0.8, 1]`)

---

## Arrow Z-Order Guide

Excalidraw renders elements in array order — **later elements appear on top**.

### Z-Order Principles

1. **Background elements first**: Canvas decorations, large boundaries
2. **Boundaries next**: Region → VPC → Security Group (outside-in)
3. **Components**: Rectangles, shapes with text
4. **Connectors last**: Arrows, lines (so they render above shapes)

### Semi-Transparent Fill Visibility

When using semi-transparent fills (e.g., `rgba(8, 51, 68, 0.4)`), arrows passing through shapes will be partially visible. This is often desirable for architecture diagrams.

**If you want arrows fully visible through shapes:**
- Use lower opacity fills: `rgba(..., 0.2)` to `rgba(..., 0.4)`
- Place arrows **after** all shapes in the elements array

**If arrows should appear behind shapes:**
- Place arrows **before** the overlapping shapes in the array
- Use solid fills (`fillStyle: "solid"` with opaque colors)

### Debugging Z-Order Issues

If arrows appear behind shapes unexpectedly:
1. Check the element order in the JSON `elements` array
2. Move arrow definitions to the end of the array
3. Verify no `groupIds` are causing unexpected stacking

### Example Element Order

```json
{
  "elements": [
    // 1. Boundaries (back to front)
    {"type": "rectangle", "id": "region_boundary", ...},
    {"type": "rectangle", "id": "vpc_boundary", ...},
    {"type": "rectangle", "id": "sg_boundary", ...},
    
    // 2. Components
    {"type": "rectangle", "id": "frontend_box", ...},
    {"type": "text", "id": "frontend_label", ...},
    {"type": "rectangle", "id": "backend_box", ...},
    {"type": "text", "id": "backend_label", ...},
    
    // 3. Arrows (always last for max visibility)
    {"type": "arrow", "id": "arrow_frontend_to_backend", ...},
    {"type": "arrow", "id": "arrow_backend_to_db", ...},
    
    // 4. Legend (on top of everything)
    {"type": "rectangle", "id": "legend_bg", ...},
    {"type": "text", "id": "legend_title", ...}
  ]
}
