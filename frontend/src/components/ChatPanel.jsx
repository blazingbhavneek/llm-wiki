import { useEffect, useRef, useState } from 'react'

export default function ChatPanel({ messages, health, onAsk, onSearch, onOpenNode, onAddWiki }) {
  const [question, setQuestion] = useState('')
  const [search, setSearch] = useState('')
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const submit = () => {
    if (!question.trim()) return
    onAsk(question.trim())
    setQuestion('')
  }

  return (
    <aside className="flex h-full min-h-0 min-w-0 flex-col overflow-hidden border border-line bg-white/95 shadow-lg">
      {/* brand */}
      <div className="border-b border-line bg-gradient-to-b from-white to-[#fbfdff] p-[20px]">
        <div className="flex items-center justify-between gap-[14px]">
          <div className="flex min-w-0 items-center gap-3">
            <div className="grid h-[42px] w-[42px] place-items-center border border-blue/15 bg-gradient-to-br from-blue/15 to-orange/15 font-extrabold text-[#244a9d]">
              LW
            </div>
            <div>
              <h1 className="m-0 text-[17px] tracking-tight">LLM-Wiki</h1>
              <p className="mt-[3px] text-[12px] text-muted">Chat over a living knowledge graph</p>
            </div>
          </div>
          <div className="whitespace-nowrap border border-green/20 bg-green/10 px-[10px] py-[8px] text-[12px] text-[#08785a]">
            Upload processed
          </div>
        </div>

        <div className="relative mt-[16px]">
          <span className="pointer-events-none absolute left-[14px] top-[9px] text-[18px] text-muted2">⌕</span>
          <input
            className="w-full border border-line bg-white py-[12px] pl-[39px] pr-[12px] text-ink outline-none focus:border-blue/45 focus:shadow-[0_0_0_4px_rgba(57,119,246,.1)]"
            placeholder="Find a note or topic…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && onSearch?.(search)}
          />
        </div>

        {health && (
          <div className="mt-[12px] border border-line bg-soft px-[12px] py-[11px] text-[12.5px] leading-[1.45] text-muted">
            <strong className="text-ink">{health.endogenous_nodes}</strong> source notes ·{' '}
            <strong className="text-ink">{health.exogenous_nodes}</strong> agent notes ·{' '}
            <strong className="text-ink">{health.total_edges}</strong> links across{' '}
            <strong className="text-ink">{Object.keys(health.clusters || {}).length}</strong> topics.
          </div>
        )}
      </div>

      {/* messages */}
      <div className="min-h-0 flex-1 overflow-auto bg-gradient-to-b from-[#fbfdff] to-white p-[18px]">
        {messages.map((m, i) =>
          m.role === 'user' ? (
            <div key={i} className="mb-[16px]">
              <div className="ml-[42px] border border-[#cadcff] bg-[#f1f6ff] px-[15px] py-[14px] text-[14px] leading-[1.5] shadow-sm">
                {m.text}
              </div>
            </div>
          ) : (
            <div key={i} className="mb-[16px]">
              <div className="mb-[8px] flex items-center gap-2 text-[12px] text-muted">
                <span className="inline-grid h-[22px] w-[22px] place-items-center bg-blue/10 text-[11px] font-bold text-[#244a9d]">AI</span>
                Answer completed · opened markdown tab on the right
              </div>
              <div className="border border-line bg-white px-[15px] py-[14px] text-[14px] leading-[1.5] shadow-sm">
                <div className="mb-[6px] font-bold">{m.title}</div>
                <p className="m-0">{m.text}</p>

                {m.refs?.length > 0 && (
                  <div className="mt-[12px] border-t border-line pt-[12px]">
                    <h3 className="m-0 mb-[8px] text-[12px] font-bold uppercase tracking-wider text-muted">References</h3>
                    <ol className="m-0 list-decimal pl-[20px] text-[13px] text-muted">
                      {m.refs.map((r) => (
                        <li key={r.id} className="my-[6px] pl-[3px]">
                          <button className="border-b border-dotted border-[#244a9d]/40 text-[#244a9d] hover:text-blue" onClick={() => onOpenNode(r.id)}>
                            {r.label}
                          </button>{' '}
                          — {r.note}
                        </li>
                      ))}
                    </ol>
                  </div>
                )}

                {m.canSave && (
                  <div className="mt-[13px] flex items-center gap-[10px]">
                    <button className="border-0 bg-ink px-[13px] py-[10px] text-[13px] font-bold text-white shadow-md" onClick={onAddWiki}>
                      Add to wiki
                    </button>
                    <span className="text-[12px] text-muted">Creates a clean markdown note from this answer.</span>
                  </div>
                )}
              </div>
            </div>
          ),
        )}
        <div ref={endRef} />
      </div>

      {/* composer */}
      <div className="shrink-0 border-t border-line bg-white p-[14px]">
        <div className="flex gap-[9px] border border-line bg-soft p-[8px]">
          <input
            className="min-w-0 flex-1 border-0 bg-transparent p-[8px] text-ink outline-none"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && submit()}
            placeholder="Ask the graph…"
          />
          <button className="border-0 bg-blue px-[14px] font-bold text-white" onClick={submit}>
            Ask
          </button>
        </div>
      </div>
    </aside>
  )
}
