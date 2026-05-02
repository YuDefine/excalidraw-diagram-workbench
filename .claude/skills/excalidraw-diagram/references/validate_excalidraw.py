"""Validate Excalidraw JSON for text overflow and binding consistency.

For text overflow: measures every text element via headless Chromium canvas
measureText() with the same font stacks Excalidraw uses, so widths are
pixel-equivalent to what gets rendered. Then compares each text's right edge
against any rectangle/ellipse/diamond that visually contains it (or its
explicit ``containerId``), flagging anything that spills past the container.

For bindings: walks the JSON to verify every ``startBinding`` /
``endBinding`` references an existing element, every bound element has the
matching reverse pointer in ``boundElements``, and reports unbound arrow
endpoints that sit on a rectangle edge (likely missed binding).

Usage:
    cd .claude/skills/excalidraw-diagram/references

    # Validate one or more files / directories
    uv run python validate_excalidraw.py path/to/file.excalidraw [more.excalidraw]
    uv run python validate_excalidraw.py path/to/dir/

    # Default scope: every *.excalidraw under <repo>/output and <repo>/temp
    uv run python validate_excalidraw.py

    # JSON output for CI / scripts
    uv run python validate_excalidraw.py --json

    # Auto-fix safe issues (orphan boundElements, missing reverse pointers,
    # unambiguous unbound endpoints) — writes back to the source file.
    uv run python validate_excalidraw.py path/to/file.excalidraw --fix

First-time setup is shared with render_excalidraw.py:
    uv sync && uv run playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Excalidraw constant: padding inside a container before bound text starts.
# Source: BOUND_TEXT_PADDING in @excalidraw/excalidraw constants.
BOUND_TEXT_PADDING_PX = 5

# Strict check for unbound text whose origin sits inside a rectangle.
# We don't know the designer's intended padding, so we only flag when the
# text's rendered right edge spills past the rectangle's right edge by more
# than this slack. This catches "real" overflow (text visibly escapes the
# box) without false-positive on tight-fit decorative labels.
UNBOUND_TEXT_OVERFLOW_SLACK_PX = 0.5

# Distance an arrow endpoint may sit from a rectangle edge before we assume
# it was meant to be bound to that rectangle. Excalidraw itself usually
# binds when the gap is ≤ ~12-15px during interactive draw.
EDGE_PROXIMITY_PX = 12


@dataclass
class Finding:
    level: str  # "error" | "warning" | "info"
    kind: str
    message: str
    fix_payload: dict[str, Any] | None = None  # for --fix mode

    def as_dict(self) -> dict:
        d = {"level": self.level, "kind": self.kind, "message": self.message}
        if self.fix_payload is not None:
            d["fix_payload"] = self.fix_payload
        return d


# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------


def load_excalidraw(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_excalidraw(path: Path, data: dict[str, Any]) -> None:
    # Preserve a trailing newline because Excalidraw's own writer emits one
    # and most editors will re-add it on save anyway.
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Browser-backed text measurement
# ---------------------------------------------------------------------------


def measure_batch(file_data: list[tuple[Path, dict]], template_url: str) -> dict[Path, dict[str, dict] | None]:
    """Open one Chromium, measure every file, return per-file element-id → metrics."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: uv sync && uv run playwright install chromium", file=sys.stderr)
        sys.exit(2)

    results: dict[Path, dict[str, dict] | None] = {}

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                print("ERROR: Chromium not installed for Playwright. Run: uv run playwright install chromium", file=sys.stderr)
                sys.exit(2)
            raise

        try:
            page = browser.new_page(viewport={"width": 800, "height": 600})
            load_events: list[str] = []
            page.on("pageerror", lambda exc: load_events.append(f"pageerror: {exc}"))
            page.on(
                "requestfailed",
                lambda req: load_events.append(f"requestfailed: {req.url} {req.failure}"),
            )
            page.on(
                "console",
                lambda msg: (
                    load_events.append(f"console.{msg.type}: {msg.text}")
                    if msg.type in ("error", "warning")
                    else None
                ),
            )

            page.goto(template_url)
            try:
                page.wait_for_function(
                    "window.__moduleReady === true || Boolean(window.__moduleError)",
                    timeout=60000,
                )
            except Exception:
                print("ERROR: Renderer libraries did not become ready within 60 seconds.", file=sys.stderr)
                for event in load_events[-12:]:
                    print(f"  - {event}", file=sys.stderr)
                sys.exit(2)

            module_error = page.evaluate("window.__moduleError || null")
            if module_error:
                print("ERROR: Renderer libraries failed to load:", file=sys.stderr)
                for line in str(module_error).splitlines():
                    print(f"  - {line}", file=sys.stderr)
                for event in load_events[-12:]:
                    print(f"  - {event}", file=sys.stderr)
                sys.exit(2)

            for path, data in file_data:
                try:
                    result = page.evaluate(
                        "(d) => window.measureElements(d)",
                        data,
                    )
                except Exception as e:
                    print(f"✗ {path}: measurement evaluate failed: {e}", file=sys.stderr)
                    results[path] = None
                    continue
                if not result or not result.get("success"):
                    err = result.get("error") if result else "null"
                    print(f"✗ {path}: measurement failed: {err}", file=sys.stderr)
                    results[path] = None
                else:
                    results[path] = result.get("measurements", {})
        finally:
            browser.close()

    return results


# ---------------------------------------------------------------------------
# Overflow detection
# ---------------------------------------------------------------------------


CONTAINER_TYPES = {"rectangle", "ellipse", "diamond"}


def find_geometric_container(text_el: dict, candidates: list[dict]) -> dict | None:
    """Smallest container that geometrically encloses the text element's origin."""
    tx, ty = text_el["x"], text_el["y"]
    smallest = None
    smallest_area = float("inf")
    for c in candidates:
        cx, cy = c["x"], c["y"]
        cw, ch = c["width"], c["height"]
        if cx <= tx <= cx + cw and cy <= ty <= cy + ch:
            area = cw * ch
            if area < smallest_area:
                smallest_area = area
                smallest = c
    return smallest


def check_overflow(elements: list[dict], measurements: dict[str, dict]) -> list[Finding]:
    findings: list[Finding] = []
    by_id = {e["id"]: e for e in elements if not e.get("isDeleted")}
    containers = [e for e in elements if not e.get("isDeleted") and e.get("type") in CONTAINER_TYPES]

    for el in elements:
        if el.get("isDeleted") or el.get("type") != "text":
            continue
        m = measurements.get(el["id"])
        if not m:
            continue

        text_w = m["renderedWidth"]
        text_h = m["renderedHeight"]

        # Determine intended container and padding model.
        container = None
        padding = 0.0
        is_explicit = False
        if el.get("containerId"):
            container = by_id.get(el["containerId"])
            padding = BOUND_TEXT_PADDING_PX
            is_explicit = True
        else:
            container = find_geometric_container(el, containers)
            padding = 0.0  # unknown intent — only flag when text actually escapes

        if container is None:
            continue

        # Arrow / line "containers" are label hosts: Excalidraw centers the
        # label along the curve and the curve's bbox is not a content area.
        # Width/height comparison is meaningless here — skip.
        if container.get("type") in ("arrow", "line"):
            continue

        cx, cy = container["x"], container["y"]
        cw, ch = container["width"], container["height"]

        if is_explicit:
            # Excalidraw centers bound text inside the container, so check
            # against the container's interior extents.
            interior_w = cw - 2 * padding
            interior_h = ch - 2 * padding
            overflow_x = text_w - interior_w
            overflow_y = text_h - interior_h
        else:
            # The text element is laid out at its own (x, y). Only flag if
            # its right/bottom edge actually escapes the container's right/
            # bottom edge.
            tx, ty = el["x"], el["y"]
            overflow_x = (tx + text_w) - (cx + cw)
            overflow_y = (ty + text_h) - (cy + ch)

        if overflow_x > UNBOUND_TEXT_OVERFLOW_SLACK_PX or overflow_y > UNBOUND_TEXT_OVERFLOW_SLACK_PX:
            preview = (el.get("originalText") or el.get("text") or "")
            preview = preview.replace("\n", " ⏎ ")[:48]
            mode = "containerId" if is_explicit else "geometric"
            details = (
                f"text {el['id']!r} (\"{preview}\") renders {text_w:.1f}×{text_h:.1f}px "
                f"but container {container['id']!r} ({container.get('type')}, {cw:.0f}×{ch:.0f}px) "
                f"only allows {(cw - 2 * padding):.0f}×{(ch - 2 * padding):.0f}px interior; "
                f"overflow x={overflow_x:+.1f}px y={overflow_y:+.1f}px ({mode})"
            )
            findings.append(
                Finding(
                    level="error",
                    kind="text-overflow",
                    message=details,
                    fix_payload=None,  # auto-fix would require resizing — leave to designer
                )
            )

    return findings


# ---------------------------------------------------------------------------
# Binding validation
# ---------------------------------------------------------------------------


BINDABLE_TYPES = {"rectangle", "ellipse", "diamond", "text", "image"}


def arrow_endpoints(arrow: dict) -> tuple[tuple[float, float], tuple[float, float]] | None:
    pts = arrow.get("points")
    if not pts or len(pts) < 2:
        return None
    x, y = arrow["x"], arrow["y"]
    return (x + pts[0][0], y + pts[0][1]), (x + pts[-1][0], y + pts[-1][1])


def distance_to_rect_edge(point: tuple[float, float], el: dict) -> float:
    """Closest distance from point to element's perimeter."""
    px, py = point
    rx, ry = el["x"], el["y"]
    rw, rh = el["width"], el["height"]
    rr, rb = rx + rw, ry + rh
    if rx <= px <= rr and ry <= py <= rb:
        return min(px - rx, rr - px, py - ry, rb - py)
    cx = max(rx, min(px, rr))
    cy = max(ry, min(py, rb))
    dx, dy = px - cx, py - cy
    return (dx * dx + dy * dy) ** 0.5


def check_bindings(elements: list[dict]) -> list[Finding]:
    findings: list[Finding] = []
    by_id = {e["id"]: e for e in elements if not e.get("isDeleted")}

    for el in elements:
        if el.get("isDeleted"):
            continue

        # Arrow → bindings
        if el.get("type") == "arrow":
            for side in ("startBinding", "endBinding"):
                binding = el.get(side)
                if not binding:
                    continue
                target_id = binding.get("elementId")
                target = by_id.get(target_id)
                if target is None:
                    findings.append(
                        Finding(
                            level="error",
                            kind="binding-target-missing",
                            message=f"arrow {el['id']!r} {side} → missing element {target_id!r}",
                            fix_payload={"action": "clear-binding", "arrow_id": el["id"], "side": side},
                        )
                    )
                    continue
                if target.get("type") not in BINDABLE_TYPES:
                    findings.append(
                        Finding(
                            level="error",
                            kind="binding-target-not-bindable",
                            message=(
                                f"arrow {el['id']!r} {side} → {target_id!r} of type "
                                f"{target.get('type')!r} is not bindable"
                            ),
                            fix_payload={"action": "clear-binding", "arrow_id": el["id"], "side": side},
                        )
                    )
                    continue
                bound = target.get("boundElements") or []
                if not any(b.get("id") == el["id"] for b in bound):
                    findings.append(
                        Finding(
                            level="error",
                            kind="binding-reverse-missing",
                            message=(
                                f"arrow {el['id']!r} {side} → {target_id!r} but "
                                f"{target_id}.boundElements is missing this arrow"
                            ),
                            fix_payload={
                                "action": "add-bound-element",
                                "host_id": target_id,
                                "arrow_id": el["id"],
                            },
                        )
                    )

            # Suggest binding for unbound endpoints sitting on a bindable edge.
            endpoints = arrow_endpoints(el)
            if endpoints:
                for side, point in zip(("startBinding", "endBinding"), endpoints):
                    if el.get(side):
                        continue
                    candidates = []
                    for other in elements:
                        if other.get("isDeleted") or other["id"] == el["id"]:
                            continue
                        if other.get("type") not in BINDABLE_TYPES:
                            continue
                        d = distance_to_rect_edge(point, other)
                        if d <= EDGE_PROXIMITY_PX:
                            candidates.append((other["id"], d))
                    if len(candidates) == 1:
                        cid, dist = candidates[0]
                        findings.append(
                            Finding(
                                level="warning",
                                kind="binding-suggested",
                                message=(
                                    f"arrow {el['id']!r} {side} unbound; endpoint sits "
                                    f"{dist:.1f}px from {cid!r} edge — likely intended binding"
                                ),
                                fix_payload={
                                    "action": "create-binding",
                                    "arrow_id": el["id"],
                                    "side": side,
                                    "target_id": cid,
                                    "gap": max(1, round(dist)),
                                },
                            )
                        )
                    elif len(candidates) > 1:
                        ids = sorted(candidates, key=lambda t: t[1])
                        findings.append(
                            Finding(
                                level="info",
                                kind="binding-ambiguous",
                                message=(
                                    f"arrow {el['id']!r} {side} unbound; endpoint near "
                                    f"multiple candidates: {[c[0] for c in ids]} — pick one manually"
                                ),
                            )
                        )

        # Element with boundElements → arrow consistency
        bound = el.get("boundElements")
        if isinstance(bound, list):
            for ref in bound:
                ref_id = ref.get("id")
                ref_type = ref.get("type")
                referenced = by_id.get(ref_id)
                if referenced is None:
                    findings.append(
                        Finding(
                            level="error",
                            kind="boundelements-target-missing",
                            message=(
                                f"element {el['id']!r} boundElements references missing {ref_id!r}"
                            ),
                            fix_payload={
                                "action": "remove-bound-element",
                                "host_id": el["id"],
                                "ref_id": ref_id,
                            },
                        )
                    )
                    continue
                if ref_type == "arrow" and referenced.get("type") == "arrow":
                    points_back = (
                        (referenced.get("startBinding") or {}).get("elementId") == el["id"]
                        or (referenced.get("endBinding") or {}).get("elementId") == el["id"]
                    )
                    if not points_back:
                        findings.append(
                            Finding(
                                level="error",
                                kind="boundelements-reverse-missing",
                                message=(
                                    f"element {el['id']!r} boundElements lists arrow "
                                    f"{ref_id!r} but the arrow has no startBinding / endBinding "
                                    f"pointing back to {el['id']!r}"
                                ),
                                fix_payload={
                                    "action": "remove-bound-element",
                                    "host_id": el["id"],
                                    "ref_id": ref_id,
                                },
                            )
                        )

    return findings


# ---------------------------------------------------------------------------
# Auto-fix
# ---------------------------------------------------------------------------


def apply_fixes(data: dict, findings: list[Finding]) -> int:
    """Mutate `data` in place using each finding's fix_payload. Return count applied."""
    elements = data.get("elements", [])
    by_id = {e["id"]: e for e in elements if not e.get("isDeleted")}
    applied = 0

    for f in findings:
        payload = f.fix_payload
        if not payload:
            continue
        action = payload.get("action")

        if action == "clear-binding":
            arrow = by_id.get(payload["arrow_id"])
            if arrow:
                arrow[payload["side"]] = None
                applied += 1

        elif action == "add-bound-element":
            host = by_id.get(payload["host_id"])
            if host:
                host.setdefault("boundElements", [])
                if not any(b.get("id") == payload["arrow_id"] for b in host["boundElements"]):
                    host["boundElements"].append({"id": payload["arrow_id"], "type": "arrow"})
                    applied += 1

        elif action == "remove-bound-element":
            host = by_id.get(payload["host_id"])
            if host and isinstance(host.get("boundElements"), list):
                before = len(host["boundElements"])
                host["boundElements"] = [
                    b for b in host["boundElements"] if b.get("id") != payload["ref_id"]
                ]
                if len(host["boundElements"]) != before:
                    applied += 1

        elif action == "create-binding":
            arrow = by_id.get(payload["arrow_id"])
            target = by_id.get(payload["target_id"])
            if arrow and target:
                arrow[payload["side"]] = {
                    "elementId": payload["target_id"],
                    "focus": 0,
                    "gap": payload["gap"],
                }
                target.setdefault("boundElements", [])
                if not any(b.get("id") == arrow["id"] for b in target["boundElements"]):
                    target["boundElements"].append({"id": arrow["id"], "type": "arrow"})
                applied += 1

    return applied


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def format_text_report(path: Path, overflows: list[Finding], bindings: list[Finding]) -> str:
    if not overflows and not bindings:
        return f"✓ {path}"
    lines = [f"✗ {path}"]
    if overflows:
        lines.append("  [Text Overflow]")
        for f in overflows:
            lines.append(f"    - {f.message}")
    if bindings:
        errors = [f for f in bindings if f.level == "error"]
        warnings = [f for f in bindings if f.level == "warning"]
        infos = [f for f in bindings if f.level == "info"]
        if errors:
            lines.append("  [Binding Errors]")
            for f in errors:
                lines.append(f"    - {f.message}")
        if warnings:
            lines.append("  [Binding Warnings]")
            for f in warnings:
                lines.append(f"    - {f.message}")
        if infos:
            lines.append("  [Binding Info]")
            for f in infos:
                lines.append(f"    - {f.message}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def collect_files(inputs: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in inputs:
        if p.is_dir():
            files.extend(sorted(p.rglob("*.excalidraw")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"WARN: skipping {p} (not found)", file=sys.stderr)
    return files


def resolve_default_inputs() -> list[Path]:
    """Default scope when no args: every *.excalidraw under repo `output/` and `temp/`."""
    cwd = Path.cwd()
    repo_root = Path(__file__).resolve().parents[4]
    roots: list[Path] = []
    for candidate in (cwd / "output", cwd / "temp", repo_root / "output", repo_root / "temp"):
        if candidate.is_dir() and candidate not in roots:
            roots.append(candidate)
    return roots


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate .excalidraw files for text overflow and binding consistency.",
    )
    parser.add_argument("inputs", nargs="*", type=Path, help=".excalidraw files or directories")
    parser.add_argument("--json", action="store_true", help="emit JSON report instead of text")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat binding warnings (suggested bindings) as failures",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="apply safe auto-fixes back to the source file (orphan refs, "
        "missing reverse pointers, unambiguous unbound endpoints)",
    )
    args = parser.parse_args()

    files = collect_files(args.inputs) if args.inputs else collect_files(resolve_default_inputs())
    if not files:
        print("No .excalidraw files to validate", file=sys.stderr)
        return 0

    template = Path(__file__).parent / "validate_template.html"
    if not template.exists():
        print(f"ERROR: template not found at {template}", file=sys.stderr)
        return 2

    parsed: list[tuple[Path, dict]] = []
    for f in files:
        try:
            parsed.append((f, load_excalidraw(f)))
        except Exception as e:
            print(f"✗ {f}: failed to read JSON: {e}", file=sys.stderr)

    if not parsed:
        return 1

    measurements_by_file = measure_batch(parsed, template.as_uri())

    overall_pass = True
    json_report = []

    for f, data in parsed:
        measurements = measurements_by_file.get(f)
        if measurements is None:
            overall_pass = False
            continue

        elements = data.get("elements", [])
        overflows = check_overflow(elements, measurements)
        bindings = check_bindings(elements)

        if args.fix and (overflows or bindings):
            fixed = apply_fixes(data, overflows + bindings)
            if fixed:
                save_excalidraw(f, data)
                # Re-validate after fix to get fresh report
                elements = data.get("elements", [])
                bindings = check_bindings(elements)
                # Don't re-run overflow (would need re-measurement)
                print(f"  → applied {fixed} fix(es) to {f}", file=sys.stderr)

        if args.json:
            json_report.append(
                {
                    "file": str(f),
                    "overflows": [x.as_dict() for x in overflows],
                    "bindings": [x.as_dict() for x in bindings],
                    "renderer_source": None,  # could surface rendererSource here
                }
            )
        else:
            print(format_text_report(f, overflows, bindings))

        if overflows:
            overall_pass = False
        if any(b.level == "error" for b in bindings):
            overall_pass = False
        if args.strict and any(b.level == "warning" for b in bindings):
            overall_pass = False

    if args.json:
        print(json.dumps(json_report, indent=2, ensure_ascii=False))

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
