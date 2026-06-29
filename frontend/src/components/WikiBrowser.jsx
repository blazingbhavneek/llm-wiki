import { useEffect, useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { wikiApi } from '../wikiApi'

// Docs-style browser over the hierarchical wiki view served by app2.py.
// Left: source -> section -> page tree (from /api/wiki/navigation).
// Right: the selected canonical page, fetched lazily via /api/wiki/page.

export default function WikiBrowser() {
  const [nav, setNav] = useState(null)
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('')
  const [openSources, setOpenSources] = useState(() => new Set())
  const [openSections, setOpenSections] = useState(() => new Set())

  const [current, setCurrent] = useState(null) // {title, path}
  const [pageContent, setPageContent] = useState('')
  const [pageLoading, setPageLoading] = useState(false)

  useEffect(() => {
    wikiApi.navigation().then(setNav).catch((e) => setError(e.message))
  }, [])

  useEffect(() => {
    if (!current) return
    setPageLoading(true)
    wikiApi
      .page(current.path)
      .then((r) => setPageContent(r.content))
      .catch((e) => setPageContent(`> Failed to load page: ${e.message}`))
      .finally(() => setPageLoading(false))
  }, [current])

  const toggle = (set, setter, key) => {
    const next = new Set(set)
    next.has(key) ? next.delete(key) : next.add(key)
    setter(next)
  }

  // Filter pages by title/summary; keep a source/section visible if it has hits.
  const filtered = useMemo(() => {
    if (!nav) return null
    const q = query.trim().toLowerCase()
    if (!q) return nav.sources
    return nav.sources
      .map((s) => {
        const sections = s.sections
          .map((sec) => ({
            ...sec,
            pages: sec.pages.filter(
              (p) =>
                p.title.toLowerCase().includes(q) ||
                (p.summary || '').toLowerCase().includes(q),
            ),
          }))
          .filter((sec) => sec.pages.length)
        return { ...s, sections }
      })
      .filter((s) => s.sections.length)
  }, [nav, query])

  if (error) return <div style={S.error}>Backend error: {error}</div>
  if (!nav) return <div style={S.loading}>Loading wiki view…</div>

  const searching = query.trim().length > 0

  return (
    <div style={S.shell}>
      <aside style={S.sidebar}>
        <div style={S.brand}>
          <strong>Wiki Browser</strong>
          <span style={S.muted}>
            {nav.source_count} sources · {nav.page_count} pages
          </span>
        </div>
        <input
          style={S.search}
          placeholder="Filter pages…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div style={S.tree}>
          {filtered.map((s) => {
            const sourceOpen = searching || openSources.has(s.doc_id)
            return (
              <div key={s.doc_id}>
                <button
                  style={S.sourceRow}
                  onClick={() => toggle(openSources, setOpenSources, s.doc_id)}
                >
                  <span style={S.caret}>{sourceOpen ? '▾' : '▸'}</span>
                  <span style={S.sourceTitle}>{s.title}</span>
                  <span style={S.count}>{s.page_count}</span>
                </button>
                {sourceOpen &&
                  s.sections.map((sec) => {
                    const key = `${s.doc_id}::${sec.header}`
                    const secOpen = searching || openSections.has(key)
                    return (
                      <div key={key} style={S.sectionWrap}>
                        <button
                          style={S.sectionRow}
                          onClick={() => toggle(openSections, setOpenSections, key)}
                        >
                          <span style={S.caret}>{secOpen ? '▾' : '▸'}</span>
                          <span style={S.sectionTitle}>{sec.header}</span>
                          <span style={S.count}>{sec.page_count}</span>
                        </button>
                        {secOpen &&
                          sec.pages.map((p) => (
                            <button
                              key={p.slug + p.line_start}
                              style={{
                                ...S.pageRow,
                                ...(current?.path === p.path ? S.pageActive : null),
                              }}
                              onClick={() => setCurrent(p)}
                              title={p.summary}
                            >
                              {p.title}
                            </button>
                          ))}
                      </div>
                    )
                  })}
              </div>
            )
          })}
        </div>
      </aside>

      <main style={S.reader}>
        {current ? (
          <>
            <div style={S.crumb}>
              <span style={S.muted}>{current.path}</span>
              {pageLoading && <span style={S.muted}> · loading…</span>}
            </div>
            <div className="wiki-md">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{pageContent}</ReactMarkdown>
            </div>
          </>
        ) : (
          <div style={S.empty}>Select a page from the tree.</div>
        )}
      </main>
    </div>
  )
}

const S = {
  shell: { display: 'flex', height: '100vh', fontFamily: 'system-ui, sans-serif', color: '#1f2933' },
  sidebar: { width: 340, borderRight: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column', background: '#f8fafc' },
  brand: { padding: '14px 16px', display: 'flex', flexDirection: 'column', gap: 2, borderBottom: '1px solid #e2e8f0' },
  muted: { color: '#64748b', fontSize: 12 },
  search: { margin: 12, padding: '8px 10px', border: '1px solid #cbd5e1', borderRadius: 6, fontSize: 13 },
  tree: { overflowY: 'auto', flex: 1, paddingBottom: 24 },
  sourceRow: { display: 'flex', alignItems: 'center', gap: 6, width: '100%', padding: '8px 12px', border: 'none', background: 'none', cursor: 'pointer', textAlign: 'left', fontWeight: 600, fontSize: 13 },
  sectionWrap: { paddingLeft: 8 },
  sectionRow: { display: 'flex', alignItems: 'center', gap: 6, width: '100%', padding: '5px 12px', border: 'none', background: 'none', cursor: 'pointer', textAlign: 'left', fontSize: 12.5, color: '#334155' },
  pageRow: { display: 'block', width: '100%', padding: '4px 12px 4px 34px', border: 'none', background: 'none', cursor: 'pointer', textAlign: 'left', fontSize: 12.5, color: '#475569' },
  pageActive: { background: '#e0f2fe', color: '#0369a1', fontWeight: 600 },
  caret: { width: 12, color: '#94a3b8', fontSize: 11 },
  sourceTitle: { flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' },
  sectionTitle: { flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' },
  count: { color: '#94a3b8', fontSize: 11 },
  reader: { flex: 1, overflowY: 'auto', padding: '24px 40px' },
  crumb: { marginBottom: 16, paddingBottom: 8, borderBottom: '1px solid #e2e8f0' },
  empty: { color: '#94a3b8', marginTop: 80, textAlign: 'center' },
  loading: { padding: 40, color: '#64748b' },
  error: { padding: 40, color: '#b91c1c' },
}
