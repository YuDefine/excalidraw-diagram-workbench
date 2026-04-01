/**
 * Channel Map diagram generator.
 * Reads a JSON spec and produces an .excalidraw file with roles → access columns → UI → feature grids.
 *
 * Usage:
 *   node generate_diagram.js [spec.json] [--dark]
 */
const fs = require('node:fs')
const path = require('node:path')
const { fontSizes, measureTextLine, createDiagram } = require('./lib/excalidraw')

// ── Themes ────────────────────────────────────────────────────────

const themes = {
  light: {
    viewBackgroundColor: '#ffffff',
    titleColor: '#1e40af',
    subtitleColor: '#3b82f6',
    detailColor: '#64748b',
    primaryStroke: '#1e3a5f',
    secondaryFill: '#60a5fa',
    triggerFill: '#fed7aa',
    triggerStroke: '#c2410c',
    successFill: '#a7f3d0',
    successStroke: '#047857',
    nodeFill: '#dbeafe',
    textColor: '#374151',
    frameStroke: '#1e3a5f',
  },
  dark: {
    viewBackgroundColor: '#1e1e2e',
    titleColor: '#89b4fa',
    subtitleColor: '#74c7ec',
    detailColor: '#a6adc8',
    primaryStroke: '#89b4fa',
    secondaryFill: '#313244',
    triggerFill: '#45475a',
    triggerStroke: '#fab387',
    successFill: '#313244',
    successStroke: '#a6e3a1',
    nodeFill: '#313244',
    textColor: '#cdd6f4',
    frameStroke: '#585b70',
  },
}

const specArgs = process.argv.slice(2).filter((arg) => !arg.startsWith('--'))
const themeName = process.argv.includes('--dark') ? 'dark' : 'light'
const palette = themes[themeName]

const {
  viewBackgroundColor, titleColor, subtitleColor, detailColor,
  primaryStroke, secondaryFill, triggerFill, triggerStroke,
  successFill, successStroke, nodeFill, textColor, frameStroke,
} = palette

// ── Channel-map layout constants ─────────────────────────────────

const defaultSpecPath = path.join(__dirname, 'examples', 'channel-map.example.json')

const toneStyles = {
  warm: { stroke: triggerStroke, fill: triggerFill },
  primary: { stroke: primaryStroke, fill: secondaryFill },
  success: { stroke: successStroke, fill: successFill },
  neutral: { stroke: primaryStroke, fill: nodeFill },
}

const sectionDefaults = {
  rolesTitle: '角色',
  accessTitle: '入口管道',
  accessNote: '虛線通道與圓點顯示各角色可使用的入口。',
  uiTitle: '體驗層',
  uiNote: '各入口會導向對應的介面。',
  mobileTitle: '行動端功能',
  desktopTitle: '桌面端功能',
}

const accessColumnStartX = 440
const accessColumnGap = 20

const roleLayout = {
  frameX: 40, frameY: 140,
  cardX: 80, cardY: 180,
  cardWidth: 220, cardHeight: 62,
  rowStep: 110,
}

const uiNodeWidth = 240
const uiSlotYs = [
  { y: 180, minHeight: 86 },
  { y: 355, minHeight: 96 },
  { y: 610, minHeight: 86 },
]

const gridFrameWidth = 660
const gridCardWidth = 220
const gridCardHeight = 82
const gridColumns = 2
const gridColumnStep = 290

// ── Spec helpers ──────────────────────────────────────────────────

function readSpec(specArg) {
  const specPath = specArg ? path.resolve(process.cwd(), specArg) : defaultSpecPath
  try {
    return JSON.parse(fs.readFileSync(specPath, 'utf8'))
  } catch (error) {
    throw new Error(`Failed to read diagram spec at ${specPath}: ${error.message}`)
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message)
}

function ensureUniqueIds(nodes, label) {
  const seen = new Set()
  for (const node of nodes) {
    assert(typeof node.id === 'string' && node.id.length > 0, `${label} entries must include an id.`)
    assert(!seen.has(node.id), `${label} ids must be unique. Duplicate id: ${node.id}`)
    seen.add(node.id)
  }
  return seen
}

function normalizeSpec(rawSpec) {
  assert(rawSpec && typeof rawSpec === 'object', 'The diagram spec must be a JSON object.')
  assert(typeof rawSpec.title === 'string' && rawSpec.title.length > 0, 'The diagram spec must include a title.')
  assert(typeof rawSpec.subtitle === 'string' && rawSpec.subtitle.length > 0, 'The diagram spec must include a subtitle.')
  assert(Array.isArray(rawSpec.roles) && rawSpec.roles.length > 0, 'The diagram spec must include at least one role.')
  assert(Array.isArray(rawSpec.accessColumns) && rawSpec.accessColumns.length >= 1, 'The diagram spec must include at least one access column.')
  assert(Array.isArray(rawSpec.uiNodes) && rawSpec.uiNodes.length === uiSlotYs.length, `This sample renderer expects exactly ${uiSlotYs.length} UI nodes.`)
  assert(Array.isArray(rawSpec.mobileNodes) && rawSpec.mobileNodes.length > 0, 'The diagram spec must include mobile nodes.')
  assert(Array.isArray(rawSpec.desktopNodes) && rawSpec.desktopNodes.length > 0, 'The diagram spec must include desktop nodes.')

  const sections = { ...sectionDefaults, ...(rawSpec.sections ?? {}) }

  const roles = rawSpec.roles.map((role) => {
    assert(typeof role.label === 'string' && role.label.length > 0, 'Each role must include a label.')
    return { id: role.id, label: role.label }
  })
  const roleIds = ensureUniqueIds(roles, 'Role')

  const uiNodesRaw = rawSpec.uiNodes.map((node, index) => {
    assert(typeof node.label === 'string' && node.label.length > 0, 'Each UI node must include a label.')
    assert(typeof node.tone === 'string' && Object.hasOwn(toneStyles, node.tone), `Unknown UI tone: ${node.tone}`)
    return { ...node, ...uiSlotYs[index], width: uiNodeWidth, ...toneStyles[node.tone] }
  })
  const uiIds = ensureUniqueIds(uiNodesRaw, 'UI node')
  const uiNodeById = new Map(uiNodesRaw.map((node) => [node.id, node]))

  const accessColumnKeys = new Set()
  const accessColumnsRaw = rawSpec.accessColumns.map((column) => {
    assert(typeof column.key === 'string' && column.key.length > 0, 'Each access column must include a key.')
    assert(!accessColumnKeys.has(column.key), `Access column keys must be unique. Duplicate key: ${column.key}`)
    accessColumnKeys.add(column.key)
    assert(typeof column.label === 'string' && column.label.length > 0, 'Each access column must include a label.')
    assert(typeof column.tone === 'string' && Object.hasOwn(toneStyles, column.tone), `Unknown access tone: ${column.tone}`)
    assert(typeof column.uiId === 'string' && uiIds.has(column.uiId), `Unknown UI node reference: ${column.uiId}`)
    assert(Array.isArray(column.roles), `Access column "${column.key}" must include a roles array.`)
    for (const roleId of column.roles) {
      assert(roleIds.has(roleId), `Access column "${column.key}" references an unknown role id: ${roleId}`)
    }

    const fontSize = fontSizes.sm
    const lines = column.label.split('\n')
    const contentWidth = Math.max(...lines.map((line) => measureTextLine(line, fontSize)))
    const labelWidth = Math.max(62, Math.ceil(contentWidth + 18))

    return {
      ...column,
      id: column.id ?? `access_${column.key}`,
      ...toneStyles[column.tone],
      uiNode: uiNodeById.get(column.uiId),
      labelWidth,
    }
  })

  let cursorX = accessColumnStartX
  const accessColumns = accessColumnsRaw.map((column) => {
    const x = cursorX + Math.round(column.labelWidth / 2)
    cursorX += column.labelWidth + accessColumnGap
    return { ...column, x }
  })

  const accessRightEdge = cursorX - accessColumnGap
  const uiFrameX = accessRightEdge + 40
  const uiNodeX = uiFrameX + 45
  const uiFrameWidth = uiNodeWidth + 90
  const gridFrameX = uiFrameX + uiFrameWidth + 240
  const gridCardX = gridFrameX + 50

  const uiNodes = uiNodesRaw.map((node) => ({ ...node, x: uiNodeX }))
  const finalUiNodeById = new Map(uiNodes.map((node) => [node.id, node]))
  for (const column of accessColumns) {
    column.uiNode = finalUiNodeById.get(column.uiId)
  }

  const uiFrameLayout = { x: uiFrameX, y: 140, width: uiFrameWidth, height: 720 }
  const mobileGridLayout = {
    frameX: gridFrameX, frameY: 140, frameWidth: gridFrameWidth,
    cardX: gridCardX, cardY: 240, cardWidth: gridCardWidth, cardHeight: gridCardHeight,
    columns: gridColumns, columnStep: gridColumnStep, rowStep: 130, bottomPadding: 48,
  }
  const desktopGridLayout = {
    frameX: gridFrameX, frameY: 550, frameWidth: gridFrameWidth,
    cardX: gridCardX, cardY: 650, cardWidth: gridCardWidth, cardHeight: gridCardHeight,
    columns: gridColumns, columnStep: gridColumnStep, rowStep: 140, bottomPadding: 38,
  }

  const mobileNodes = rawSpec.mobileNodes.map((node) => {
    assert(typeof node.id === 'string' && node.id.length > 0, 'Each mobile node must include an id.')
    assert(typeof node.label === 'string' && node.label.length > 0, 'Each mobile node must include a label.')
    return node
  })
  ensureUniqueIds(mobileNodes, 'Mobile node')

  const desktopNodes = rawSpec.desktopNodes.map((node) => {
    assert(typeof node.id === 'string' && node.id.length > 0, 'Each desktop node must include an id.')
    assert(typeof node.label === 'string' && node.label.length > 0, 'Each desktop node must include a label.')
    return node
  })
  ensureUniqueIds(desktopNodes, 'Desktop node')

  return {
    title: rawSpec.title, subtitle: rawSpec.subtitle, sections,
    roles, accessColumns, uiNodes, uiFrameLayout,
    mobileGridLayout, desktopGridLayout, mobileNodes, desktopNodes,
  }
}

// ── Channel-map helpers ──────────────────────────────────────────

function uiNodeFontSize(label) {
  return label.split('\n').length > 1 ? fontSizes.md : fontSizes.lg
}

function uiNodeHeight(label, fontSize, minHeight) {
  return Math.max(minHeight, Math.ceil(label.split('\n').length * fontSize * 1.25 + 36))
}

function gridPositions(nodes, layout) {
  return nodes.map((node, index) => ({
    ...node,
    x: layout.cardX + (index % layout.columns) * layout.columnStep,
    y: layout.cardY + Math.floor(index / layout.columns) * layout.rowStep,
  }))
}

function frameHeightFromGrid(layout, positionedNodes) {
  const lastBottom = Math.max(...positionedNodes.map((node) => node.y + layout.cardHeight))
  return lastBottom - layout.frameY + layout.bottomPadding
}

function accessColumnWidth(label, fontSize) {
  const lines = label.split('\n')
  const contentWidth = Math.max(...lines.map((line) => measureTextLine(line, fontSize)))
  return Math.max(62, Math.ceil(contentWidth + 18))
}

// ── Build diagram ────────────────────────────────────────────────

const d = createDiagram()
const spec = normalizeSpec(readSpec(specArgs[0]))

d.text('diagram_title', 60, 22, 760, 36, spec.title, titleColor, fontSizes.xl, 'left')
d.text('diagram_subtitle', 60, 62, 1120, 24, spec.subtitle, detailColor, fontSizes.md, 'left')

const roleFrameHeight = spec.roles.length * roleLayout.rowStep + 20
const mobileNodes = gridPositions(spec.mobileNodes, spec.mobileGridLayout)
const desktopNodes = gridPositions(spec.desktopNodes, spec.desktopGridLayout)
const mobileFrameHeight = frameHeightFromGrid(spec.mobileGridLayout, mobileNodes)
const desktopFrameHeight = frameHeightFromGrid(spec.desktopGridLayout, desktopNodes)

d.rect('roles_frame', roleLayout.frameX, roleLayout.frameY, 300, roleFrameHeight, frameStroke, 'transparent', 'dashed')
d.rect('ui_frame', spec.uiFrameLayout.x, spec.uiFrameLayout.y, spec.uiFrameLayout.width, spec.uiFrameLayout.height, frameStroke, 'transparent', 'dashed')
d.rect('mobile_frame', spec.mobileGridLayout.frameX, spec.mobileGridLayout.frameY, spec.mobileGridLayout.frameWidth, mobileFrameHeight, primaryStroke, 'transparent', 'dashed')
d.rect('desktop_frame', spec.desktopGridLayout.frameX, spec.desktopGridLayout.frameY, spec.desktopGridLayout.frameWidth, desktopFrameHeight, primaryStroke, 'transparent', 'dashed')

d.text('roles_title', 60, 108, 220, 28, spec.sections.rolesTitle, titleColor, fontSizes.lg, 'left')
d.text('access_title', 390, 108, Math.max(100, spec.uiFrameLayout.x - 390 - 10), 28, spec.sections.accessTitle, titleColor, fontSizes.lg, 'left')
d.text('access_note', 390, 136, Math.max(100, spec.uiFrameLayout.x - 390 - 10), 16, spec.sections.accessNote, detailColor, fontSizes.sm, 'left')
d.text('ui_title', spec.uiFrameLayout.x + 20, 108, spec.uiFrameLayout.width - 40, 28, spec.sections.uiTitle, titleColor, fontSizes.lg, 'left')
d.text('ui_note', spec.uiFrameLayout.x + 20, 136, 300, 24, spec.sections.uiNote, subtitleColor, fontSizes.sm, 'left')
d.text('mobile_title', spec.mobileGridLayout.frameX + 20, 108, 280, 28, spec.sections.mobileTitle, titleColor, fontSizes.lg, 'left')
d.text('desktop_title', spec.mobileGridLayout.frameX + 20, 518, 280, 28, spec.sections.desktopTitle, titleColor, fontSizes.lg, 'left')

const roleRows = {}

spec.roles.forEach((role, index) => {
  const y = roleLayout.cardY + index * roleLayout.rowStep
  d.labeledRect(role.id, roleLayout.cardX, y, roleLayout.cardWidth, roleLayout.cardHeight, role.label, primaryStroke, nodeFill, {
    textStrokeColor: textColor, fontSize: fontSizes.md,
  })
  roleRows[role.id] = y + Math.round(roleLayout.cardHeight / 2)
})

spec.uiNodes.forEach((uiNode) => {
  const fontSize = uiNodeFontSize(uiNode.label)
  const height = uiNodeHeight(uiNode.label, fontSize, uiNode.minHeight)
  uiNode.height = height
  uiNode.centerY = uiNode.y + Math.round(height / 2)
  d.labeledRect(uiNode.id, uiNode.x, uiNode.y, uiNode.width, height, uiNode.label, uiNode.stroke, uiNode.fill, {
    textStrokeColor: textColor, fontSize,
  })
})

const accessX = {}
const roleAccessMap = Object.fromEntries(spec.roles.map((role) => [role.id, []]))
const accessLineHeight = Math.max(...Object.values(roleRows)) + 3 - 206

spec.accessColumns.forEach((column) => {
  accessX[column.key] = column.x
  column.roles.forEach((roleId) => { roleAccessMap[roleId].push(column.key) })

  const fontSize = fontSizes.sm
  const width = accessColumnWidth(column.label, fontSize)
  const left = column.x - width / 2

  d.labeledRect(column.id, left, 154, width, 42, column.label, column.stroke, column.fill, {
    textStrokeColor: textColor, fontSize,
  })
  d.line(`access_${column.key}_line`, column.x, 206, [[0, 0], [0, accessLineHeight]], column.stroke, 'dashed')

  for (const roleId of column.roles) {
    d.dot(`access_${column.key}_${roleId}`, column.x - 6, roleRows[roleId] - 6, column.stroke)
  }

  const accessBottomY = 196
  const uiCenterY = column.uiNode.centerY
  const uiLeftX = column.uiNode.x
  d.arrow(
    `access_${column.key}_to_ui`,
    column.x, accessBottomY,
    [[0, 0], [0, uiCenterY - accessBottomY], [uiLeftX - column.x, uiCenterY - accessBottomY]],
    column.stroke, 'arrow',
    {
      startBinding: d.elementBinding(column.id, [0.5, 1]),
      endBinding: d.elementBinding(column.uiNode.id, [0, 0.5]),
    },
  )
})

for (const [roleId, keys] of Object.entries(roleAccessMap)) {
  const offsets = keys.length === 1 ? [0] : keys.length === 2 ? [-10, 10] : [-14, 0, 14]

  keys.forEach((key, index) => {
    const startX = roleLayout.cardX + roleLayout.cardWidth
    const startY = roleRows[roleId] + offsets[index]
    const endX = accessX[key]
    const endY = roleRows[roleId]
    const elbowX = endX - 18

    d.arrow(
      `role_${roleId}_to_${key}`,
      startX, startY,
      [[0, 0], [elbowX - startX, 0], [elbowX - startX, endY - startY], [endX - startX, endY - startY]],
      spec.accessColumns.find((column) => column.key === key).stroke,
      null,
      {
        startBinding: d.elementBinding(roleId, [1, 0.5]),
        endBinding: d.elementBinding(`access_${key}_${roleId}`, [0.5, 0.5]),
      },
    )
  })
}

const firstUiCenterX = spec.uiNodes[0].x + Math.round(spec.uiNodes[0].width / 2)
const secondUiRight = spec.uiNodes[1].x + spec.uiNodes[1].width
const thirdUiRight = spec.uiNodes[2].x + spec.uiNodes[2].width
const mobileFrameLeft = [spec.mobileGridLayout.frameX, spec.mobileGridLayout.frameY + Math.round(mobileFrameHeight / 2)]
const desktopFrameLeft = [spec.desktopGridLayout.frameX, spec.desktopGridLayout.frameY + Math.round(desktopFrameHeight / 2)]

d.arrow(
  'ui_flow_1',
  firstUiCenterX, spec.uiNodes[0].centerY,
  [[0, 0], [0, spec.uiNodes[1].centerY - spec.uiNodes[0].centerY]],
  triggerStroke, 'arrow',
  {
    startBinding: d.elementBinding(spec.uiNodes[0].id, [0.5, 1]),
    endBinding: d.elementBinding(spec.uiNodes[1].id, [0.5, 0]),
  },
)

mobileNodes.forEach((node) => {
  d.labeledRect(node.id, node.x, node.y, spec.mobileGridLayout.cardWidth, spec.mobileGridLayout.cardHeight, node.label, primaryStroke, nodeFill, {
    textStrokeColor: textColor, fontSize: fontSizes.md,
  })
})

desktopNodes.forEach((node) => {
  d.labeledRect(node.id, node.x, node.y, spec.desktopGridLayout.cardWidth, spec.desktopGridLayout.cardHeight, node.label, primaryStroke, nodeFill, {
    textStrokeColor: textColor, fontSize: fontSizes.md,
  })
})

// orthogonal arrows: UI → feature frames
function orthArrow(id, from, to, lane, strokeColor, endArrowhead, opts) {
  const [sx, sy] = from
  const [ex, ey] = to
  d.arrow(id, sx, sy, [[0, 0], [lane, 0], [lane, ey - sy], [ex - sx, ey - sy]], strokeColor, endArrowhead, opts)
}

orthArrow('ui_to_mobile_frame', [secondUiRight, spec.uiNodes[1].centerY], mobileFrameLeft, 125, primaryStroke, 'arrow', {
  startBinding: d.elementBinding(spec.uiNodes[1].id, [1, 0.5]),
  endBinding: d.elementBinding('mobile_frame', [0, 0.5]),
})
orthArrow('ui_to_desktop_frame', [thirdUiRight, spec.uiNodes[2].centerY], desktopFrameLeft, 125, successStroke, 'arrow', {
  startBinding: d.elementBinding(spec.uiNodes[2].id, [1, 0.5]),
  endBinding: d.elementBinding('desktop_frame', [0, 0.5]),
})

// ── Validation ───────────────────────────────────────────────────

const frameIds = new Set(['roles_frame', 'ui_frame', 'mobile_frame', 'desktop_frame'])
const overlapWarnings = d.detectOverlaps({ ignoreIds: frameIds })

const fontSizeGroups = {
  'section titles': ['roles_title', 'access_title', 'ui_title', 'mobile_title', 'desktop_title'],
  'section notes': ['access_note', 'ui_note'],
}
const fontWarnings = d.detectInconsistentFontSizes(fontSizeGroups)

const allWarnings = [...overlapWarnings, ...fontWarnings]

if (allWarnings.length > 0) {
  process.stderr.write(`⚠ Diagram warnings (${allWarnings.length}):\n`)
  for (const warning of allWarnings) {
    process.stderr.write(`  ${warning}\n`)
  }
}

// ── Output ────────────────────────────────────────────────────────

const specPath = specArgs[0] ? path.resolve(process.cwd(), specArgs[0]) : null

if (specPath) {
  const baseName = path.basename(specPath).replace(/\.spec\.json$/, '').replace(/\.json$/, '')
  const suffix = themeName === 'dark' ? '-dark' : ''
  const outPath = path.join(path.dirname(specPath), `${baseName}${suffix}.excalidraw`)
  d.writeTo(outPath, { viewBackgroundColor, theme: themeName })
  process.stdout.write(`${outPath}\n`)
} else {
  process.stdout.write(d.toJSON({ viewBackgroundColor, theme: themeName }))
}
