# Render & Validate 改善計畫

> 本文件分析 render-validate loop 在實際使用時為何無法捕捉明顯視覺問題，並提出具體可執行的改善方案。
> 不修改 SKILL.md 本身——此處紀錄的是後續可推動的工程改善。

---

## 根本原因分析

問題不是「agent 沒認真看」，而是流程設計存在幾個結構性缺陷，讓 agent 在主觀上覺得已完成審查，卻遺漏了客觀可量化的問題。

### 原因 1：視覺審查完全依賴 agent 的主觀判斷

目前的流程是：render → Read PNG → agent 自己描述問題 → 修正。

這個鏈路的斷點在於：

- Agent 生成 JSON 後，對這張圖有「設計者偏見」（designer's bias）——它知道自己想要畫什麼，傾向於「看到」預期的樣子，而不是實際渲染的樣子。
- SKILL.md 的 "Self-Honesty Rule" 是一條 prompt-level 的規範，但 prompt 規範在 agent 已進入高信心狀態時效果很弱。
- 「逐條檢查 checklist」在實際執行時很容易變成形式審查：agent 在內部 reasoning 中快速過一遍，並未真正逐一驗證每條。

**後果**：即使箭頭實際上大量重疊，agent 可能在自我審查時說「箭頭路徑看起來合理」然後繼續。

### 原因 2：render_excalidraw.py 只做結構驗證，不做視覺幾何分析

目前 `render_excalidraw.py` 的 `validate_excalidraw()` 函數只檢查：

1. `type` 是否為 `"excalidraw"`
2. `elements` 是否存在且非空

它完全不分析：

- 元素的 bounding box 是否互相交疊
- 箭頭路徑是否穿過不相關的元素
- 多條箭頭是否在空間上幾乎重合
- 文字是否超出其 container 邊界

**後果**：agent 從 render script 拿到的唯一反饋是「渲染成功，PNG 產出」，沒有任何量化的異常訊號。

### 原因 3：生成者與審查者是同一個 agent

SKILL.md 要求「spawn a Sonnet agent」來執行整個任務，但生成 JSON 和視覺審查都由同一個 agent 的同一個對話上下文完成。這意味著：

- 設計決策、JSON 生成、視覺審查都在同一個思維鏈中發生
- Agent 在審查時仍然「記得」自己設計了什麼，認知偏差最大
- 沒有任何機制迫使 agent 用全新視角看待結果

### 原因 4：反饋信號粒度太粗

目前 agent 看到的是完整的 PNG 圖片，但：

- 複雜圖表的 PNG 在 LLM 視野中等比縮小後，細節問題（如兩條幾乎重合的箭頭）難以分辨
- 沒有數字指標：「這張圖有 7 對 bounding box 重疊、3 條箭頭路徑重合度超過 80%」這樣的客觀數據
- Agent 無法將視覺觀察轉化為可操作的 JSON 修正建議（要知道「是哪兩個元素重疊」才能修）

---

## 改善方案

### 方案 A：在 render_excalidraw.py 加入幾何分析報告（優先度：高）

在渲染完成後，輸出一份文字報告，讓 agent 有客觀數據輔助審查。

#### A1：Bounding Box 重疊偵測

偵測所有非箭頭元素之間的 bounding box 交疊，輸出重疊對清單。

```python
def detect_bbox_overlaps(elements: list[dict]) -> list[dict]:
    """
    回傳所有 bounding box 互相交疊的元素對。
    每個結果包含：id_a, id_b, type_a, type_b, overlap_area。
    箭頭類型 (arrow/line) 跳過，只檢查 rect/ellipse/diamond/text。
    """
    NON_ARROW_TYPES = {"rectangle", "ellipse", "diamond", "text", "image"}
    boxes = []
    for el in elements:
        if el.get("isDeleted") or el.get("type") not in NON_ARROW_TYPES:
            continue
        x, y = el.get("x", 0), el.get("y", 0)
        w, h = abs(el.get("width", 0)), abs(el.get("height", 0))
        boxes.append({"id": el["id"], "type": el["type"], "x": x, "y": y, "w": w, "h": h})

    overlaps = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ox = max(0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
            oy = max(0, min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))
            if ox > 0 and oy > 0:
                overlaps.append({
                    "id_a": a["id"], "type_a": a["type"],
                    "id_b": b["id"], "type_b": b["type"],
                    "overlap_area": round(ox * oy),
                    "overlap_px": f"{round(ox)}×{round(oy)}"
                })
    return overlaps
```

#### A2：箭頭路徑重合偵測

採樣每條箭頭的折線路徑，比較兩兩路徑間的最近距離，標記路徑重合度高的箭頭對。

```python
def detect_arrow_path_overlaps(elements: list[dict], threshold_px: float = 15.0) -> list[dict]:
    """
    偵測兩條箭頭路徑上是否存在過近的線段（距離 < threshold_px），
    回傳可能視覺重疊的箭頭對清單。
    """
    import math

    def sample_path(el: dict, samples: int = 20) -> list[tuple]:
        """從 arrow/line 的 points 採樣均勻分佈的點。"""
        ox, oy = el.get("x", 0), el.get("y", 0)
        pts = [(ox + p[0], oy + p[1]) for p in el.get("points", [[0,0],[0,0]])]
        if len(pts) < 2:
            return pts
        # 計算總長
        total = sum(
            math.hypot(pts[k+1][0]-pts[k][0], pts[k+1][1]-pts[k][1])
            for k in range(len(pts)-1)
        )
        if total == 0:
            return [pts[0]]
        result = []
        step = total / samples
        walked = 0.0
        seg = 0
        for s in range(samples + 1):
            target = s * step
            while seg < len(pts) - 2:
                seg_len = math.hypot(pts[seg+1][0]-pts[seg][0], pts[seg+1][1]-pts[seg][1])
                if walked + seg_len >= target:
                    break
                walked += seg_len
                seg += 1
            seg_len = math.hypot(pts[seg+1][0]-pts[seg][0], pts[seg+1][1]-pts[seg][1])
            t = (target - walked) / seg_len if seg_len > 0 else 0
            result.append((
                pts[seg][0] + t * (pts[seg+1][0] - pts[seg][0]),
                pts[seg][1] + t * (pts[seg+1][1] - pts[seg][1]),
            ))
        return result

    arrows = [e for e in elements if not e.get("isDeleted") and e.get("type") in ("arrow", "line")]
    sampled = [(a, sample_path(a)) for a in arrows]

    close_pairs = []
    for i in range(len(sampled)):
        for j in range(i + 1, len(sampled)):
            a_el, a_pts = sampled[i]
            b_el, b_pts = sampled[j]
            min_dist = min(
                math.hypot(p[0]-q[0], p[1]-q[1])
                for p in a_pts for q in b_pts
            )
            if min_dist < threshold_px:
                close_pairs.append({
                    "id_a": a_el["id"],
                    "id_b": b_el["id"],
                    "min_distance_px": round(min_dist, 1),
                    "warning": "路徑重合（可能視覺上無法區分）" if min_dist < 5 else "路徑過近"
                })
    return close_pairs
```

#### A3：文字溢出偵測

比對 text 元素的計算尺寸與其 container 的邊界。

```python
def detect_text_overflow(elements: list[dict]) -> list[dict]:
    """
    偵測 text 元素是否超出其 container 的 bounding box。
    僅檢查有 containerId 的 text（bound text）。
    """
    id_map = {e["id"]: e for e in elements if not e.get("isDeleted")}
    issues = []
    for el in elements:
        if el.get("isDeleted") or el.get("type") != "text":
            continue
        cid = el.get("containerId")
        if not cid or cid not in id_map:
            continue
        container = id_map[cid]
        # text 邊界
        tx, ty = el.get("x", 0), el.get("y", 0)
        tw, th = abs(el.get("width", 0)), abs(el.get("height", 0))
        # container 邊界
        cx, cy = container.get("x", 0), container.get("y", 0)
        cw, ch = abs(container.get("width", 0)), abs(container.get("height", 0))
        # 加 4px 容差
        tol = 4
        if (tx < cx - tol or tx + tw > cx + cw + tol or
                ty < cy - tol or ty + th > cy + ch + tol):
            issues.append({
                "text_id": el["id"],
                "container_id": cid,
                "text_preview": el.get("text", "")[:30],
                "overflow_detail": {
                    "left": round(cx - tx, 1) if tx < cx else 0,
                    "right": round((tx + tw) - (cx + cw), 1) if tx + tw > cx + cw else 0,
                    "top": round(cy - ty, 1) if ty < cy else 0,
                    "bottom": round((ty + th) - (cy + ch), 1) if ty + th > cy + ch else 0,
                }
            })
    return issues
```

#### A4：輸出整合報告

在 render 後自動輸出（不論是否有問題），讓 agent 在閱讀 PNG 前先有量化數據：

```python
def print_geometry_report(elements: list[dict]) -> None:
    """渲染後輸出幾何分析報告到 stdout。"""
    active = [e for e in elements if not e.get("isDeleted")]

    overlaps = detect_bbox_overlaps(active)
    arrow_overlaps = detect_arrow_path_overlaps(active)
    text_overflows = detect_text_overflow(active)

    print("\n── Geometry Report ──────────────────────────────")
    print(f"Elements: {len(active)} active")

    if overlaps:
        print(f"\n[WARN] Bounding box overlaps: {len(overlaps)}")
        for o in overlaps[:10]:  # 最多顯示 10 筆
            print(f"  {o['type_a']}({o['id_a'][:12]}) ∩ {o['type_b']}({o['id_b'][:12]})  area={o['overlap_px']}px")
    else:
        print("\n[OK] No bounding box overlaps")

    if arrow_overlaps:
        critical = [x for x in arrow_overlaps if x["min_distance_px"] < 5]
        print(f"\n[WARN] Arrow path overlaps: {len(arrow_overlaps)} pairs  ({len(critical)} critical <5px)")
        for o in arrow_overlaps[:10]:
            print(f"  {o['id_a'][:12]} ↔ {o['id_b'][:12]}  dist={o['min_distance_px']}px  {o['warning']}")
    else:
        print("\n[OK] No arrow path overlaps")

    if text_overflows:
        print(f"\n[WARN] Text overflow: {len(text_overflows)} elements")
        for o in text_overflows[:10]:
            print(f"  text({o['text_id'][:12]}) overflows container({o['container_id'][:12]})  \"{o['text_preview']}\"")
    else:
        print("\n[OK] No text overflow")

    total_warnings = len(overlaps) + len(arrow_overlaps) + len(text_overflows)
    print(f"\n── Total warnings: {total_warnings} ──────────────────────────")
```

在 `render()` 函數結束前呼叫 `print_geometry_report(elements)`。

---

### 方案 B：結構檢查與視覺檢查分成兩個獨立步驟（優先度：中）

目前 SKILL.md 的流程將「JSON 結構審查」和「視覺渲染審查」混在同一個循環裡，agent 通常在生成 JSON 後立刻 render，來不及在純 JSON 層做充分的靜態分析。

建議明確分成兩個階段，並在 SKILL.md 的 Step 6 之前插入 Step 5.5：

**Step 5.5：JSON 靜態審查（在渲染前）**

Agent 在執行 render script 之前，應先對 JSON 自行回答以下問題（逐一作答，不能跳過）：

```
靜態審查問卷（每條必須明確回答 Pass / Fix）：

1. Arrow congestion：有哪些 entity 的同一邊有 3 條以上箭頭抵達？  → Pass / Fix
2. Focus 分佈：fan-out 箭頭的 focus 值差距是否 ≥ 0.3？             → Pass / Fix
3. 對角線箭頭：是否有箭頭在斜線路徑上可能穿越中間的 entity？        → Pass / Fix
4. Text 尺寸估算：每個 bound text 的 width 是否按公式計算（非估值）？ → Pass / Fix
5. Binding 雙向一致：每條 arrow 的兩端 elementId 是否都存在？        → Pass / Fix
```

這 5 個問題在 JSON 層就能機械性回答，不依賴視覺判斷，可以在 render 之前消除一大類問題。

**Step 6：視覺渲染審查（在渲染後）**

視覺審查的重點縮小為「JSON 層看不到的問題」：
- 曲線實際路徑（focus 值計算出的曲率）
- 文字 autoResize 後的實際尺寸
- 顏色對比（背景色與文字色的實際差距）
- 整體構圖平衡

這樣的分工使每個步驟的目標更明確，也更容易發現問題屬於哪一層。

---

### 方案 C：生成與審查分由不同 agent 執行（優先度：中）

目前 SKILL.md 要求 spawn 一個 Sonnet agent 執行全部工作。建議改為：

**第一個 agent（Generator）**：執行 Step 0-5，產出 JSON 和 PNG。
**第二個 agent（Reviewer）**：接收 PNG + JSON + Geometry Report，執行獨立視覺審查。

Reviewer agent 的 prompt 應包含：
- 「你沒有參與這張圖的設計，你只負責找問題」
- Geometry Report 中的所有 warning（如果 Generator 已執行 A4）
- 明確要求：「列出你看到的所有問題，不要說『看起來可以』，說具體的問題在哪裡」

這個架構的核心價值：Reviewer 沒有設計者偏見，看到的是純粹的視覺輸出。

**實作方式**：在 Generator agent 完成 PNG 後，main agent 再 spawn 一個 Reviewer agent，傳入 PNG 路徑和 Geometry Report，要求輸出一份問題清單，再由 Generator 根據清單修正。

---

### 方案 D：增加 Arrow Endpoint Congestion 密度計算（優先度：低）

這是 A4 Geometry Report 的延伸：計算每個 entity 的各邊有多少箭頭端點落在其上。

```python
def detect_endpoint_congestion(elements: list[dict], congestion_threshold: int = 3) -> list[dict]:
    """
    計算每個元素的各邊上有多少箭頭端點。
    超過 congestion_threshold 的邊標記為 congested。
    """
    from collections import defaultdict

    id_map = {e["id"]: e for e in elements if not e.get("isDeleted")}
    edge_count: dict[tuple, int] = defaultdict(int)

    for el in elements:
        if el.get("isDeleted") or el.get("type") not in ("arrow", "line"):
            continue
        for binding_key in ("startBinding", "endBinding"):
            b = el.get(binding_key)
            if not b or "elementId" not in b:
                continue
            target_id = b["elementId"]
            if target_id not in id_map:
                continue
            fp = b.get("fixedPoint")
            if fp:
                # 判斷是哪條邊（left/right/top/bottom）
                fx, fy = fp[0], fp[1]
                if fx == 0:
                    edge = (target_id, "left")
                elif fx == 1:
                    edge = (target_id, "right")
                elif fy == 0:
                    edge = (target_id, "top")
                else:
                    edge = (target_id, "bottom")
            else:
                edge = (target_id, "unknown")
            edge_count[edge] += 1

    congested = []
    for (eid, edge_side), count in edge_count.items():
        if count >= congestion_threshold:
            el = id_map.get(eid, {})
            congested.append({
                "element_id": eid,
                "element_type": el.get("type", "?"),
                "edge": edge_side,
                "arrow_count": count,
            })
    return congested
```

---

## 實作優先序

| 方案 | 優先度 | 工作量 | 影響 |
|------|--------|--------|------|
| A（Geometry Report）| **高** | 中（在 render_excalidraw.py 加函數） | 給 agent 客觀數據，破除主觀合理化 |
| B（兩階段審查流程） | **中** | 低（只需更新 workflow 文件或在 agent prompt 中強制） | 讓每個步驟目標更清晰 |
| C（獨立 Reviewer agent）| **中** | 中（需調整 main skill 的 agent 派發邏輯） | 消除設計者偏見，最根本的結構修正 |
| D（Endpoint Congestion）| 低 | 低（是 A 的延伸） | 補充 A4 的盲點 |

建議先實作方案 A，讓 Geometry Report 在每次 render 後自動輸出。這是最低成本、最高即時反饋的改善，可以在一次修改 `render_excalidraw.py` 後立即生效，無需調整 agent 的 prompt 結構。

---

## 結語：最根本的問題

所有方案的底層目標一致：**把依賴 agent 主觀判斷的部分，盡量替換成客觀可量化的機器檢查**。

SKILL.md 的 Self-Honesty Rule 說的是對的，但它是一條靠意志力維持的規範。工程上更可靠的做法是：讓 agent 在看 PNG 之前先看到一份清單「有 12 對 bounding box 重疊、5 對箭頭路徑距離 < 5px」，這樣 agent 就算有偏見也有明確的起點去驗證。

主觀視覺判斷作為最後一道關卡是對的；但它不應該是唯一的關卡。
