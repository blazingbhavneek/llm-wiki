import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function MarkdownView({
  doc,
  draft,
  isEditing,
  dirty,
  editable,
  onStartEdit,
  onConfirm,
  onDelete,
  onShowGraph,
  onChangeTitle,
  onChangeBody,
}) {
  if (!doc) return null
  const badgeClass =
    doc.badge === 'Agent note'
      ? 'bg-orange/15 text-[#925d00] border-orange/25'
      : doc.badge === 'Greyed old note'
        ? 'bg-orange/15 text-[#925d00] border-orange/25'
        : 'bg-green/10 text-[#08785a] border-green/20'

  return (
    <div className="grid h-full grid-rows-[auto_minmax(0,1fr)] bg-white">
      <div className="border-b border-line bg-white px-[26px] pb-[14px] pt-[18px]">
        <div className="mb-[8px] flex flex-wrap items-center gap-2 text-[12px] text-muted">
          <span className={`inline-flex items-center gap-[6px] border px-[8px] py-[5px] font-bold ${isEditing ? 'border-blue/20 bg-blue/10 text-[#244a9d]' : badgeClass}`}>
            {isEditing ? 'Editing' : dirty ? 'Unsaved edits' : doc.badge}
          </span>
          <span>{dirty ? 'Review the changes, then confirm them.' : doc.meta}</span>
        </div>

        <div className="flex items-center gap-3">
          <input
            className="w-full border-0 bg-transparent p-0 text-[27px] font-extrabold tracking-tight text-ink outline-none read-only:cursor-default"
            value={draft.title}
            readOnly={!isEditing}
            onChange={(e) => onChangeTitle(e.target.value)}
          />
        </div>

        <div className="mt-[12px] flex flex-wrap items-center gap-2">
          <SmallBtn onClick={onStartEdit} active={isEditing} disabled={!editable}>
            {isEditing ? 'Editing' : 'Edit'}
          </SmallBtn>
          <SmallBtn onClick={onConfirm} disabled={!dirty} confirm>
            Confirm changes
          </SmallBtn>
          {editable && (
            <SmallBtn onClick={onDelete} danger>
              Delete
            </SmallBtn>
          )}
          <SmallBtn onClick={onShowGraph}>Show in graph</SmallBtn>
          <span className="text-[12px] text-muted">
            {!editable
              ? 'Unsaved draft — save it from chat to edit and keep it.'
              : isEditing
                ? 'Edit raw markdown on the left, preview on the right.'
                : 'Rendered markdown preview. Click Edit to change it.'}
          </span>
        </div>
      </div>

      <div className="min-h-0 overflow-auto bg-gradient-to-b from-white to-[#fbfdff]">
        {isEditing ? (
          <div className="grid h-full grid-cols-2 gap-0">
            <textarea
              className="h-full w-full resize-none border-r border-line bg-soft p-[26px] font-mono text-[13px] leading-[1.6] text-ink outline-none"
              value={draft.markdown}
              onChange={(e) => onChangeBody(e.target.value)}
              spellCheck={false}
            />
            <div className="h-full overflow-auto p-[36px]">
              <article className="md mx-auto max-w-[760px]">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{draft.markdown}</ReactMarkdown>
              </article>
            </div>
          </div>
        ) : (
          <article className="md mx-auto max-w-[860px] px-[36px] pb-[90px] pt-[36px]">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{draft.markdown}</ReactMarkdown>
          </article>
        )}
      </div>
    </div>
  )
}

function SmallBtn({ children, onClick, active, disabled, confirm, danger }) {
  const base = 'border px-[11px] py-[8px] text-[12px] font-bold'
  const tone = disabled
    ? 'cursor-not-allowed border-line bg-white text-muted opacity-45'
    : danger
      ? 'border-red/25 bg-red/10 text-[#7c1230] hover:bg-red/15'
      : confirm && !disabled
        ? 'border-green/25 bg-[#ecfdf5] text-[#065f46]'
        : active
          ? 'border-blue/25 bg-blue/10 text-[#244a9d]'
          : 'border-line bg-white text-muted hover:border-line2 hover:text-ink'
  return (
    <button className={`${base} ${tone}`} onClick={onClick} disabled={disabled}>
      {children}
    </button>
  )
}
