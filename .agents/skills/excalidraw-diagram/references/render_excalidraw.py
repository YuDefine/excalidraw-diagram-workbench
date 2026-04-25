"""Render Excalidraw JSON to PNG using Playwright + headless Chromium.

Usage:
    cd .claude/skills/excalidraw-diagram/references

    # Single file
    uv run python render_excalidraw.py <path-to-file.excalidraw> [--output path.png] [--scale 2] [--width 1920] [--dark]

    # Directory (renders every *.excalidraw inside it, replacing existing PNGs)
    uv run python render_excalidraw.py <path-to-dir>

    # No input → batch-render every *.excalidraw under the repo's `output/` directory
    uv run python render_excalidraw.py

First-time setup:
    cd .claude/skills/excalidraw-diagram/references
    uv sync
    uv run playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DARK_BACKGROUNDS = {"#1e1e2e", "#181825", "#11111b", "#000000"}


def validate_excalidraw(data: dict) -> list[str]:
    """Validate Excalidraw JSON structure. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    if data.get("type") != "excalidraw":
        errors.append(f"Expected type 'excalidraw', got '{data.get('type')}'")

    if "elements" not in data:
        errors.append("Missing 'elements' array")
    elif not isinstance(data["elements"], list):
        errors.append("'elements' must be an array")
    elif len(data["elements"]) == 0:
        errors.append("'elements' array is empty — nothing to render")

    return errors


def detect_dark_mode(data: dict) -> bool:
    """Auto-detect dark mode from appState or theme field."""
    app_state = data.get("appState", {})
    if app_state.get("theme") == "dark":
        return True
    bg = app_state.get("viewBackgroundColor", "#ffffff").lower()
    return bg in DARK_BACKGROUNDS


def compute_bounding_box(elements: list[dict]) -> tuple[float, float, float, float]:
    """Compute bounding box (min_x, min_y, max_x, max_y) across all elements."""
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for el in elements:
        if el.get("isDeleted"):
            continue
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)

        # For arrows/lines, points array defines the shape relative to x,y
        if el.get("type") in ("arrow", "line") and "points" in el:
            for px, py in el["points"]:
                if px is None or py is None:
                    continue
                min_x = min(min_x, x + px)
                min_y = min(min_y, y + py)
                max_x = max(max_x, x + px)
                max_y = max(max_y, y + py)
        else:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + abs(w))
            max_y = max(max_y, y + abs(h))

    if min_x == float("inf"):
        return (0, 0, 800, 600)

    return (min_x, min_y, max_x, max_y)


def resolve_default_output_dir() -> Path:
    """Locate the repo's `output/` directory.

    Resolution order:
    1. ``$PWD/output`` if the user invoked the script from the repo root.
    2. ``<repo_root>/output`` where ``<repo_root>`` is computed from this file's
       location: ``.claude/skills/excalidraw-diagram/references/render_excalidraw.py``
       → 4 parents up.
    """
    cwd_candidate = Path.cwd() / "output"
    if cwd_candidate.is_dir():
        return cwd_candidate

    repo_root = Path(__file__).resolve().parents[4]
    return repo_root / "output"


def render(
    excalidraw_path: Path,
    output_path: Path | None = None,
    scale: int = 2,
    max_width: int = 1920,
    dark_mode: bool | None = None,
) -> Path:
    """Render an .excalidraw file to PNG. Returns the output PNG path."""
    # Import playwright here so validation errors show before import errors
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.", file=sys.stderr)
        print("Run: cd .claude/skills/excalidraw-diagram/references && uv sync && uv run playwright install chromium", file=sys.stderr)
        sys.exit(1)

    # Read and validate
    raw = excalidraw_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {excalidraw_path}: {e}", file=sys.stderr)
        sys.exit(1)

    errors = validate_excalidraw(data)
    if errors:
        print(f"ERROR: Invalid Excalidraw file:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Determine dark mode: explicit flag > auto-detect from file
    if dark_mode is None:
        dark_mode = detect_dark_mode(data)

    # Compute viewport size from element bounding box
    elements = [e for e in data["elements"] if not e.get("isDeleted")]
    min_x, min_y, max_x, max_y = compute_bounding_box(elements)
    padding = 80
    diagram_w = max_x - min_x + padding * 2
    diagram_h = max_y - min_y + padding * 2

    # Cap viewport width, let height be natural
    vp_width = min(int(diagram_w), max_width)
    vp_height = max(int(diagram_h), 600)

    # Output path
    if output_path is None:
        output_path = excalidraw_path.with_suffix(".png")

    # Template path (same directory as this script)
    template_path = Path(__file__).parent / "render_template.html"
    if not template_path.exists():
        print(f"ERROR: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    template_url = template_path.as_uri()

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            if "Executable doesn't exist" in str(e) or "browserType.launch" in str(e):
                print("ERROR: Chromium not installed for Playwright.", file=sys.stderr)
                print("Run: cd .claude/skills/excalidraw-diagram/references && uv run playwright install chromium", file=sys.stderr)
                sys.exit(1)
            raise

        page = browser.new_page(
            viewport={"width": vp_width, "height": vp_height},
            device_scale_factor=scale,
        )

        # Load the template
        page.goto(template_url)

        # Wait for the UMD bundles to expose window.ExcalidrawLib
        page.wait_for_function("window.__moduleReady === true", timeout=60000)

        # Inject the diagram data and render
        result = page.evaluate(
            "([d, o]) => window.renderDiagram(d, o)",
            [data, {"darkMode": dark_mode}],
        )

        if not result or not result.get("success"):
            error_msg = result.get("error", "Unknown render error") if result else "renderDiagram returned null"
            print(f"ERROR: Render failed: {error_msg}", file=sys.stderr)
            browser.close()
            sys.exit(1)

        # Wait for render completion signal
        page.wait_for_function("window.__renderComplete === true", timeout=15000)

        # Screenshot the SVG element
        svg_el = page.query_selector("#root svg")
        if svg_el is None:
            print("ERROR: No SVG element found after render.", file=sys.stderr)
            browser.close()
            sys.exit(1)

        svg_el.screenshot(path=str(output_path))
        browser.close()

    return output_path


def render_batch(
    files: list[Path],
    scale: int,
    max_width: int,
    dark_mode: bool | None,
    label: str,
) -> int:
    """Render every file in *files*, replacing existing PNGs. Returns process exit code."""
    if not files:
        print(f"No .excalidraw files found in {label}.", file=sys.stderr)
        return 0

    files = sorted(files)
    total = len(files)
    ok = 0
    fail = 0
    print(f"Batch rendering {total} file(s) from {label}")
    for idx, src in enumerate(files, start=1):
        png_path = src.with_suffix(".png")
        marker = "↻" if png_path.exists() else "+"
        print(f"  [{idx}/{total}] {marker} {src.name} → {png_path.name}")
        try:
            render(src, png_path, scale, max_width, dark_mode)
            ok += 1
        except SystemExit:
            # render() already printed the failure to stderr
            fail += 1
        except Exception as e:
            print(f"    ERROR: {e}", file=sys.stderr)
            fail += 1

    print(f"\nDone: {ok} ok, {fail} failed (of {total}).")
    return 0 if fail == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Excalidraw JSON to PNG")
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=None,
        help=(
            "Path to .excalidraw file or directory containing .excalidraw files. "
            "If omitted, batch-renders every *.excalidraw under the repo's `output/` directory, "
            "overwriting any existing PNG with the same name."
        ),
    )
    parser.add_argument("--output", "-o", type=Path, default=None, help="Output PNG path (single-file mode only; default: same name with .png)")
    parser.add_argument("--scale", "-s", type=int, default=2, help="Device scale factor (default: 2)")
    parser.add_argument("--width", "-w", type=int, default=1920, help="Max viewport width (default: 1920)")
    parser.add_argument("--dark", action="store_true", default=None, help="Force dark mode rendering (default: auto-detect from file)")
    parser.add_argument("--light", action="store_true", default=None, help="Force light mode rendering")
    args = parser.parse_args()

    dark_mode = None
    if args.dark:
        dark_mode = True
    elif args.light:
        dark_mode = False

    # No input → batch-render the default output/ directory
    if args.input is None:
        out_dir = resolve_default_output_dir()
        if not out_dir.is_dir():
            print(f"ERROR: Default output directory not found: {out_dir}", file=sys.stderr)
            sys.exit(1)
        files = list(out_dir.glob("*.excalidraw"))
        sys.exit(render_batch(files, args.scale, args.width, dark_mode, str(out_dir)))

    if not args.input.exists():
        print(f"ERROR: Path not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Directory → batch
    if args.input.is_dir():
        files = list(args.input.glob("*.excalidraw"))
        sys.exit(render_batch(files, args.scale, args.width, dark_mode, str(args.input)))

    # Single file
    if args.input.suffix != ".excalidraw":
        print(f"ERROR: Expected .excalidraw file, got: {args.input}", file=sys.stderr)
        sys.exit(1)

    png_path = render(args.input, args.output, args.scale, args.width, dark_mode)
    print(str(png_path))


if __name__ == "__main__":
    main()
