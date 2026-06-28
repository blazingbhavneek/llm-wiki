import { useCallback, useEffect, useMemo, useState } from 'react'
import ChatPanel from './components/ChatPanel'
import GraphCanvas from './components/GraphCanvas'
import MarkdownView from './components/MarkdownView'
import ErrorBoundary from './components/ErrorBoundary'
import { api } from './api'
import { layoutGraph, docFromNode } from './data/layout'

export default function App() {
  const [raw, setRaw] = useState({ nodes: [], edges: [] })
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [docs, setDocs] = useState({}) // id -> {title,badge,meta,markdown}
  const [currentId, setCurrentId] = useState(null)
  const [tab, setTab] = useState('graph')
  const [messages, setMessages] = useState([])
  const [pending, setPending] = useState(null) // {answer, citedIds} draft awaiting save

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

  const doc = currentId === '__draft__' ? docs['__draft__'] : docs[currentId]
  const editable = currentId && currentId !== '__draft__'
  const dirty = !!doc && (draft.title !== doc.title || draft.markdown !== doc.markdown)

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
    return { id, label: n?.title || n?.entity || id, note: n?.type === 'exogenous' ? 'agent note' : 'source note' }
  }

  const ask = async (q) => {
    setMessages((prev) => [...prev, { role: 'user', text: q }])
    try {
      const ans = await api.ask(q)
      const cited = ans.cited_node_ids || []
      const refs = cited.map(refLabel)
      const hasAnswer = !!(ans.answer && ans.answer.trim())

      setMessages((prev) => [
        ...prev,
        hasAnswer
          ? { role: 'assistant', title: `Answer in ${ans.steps} step${ans.steps === 1 ? '' : 's'}.`, text: ans.answer, refs, canSave: true }
          : {
              role: 'assistant',
              title: 'Found sources, but no written answer.',
              text: `The agent gathered ${cited.length} source${cited.length === 1 ? '' : 's'} in ${ans.steps} steps but did not produce a final answer (the current model is small). Sources are highlighted in the graph — open one, or try a stronger chat model.`,
              refs,
              canSave: false,
            },
      ])
      setFocusIds(new Set(cited))

      // Keep the user on whatever tab they're on (don't yank them to the note).
      // The answer is in the chat; cited nodes light up in the graph.
      if (hasAnswer) {
        setPending({ answer: ans.answer, citedIds: cited, question: q })
        openDoc(
          '__draft__',
          {
            title: 'Draft answer',
            badge: 'Agent note',
            meta: 'Unsaved draft. Click "Add to wiki" in the chat to keep it.',
            markdown: ans.answer,
          },
          { switchTab: false },
        )
      } else {
        setPending(null)
        if (cited[0]) openById(cited[0], { switchTab: false })
      }
    } catch (e) {
      setMessages((prev) => [...prev, { role: 'assistant', title: 'Request failed', text: e.message }])
    }
  }

  const addWiki = async () => {
    if (!pending) return
    try {
      const node = await api.createExogenous(pending.answer, pending.citedIds, `agent:${pending.question.slice(0, 60)}`)
      await reload()
      setPending(null)
      openDoc(node.id, docFromNode(node))
      setFocusIds(new Set([node.id, ...pending.citedIds]))
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
    { n: conflictCount, label: 'possible conflicts', action: 'Review', onClick: () => { setShowConflict(true); setTab('graph'); setInsightsOpen(false) } },
    { n: staleCount, label: 'old / superseded notes', action: 'Show', onClick: () => { setShowStale(true); setTab('graph'); setInsightsOpen(false) } },
    { n: isolated, label: 'isolated notes', action: 'View', onClick: () => { setTab('graph'); setInsightsOpen(false) } },
    { n: health?.exogenous_nodes ?? 0, label: 'agent notes', action: 'Recluster', onClick: doRecluster },
  ]

  return (
    <div className="grid h-screen grid-cols-[410px_minmax(0,1fr)] grid-rows-[minmax(0,1fr)] gap-[16px] p-[16px]">
      <ChatPanel
        messages={messages}
        health={health}
        onAsk={ask}
        onSearch={onSearch}
        onOpenNode={openById}
        onAddWiki={addWiki}
        canSave={!!pending}
      />

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
                <p className="mt-2 text-[13px] text-muted">Start it: <code className="bg-soft2 px-1">uvicorn app:app --port 8787</code></p>
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
            </ErrorBoundary>
          )}

          {insightsOpen && (
            <div className="absolute right-[18px] top-[12px] z-[9] w-[280px] border border-line bg-white p-[10px] shadow-xl">
              {insights.map((it) => (
                <button key={it.label} className="flex w-full justify-between gap-[10px] p-[10px] text-[13px] text-muted hover:bg-soft" onClick={it.onClick}>
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
