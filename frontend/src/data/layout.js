// Backend nodes have no coordinates. Compute a deterministic layout grouped by
// COARSE topic (chapter), so 900+ fine-grained headings don't each become their
// own 1-node cell. World size grows with the number of groups so nodes spread out
// and stay readable. Maps backend fields -> render flags.

const PALETTE = ['#3977f6', '#f59e0b', '#8b5cf6', '#10b981', '#ef476f', '#0ea5e9', '#ec4899', '#14b8a6', '#a855f7', '#f97316']

function hash(str) {
  let h = 2166136261
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return (h >>> 0) / 4294967295
}
function gaussian(seed) {
  const u = Math.max(hash(seed + 'u'), 0.001)
  const v = Math.max(hash(seed + 'v'), 0.001)
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v)
}

const STALE_STATUS = new Set(['stale', 'superseded', 'deleted'])

// Collapse a fine cluster label ("24.3.2.4.7 Memcpy…", "Chapter 26. …") into a
// coarse chapter bucket. Falls back to the raw label / "Misc".
function coarseKey(label) {
  if (!label) return 'Misc'
  const m = label.match(/^(?:Chapter\s+)?(\d+)/i)
  if (m) return `Ch ${m[1]}`
  // short topical labels (e.g. "Managed", "Shared Memory") keep their own bucket
  if (label.length <= 22) return label
  return 'Misc'
}

function chapterOrder(key) {
  const m = key.match(/^Ch (\d+)$/)
  return m ? parseInt(m[1], 10) : 9999
}

export function layoutGraph(rawNodes, rawEdges) {
  const conflictNodes = new Set()
  rawEdges.forEach((e) => {
    if (e.label === 'contradicts') {
      conflictNodes.add(e.source_node_id)
      conflictNodes.add(e.target_node_id)
    }
  })

  // AUTO: if the backend gave meaningful clusters (e.g. after recluster()), group
  // by node.cluster directly. Only when clusters are mostly singletons (a weak
  // model left every heading its own cluster) do we collapse by chapter number.
  const distinct = new Set(rawNodes.map((n) => n.cluster || 'Misc')).size
  const mostlySingletons = rawNodes.length > 0 && distinct > rawNodes.length * 0.4
  const keyFn = mostlySingletons ? (n) => coarseKey(n.cluster) : (n) => n.cluster || 'Misc'

  const groups = new Map()
  rawNodes.forEach((n) => {
    const key = keyFn(n)
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key).push(n)
  })

  // order: numbered chapters first, then alpha
  const labels = [...groups.keys()].sort((a, b) => {
    const oa = chapterOrder(a)
    const ob = chapterOrder(b)
    return oa !== ob ? oa - ob : a.localeCompare(b)
  })

  // grid of cells; cell size scales with the biggest group so dense chapters fit
  const cols = Math.max(1, Math.ceil(Math.sqrt(labels.length)))
  const rows = Math.max(1, Math.ceil(labels.length / cols))
  const maxGroup = Math.max(...[...groups.values()].map((g) => g.length), 1)
  const cell = Math.max(420, 120 + Math.sqrt(maxGroup) * 90)
  const worldW = cols * cell
  const worldH = rows * cell

  const clusters = labels.map((label, i) => {
    const members = groups.get(label)
    const cx = (i % cols) * cell + cell / 2
    const cy = Math.floor(i / cols) * cell + cell / 2
    const r = Math.min(cell * 0.46, 70 + Math.sqrt(members.length) * 26)
    return { id: label, label, cx, cy, rx: r, ry: r * 0.82, color: PALETTE[i % PALETTE.length] }
  })
  const clusterById = new Map(clusters.map((c) => [c.id, c]))

  const nodes = rawNodes.map((n) => {
    const c = clusterById.get(keyFn(n))
    const gx = gaussian(n.id + 'x') * c.rx * 0.42
    const gy = gaussian(n.id + 'y') * c.ry * 0.42
    return {
      id: n.id,
      x: Math.max(20, Math.min(worldW - 20, c.cx + gx)),
      y: Math.max(20, Math.min(worldH - 20, c.cy + gy)),
      cluster: c.id,
      type: n.type === 'exogenous' ? 'agent' : 'source',
      stale: STALE_STATUS.has(n.status),
      conflict: conflictNodes.has(n.id),
      title: n.title || n.entity || n.id,
      summary: n.summary || '',
    }
  })

  const edges = rawEdges.map((e) => ({
    a: e.source_node_id,
    b: e.target_node_id,
    conflict: e.label === 'contradicts',
    stale: !!e.invalid_at || e.label === 'superseded_by' || e.label === 'supersedes',
    support: e.label === 'supports',
  }))

  return { nodes, edges, clusters, worldW, worldH }
}

export function docFromNode(n) {
  return {
    title: n.title || n.entity || n.id,
    badge: n.type === 'exogenous' ? 'Agent note' : 'Source note',
    meta:
      n.status && n.status !== 'active'
        ? `Status: ${n.status}. Kept for history.`
        : n.original_document_name
          ? `Source: ${n.original_document_name}`
          : 'Click Edit to change this note.',
    markdown: n.body || `# ${n.title || n.id}\n\n${n.summary || ''}`,
  }
}
