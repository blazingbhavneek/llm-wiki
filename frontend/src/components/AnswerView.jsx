import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import MermaidDiagram from './MermaidDiagram'

/**
 * Read-only viewer for an LLM-generated answer (3rd workspace tab).
 * Renders the answer markdown (with zoomable Mermaid diagrams), the cited
 * references, and the "Add to wiki" action.
 */
export default function AnswerView({ answer, onAddWiki, onOpenNode, canSave }) {
  if (!answer) return null

  const refs = answer.refs || []

  return (
    <div className="grid h-full grid-rows-[auto_minmax(0,1fr)] bg-white">
      <div className="border-b border-line bg-white px-[26px] pb-[14px] pt-[18px]">
        <div className="mb-[8px] flex flex-wrap items-center gap-2 text-[12px] text-muted">
          <span className="inline-flex items-center gap-[6px] border border-orange/25 bg-orange/15 px-[8px] py-[5px] font-bold text-[#925d00]">
            Agent answer
          </span>
          <span>
            {answer.steps ? `Generated in ${answer.steps} step${answer.steps === 1 ? '' : 's'}.` : ''}{' '}
            Unsaved — add it to the wiki to keep it.
          </span>
        </div>

        <h1 className="m-0 text-[27px] font-extrabold tracking-tight text-ink">
          {answer.title || 'Answer'}
        </h1>

        <div className="mt-[12px] flex flex-wrap items-center gap-2">
          <button
            className="border border-green/25 bg-[#ecfdf5] px-[11px] py-[8px] text-[12px] font-bold text-[#065f46] disabled:cursor-not-allowed disabled:opacity-45"
            onClick={onAddWiki}
            disabled={!canSave}
          >
            Add to wiki
          </button>
          <span className="text-[12px] text-muted">
            Creates a clean markdown note from this answer, linked to its sources.
          </span>
        </div>
      </div>

      <div className="min-h-0 overflow-auto bg-gradient-to-b from-white to-[#fbfdff]">
        <article className="md mx-auto max-w-[860px] px-[36px] pb-[90px] pt-[36px]">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code: ({ node, inline, className, children, ...props }) => {
                if (!inline && (className || '').includes('language-mermaid')) {
                  return (
                    <MermaidDiagram
                      code={String(children).replace(/\n$/, '')}
                      state={answer.diagramState}
                    />
                  )
                }
                if (inline) {
                  return (
                    <code className="rounded bg-soft px-1.5 py-0.5 font-mono text-[0.9em]" {...props}>
                      {children}
                    </code>
                  )
                }
                return (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              },
              pre: ({ node, children, ...props }) => {
                const child = Array.isArray(children) ? children[0] : children
                if ((child?.props?.className || '').includes('language-mermaid')) return <>{children}</>
                return (
                  <pre
                    className="my-4 overflow-x-auto rounded-lg border border-line bg-[#0f172a] p-4 text-sm text-white"
                    {...props}
                  >
                    {children}
                  </pre>
                )
              },
            }}
          >
            {answer.markdown || ''}
          </ReactMarkdown>
        </article>

        {refs.length > 0 && (
          <div className="mx-auto max-w-[860px] px-[36px] pb-[60px]">
            <h3 className="mb-[8px] text-[12px] font-bold uppercase tracking-wider text-muted">
              References
            </h3>
            <ol className="m-0 list-decimal pl-[20px] text-[13px] text-muted">
              {refs.map((r) => (
                <li key={r.id} className="my-[6px]">
                  <button
                    className="border-b border-dotted border-[#244a9d]/40 text-left text-[#244a9d] hover:text-blue"
                    onClick={() => onOpenNode(r.id)}
                  >
                    {r.label}
                  </button>{' '}
                  — {r.note}
                </li>
              ))}
            </ol>
          </div>
        )}
      </div>
    </div>
  )
}
