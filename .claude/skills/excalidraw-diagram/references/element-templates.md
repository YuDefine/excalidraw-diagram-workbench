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
  "boundElements": null,
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
- `"elbowed": true` — Orthogonal (right-angle) routing. Best for structured diagrams, channel maps. This is what `generate_diagram.js` uses.
- `"elbowed": false` + `"roundness": {"type": 2}` — Smooth curves. Best for ER diagrams, organic flows.

**Binding format**: Include both `fixedPoint` and `focus` for maximum compatibility (matches `generate_diagram.js` convention):
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
  "fontFamily": 3,
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
- The `generate_diagram.js` `arrow()` function accepts `label` in its options object — it calls `pathMidpoint()` and creates the bound text automatically

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
