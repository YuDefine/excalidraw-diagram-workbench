/**
 * Excalidraw Core — reusable primitives for building .excalidraw diagrams.
 *
 * Usage:
 *   const { createDiagram, measureTextLine, centeredTextBounds, pathMidpoint } = require('./lib/excalidraw')
 *   const d = createDiagram({ startSeed: 100000 })
 *   d.text('title', 60, 22, 760, 36, 'Hello', '#1e40af', 36, 'left')
 *   d.writeTo('output.excalidraw', { viewBackgroundColor: '#ffffff', theme: 'light' })
 */
const fs = require('node:fs')
const path = require('node:path')

// ── Font sizes (mandatory scale — no other values allowed) ────────

const fontSizes = { sm: 16, md: 20, lg: 28, xl: 36 }

// ── Static text utilities (no diagram state) ─────────────────────

function measureTextLine(line, fontSize) {
  let width = 0
  for (const char of line) {
    if (/\p{Script=Han}/u.test(char)) { width += fontSize; continue }
    if (/\s/.test(char)) { width += fontSize * 0.35; continue }
    if (/[A-Z0-9]/.test(char)) { width += fontSize * 0.7; continue }
    if (/[a-z]/.test(char)) { width += fontSize * 0.6; continue }
    width += fontSize * 0.55
  }
  return Math.max(width, fontSize)
}

function centeredTextBounds(containerWidth, containerHeight, value, fontSize) {
  const lines = value.split('\n')
  const contentWidth = Math.max(...lines.map((line) => measureTextLine(line, fontSize)))
  const width = Math.min(containerWidth - 16, Math.ceil(contentWidth))
  const height = Math.ceil(lines.length * fontSize * 1.25)
  return {
    width,
    height,
    offsetX: Math.round((containerWidth - width) / 2),
    offsetY: Math.round((containerHeight - height) / 2),
  }
}

function pathMidpoint(startX, startY, points) {
  const absPoints = points.map((p) => [startX + p[0], startY + p[1]])
  let totalLength = 0
  const segments = []

  for (let i = 1; i < absPoints.length; i++) {
    const dx = absPoints[i][0] - absPoints[i - 1][0]
    const dy = absPoints[i][1] - absPoints[i - 1][1]
    const len = Math.sqrt(dx * dx + dy * dy)
    if (len > 0) {
      segments.push({ from: absPoints[i - 1], to: absPoints[i], len })
      totalLength += len
    }
  }

  if (totalLength === 0) return [startX, startY]

  const halfLength = totalLength / 2
  let cumLength = 0

  for (const seg of segments) {
    if (cumLength + seg.len >= halfLength) {
      const t = (halfLength - cumLength) / seg.len
      return [
        seg.from[0] + t * (seg.to[0] - seg.from[0]),
        seg.from[1] + t * (seg.to[1] - seg.from[1]),
      ]
    }
    cumLength += seg.len
  }

  return absPoints[absPoints.length - 1]
}

// ── Diagram builder (stateful) ───────────────────────────────────

function createDiagram({ startSeed = 100000 } = {}) {
  let seed = startSeed
  const elements = []
  const elementsById = new Map()

  function nextSeed() { return seed++ }

  function base(type, extra = {}) {
    return {
      type,
      angle: 0,
      strokeWidth: type === 'text' ? 1 : 2,
      strokeStyle: 'solid',
      roughness: 0,
      opacity: 100,
      fillStyle: 'solid',
      isDeleted: false,
      groupIds: [],
      boundElements: [],
      link: null,
      locked: false,
      seed: nextSeed(),
      version: 1,
      versionNonce: nextSeed(),
      ...extra,
    }
  }

  function addElement(type, extra = {}) {
    const element = base(type, extra)
    elements.push(element)
    if (element.id) elementsById.set(element.id, element)
    return element
  }

  function getElement(id) {
    const element = elementsById.get(id)
    if (!element) throw new Error(`Unknown element: ${id}`)
    return element
  }

  function attachBoundElement(hostId, type, id) {
    const host = getElement(hostId)
    if (!host.boundElements) host.boundElements = []
    if (!host.boundElements.some((b) => b.type === type && b.id === id)) {
      host.boundElements.push({ type, id })
    }
  }

  function elementBinding(elementId, fixedPoint = [0.5, 0.5]) {
    return {
      elementId,
      fixedPoint: fixedPoint.map((v) => (v === 0.5 ? 0.5001 : v)),
      focus: 0,
    }
  }

  function focusBinding(elementId, focus = 0.0, gap = 1) {
    return { elementId, focus, gap }
  }

  // ── Primitives ────────────────────────────────────────────────

  function rect(id, x, y, width, height, strokeColor, backgroundColor, strokeStyle = 'solid') {
    return addElement('rectangle', {
      id, x, y, width, height,
      strokeColor, backgroundColor, strokeStyle,
      roundness: { type: 3 },
    })
  }

  function text(id, x, y, width, height, value, strokeColor, fontSize = 16, textAlign = 'center') {
    return addElement('text', {
      id, x, y, width, height,
      text: value,
      originalText: value,
      fontSize,
      fontFamily: 3,
      textAlign,
      verticalAlign: 'middle',
      strokeColor,
      backgroundColor: 'transparent',
      lineHeight: 1.25,
      containerId: null,
      autoResize: true,
    })
  }

  function labeledRect(id, x, y, width, height, label, strokeColor, backgroundColor, opts = {}) {
    const {
      textId = `${id}_text`,
      textStrokeColor,
      fontSize = fontSizes.md,
      textAlign = 'center',
      strokeStyle = 'solid',
    } = opts

    const textBounds = centeredTextBounds(width, height, label, fontSize)

    addElement('rectangle', {
      id, x, y, width, height,
      strokeColor, backgroundColor, strokeStyle,
      roundness: { type: 3 },
    })
    attachBoundElement(id, 'text', textId)

    addElement('text', {
      id: textId,
      x: x + textBounds.offsetX,
      y: y + textBounds.offsetY,
      width: textBounds.width,
      height: textBounds.height,
      text: label,
      originalText: label,
      fontSize,
      fontFamily: 3,
      textAlign,
      verticalAlign: 'middle',
      strokeColor: textStrokeColor ?? strokeColor,
      backgroundColor: 'transparent',
      lineHeight: 1.25,
      containerId: id,
      autoResize: true,
    })
  }

  function line(id, x, y, points, strokeColor, strokeStyle = 'solid', strokeWidth = 2) {
    const [endX, endY] = points[points.length - 1]
    addElement('line', {
      id, x, y,
      width: endX,
      height: endY,
      strokeColor,
      backgroundColor: 'transparent',
      strokeStyle,
      strokeWidth,
      points,
    })
  }

  function dot(id, x, y, color) {
    addElement('ellipse', {
      id, x, y,
      width: 12, height: 12,
      strokeColor: color,
      backgroundColor: color,
    })
  }

  function arrow(id, x, y, points, strokeColor, endArrowhead = 'arrow', opts = {}) {
    const {
      startBinding = null,
      endBinding = null,
      label: labelText = null,
      startArrowhead = null,
      elbowed = true,
      roundness = null,
      strokeWidth = 2,
      strokeStyle = 'solid',
      labelColor,
    } = opts

    const allX = points.map((p) => p[0])
    const allY = points.map((p) => p[1])
    const width = Math.max(...allX) - Math.min(...allX)
    const height = Math.max(...allY) - Math.min(...allY)

    addElement('arrow', {
      id, x, y, width, height,
      strokeColor,
      backgroundColor: 'transparent',
      strokeWidth,
      strokeStyle,
      points,
      elbowed,
      ...(roundness ? { roundness } : {}),
      fixedSegments: elbowed ? null : undefined,
      startBinding,
      endBinding,
      startIsSpecial: null,
      endIsSpecial: null,
      startArrowhead,
      endArrowhead,
    })

    if (startBinding?.elementId) attachBoundElement(startBinding.elementId, 'arrow', id)
    if (endBinding?.elementId) attachBoundElement(endBinding.elementId, 'arrow', id)

    if (labelText) {
      const textId = `${id}_label`
      const [midX, midY] = pathMidpoint(x, y, points)
      const fontSize = fontSizes.sm
      const lines = labelText.split('\n')
      const textWidth = Math.max(...lines.map((l) => measureTextLine(l, fontSize)))
      const textHeight = Math.ceil(lines.length * fontSize * 1.35)

      addElement('text', {
        id: textId,
        x: Math.round(midX - textWidth / 2),
        y: Math.round(midY - textHeight / 2),
        width: Math.ceil(textWidth),
        height: textHeight,
        text: labelText,
        originalText: labelText,
        fontSize,
        fontFamily: 3,
        textAlign: 'center',
        verticalAlign: 'middle',
        strokeColor: labelColor ?? strokeColor,
        backgroundColor: 'transparent',
        lineHeight: 1.35,
        containerId: id,
        autoResize: true,
      })
      attachBoundElement(id, 'text', textId)
    }
  }

  // ── Overlap detection ─────────────────────────────────────────

  function renderedTextWidth(el) {
    if (el.type !== 'text') return el.width || 0
    const lines = (el.text || '').split('\n')
    return Math.max(...lines.map((line) => measureTextLine(line, el.fontSize || 16)))
  }

  function effectiveBounds(el) {
    const w = el.type === 'text' ? Math.max(el.width || 0, renderedTextWidth(el)) : (el.width || 0)
    return { x1: el.x, y1: el.y, x2: el.x + w, y2: el.y + (el.height || 0) }
  }

  function detectOverlaps({ ignoreIds = new Set(), threshold = 50 } = {}) {
    const checkable = elements.filter(
      (e) => ['rectangle', 'ellipse', 'text'].includes(e.type) && !e.isDeleted && !ignoreIds.has(e.id),
    )
    const warnings = []

    // Text overflow detection
    for (const el of checkable) {
      if (el.type !== 'text' || el.containerId) continue
      const rendered = renderedTextWidth(el)
      const declared = el.width || 0
      if (rendered > declared + 4) {
        warnings.push(`TEXT_OVERFLOW (+${Math.round(rendered - declared)}px): ${el.id} rendered=${Math.round(rendered)}px, declared=${Math.round(declared)}px`)
      }
    }

    // Bounding-box overlap detection (using rendered text width)
    for (let i = 0; i < checkable.length; i++) {
      const a = checkable[i]
      for (let j = i + 1; j < checkable.length; j++) {
        const b = checkable[j]
        if (a.containerId === b.id || b.containerId === a.id) continue

        const ab = effectiveBounds(a)
        const bb = effectiveBounds(b)

        if (ab.x1 >= bb.x2 || bb.x1 >= ab.x2 || ab.y1 >= bb.y2 || bb.y1 >= ab.y2) continue

        const overlapArea =
          Math.max(0, Math.min(ab.x2, bb.x2) - Math.max(ab.x1, bb.x1)) *
          Math.max(0, Math.min(ab.y2, bb.y2) - Math.max(ab.y1, bb.y1))

        if (overlapArea > threshold) {
          warnings.push(`OVERLAP (${Math.round(overlapArea)}px²): ${a.id} (${a.type}) <-> ${b.id} (${b.type})`)
        }
      }
    }
    return warnings
  }

  function detectInconsistentFontSizes(groups) {
    const warnings = []
    for (const [groupName, ids] of Object.entries(groups)) {
      const sizes = new Map()
      for (const id of ids) {
        const el = elementsById.get(id)
        if (!el || el.type !== 'text') continue
        const fs = el.fontSize
        if (!sizes.has(fs)) sizes.set(fs, [])
        sizes.get(fs).push(id)
      }
      if (sizes.size > 1) {
        const detail = [...sizes.entries()].map(([fs, elIds]) => `${fs}px=[${elIds.join(',')}]`).join(', ')
        warnings.push(`INCONSISTENT_FONT_SIZE in "${groupName}": ${detail}`)
      }
    }
    return warnings
  }

  // ── Output ────────────────────────────────────────────────────

  function toJSON({ viewBackgroundColor = '#ffffff', theme = 'light', gridSize = 20 } = {}) {
    return JSON.stringify({
      type: 'excalidraw',
      version: 2,
      source: 'https://excalidraw.com',
      elements,
      appState: { viewBackgroundColor, theme, gridSize },
      files: {},
    }, null, 2)
  }

  function writeTo(filePath, appState = {}) {
    const json = toJSON(appState)
    fs.mkdirSync(path.dirname(filePath), { recursive: true })
    fs.writeFileSync(filePath, json, 'utf8')
    return filePath
  }

  return {
    // state access
    elements,
    getElement,

    // binding
    attachBoundElement,
    elementBinding,
    focusBinding,

    // primitives
    rect,
    text,
    labeledRect,
    line,
    dot,
    arrow,

    // validation
    detectOverlaps,
    detectInconsistentFontSizes,

    // output
    toJSON,
    writeTo,
  }
}

module.exports = {
  fontSizes,
  measureTextLine,
  centeredTextBounds,
  pathMidpoint,
  createDiagram,
}
