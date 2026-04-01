#!/usr/bin/env python3
"""Generate TRAC permission matrix Excalidraw diagram (dark theme)."""

import json
import random

random.seed(42)

def seed():
    return random.randint(10000, 99999)

# Permission data: [Accountant, Admin, Payroll, Manager, Employee]
# 'g'=完整存取(green), 'y'=過濾後(yellow), 'b'=所轄(light blue), 'x'=禁止(gray)
PERMS = {
    'R1': ['g', 'g', 'x', 'x', 'x'],
    'R2': ['g', 'g', 'x', 'x', 'x'],
    'R3': ['x', 'g', 'x', 'b', 'x'],
    'R4': ['x', 'g', 'x', 'b', 'x'],
    'R5': ['g', 'g', 'x', 'x', 'x'],
    'R6': ['g', 'g', 'x', 'x', 'x'],
    'R7': ['y', 'y', 'y', 'y', 'y'],
    'R8': ['y', 'y', 'y', 'y', 'y'],
}

REPORT_NAMES = {
    'R1': 'R1\n各客戶投入\n成本分析',
    'R2': 'R2\n時薪分析',
    'R3': 'R3\n請休假\n時數統計',
    'R4': 'R4\n加班時數統計',
    'R5': 'R5\n9999時數\n佔比',
    'R6': 'R6\n同仁薪資統計',
    'R7': 'R7\n工時明細報表',
    'R8': 'R8\n彙總報表',
}

ROLES = ['Accountant', 'Admin', 'Payroll', 'Manager', 'Employee']

# Color definitions (dark theme - tinted fills for better scannability)
COLORS = {
    'g': {'fill': '#1a3a2a', 'stroke': '#a6e3a1', 'label': '✅'},   # green
    'y': {'fill': '#3a3010', 'stroke': '#fab387', 'label': '✅\n過濾'},  # yellow/orange
    'b': {'fill': '#1a2a3a', 'stroke': '#89b4fa', 'label': '✅\n所轄'},   # blue
    'x': {'fill': '#1e1e2e', 'stroke': '#585b70', 'label': '🚫'},   # gray/disabled
}

# Layout constants
ROLE_COL_X = 80
ROLE_COL_W = 160
COL_W = 130
COL_STRIDE = 132
HEADER_ROW_Y = 110
HEADER_ROW_H = 90
DATA_ROW_H = 52
DATA_ROW_STRIDE = 54
GRID_START_X = ROLE_COL_X + ROLE_COL_W + 2  # start of report columns

REPORTS = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8']

elements = []
element_id = [0]

def next_id(prefix='elem'):
    element_id[0] += 1
    return f"{prefix}_{element_id[0]}"

def make_rect(x, y, w, h, fill, stroke, stroke_width=2, rounded=False, eid=None):
    if eid is None:
        eid = next_id('rect')
    elem = {
        "type": "rectangle",
        "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": [],
        "link": None,
        "locked": False,
        "roundness": {"type": 3} if rounded else None
    }
    return elem

def make_text(x, y, w, h, text, font_size, color, container_id=None, align='center', valign='middle'):
    eid = next_id('text')
    elem = {
        "type": "text",
        "id": eid,
        "x": x, "y": y, "width": w, "height": h,
        "text": text,
        "originalText": text,
        "fontSize": font_size,
        "fontFamily": 3,
        "textAlign": align,
        "verticalAlign": valign,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": [],
        "link": None,
        "locked": False,
        "containerId": container_id,
        "lineHeight": 1.25,
        "autoResize": True
    }
    return elem

def make_cell(x, y, w, h, fill, stroke, label, font_size=16):
    """Create a colored rectangle cell with bound text label."""
    rect_id = next_id('cell')
    text_id = next_id('cell_txt')

    rect = {
        "type": "rectangle",
        "id": rect_id,
        "x": x, "y": y, "width": w, "height": h,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": [{"id": text_id, "type": "text"}],
        "link": None,
        "locked": False,
        "roundness": None
    }

    text = {
        "type": "text",
        "id": text_id,
        "x": x + w/2 - 30,
        "y": y + h/2 - 12,
        "width": 60, "height": 25,
        "text": label,
        "originalText": label,
        "fontSize": font_size,
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
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": [],
        "link": None,
        "locked": False,
        "containerId": rect_id,
        "lineHeight": 1.25,
        "autoResize": True
    }

    return rect, text

# ------- Title -------
title_text = make_text(
    x=ROLE_COL_X, y=30,
    w=ROLE_COL_W + COL_STRIDE * 8 + 20, h=40,
    text="TRAC 報表權限矩陣",
    font_size=36,
    color="#89b4fa",
    align="center"
)
elements.append(title_text)

# ------- Role column header (top-left corner cell) -------
corner_rect = make_rect(
    x=ROLE_COL_X, y=HEADER_ROW_Y,
    w=ROLE_COL_W, h=HEADER_ROW_H,
    fill='#313244', stroke='#585b70', stroke_width=2
)
corner_text_id = next_id('corner_text')
corner_text = {
    "type": "text",
    "id": corner_text_id,
    "x": ROLE_COL_X + ROLE_COL_W/2 - 25,
    "y": HEADER_ROW_Y + HEADER_ROW_H/2 - 12,
    "width": 50, "height": 25,
    "text": "角色",
    "originalText": "角色",
    "fontSize": 20,
    "fontFamily": 3,
    "textAlign": "center",
    "verticalAlign": "middle",
    "strokeColor": "#89b4fa",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "strokeWidth": 1,
    "strokeStyle": "solid",
    "roughness": 0,
    "opacity": 100,
    "angle": 0,
    "seed": seed(),
    "version": 1,
    "versionNonce": seed(),
    "isDeleted": False,
    "groupIds": [],
    "boundElements": [],
    "link": None,
    "locked": False,
    "containerId": corner_rect["id"],
    "lineHeight": 1.25,
    "autoResize": True
}
corner_rect["boundElements"].append({"id": corner_text_id, "type": "text"})
elements.append(corner_rect)
elements.append(corner_text)

# ------- Report column headers -------
for i, report_key in enumerate(REPORTS):
    col_x = GRID_START_X + i * COL_STRIDE
    header_rect = make_rect(
        x=col_x, y=HEADER_ROW_Y,
        w=COL_W, h=HEADER_ROW_H,
        fill='#313244', stroke='#89b4fa', stroke_width=2
    )
    header_text_id = next_id('hdr_text')
    header_text = {
        "type": "text",
        "id": header_text_id,
        "x": col_x + 2,
        "y": HEADER_ROW_Y + 5,
        "width": COL_W - 4, "height": HEADER_ROW_H - 10,
        "text": REPORT_NAMES[report_key],
        "originalText": REPORT_NAMES[report_key],
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
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": [],
        "link": None,
        "locked": False,
        "containerId": header_rect["id"],
        "lineHeight": 1.25,
        "autoResize": True
    }
    header_rect["boundElements"].append({"id": header_text_id, "type": "text"})
    elements.append(header_rect)
    elements.append(header_text)

# ------- Role rows -------
for row_idx, role in enumerate(ROLES):
    row_y = HEADER_ROW_Y + HEADER_ROW_H + 2 + row_idx * DATA_ROW_STRIDE

    # Role label cell (left column)
    role_rect = make_rect(
        x=ROLE_COL_X, y=row_y,
        w=ROLE_COL_W, h=DATA_ROW_H,
        fill='#313244', stroke='#585b70', stroke_width=2
    )
    role_text_id = next_id('role_text')
    role_text = {
        "type": "text",
        "id": role_text_id,
        "x": ROLE_COL_X + 5,
        "y": row_y + DATA_ROW_H/2 - 12,
        "width": ROLE_COL_W - 10, "height": 25,
        "text": role,
        "originalText": role,
        "fontSize": 16,
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
        "seed": seed(),
        "version": 1,
        "versionNonce": seed(),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": [],
        "link": None,
        "locked": False,
        "containerId": role_rect["id"],
        "lineHeight": 1.25,
        "autoResize": True
    }
    role_rect["boundElements"].append({"id": role_text_id, "type": "text"})
    elements.append(role_rect)
    elements.append(role_text)

    # Data cells for each report
    for col_idx, report_key in enumerate(REPORTS):
        perm = PERMS[report_key][row_idx]
        color_info = COLORS[perm]
        col_x = GRID_START_X + col_idx * COL_STRIDE

        rect, text = make_cell(
            x=col_x, y=row_y,
            w=COL_W, h=DATA_ROW_H,
            fill=color_info['fill'],
            stroke=color_info['stroke'],
            label=color_info['label'],
            font_size=16
        )
        elements.append(rect)
        elements.append(text)

# ------- Legend -------
legend_y = HEADER_ROW_Y + HEADER_ROW_H + 2 + len(ROLES) * DATA_ROW_STRIDE + 30
legend_title = make_text(
    x=ROLE_COL_X, y=legend_y,
    w=200, h=25,
    text="圖例說明",
    font_size=20,
    color="#89b4fa",
    align="left"
)
elements.append(legend_title)

legend_items = [
    ('g', '完整存取'),
    ('y', '過濾後存取（依角色過濾敏感欄位）'),
    ('b', '所轄存取（僅限所轄員工）'),
    ('x', '無存取權限'),
]

legend_box_w = 36
legend_box_h = 28
legend_item_x = ROLE_COL_X
legend_item_y = legend_y + 35

for i, (perm_key, label) in enumerate(legend_items):
    color_info = COLORS[perm_key]
    ix = legend_item_x + i * 340

    # Colored box
    box_rect = make_rect(
        x=ix, y=legend_item_y,
        w=legend_box_w, h=legend_box_h,
        fill=color_info['fill'],
        stroke=color_info['stroke'],
        stroke_width=2
    )
    elements.append(box_rect)

    # Label text next to box
    lbl_text = make_text(
        x=ix + legend_box_w + 8, y=legend_item_y + 2,
        w=290, h=25,
        text=label,
        font_size=16,
        color="#a6adc8",
        align="left"
    )
    elements.append(lbl_text)

# ------- Assemble document -------
doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "generated",
    "elements": elements,
    "appState": {
        "theme": "dark",
        "viewBackgroundColor": "#1e1e2e",
        "currentItemFontFamily": 3,
        "zoom": {"value": 1},
        "scrollX": 0,
        "scrollY": 0
    },
    "files": {}
}

output_path = "/Users/charles/offline/excalidraw-diagram-workbench/trac-permission-matrix-dark.excalidraw"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

print(f"Written: {output_path}")
print(f"Total elements: {len(elements)}")
