import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ChatPanel from './components/ChatPanel'
import GraphCanvas from './components/GraphCanvas'
import MarkdownView from './components/MarkdownView'
import AnswerView from './components/AnswerView'
import ErrorBoundary from './components/ErrorBoundary'
import { api } from './api'
import { layoutGraph, docFromNode } from './data/layout'

const DEFAULT_LEFT_WIDTH = 410
const MIN_LEFT_WIDTH = 300
const MAX_LEFT_WIDTH = 760
const MIN_RIGHT_WIDTH = 460
const DIVIDER_WIDTH = 12
const OUTER_PADDING_X = 32

export default function App() {
  const shellRef = useRef(null)
  const isResizingRef = useRef(false)

  const [leftWidth, setLeftWidth] = useState(() => {
    if (typeof window === 'undefined') return DEFAULT_LEFT_WIDTH

    const saved = Number(window.localStorage.getItem('leftPanelWidth'))
    return Number.isFinite(saved) && saved > 0 ? saved : DEFAULT_LEFT_WIDTH
  })

  const [isResizing, setIsResizing] = useState(false)

  const [raw, setRaw] = useState({ nodes: [], edges: [] })
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [docs, setDocs] = useState({}) // id -> {title,badge,meta,markdown}
  const [currentId, setCurrentId] = useState(null)
  const [tab, setTab] = useState('graph')
  const [messages, setMessages] = useState([])
  const [activeAnswerId, setActiveAnswerId] = useState(null) // which message's answer the Answer tab shows
  const [savedIds, setSavedIds] = useState(() => new Set()) // answer ids already added to the wiki
  const answerSeq = useRef(0)

  const [isEditing, setEditing] = useState(false)
  const [draft, setDraft] = useState({ title: '', markdown: '' })

  const [showConflict, setShowConflict] = useState(false)
  const [showStale, setShowStale] = useState(false)
  const [insightsOpen, setInsightsOpen] = useState(false)
  const [focusIds, setFocusIds] = useState(null)
  const [toast, setToast] = useState(null)

  const graph = useMemo(() => layoutGraph(raw.nodes, raw.edges), [raw])
  const rawById = useMemo(() => new Map(raw.nodes.map((n) => [n.id, n])), [raw])
  const usedIds = useMemo(() => new Set(focusIds || []), [focusIds])

  // The answer currently shown in the Answer tab (one of possibly many in the chat).
  const activeAnswer = useMemo(() => {
    for (const m of messages) if (m.answer && m.answer.id === activeAnswerId) return m.answer
    return null
  }, [messages, activeAnswerId])

  const doc = currentId === '__draft__' ? docs['__draft__'] : docs[currentId]
  const editable = currentId && currentId !== '__draft__'
  const dirty = !!doc && (draft.title !== doc.title || draft.markdown !== doc.markdown)

  const clampLeftWidth = useCallback((value) => {
    const shell = shellRef.current
    const availableWidth = shell
      ? shell.clientWidth - OUTER_PADDING_X
      : window.innerWidth - OUTER_PADDING_X

    const maxAllowedByRightPanel = availableWidth - DIVIDER_WIDTH - MIN_RIGHT_WIDTH
    const maxLeft = Math.max(MIN_LEFT_WIDTH, Math.min(MAX_LEFT_WIDTH, maxAllowedByRightPanel))

    return Math.round(Math.min(Math.max(value, MIN_LEFT_WIDTH), maxLeft))
  }, [])

  useEffect(() => {
    setLeftWidth((w) => clampLeftWidth(w))
  }, [clampLeftWidth])

  useEffect(() => {
    if (typeof window === 'undefined') return
    window.localStorage.setItem('leftPanelWidth', String(leftWidth))
  }, [leftWidth])

  useEffect(() => {
    const onPointerMove = (e) => {
      if (!isResizingRef.current || !shellRef.current) return

      const rect = shellRef.current.getBoundingClientRect()
      const nextWidth = e.clientX - rect.left - 16

      setLeftWidth(clampLeftWidth(nextWidth))
    }

    const onPointerUp = () => {
      if (!isResizingRef.current) return

      isResizingRef.current = false
      setIsResizing(false)

      document.body.style.cursor = ''
      document.body.style.userSelect = ''
    }

    window.addEventListener('pointermove', onPointerMove)
    window.addEventListener('pointerup', onPointerUp)
    window.addEventListener('pointercancel', onPointerUp)

    return () => {
      window.removeEventListener('pointermove', onPointerMove)
      window.removeEventListener('pointerup', onPointerUp)
      window.removeEventListener('pointercancel', onPointerUp)

      document.body.style.cursor = ''
      document.body.style.userSelect = ''
    }
  }, [clampLeftWidth])

  const startResize = (e) => {
    e.preventDefault()

    isResizingRef.current = true
    setIsResizing(true)

    document.body.style.cursor = 'col-resize'
    document.body.style.userSelect = 'none'
  }

  const resetResize = () => {
    setLeftWidth(clampLeftWidth(DEFAULT_LEFT_WIDTH))
  }

  const fireToast = (text) => {
    setToast(text)
    setTimeout(() => setToast(null), 3600)
  }

  const reload = useCallback(async () => {
    const [g, h] = await Promise.all([api.graph(), api.health()])
    setRaw({ nodes: g.nodes, edges: g.edges })
    setHealth(h)
    return g
  }, [])

  useEffect(() => {
    reload()
      .catch((e) => setError(String(e.message || e)))
      .finally(() => setLoading(false))
  }, [reload])

  const openDoc = (id, d, { switchTab = true } = {}) => {
    const built = d || docs[id]
    if (!built) return

    setDocs((prev) => ({ ...prev, [id]: built }))
    setCurrentId(id)
    setDraft({ title: built.title, markdown: built.markdown })
    setEditing(false)

    if (switchTab) setTab('editor')
  }

  const openById = async (id, { switchTab = true } = {}) => {
    try {
      const node = await api.node(id)
      openDoc(id, docFromNode(node), { switchTab })
    } catch (e) {
      fireToast(`Could not open note: ${e.message}`)
    }
  }

  const openNode = (n) => openById(n.id)

  const refLabel = (id) => {
    const n = rawById.get(id)

    return {
      id,
      label: n?.title || n?.entity || id,
      note: n?.type === 'exogenous' ? 'agent note' : 'source note',
    }
  }

  // Replace the last (streaming) assistant message in place.
  const patchLast = (fn) =>
    setMessages((prev) => {
      const copy = prev.slice()
      const i = copy.length - 1
      if (i >= 0 && copy[i].role === 'assistant') copy[i] = fn(copy[i])
      return copy
    })

  const activityLine = (ev) => {
    const who = ev.agent ? `Explorer ${ev.agent}` : null
    const t = (n) => n?.title || n?.id || '…'
    switch (ev.type) {
      case 'search':
        return who ? `${who} · searching “${ev.query}”` : `Searching “${ev.query}”`
      case 'candidates':
        return `Found ${ev.count} page${ev.count === 1 ? '' : 's'}`
      case 'subagents_spawned':
        return `Spawned ${ev.starts?.length || 0} explorers`
      case 'subagent_start':
        return `${who} · exploring ${t(ev.node)}`
      case 'read':
        return `${who} · reading ${t(ev.node)}`
      case 'follow_link':
        return `${who} · following links from ${t(ev.node)} (${ev.neighbors})`
      case 'subagent_done':
        return `${who} · done (${ev.cited?.length || 0} source${ev.cited?.length === 1 ? '' : 's'})`
      case 'compiling':
        return 'Compiling answer…'
      case 'diagram_pending':
        return 'Building diagram…'
      case 'diagram_ready':
        return 'Diagram ready'
      case 'diagram_failed':
        return 'Diagram could not be rendered'
      default:
        return null
    }
  }

  const openAnswer = (answer) => {
    if (!answer) return
    setActiveAnswerId(answer.id)
    setTab('answer')
    setFocusIds(new Set(answer.citedIds || []))
  }

  const finalizeAnswer = (ans, activity, q) => {
    const cited = ans.cited_node_ids || []
    const refs = cited.map(refLabel)
    const hasAnswer = !!(ans.answer && ans.answer.trim())

    setFocusIds(new Set(cited))

    if (hasAnswer) {
      answerSeq.current += 1
      const id = answerSeq.current
      // Carry the answer payload on the message itself, so every answer in the
      // conversation stays independently viewable. Diagram events ran first and
      // stashed _diagState/_diagMd on the streaming message — fold them in.
      patchLast((prev) => ({
        role: 'assistant',
        title: `Answer ready in ${ans.steps} step${ans.steps === 1 ? '' : 's'}.`,
        text: 'Opened in the workspace on the right →. Review it, then add it to the wiki.',
        activity,
        answer: {
          id,
          question: q,
          title: q,
          markdown: prev?._diagMd ?? ans.answer,
          refs,
          steps: ans.steps,
          citedIds: cited,
          diagramState: prev?._diagState,
        },
      }))
      setActiveAnswerId(id)
      setTab('answer')
    } else {
      patchLast(() => ({
        role: 'assistant',
        title: 'Found sources, but no written answer.',
        text: `The agent gathered ${cited.length} source${
          cited.length === 1 ? '' : 's'
        } in ${ans.steps} steps but did not produce a final answer. Sources are highlighted in the graph — open one, or try a stronger chat model.`,
        refs,
        activity,
      }))
      if (cited[0]) openById(cited[0], { switchTab: false })
    }
  }

  const ask = async (q) => {
    setMessages((prev) => [
      ...prev,
      { role: 'user', text: q },
      { role: 'assistant', streaming: true, title: 'Working…', activity: [] },
    ])

    const activity = []
    try {
      await api.askStream(q, (ev) => {
        if (ev.type === 'answer') {
          finalizeAnswer(ev, activity, q)
          return
        }
        if (ev.type === 'error') {
          patchLast(() => ({ role: 'assistant', title: 'Request failed', text: ev.message }))
          return
        }
        // Diagram events arrive before the final answer; stash markdown/state on
        // the streaming message so finalizeAnswer can fold them into the payload.
        if (ev.type === 'diagram_pending') {
          patchLast((m) => ({ ...m, _diagState: 'pending' }))
        } else if (ev.type === 'diagram_ready') {
          patchLast((m) => ({ ...m, _diagState: 'ready', _diagMd: ev.answer ?? m._diagMd }))
        } else if (ev.type === 'diagram_failed') {
          patchLast((m) => ({ ...m, _diagState: 'failed', _diagMd: ev.answer ?? m._diagMd }))
        }

        const line = activityLine(ev)
        if (!line) return
        activity.push(line)
        patchLast((m) => ({ ...m, activity: [...activity] }))
      })
    } catch (e) {
      patchLast(() => ({ role: 'assistant', title: 'Request failed', text: e.message }))
    }
  }

  const addWiki = async (answer) => {
    if (!answer || savedIds.has(answer.id)) return

    try {
      const node = await api.createExogenous(
        answer.markdown,
        answer.citedIds,
        `agent:${answer.question.slice(0, 60)}`,
      )

      await reload()

      setSavedIds((prev) => new Set(prev).add(answer.id))
      openDoc(node.id, docFromNode(node))
      setFocusIds(new Set([node.id, ...answer.citedIds]))

      fireToast('Saved as a wiki note. It now lives in the graph, linked to its sources.')
    } catch (e) {
      fireToast(`Save failed: ${e.message}`)
    }
  }

  const confirmEdit = async () => {
    if (!editable) return

    try {
      const node = await api.updateNode(currentId, draft.markdown)

      await reload()

      openDoc(node.id, docFromNode(node))
      fireToast('Saved. A new version supersedes the old one; derived notes refresh automatically.')
    } catch (e) {
      fireToast(`Update failed: ${e.message}`)
    }
  }

  const deleteNode = async () => {
    if (!editable) return

    const id = currentId

    try {
      await api.deleteNode(id)
      await reload()

      setCurrentId(null)
      setTab('graph')

      fireToast('Note deleted.')
    } catch (e) {
      fireToast(`Delete failed: ${e.message}`)
    }
  }

  const onSearch = async (text) => {
    if (!text.trim()) return

    try {
      const results = await api.search(text, 8)

      if (results.length) openDoc(results[0].id, docFromNode(results[0]))
      else fireToast('No matching notes.')
    } catch (e) {
      fireToast(`Search failed: ${e.message}`)
    }
  }

  const doRecluster = async () => {
    try {
      await api.recluster()
      await reload()

      setInsightsOpen(false)

      fireToast('Recomputed topic clusters.')
    } catch (e) {
      fireToast(`Recluster failed: ${e.message}`)
    }
  }

  const conflictCount = graph.nodes.filter((n) => n.conflict).length
  const staleCount = graph.nodes.filter((n) => n.stale).length
  const isolated = health?.isolated_nodes ?? 0
  const insightTotal = conflictCount + staleCount + isolated

  const insights = [
    {
      n: conflictCount,
      label: 'possible conflicts',
      action: 'Review',
      onClick: () => {
        setShowConflict(true)
        setTab('graph')
        setInsightsOpen(false)
      },
    },
    {
      n: staleCount,
      label: 'old / superseded notes',
      action: 'Show',
      onClick: () => {
        setShowStale(true)
        setTab('graph')
        setInsightsOpen(false)
      },
    },
    {
      n: isolated,
      label: 'isolated notes',
      action: 'View',
      onClick: () => {
        setTab('graph')
        setInsightsOpen(false)
      },
    },
    {
      n: health?.exogenous_nodes ?? 0,
      label: 'agent notes',
      action: 'Recluster',
      onClick: doRecluster,
    },
  ]

  return (
    <div
      ref={shellRef}
      className="grid h-screen grid-rows-[minmax(0,1fr)] p-[16px]"
      style={{
        gridTemplateColumns: `${leftWidth}px ${DIVIDER_WIDTH}px minmax(0,1fr)`,
      }}
    >
      <ChatPanel
        messages={messages}
        health={health}
        onAsk={ask}
        onSearch={onSearch}
        onOpenNode={openById}
        onAddWiki={addWiki}
        onViewAnswer={openAnswer}
        activeAnswerId={activeAnswerId}
        savedIds={savedIds}
      />

      <div
        role="separator"
        aria-orientation="vertical"
        aria-label="Resize chat and workspace panels"
        title="Drag to resize panels. Double-click to reset."
        onPointerDown={startResize}
        onDoubleClick={resetResize}
        className={`group flex h-full cursor-col-resize items-stretch justify-center px-[4px] ${
          isResizing ? 'bg-blue/5' : ''
        }`}
      >
        <div
          className={`my-[4px] w-[4px] rounded-full transition-colors ${
            isResizing ? 'bg-blue/60' : 'bg-line group-hover:bg-blue/45'
          }`}
        />
      </div>

      <main className="relative flex min-w-0 flex-col border border-line bg-white/95 shadow-lg">
        {/* tabs */}
        <div className="flex h-[56px] items-end justify-between gap-3 border-b border-line bg-gradient-to-b from-white to-[#fbfdff] px-[12px] pt-[10px]">
          <div className="flex min-w-0 items-end gap-[6px]">
            <TabBtn active={tab === 'graph'} onClick={() => setTab('graph')} dot="bg-blue">
              Graph{health ? ` · ${health.total_nodes} nodes · ${health.total_edges} links` : ''}
            </TabBtn>

            {doc && (
              <TabBtn active={tab === 'editor'} onClick={() => setTab('editor')} dot="bg-orange" unsaved={dirty}>
                {(doc.title || 'Note').slice(0, 25)}.md
              </TabBtn>
            )}

            {activeAnswer && (
              <TabBtn active={tab === 'answer'} onClick={() => setTab('answer')} dot="bg-green">
                Answer
              </TabBtn>
            )}
          </div>

          <div className="flex items-center gap-2 pb-[9px]">
            <ToolBtn active={insightsOpen} tone="insights" onClick={() => setInsightsOpen((v) => !v)}>
              Insights {insightTotal}
            </ToolBtn>

            <ToolBtn active={showConflict} tone="conflict" onClick={() => setShowConflict((v) => !v)}>
              Conflicts
            </ToolBtn>

            <ToolBtn active={showStale} onClick={() => setShowStale((v) => !v)}>
              Stale
            </ToolBtn>
          </div>
        </div>

        {/* content */}
        <div className="relative min-h-0 flex-1 overflow-hidden bg-white">
          {loading && <Centered>Loading graph…</Centered>}

          {error && !loading && (
            <Centered>
              <div className="max-w-[420px] text-center">
                <p className="font-bold text-red">Backend not reachable</p>
                <p className="mt-2 text-[13px] text-muted">{error}</p>
                <p className="mt-2 text-[13px] text-muted">
                  Start it:{' '}
                  <code className="bg-soft2 px-1">
                    uvicorn app:app --port 8787
                  </code>
                </p>
              </div>
            </Centered>
          )}

          {!loading && !error && (
            <ErrorBoundary resetKey={`${tab}:${currentId}`}>
              <div className={`h-full ${tab === 'graph' ? 'block' : 'hidden'}`}>
                <GraphCanvas
                  nodes={graph.nodes}
                  edges={graph.edges}
                  clusters={graph.clusters}
                  worldW={graph.worldW}
                  worldH={graph.worldH}
                  currentId={currentId}
                  usedIds={usedIds}
                  focusIds={focusIds}
                  showConflict={showConflict}
                  showStale={showStale}
                  onOpenNode={openNode}
                />
              </div>

              <div className={`h-full ${tab === 'editor' ? 'block' : 'hidden'}`}>
                <MarkdownView
                  doc={doc}
                  draft={draft}
                  isEditing={isEditing}
                  dirty={dirty}
                  editable={editable}
                  onStartEdit={() => setEditing(true)}
                  onConfirm={confirmEdit}
                  onDelete={deleteNode}
                  onShowGraph={() => setTab('graph')}
                  onChangeTitle={(title) => setDraft((d) => ({ ...d, title }))}
                  onChangeBody={(markdown) => setDraft((d) => ({ ...d, markdown }))}
                />
              </div>

              <div className={`h-full ${tab === 'answer' ? 'block' : 'hidden'}`}>
                <AnswerView
                  answer={activeAnswer}
                  canSave={!!activeAnswer && !savedIds.has(activeAnswer.id)}
                  onAddWiki={() => addWiki(activeAnswer)}
                  onOpenNode={openById}
                />
              </div>
            </ErrorBoundary>
          )}

          {insightsOpen && (
            <div className="absolute right-[18px] top-[12px] z-[9] w-[280px] border border-line bg-white p-[10px] shadow-xl">
              {insights.map((it) => (
                <button
                  key={it.label}
                  className="flex w-full justify-between gap-[10px] p-[10px] text-[13px] text-muted hover:bg-soft"
                  onClick={it.onClick}
                >
                  <span>
                    <strong className="text-ink">{it.n}</strong> {it.label}
                  </span>
                  <span>{it.action}</span>
                </button>
              ))}
            </div>
          )}

          {toast && (
            <div className="absolute bottom-[22px] right-[22px] z-20 max-w-[390px] border border-green/25 bg-[#f0fdf8] px-[14px] py-[13px] text-[13px] leading-[1.45] text-[#065f46] shadow-xl">
              {toast}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

function Centered({ children }) {
  return <div className="grid h-full place-items-center text-[14px] text-muted">{children}</div>
}

function TabBtn({ children, active, onClick, dot, unsaved }) {
  return (
    <button
      className={`flex h-[36px] max-w-[320px] items-center gap-2 overflow-hidden text-ellipsis whitespace-nowrap border px-[13px] text-[13px] ${
        active ? 'border-line bg-white text-ink shadow-sm' : 'border-transparent bg-transparent text-muted'
      }`}
      onClick={onClick}
    >
      <span className={`h-[8px] w-[8px] ${dot}`} />
      {children}
      {unsaved && <span className="text-[20px] leading-none text-orange">•</span>}
    </button>
  )
}

function ToolBtn({ children, active, onClick, tone }) {
  const toneCls = active
    ? tone === 'conflict'
      ? 'border-red/25 bg-red/10 text-[#7c1230]'
      : tone === 'insights'
        ? 'border-orange/25 bg-[#fff6df] text-[#724b00]'
        : 'border-blue/25 bg-blue/10 text-[#244a9d]'
    : tone === 'insights'
      ? 'border-orange/25 bg-[#fff6df] text-[#724b00]'
      : 'border-line bg-white text-muted hover:border-line2 hover:text-ink'

  return (
    <button className={`border px-[11px] py-[8px] text-[12px] font-bold ${toneCls}`} onClick={onClick}>
      {children}
    </button>
  )
}
