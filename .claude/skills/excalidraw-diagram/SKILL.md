---
name: excalidraw-diagram
description: Create Excalidraw diagram JSON files that make visual arguments. Use when the user wants to visualize workflows, architectures, or concepts.
model: sonnet
---

# Excalidraw Diagram Creator

## Execution Model

**After loading this skill, you MUST immediately spawn an Agent with `model: "sonnet"` to execute the entire diagram generation task.** Do not generate the diagram in the main conversation — delegate all work (planning, JSON generation, rendering, validation) to the Sonnet agent. Pass the full user request and the skill's base directory path to the agent prompt.

---

Generate `.excalidraw` JSON files that **argue visually**, not just display information.

**Setup:** If the user asks you to set up this skill (renderer, dependencies, etc.), see `README.md` for instructions.

## Language Defaults

Default diagram wording based on the user's request language:

- If the user asks in **Traditional Chinese** and does not specify another language, generate diagram text primarily in **Traditional Chinese (Taiwan)**.
- If the user explicitly requests English or another language, follow that request.
- Keep code symbols, API names, framework names, file paths, and protocol keywords in their original English form.

### Terminology Guardrails (zh-TW requests)

Use Traditional Chinese for descriptive wording, but preserve English for domain-specific proper terms.

- **Preserve English terms** (do not translate): product names, protocol names, technical labels, and feature names.
- **Translate expressive wording** (can be zh-TW): actions, descriptions, relationship labels, and explanatory text.

If unsure, prefer keeping the technical term in English and localize surrounding explanatory text in Traditional Chinese.

## Customization

**All colors and brand-specific styles live in one file:** `references/color-palette.md`. Read it before generating any diagram and use it as the single source of truth for all color choices — shape fills, strokes, text colors, evidence artifact backgrounds, everything.

To make this skill produce diagrams in your own brand style, edit `color-palette.md`. Everything else in this file is universal design methodology and Excalidraw best practices.

---

## Theme Defaults

When the user does not specify a theme:
- Generate **both** light and dark versions of every diagram.
- Light version: `<name>.excalidraw` — uses light palette from `references/color-palette.md`.
- Dark version: `<name>-dark.excalidraw` — uses dark palette from `references/color-palette.md`.
- Render both versions to PNG for validation.

When the user specifies a single theme, generate only that version.

---

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram isn't formatted text. It's a visual argument that shows relationships, causality, and flow that words alone can't express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches—it shows actual formats, real event names, concrete examples.

---

## Depth Assessment (Do This First)

Before designing, determine what level of detail this diagram needs:

### Simple/Conceptual Diagrams

Use abstract shapes when:

- Explaining a mental model or philosophy
- The audience doesn't need technical specifics
- The concept IS the abstraction (e.g., "separation of concerns")

### Comprehensive/Technical Diagrams

Use concrete examples when:

- Diagramming a real system, protocol, or architecture
- The diagram will be used to teach or explain (e.g., YouTube video)
- The audience needs to understand what things actually look like
- You're showing how multiple technologies integrate

**For technical diagrams, you MUST include evidence artifacts** (see below).

---

## Research Mandate (For Technical Diagrams)

**Before drawing anything technical, research the actual specifications.**

If you're diagramming a protocol, API, or framework:

1. Look up the actual JSON/data formats
2. Find the real event names, method names, or API endpoints
3. Understand how the pieces actually connect
4. Use real terminology, not generic placeholders

Bad: "Protocol" → "Frontend"
Good: "AG-UI streams events (RUN_STARTED, STATE_DELTA, A2UI_UPDATE)" → "CopilotKit renders via createA2UIMessageRenderer()"

**Research makes diagrams accurate AND educational.**

---

## Evidence Artifacts

Evidence artifacts are concrete examples that prove your diagram is accurate and help viewers learn. Include them in technical diagrams.

**Types of evidence artifacts** (choose what's relevant to your diagram):

| Artifact Type            | When to Use                                | How to Render                                                                         |
| ------------------------ | ------------------------------------------ | ------------------------------------------------------------------------------------- |
| **Code snippets**        | APIs, integrations, implementation details | Dark rectangle + syntax-colored text (see color palette for evidence artifact colors) |
| **Data/JSON examples**   | Data formats, schemas, payloads            | Dark rectangle + colored text (see color palette)                                     |
| **Event/step sequences** | Protocols, workflows, lifecycles           | Timeline pattern (line + dots + labels)                                               |
| **UI mockups**           | Showing actual output/results              | Nested rectangles mimicking real UI                                                   |
| **Real input content**   | Showing what goes IN to a system           | Rectangle with sample content visible                                                 |
| **API/method names**     | Real function calls, endpoints             | Use actual names from docs, not placeholders                                          |

**Example**: For a diagram about a streaming protocol, you might show:

- The actual event names from the spec (not just "Event 1", "Event 2")
- A code snippet showing how to connect
- What the streamed data actually looks like

**Example**: For a diagram about a data transformation pipeline:

- Show sample input data (actual format, not "Input")
- Show sample output data (actual format, not "Output")
- Show intermediate states if relevant

The key principle: **show what things actually look like**, not just what they're called.

---

## Multi-Zoom Architecture

Comprehensive diagrams operate at multiple zoom levels simultaneously. Think of it like a map that shows both the country borders AND the street names.

### Level 1: Summary Flow

A simplified overview showing the full pipeline or process at a glance. Often placed at the top or bottom of the diagram.

_Example_: `Input → Processing → Output` or `Client → Server → Database`

### Level 2: Section Boundaries

Labeled regions that group related components. These create visual "rooms" that help viewers understand what belongs together.

_Example_: Grouping by responsibility (Backend / Frontend), by phase (Setup / Execution / Cleanup), or by team (User / System / External)

### Level 3: Detail Inside Sections

Evidence artifacts, code snippets, and concrete examples within each section. This is where the educational value lives.

_Example_: Inside a "Backend" section, you might show the actual API response format, not just a box labeled "API Response"

**For comprehensive diagrams, aim to include all three levels.** The summary gives context, the sections organize, and the details teach.

### Bad vs Good

| Bad (Displaying)              | Good (Arguing)                                     |
| ----------------------------- | -------------------------------------------------- |
| 5 equal boxes with labels     | Each concept has a shape that mirrors its behavior |
| Card grid layout              | Visual structure matches conceptual structure      |
| Icons decorating text         | Shapes that ARE the meaning                        |
| Same container for everything | Distinct visual vocabulary per concept             |
| Everything in a box           | Free-floating text with selective containers       |

### Simple vs Comprehensive (Know Which You Need)

| Simple Diagram                                 | Comprehensive Diagram                                     |
| ---------------------------------------------- | --------------------------------------------------------- |
| Generic labels: "Input" → "Process" → "Output" | Specific: shows what the input/output actually looks like |
| Named boxes: "API", "Database", "Client"       | Named boxes + examples of actual requests/responses       |
| "Events" or "Messages" label                   | Timeline with real event/message names from the spec      |
| "UI" or "Dashboard" rectangle                  | Mockup showing actual UI elements and content             |
| ~30 seconds to explain                         | ~2-3 minutes of teaching content                          |
| Viewer learns the structure                    | Viewer learns the structure AND the details               |

**Simple diagrams** are fine for abstract concepts, quick overviews, or when the audience already knows the details. **Comprehensive diagrams** are needed for technical architectures, tutorials, educational content, or when you want the diagram itself to teach.

---

## Container vs. Free-Floating Text

**Not every piece of text needs a shape around it.** Default to free-floating text. Add containers only when they serve a purpose.

| Use a Container When...                                   | Use Free-Floating Text When...                |
| --------------------------------------------------------- | --------------------------------------------- |
| It's the focal point of a section                         | It's a label or description                   |
| It needs visual grouping with other elements              | It's supporting detail or metadata            |
| Arrows need to connect to it                              | It describes something nearby                 |
| The shape itself carries meaning (decision diamond, etc.) | Typography alone creates sufficient hierarchy |
| It represents a distinct "thing" in the system            | It's a section title, subtitle, or annotation |

**Typography as hierarchy**: Use font size, weight, and color to create visual hierarchy without boxes. A 28px title doesn't need a rectangle around it.

**The container test**: For each boxed element, ask "Would this work as free-floating text?" If yes, remove the container.

---

## Design Process (Do This BEFORE Generating JSON)

### Step 0: Assess Depth Required

Before anything else, determine if this needs to be:

- **Simple/Conceptual**: Abstract shapes, labels, relationships (mental models, philosophies)
- **Comprehensive/Technical**: Concrete examples, code snippets, real data (systems, architectures, tutorials)

**If comprehensive**: Do research first. Look up actual specs, formats, event names, APIs.

### Step 1: Understand Deeply

Read the content. For each concept, ask:

- What does this concept **DO**? (not what IS it)
- What relationships exist between concepts?
- What's the core transformation or flow?
- **What would someone need to SEE to understand this?** (not just read about)

### Step 2: Map Concepts to Patterns

For each concept, find the visual pattern that mirrors its behavior:

| If the concept...               | Use this pattern                                   |
| ------------------------------- | -------------------------------------------------- |
| Spawns multiple outputs         | **Fan-out** (radial arrows from center)            |
| Combines inputs into one        | **Convergence** (funnel, arrows merging)           |
| Has hierarchy/nesting           | **Tree** (lines + free-floating text)              |
| Is a sequence of steps          | **Timeline** (line + dots + free-floating labels)  |
| Loops or improves continuously  | **Spiral/Cycle** (arrow returning to start)        |
| Is an abstract state or context | **Cloud** (overlapping ellipses)                   |
| Transforms input to output      | **Assembly line** (before → process → after)       |
| Compares two things             | **Side-by-side** (parallel with contrast)          |
| Separates into phases           | **Gap/Break** (visual separation between sections) |

### Step 3: Ensure Variety

For multi-concept diagrams: **each major concept must use a different visual pattern**. No uniform cards or grids.

### Step 4: Sketch the Flow

Before JSON, mentally trace how the eye moves through the diagram. There should be a clear visual story.

### Step 5: Generate JSON

Only now create the Excalidraw elements. **See below for how to handle large diagrams.**

### Step 6: Render & Validate (MANDATORY)

After generating the JSON, you MUST run the render-view-fix loop until the diagram looks right. This is not optional — see the **Render & Validate** section below for the full process.

---

## Large / Comprehensive Diagram Strategy

**For comprehensive or technical diagrams, you MUST build the JSON one section at a time.** Do NOT attempt to generate the entire file in a single pass. This is a hard constraint — Claude Code has a ~32,000 token output limit per response, and a comprehensive diagram easily exceeds that in one shot. Even if it didn't, generating everything at once leads to worse quality. Section-by-section is better in every way.

### The Section-by-Section Workflow

**Phase 1: Build each section**

1. **Create the base file** with the JSON wrapper (`type`, `version`, `appState`, `files`) and the first section of elements.
2. **Add one section per edit.** Each section gets its own dedicated pass — take your time with it. Think carefully about the layout, spacing, and how this section connects to what's already there.
3. **Use descriptive string IDs** (e.g., `"trigger_rect"`, `"arrow_fan_left"`) so cross-section references are readable.
4. **Namespace seeds by section** (e.g., section 1 uses 100xxx, section 2 uses 200xxx) to avoid collisions.
5. **Update cross-section bindings** as you go. When a new section's element needs to bind to an element from a previous section (e.g., an arrow connecting sections), edit the earlier element's `boundElements` array at the same time.

**Phase 2: Review the whole**

After all sections are in place, read through the complete JSON and check:

- Are cross-section arrows bound correctly on both ends?
- Is the overall spacing balanced, or are some sections cramped while others have too much whitespace?
- Do IDs and bindings all reference elements that actually exist?

Fix any alignment or binding issues before rendering.

**Phase 3: Render & validate**

Now run the render-view-fix loop from the Render & Validate section. This is where you'll catch visual issues that aren't obvious from JSON — overlaps, clipping, imbalanced composition.

### Section Boundaries

Plan your sections around natural visual groupings from the diagram plan. A typical large diagram might split into:

- **Section 1**: Entry point / trigger
- **Section 2**: First decision or routing
- **Section 3**: Main content (hero section — may be the largest single section)
- **Section 4-N**: Remaining phases, outputs, etc.

Each section should be independently understandable: its elements, internal arrows, and any cross-references to adjacent sections.

### What NOT to Do

- **Don't generate the entire diagram in one response.** You will hit the output token limit and produce truncated, broken JSON. Even if the diagram is small enough to fit, splitting into sections produces better results.
- **Don't use a coding agent** to generate the JSON. The agent won't have sufficient context about the skill's rules, and the coordination overhead negates any benefit.
- **Don't write a Python generator script.** The templating and coordinate math seem helpful but introduce a layer of indirection that makes debugging harder. Hand-crafted JSON with descriptive IDs is more maintainable.

---

## Visual Pattern Library

### Fan-Out (One-to-Many)

Central element with arrows radiating to multiple targets. Use for: sources, PRDs, root causes, central hubs.

```
        ○
       ↗
  □ → ○
       ↘
        ○
```

### Convergence (Many-to-One)

Multiple inputs merging through arrows to single output. Use for: aggregation, funnels, synthesis.

```
  ○ ↘
  ○ → □
  ○ ↗
```

### Tree (Hierarchy)

Parent-child branching with connecting lines and free-floating text (no boxes needed). Use for: file systems, org charts, taxonomies.

```
  label
  ├── label
  │   ├── label
  │   └── label
  └── label
```

Use `line` elements for the trunk and branches, free-floating text for labels.

### Spiral/Cycle (Continuous Loop)

Elements in sequence with arrow returning to start. Use for: feedback loops, iterative processes, evolution.

```
  □ → □
  ↑     ↓
  □ ← □
```

### Cloud (Abstract State)

Overlapping ellipses with varied sizes. Use for: context, memory, conversations, mental states.

### Assembly Line (Transformation)

Input → Process Box → Output with clear before/after. Use for: transformations, processing, conversion.

```
  ○○○ → [PROCESS] → □□□
  chaos              order
```

### Side-by-Side (Comparison)

Two parallel structures with visual contrast. Use for: before/after, options, trade-offs.

### Gap/Break (Separation)

Visual whitespace or barrier between sections. Use for: phase changes, context resets, boundaries.

### Lines as Structure

Use lines (type: `line`, not arrows) as primary structural elements instead of boxes:

- **Timelines**: Vertical or horizontal line with small dots (10-20px ellipses) at intervals, free-floating labels beside each dot
- **Tree structures**: Vertical trunk line + horizontal branch lines, with free-floating text labels (no boxes needed)
- **Dividers**: Thin dashed lines to separate sections
- **Flow spines**: A central line that elements relate to, rather than connecting boxes

```
Timeline:           Tree:
  ●─── Label 1        │
  │                   ├── item
  ●─── Label 2        │   ├── sub
  │                   │   └── sub
  ●─── Label 3        └── item
```

Lines + free-floating text often creates a cleaner result than boxes + contained text.

---

## Shape Meaning

Choose shape based on what it represents—or use no shape at all:

| Concept Type                  | Shape                         | Why                          |
| ----------------------------- | ----------------------------- | ---------------------------- |
| Labels, descriptions, details | **none** (free-floating text) | Typography creates hierarchy |
| Section titles, annotations   | **none** (free-floating text) | Font size/weight is enough   |
| Markers on a timeline         | small `ellipse` (10-20px)     | Visual anchor, not container |
| Start, trigger, input         | `ellipse`                     | Soft, origin-like            |
| End, output, result           | `ellipse`                     | Completion, destination      |
| Decision, condition           | `diamond`                     | Classic decision symbol      |
| Process, action, step         | `rectangle`                   | Contained action             |
| Abstract state, context       | overlapping `ellipse`         | Fuzzy, cloud-like            |
| Hierarchy node                | lines + text (no boxes)       | Structure through lines      |

**Rule**: Default to no container. Add shapes only when they carry meaning. Aim for <30% of text elements to be inside containers.

---

## ER Diagram (Entity-Relationship)

Excalidraw natively supports **crowfoot notation** arrowheads for proper ER diagrams. Use crowfoot arrowheads **plus** cardinality text labels for maximum clarity.

### When to Use

When the user asks for an ER diagram, data model diagram, or entity-relationship visualization.

### Conceptual Model Discipline (Simple ER — entities + relationships only)

When building a simplified ER diagram (no attributes, only entities and relationships), apply these 4 principles **before generating any JSON**. These are blocking checks — do not proceed to drawing until each is resolved.

#### 1. Eliminate Topological Redundancy & Transitive Dependencies

**Before drawing a direct line between two entities, check if the relationship can be inferred through intermediate entities.**

Example: If the path `使用者 → 專案 → 活動 → 問卷回覆` exists, a direct `使用者 → 問卷回覆` line is redundant UNLESS it represents an independent business concept (e.g., "問卷填寫者" vs "問卷建立者" are different roles).

**Rule**: For each cross-layer direct connection, ask: "Does this relationship carry independent business meaning that cannot be derived from the chain?" If no → remove. If yes → annotate with the distinct verb that justifies it.

#### 2. Standardize Notation (No Mixing)

Use **one** standard notation consistently throughout the diagram:

- **Crow's Foot Notation** (recommended): Use `crowfoot_one`, `crowfoot_many`, `crowfoot_one_or_many` arrowheads. Both ends of every relationship line must accurately express cardinality AND optionality (mandatory vs optional participation).
- **Chen Notation** (alternative): Diamond shapes for relationships, lines to entities with cardinality labels.

**Never mix**: Do not combine custom arrows, plain text labels, circle endpoints, and crowfoot marks in the same diagram. Pick one system and apply it uniformly.

#### 3. Label Relationships with Verbs

**Every relationship line MUST have a verb or verb phrase** (fontSize S/16) placed near the midpoint of the arrow. In a conceptual model without attributes, the verb on the relationship line is the ONLY thing that defines the business boundary between entities.

| Bad | Good |
|-----|------|
| 專案 → 活動 (unlabeled or "1:N") | 專案 —包含→ 活動 |
| 使用者 → 問卷回覆 | 使用者 —填寫→ 問卷回覆 |
| 活動 → 活動投入 | 活動 —產生→ 活動投入 |

The cardinality notation (crowfoot marks) expresses HOW MANY. The verb expresses WHAT the relationship IS. Both are required.

Format: **Bind the verb label directly to the arrow** — set `containerId: arrow_id` on the text and add the text id to the arrow's `boundElements`. Use fontSize S/16, color `#a6adc8` dark / `#64748b` light, `lineHeight: 1.35`, `autoResize: true`, `boundElements: []`. Position the text at the geometric midpoint of the arrow path. See the "Arrow with Bound Label" template in `references/element-templates.md`. **Verb only** — no cardinality text (the crowfoot marks express cardinality visually).

#### 4. Verify Cardinality Against Business Reality

**Challenge every assumed cardinality before drawing.**

For each relationship, explicitly ask:
- "Can entity A really only relate to ONE entity B, or could it be many?" (1:N vs M:N)
- "Is participation mandatory or optional?" (must every 活動 belong to a 專案, or could it be standalone?)
- "If this is M:N, do I need an associative entity to break it down?"

Common mistakes to catch:
| Assumed | Reality Check | Possible Fix |
|---------|--------------|--------------|
| 使用者 1:N 專案 (one owner) | Can projects have multiple collaborators? | → M:N via 專案成員 associative entity |
| 活動 1:N 問卷回覆 (one survey per activity) | Can one activity use multiple survey templates? | → Verify with stakeholder |
| 問卷模板 1:N 問卷回覆 | Is this always true, or can a response exist without a template? | → Check optionality (0..N vs 1..N) |

**When uncertain**: Ask the user. Do not guess cardinality — an incorrect cardinality in a conceptual model propagates errors into every downstream artifact (logical model, physical schema, application code).

### Available Arrowhead Types

Excalidraw supports these `endArrowhead` / `startArrowhead` values:

| Value | Visual | Use For |
|-------|--------|---------|
| `"arrow"` | → | Default, general flow |
| `"crowfoot_one"` | ─\|─ | "Exactly one" (crowfoot notation) |
| `"crowfoot_many"` | ─<─ | "Many" (crowfoot notation) |
| `"crowfoot_one_or_many"` | ─\|<─ | "One or many" (crowfoot notation) |
| `"circle"` | ─●─ | Filled circle endpoint |
| `"circle_outline"` | ─○─ | "Zero/optional" (hollow circle) |
| `"diamond"` | ─◆─ | Filled diamond (aggregation) |
| `"diamond_outline"` | ─◇─ | Hollow diamond (composition) |
| `"bar"` | ─\|─ | Bar/tick mark |
| `null` | ─── | No arrowhead |

### Crowfoot Cardinality Combos

Combine `startArrowhead` and `endArrowhead` to express ER cardinality:

| Relationship | Start → End | startArrowhead | endArrowhead |
|-------------|-------------|----------------|--------------|
| One-to-Many (1:N) | Parent → Child | `"crowfoot_one"` | `"crowfoot_many"` |
| One-to-One (1:1) | A → B | `"crowfoot_one"` | `"crowfoot_one"` |
| Many-to-Many (M:N) | A → B | `"crowfoot_many"` | `"crowfoot_many"` |
| Zero-or-Many (0..N) | Optional → Many | `"circle_outline"` | `"crowfoot_many"` |
| Zero-or-One (0..1) | Optional → One | `"circle_outline"` | `"crowfoot_one"` |
| One-to-One-or-Many | Parent → Flex | `"crowfoot_one"` | `"crowfoot_one_or_many"` |

### ER Diagram Design Rules

1. **Entity names**: Use the user's domain language (繁體中文 or English as requested), not raw SQL table names — unless the user explicitly wants technical names.
2. **Entity boxes**: Simple rectangles with contained text (table/entity name only). No column attributes unless the user asks for a detailed/comprehensive ER.
3. **Both endpoints must be specified**: Every ER relationship arrow MUST set BOTH `startArrowhead` and `endArrowhead`. Never leave either as `null` — the "1" side uses `"crowfoot_one"`, the "N" side uses `"crowfoot_many"` or `"crowfoot_one_or_many"`. Never use `"arrow"` for ER relationships. Reserve `"circle"`/`"circle_outline"` only for actual optional (0..1) relationships.
4. **Structural vs FK visual differentiation**: Use color and stroke weight to distinguish importance, NOT arrowhead type:
   - **Structural arrows**: Semantic stroke color (matching source entity) + `strokeWidth: 2`
   - **FK reference arrows**: Neutral color (`#ffffff` light / `#cdd6f4` dark) + `strokeWidth: 1`
   - Both use the SAME arrowhead notation for the same cardinality (e.g., both use `crowfoot_many` for 1:N).
5. **Arrow binding format**: Prefer `focus` + `gap` binding for natural Excalidraw curve behavior. Use `fixedPoint` only when you need precise endpoint pinning:
   ```json
   "startBinding": {"elementId": "tbl_a", "focus": 0.0, "gap": 1},
   "endBinding": {"elementId": "tbl_b", "focus": 0.0, "gap": 1}
   ```
   - `focus`: -1.0 (left/top edge) to 1.0 (right/bottom edge), 0.0 = center
   - `gap`: pixel distance from shape edge (typically 1)
6. **Arrow roundness**: Use `"roundness": {"type": 2}` for smooth curved ER arrows, not the sharp default.
7. **Relationship verb labels only — no cardinality text**: Since both arrow endpoints now use proper crowfoot marks (`crowfoot_one` / `crowfoot_many`), the visual notation IS the cardinality. Do NOT add redundant "1:N" text labels. Instead, label each arrow with its **verb phrase only** (e.g., "包含", "填寫", "產生"). **Bind the label to the arrow** via `containerId` (see ER Design Rule #3 above and the "Arrow with Bound Label" template in `references/element-templates.md`).

### Curved Arrow Overlap Avoidance

When multiple arrows share similar start/end regions (e.g., fan-out from a hub entity), **curved arrows will overlap** if not carefully managed. This is a common defect in ER diagrams — fix it proactively.

**Detection**: After generating arrows, mentally trace each path. If two arrows share a start entity AND have similar angles/directions, they will visually merge or cross.

**Prevention strategies**:

1. **Spread `focus` values**: When multiple arrows leave the same entity edge, assign distinct `focus` values to space them apart. E.g., three arrows leaving the bottom of "users" could use `focus: -0.6`, `focus: 0.0`, `focus: 0.6`.
2. **Use waypoints for routing**: For arrows spanning 2+ rows, add intermediate `points` to route around other entities instead of straight diagonals. An L-shaped or S-shaped path avoids crossing through Row 2 entities.
3. **Vary start/end edges**: Instead of all arrows leaving from the bottom, use left/right edges when the target is to the side. Mix bottom-exit with side-exit to reduce congestion.
4. **Check after render**: During the mandatory render-and-validate loop, specifically look for:
   - Two arrow paths that visually merge into one line (indistinguishable)
   - Arrows crossing through entity boxes they don't connect to
   - Arrow paths that run parallel and too close together (< 20px gap)
   - Cardinality labels overlapping with arrow lines or entity boxes

**Fix pattern for overlapping curves**: If two arrows from Entity A to Entity B and Entity C overlap, give them different curvature by adjusting `focus` at the shared end, or add a waypoint to push one curve outward:
```json
// Arrow 1: gentle curve
"points": [[0, 0], [100, 150]]
// Arrow 2: wider curve via waypoint
"points": [[0, 0], [60, 50], [120, 150]]
```

### ER Arrow Template

See `references/element-templates.md` → "ER Relationship Arrow" section for copy-paste JSON.

---

## Sequence Diagram

### When to Use

When the user asks for a sequence diagram, time-sequence flow, or interaction between multiple participants/systems over time.

### Structure

A sequence diagram has four structural layers:

1. **Participant headers** — Rectangles at the top, one per participant, with contained text labels.
2. **Lifelines** — Vertical dashed `line` elements extending down from each header.
3. **Activation boxes** — Thin `rectangle` elements (width ~24px) placed on lifelines during active periods. These serve as **arrow binding targets** (since `line` elements cannot be bound to).
4. **Message arrows** — Horizontal arrows between activation boxes, with bound text labels.

### Activation Boxes Are Mandatory for Binding

**Every lifeline that sends or receives an arrow MUST have an activation box at the corresponding y-position.** This is not optional — without activation boxes, arrows have no valid binding target, and users cannot reposition elements interactively.

| Participant Role | Activation Box |
|-----------------|---------------|
| Always active (main processor) | One tall box spanning the full active period |
| Called briefly (request/response) | Short box covering the call + return pair |
| Triggered once (initiator) | Small box (~24px height) at the trigger moment |

### Arrow Binding Pattern

Every message arrow must bind to activation boxes on both ends:

```json
{
  "type": "arrow",
  "id": "msg_query",
  "startBinding": {"elementId": "act_sender", "focus": -0.6, "gap": 1},
  "endBinding": {"elementId": "act_receiver", "focus": -0.7, "gap": 1}
}
```

The `focus` value (-1.0 to 1.0) controls where on the activation box edge the arrow attaches. For tall activation boxes, calculate focus based on the arrow's y-position relative to the box:

```
focus = (arrow_y - box_center_y) / (box_height / 2)
```

Where `box_center_y = box_y + box_height / 2`. This ensures arrows attach at the correct vertical position on tall boxes.

### Bidirectional Binding Consistency

Both the arrow and its target must reference each other:
- Arrow: `startBinding.elementId` → activation box ID
- Activation box: `boundElements` array must include `{"id": "arrow_id", "type": "arrow"}`

Missing either side will cause Excalidraw to treat the connection as unbound.

### Return Arrows (Dashed)

Use `strokeStyle: "dashed"` for return/response arrows. The arrow direction is reversed (start from the callee's activation box, end at the caller's).

### Alt/Error Fragments

Use a semi-transparent rectangle (`opacity: 25`) with dashed stroke to mark conditional regions. Place a small opaque label box at the top-left corner with the condition text.

### Sequence Diagram Checklist

1. Every participant has a header box + lifeline + at least one activation box
2. Every arrow has both `startBinding` and `endBinding` to activation boxes
3. Every activation box lists all its connected arrows in `boundElements`
4. Solid arrows for calls, dashed arrows for returns
5. Text labels bound to arrows via `containerId`
6. Focus values calculated correctly for tall activation boxes

---

## State Machine / Cyclic Graph Diagram

### When to Use

When the user asks for a state machine, workflow state diagram, or any diagram with bidirectional arrows between node pairs forming cycles.

### The Bidirectional Arrow Problem

Cyclic graphs inevitably have pairs of nodes with arrows going both directions (e.g., A→B and B→A). **Diagonal curved arrows between such pairs WILL cross in the center** — this is the #1 visual defect in state machine diagrams.

### Mandatory: Orthogonal Channel Routing

For any diagram with bidirectional arrows, use `elbowed: true` (orthogonal routing) instead of curved arrows. Route opposite-direction arrows through **separate parallel channels**:

```
  [A] ───────→ [B]         ← horizontal, no conflict
   ↑                ↓
   │ x=440    x=560 │      ← separate vertical channels
   │                │
  [C] ←─────── [D]
```

**Channel assignment rules:**
1. Identify all arrow pairs that share endpoints (A→B and B→A)
2. Assign each direction a distinct x-channel (for vertical segments) or y-channel (for horizontal segments)
3. Minimum channel separation: **50px** (more if labels are long)
4. Route each arrow as an L-shape or U-shape through its assigned channel

### Arrow Routing Patterns

| Pattern | Use When | Shape |
|---------|----------|-------|
| **Straight** | Direct horizontal or vertical between adjacent nodes | 2 points |
| **L-shape** | Node A's exit edge ≠ Node B's entry edge | 4 points: exit → turn → approach → enter |
| **U-shape** | Arrow must return to the same edge column (e.g., left→left) | 4 points: exit → outward → traverse → re-enter |

For L-shape and U-shape arrows, always use `elbowed: true` with explicit waypoints in the `points` array. Do NOT use `roundness: {"type": 2}` with multi-waypoint arrows — the curve smoothing causes L-shapes to bulge into neighboring paths, defeating the channel separation.

### Label Positioning for Orthogonal Arrows

**Problem**: Bound labels (`containerId` → arrow) auto-position at the arrow's geometric midpoint. For two L-shaped arrows with similar total path lengths, both midpoints land at the same y-position, causing label overlap.

**Solution**: Use **free-floating labels** (no `containerId`) for L-shape and U-shape arrows. Position each label manually along a distinct segment of its arrow path:

| Arrow direction | Place label on... | Position relative to arrow |
|----------------|-------------------|---------------------------|
| Return (A→B) | Upper portion of vertical segment | Left of the line |
| Forward (B→A) | Lower portion of vertical segment | Right of the line |

This ensures labels are visually associated with their arrow but never overlap each other.

### Color-Coding by Actor/Role

State machine transitions are often triggered by different actors. Use arrow stroke color to encode the actor:

```
Employee actions  → one color (e.g., blue)
Manager actions   → another color (e.g., green)
System actions    → another color (e.g., orange)
```

Match label `strokeColor` to the arrow color for consistency. Include a legend box showing the color-role mapping.

### State Machine Checklist

1. **No diagonal crossings**: All bidirectional pairs use separate orthogonal channels
2. **Elbowed routing**: Multi-waypoint arrows use `elbowed: true`, NOT `roundness`
3. **Channel separation ≥ 50px**: Parallel arrow paths are visually distinguishable
4. **Labels don't overlap**: Free-floating labels positioned on distinct segments
5. **Labels near their arrow**: Each label is clearly associated with one arrow, not ambiguous
6. **Color-coded by role**: Arrow colors encode the actor/trigger, with a legend
7. **All arrows bound**: Every arrow has `startBinding` and `endBinding` to state shapes

---

## Color as Meaning

Colors encode information, not decoration. Every color choice should come from `references/color-palette.md` — the semantic shape colors, text hierarchy colors, and evidence artifact colors are all defined there.

**Key principles:**

- Each semantic purpose (start, end, decision, AI, error, etc.) has a specific fill/stroke pair
- Free-floating text uses color for hierarchy (titles, subtitles, details — each at a different level)
- Evidence artifacts (code snippets, JSON examples) use their own dark background + colored text scheme
- Always pair a darker stroke with a lighter fill for contrast

**Do not invent new colors.** If a concept doesn't fit an existing semantic category, use Primary/Neutral or Secondary.

---

## Modern Aesthetics

For clean, professional diagrams:

### Roughness

- `roughness: 0` — Clean, crisp edges. Use for modern/technical diagrams.
- `roughness: 1` — Hand-drawn, organic feel. Use for brainstorming/informal diagrams.

**Default to 0** for most professional use cases.

### Stroke Width

- `strokeWidth: 1` — Thin, elegant. Good for lines, dividers, subtle connections.
- `strokeWidth: 2` — Standard. Good for shapes and primary arrows.
- `strokeWidth: 3` — Bold. Use sparingly for emphasis (main flow line, key connections).

### Opacity

**Always use `opacity: 100` for all elements.** Use color, size, and stroke width to create hierarchy instead of transparency.

### Small Markers Instead of Shapes

Instead of full shapes, use small dots (10-20px ellipses) as:

- Timeline markers
- Bullet points
- Connection nodes
- Visual anchors for free-floating text

---

## Layout Principles

### Hierarchy Through Scale

- **Hero**: 300×150 - visual anchor, most important
- **Primary**: 180×90
- **Secondary**: 120×60
- **Small**: 60×40

### Whitespace = Importance

The most important element has the most empty space around it (200px+).

### Flow Direction

Guide the eye: typically left→right or top→bottom for sequences, radial for hub-and-spoke.

### Connections Required

Position alone doesn't show relationships. If A relates to B, there must be an arrow.

### Arrow Routing Best Practices

**Avoid `elbowed: true`** — Elbowed arrows create right-angle bends that look cramped in tight spaces, especially for short vertical connectors (decision "否" paths). Prefer smooth curved arrows with `"roundness": {"type": 2}` and simple 2-point paths `[[0,0], [dx, dy]]`.

**Minimum arrow length** — Vertical connector arrows (e.g., "否" paths between cascading decisions) must be at least **80–90px** tall. Arrows shorter than 60px look cramped and make labels unreadable. When planning flowchart layout, use ≥90px vertical gap between consecutive decision shapes.

**Keep point arrays simple** — Use 2-point paths `[[0,0], [dx, dy]]` for direct connections. Only add intermediate waypoints when routing around obstacles. Multi-segment waypoints with `elbowed: true` frequently produce visual artifacts (unnecessary S-curves, tight zigzags).

---

## Text Rules

**CRITICAL**: The JSON `text` property contains ONLY readable words.

```json
{
  "id": "myElement1",
  "text": "Start",
  "originalText": "Start"
}
```

Default settings: `fontSize: 20`, `fontFamily: 3`, `textAlign: "center"`, `verticalAlign: "middle"`

### autoResize (Mandatory for ALL text elements)

**Every text element MUST include `"autoResize": true`**, regardless of whether it is free-floating, inside a container, or an arrow label.

- Without `autoResize: true`, Excalidraw treats the text box as manually sized. If the JSON specifies a width/height that doesn't match the rendered text, the box renders with excess padding or clipped content.
- With `autoResize: true`, Excalidraw recalculates the text box to fit its actual content on load. This is the correct behaviour.
- **Root cause of drift**: when the user saves from the Excalidraw UI, it writes corrected sizes back. Diffing shows `width: 204 → 133.5` / `height: 80 → 64.8` — the UI was auto-correcting what the generated JSON got wrong. Setting `autoResize: true` from the start prevents this drift.

Apply to **all** text types: free-floating labels, text bound inside shapes, and arrow labels.

### Bound Text Positioning (Critical for Correct Initial Render)

`autoResize: true` alone does NOT fix initial positioning — Excalidraw still uses the cached `x`/`y`/`width`/`height` for first render. If these are wrong (e.g., `width` set to `container.width - 20` instead of actual text width), text appears off-center until the user double-clicks to trigger recalculation.

**Always compute accurate dimensions for bound text:**

```
textHeight = numLines × fontSize × lineHeight
textWidth  = maxLineChars × fontSize × 0.6    (monospace approx for fontFamily 3)
text.x     = container.x + (container.width  - textWidth)  / 2
text.y     = container.y + (container.height - textHeight) / 2
```

- `numLines` = number of `\n`-separated lines in the text
- `maxLineChars` = character count of the longest line
- `fontSize × 0.6` approximates monospace character width for `fontFamily: 3`
- For CJK text (Chinese/Japanese/Korean), use `fontSize × 1.0` per character instead of `0.6`

**Common mistake**: setting `width` to `container.width - 20` and `height` to an arbitrary value. This produces visually correct-looking JSON but renders with misaligned text.

### Font Size Scale (Mandatory)

Only use these 4 sizes. Do NOT invent intermediate values (no 11px, 13px, 14px, 15px, etc.).

| Size | `fontSize` | Use For |
|------|-----------|---------|
| **XL** | `36` | Diagram title |
| **L** | `28` | Section headings, prominent labels |
| **M** | `20` | Entity/node names, body text, contained text in shapes |
| **S** | `16` | Labels, annotations, cardinality markers (`1:N`), metadata |

These values match `generate_diagram.js` (`fontSizes = { sm: 16, md: 20, lg: 28, xl: 36 }`).

**Rule**: Every text element must use one of these 4 sizes. If text feels too small at S (12), the diagram needs a layout change — not a different font size.

---

## Stability & Regeneration Rules

When diagrams are regenerated frequently, small JSON differences can cause arrows to shift or bindings to break after manual edits. Follow these rules to keep output stable and avoid rework.

### 1) Source of truth

- Treat the generator/spec as the source of truth.
- Do **not** make lasting fixes only in `output/*.excalidraw`; port every visual fix back to the generator/spec, then regenerate.

### 2) Binding discipline

- **Every arrow MUST have `startBinding` and `endBinding`** pointing to the shapes it connects. Arrows without bindings become disconnected when users drag elements in the Excalidraw editor — this is a usability defect, not a stylistic choice.
- The target shape's `boundElements` array must list the arrow, and the arrow's binding must reference the shape's `elementId`. Both sides of the binding must be consistent.
- For routed multi-segment arrows (L/U/Z paths), still bind both endpoints — use intermediate `points` for routing, not unbound endpoints.
- Keep rectangle↔text bindings consistent: rectangle `boundElements` references the text, and text `containerId` points back to the rectangle.
- **Binding target limitation**: Excalidraw `line` elements (e.g., lifelines, dividers) **cannot** be binding targets. Only `rectangle`, `ellipse`, `diamond`, and `image` elements support arrow binding. If you need arrows to connect to a line's position, place a small rectangle at that location as a binding anchor.

### 3) Coordinate hygiene

- Use integer `x`, `y`, `width`, `height`, and `points` values whenever possible.
- Avoid near-equal decimals (e.g., `824.9`) that can be re-snapped differently by the editor.
- Keep arrow direction intentional; do not rely on implicit sign flips in `height`/`width` to communicate flow.

### 4) Stable JSON shape

- **`boundElements`**: use `[]` (empty array) for all elements — never `null`. Using `null` causes Excalidraw to treat the element as having unknown binding state, which breaks when the editor adds connections later.
- Keep app state explicit and stable between generations (`viewBackgroundColor`, grid settings used by this repo).

### 5) Validation for drift

After render-and-review, do a quick drift check against the previous file:

- No unexpected connector reroutes
- No detached arrows
- No text/container de-binding
- No unintended appState churn

If drift appears, fix the generator/spec logic (not just the exported JSON) and regenerate.

---

## Output Directory

All generated `.excalidraw` files and their rendered `.png` files MUST be saved to the `output/` directory in the project root (e.g., `output/my-diagram-dark.excalidraw`). Do NOT save diagram files to the project root directory.

---

## JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

## Element Templates

See `references/element-templates.md` for copy-paste JSON templates for each element type (text, line, dot, rectangle, arrow). Pull colors from `references/color-palette.md` based on each element's semantic purpose.

---

## Render & Validate (MANDATORY)

You cannot judge a diagram from JSON alone. After generating or editing the Excalidraw JSON, you MUST render it to PNG, view the image, and fix what you see — in a loop until it's right. This is a core part of the workflow, not a final check.

### How to Render

```bash
cd .claude/skills/excalidraw-diagram/references && uv run python render_excalidraw.py <path-to-file.excalidraw>
```

This outputs a PNG next to the `.excalidraw` file. Then use the **Read tool** on the PNG to actually view it.

### The Loop

After generating the initial JSON, run this cycle:

**1. Render & View** — Run the render script, then Read the PNG.

**2. Audit against your original vision** — Before looking for bugs, compare the rendered result to what you designed in Steps 1-4. Ask:

- Does the visual structure match the conceptual structure you planned?
- Does each section use the pattern you intended (fan-out, convergence, timeline, etc.)?
- Does the eye flow through the diagram in the order you designed?
- Is the visual hierarchy correct — hero elements dominant, supporting elements smaller?
- For technical diagrams: are the evidence artifacts (code snippets, data examples) readable and properly placed?

**3. Check for visual defects:**

- Text clipped by or overflowing its container
- Text or shapes overlapping other elements
- Arrows crossing through elements instead of routing around them
- Arrows landing on the wrong element or pointing into empty space
- Labels floating ambiguously (not clearly anchored to what they describe)
- Uneven spacing between elements that should be evenly spaced
- Sections with too much whitespace next to sections that are too cramped
- Text too small to read at the rendered size
- Overall composition feels lopsided or unbalanced

**4. Fix** — Edit the JSON to address everything you found. Common fixes:

- Widen containers when text is clipped
- Adjust `x`/`y` coordinates to fix spacing and alignment
- Add intermediate waypoints to arrow `points` arrays to route around elements
- Reposition labels closer to the element they describe
- Resize elements to rebalance visual weight across sections

**5. Re-render & re-view** — Run the render script again and Read the new PNG.

**6. Repeat** — Keep cycling until the diagram passes both the vision check (Step 2) and the defect check (Step 3). Typically takes 2-4 iterations. Don't stop after one pass just because there are no critical bugs — if the composition could be better, improve it.

### When to Stop

The loop is done when:

- The rendered diagram matches the conceptual design from your planning steps
- No text is clipped, overlapping, or unreadable
- Arrows route cleanly and connect to the right elements
- Spacing is consistent and the composition is balanced
- You'd be comfortable showing it to someone without caveats

### First-Time Setup

If the render script hasn't been set up yet:

```bash
cd .claude/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

### Auto-Validate After Render (MANDATORY)

After every render, you MUST use the **Read tool to open the PNG image** and visually analyze it yourself. Do NOT skip this step, do NOT assume the diagram is correct based on the JSON alone, and do NOT wait for the user to point out problems. **You are a multimodal model — use your vision capability to inspect the rendered output.**

This is not a suggestion; it is a blocking step in the generation pipeline. The diagram is not done until you have personally seen and approved the rendered PNG.

**The self-review process:**

1. **Render** — Run the render script.
2. **Read the PNG** — Use the Read tool on the output `.png` file. Actually look at the image.
3. **Narrate what you see** — Mentally walk through the diagram: trace each arrow, read each label, check each connection. Describe any issues you find (even in your internal reasoning).
4. **Decide: pass or fix** — If any defect is found, fix it in the JSON, re-render, and re-read. Do NOT present a diagram with known issues to the user.

**What to check (visual inspection checklist):**

1. **Arrow path overlap** — Are any two arrows visually indistinguishable because they follow the same path? **How to actually check**: for each entity that has 2+ outgoing or incoming arrows, ask "can I trace each arrow as a separate line from start to end?" If two lines appear to merge into one at any segment, they overlap.

2. **Endpoint congestion** — Do multiple arrows arrive at the same small area of an entity? When 3+ arrows converge on the same edge within ~60px, their arrowheads (crowfoot marks, circles, arrow tips) will visually stack and become unreadable. **Fix**: spread arrival `focus` values across the full edge (-0.7, 0.0, 0.7), or route some arrows to arrive from different edges (top vs. left vs. right).

3. **Arrow-entity collision** — Do any arrows pass through entity boxes they don't connect to? **How to actually check**: for each arrow, trace its full curved path at y-values where Row 2 or Row 3 entities exist, and verify the x-coordinate falls in a gap between entities, not inside one.

4. **Label-arrow collision** — Are any labels sitting on top of an arrow line? **Arrow labels must use `containerId` binding** (see "Arrow with Bound Label" template) — they render at the midpoint automatically and never collide with the path. Free-floating text near arrows is wrong and will cause visual collisions.

5. **Label-entity collision** — Are any labels overlapping with entity boxes?

6. **Disconnected arrows** — Do arrow endpoints visually touch their target entity edges, or float in empty space?

7. **Text clipping** — Is any text cut off by its container boundary?

8. **Color contrast** — Can you read ALL text against the background? **Common blind spot**: labels using muted colors (e.g., `#585b70`) on dark backgrounds (`#1e1e2e`) are nearly invisible. If a label's color is within 2 perceptual steps of the background, it won't be readable in the PNG. Use at minimum `#a6adc8` for text on dark backgrounds.

9. **Readability at scale** — Can you read all text in the rendered image? fontSize 11 labels may be too small at certain render scales.

10. **Compositional balance** — Is one area overcrowded while another is mostly empty?

### Common Blind Spots (Patterns That Pass Mental Review But Fail Visually)

These are the defects most likely to be missed during self-review. Check for them explicitly:

| Blind Spot | Why It's Missed | How to Catch |
|-----------|----------------|--------------|
| **Same-edge fan-out overlap** | "I used different focus values" — but the curves still merge near the shared entity because the angular separation is too small | Trace the first 50px of each arrow's path. If two start <30px apart AND go in similar directions (< 30° angle difference), they WILL merge |
| **Invisible labels** | "I added labels" — but used a color too close to the background | In the PNG, try to read every single label. If you have to squint or zoom, it fails |
| **Arrowhead pile-up** | "I spread the focus values" — but 3 arrows still converge within 60px, stacking crowfoot/circle marks | Count how many arrows arrive at each entity. If ≥ 3 arrive on the same edge, at least one should be routed to a different edge |
| **Waypoint crosses entity** | "The endpoints are correct" — but the intermediate curve bulges through an entity between start and end | Calculate x-coordinate at each Row's y-level for curved/diagonal arrows |

### Self-Honesty Rule

**Do NOT rationalize issues away.** If something looks "a little close" or "probably fine", it is a defect. The standard is: "would a design reviewer accept this without comment?" If the answer is anything less than confident yes, fix it. A false PASS is worse than an extra render cycle.

**Auto-fix strategies when you find issues:**

| Problem | Fix |
|---------|-----|
| Two arrows visually merged | Change one to exit from a DIFFERENT EDGE (left vs bottom), not just different focus on same edge |
| Endpoint congestion (3+ arrows same edge) | Route at least one arrow to arrive from a different edge entirely |
| Arrow crosses through unrelated entity | Add intermediate `points` to route around the entity |
| Label overlaps arrow line | Use bound label (`containerId: arrow_id`) — renders at path midpoint automatically, eliminates manual positioning |
| Label invisible against background | Use minimum `#a6adc8` on dark, `#64748b` on light — never `#585b70` on dark |
| Arrow endpoint floating | Verify binding `elementId` matches target, adjust `focus`/`gap` |
| Text clipped | Widen container or reduce font size |
| Cramped section | Increase overall spacing, push downstream elements right/down |

**After fixing, re-render and re-read the PNG.** Repeat until the image passes all checks. Do not present the result to the user until it passes visual inspection.

**Common mistake to avoid**: Rendering the PNG but NOT reading it with the Read tool. The render step alone tells you nothing — you must actually view the image output. Another common mistake: reading the PNG but doing a cursory glance instead of tracing each arrow individually.

---

## Quality Checklist

### Depth & Evidence (Check First for Technical Diagrams)

1. **Research done**: Did you look up actual specs, formats, event names?
2. **Evidence artifacts**: Are there code snippets, JSON examples, or real data?
3. **Multi-zoom**: Does it have summary flow + section boundaries + detail?
4. **Concrete over abstract**: Real content shown, not just labeled boxes?
5. **Educational value**: Could someone learn something concrete from this?

### Conceptual

6. **Isomorphism**: Does each visual structure mirror its concept's behavior?
7. **Argument**: Does the diagram SHOW something text alone couldn't?
8. **Variety**: Does each major concept use a different visual pattern?
9. **No uniform containers**: Avoided card grids and equal boxes?

### Container Discipline

10. **Minimal containers**: Could any boxed element work as free-floating text instead?
11. **Lines as structure**: Are tree/timeline patterns using lines + text rather than boxes?
12. **Typography hierarchy**: Are font size and color creating visual hierarchy (reducing need for boxes)?

### Structural

13. **Connections**: Every relationship has an arrow or line
14. **Flow**: Clear visual path for the eye to follow
15. **Hierarchy**: Important elements are larger/more isolated

### Technical

16. **Text clean**: `text` contains only readable words
17. **Font**: `fontFamily: 3`
18. **Roughness**: `roughness: 0` for clean/modern (unless hand-drawn style requested)
19. **Opacity**: `opacity: 100` for all elements (no transparency)
20. **Container ratio**: <30% of text elements should be inside containers

### Visual Validation (Render Required)

21. **Rendered to PNG**: Diagram has been rendered and visually inspected
22. **No text overflow**: All text fits within its container
23. **No overlapping elements**: Shapes and text don't overlap unintentionally
24. **Even spacing**: Similar elements have consistent spacing
25. **Arrows land correctly**: Arrows connect to intended elements without crossing others
26. **Readable at export size**: Text is legible in the rendered PNG
27. **Balanced composition**: No large empty voids or overcrowded regions
