import { useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'
import rehypeSanitize, { defaultSchema } from 'rehype-sanitize'

const markdownSchema = {
  ...defaultSchema,

  tagNames: [
    ...(defaultSchema.tagNames || []),

    // Common HTML tags
    'div',
    'span',
    'p',
    'br',
    'hr',
    'blockquote',
    'pre',
    'code',
    'strong',
    'em',
    'u',
    's',
    'sub',
    'sup',

    // Lists
    'ul',
    'ol',
    'li',

    // Headings
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',

    // Links and media
    'a',
    'img',

    // HTML table support
    'table',
    'thead',
    'tbody',
    'tfoot',
    'tr',
    'th',
    'td',
    'caption',
    'colgroup',
    'col',
  ],

  attributes: {
    ...defaultSchema.attributes,

    '*': [
      ...(defaultSchema.attributes?.['*'] || []),
      'className',
      'class',
      'id',
      'title',
      'align',
    ],

    a: [
      ...(defaultSchema.attributes?.a || []),
      'href',
      'title',
      'target',
      'rel',
    ],

    img: [
      ...(defaultSchema.attributes?.img || []),
      'src',
      'alt',
      'title',
      'width',
      'height',
      'loading',
    ],

    table: [
      ...(defaultSchema.attributes?.table || []),
      'align',
      'border',
      'cellpadding',
      'cellspacing',
      'width',
    ],

    th: [
      ...(defaultSchema.attributes?.th || []),
      'align',
      'colspan',
      'rowspan',
      'width',
    ],

    td: [
      ...(defaultSchema.attributes?.td || []),
      'align',
      'colspan',
      'rowspan',
      'width',
    ],

    col: [
      ...(defaultSchema.attributes?.col || []),
      'align',
      'span',
      'width',
    ],

    colgroup: [
      ...(defaultSchema.attributes?.colgroup || []),
      'align',
      'span',
      'width',
    ],
  },

  protocols: {
    ...defaultSchema.protocols,

    href: [
      ...(defaultSchema.protocols?.href || []),
      'http',
      'https',
      'mailto',
      'tel',
    ],

    src: [
      ...(defaultSchema.protocols?.src || []),
      'http',
      'https',
      'data',
    ],
  },
}

function normalizeImageSrc(src) {
  if (typeof src !== 'string') return ''

  const trimmed = src.trim()

  // If the data URL somehow contains line breaks/spaces, remove them.
  if (/^data:image\//i.test(trimmed)) {
    return trimmed.replace(/\s+/g, '')
  }

  return trimmed
}

function isSafeImageSrc(src) {
  const value = normalizeImageSrc(src)

  return (
    value.startsWith('/') ||
    value.startsWith('./') ||
    value.startsWith('../') ||
    /^https?:\/\//i.test(value) ||
    /^data:image\/(png|jpe?g|gif|webp|bmp);base64,/i.test(value)
  )
}

function extractAttribute(html, attrName) {
  const pattern = new RegExp(
    `${attrName}\\s*=\\s*(?:"([^"]*)"|'([^']*)'|([^\\s>]+))`,
    'i',
  )

  const match = html.match(pattern)

  return match?.[1] || match?.[2] || match?.[3] || ''
}

function splitMarkdownByImageUnits(markdown = '') {
  const parts = []
  const imageUnitRegex = /<image-unit\b[^>]*>[\s\S]*?<\/image-unit>/gi

  let lastIndex = 0
  let match

  while ((match = imageUnitRegex.exec(markdown)) !== null) {
    const before = markdown.slice(lastIndex, match.index)

    if (before) {
      parts.push({
        type: 'markdown',
        content: before,
      })
    }

    const imageUnitHtml = match[0]
    const imgMatch = imageUnitHtml.match(/<img\b[^>]*>/i)
    const imgTag = imgMatch?.[0] || ''

    const src = normalizeImageSrc(extractAttribute(imgTag, 'src'))
    const alt = extractAttribute(imgTag, 'alt')
    const title = extractAttribute(imgTag, 'title')

    if (src) {
      parts.push({
        type: 'image',
        src,
        alt,
        title,
      })
    }

    lastIndex = match.index + match[0].length
  }

  const after = markdown.slice(lastIndex)

  if (after) {
    parts.push({
      type: 'markdown',
      content: after,
    })
  }

  return parts
}

function SafeImage({
  src,
  alt = '',
  title,
  className = '',
  width,
  height,
}) {
  const [failed, setFailed] = useState(false)

  const normalizedSrc = normalizeImageSrc(src)

  if (!isSafeImageSrc(normalizedSrc)) {
    return (
      <div className="my-4 rounded-lg border border-red/25 bg-red/10 p-3 text-[13px] text-[#7c1230]">
        Blocked unsafe image source.
      </div>
    )
  }

  if (failed) {
    return (
      <div className="my-4 rounded-lg border border-red/25 bg-red/10 p-3 text-[13px] leading-[1.45] text-[#7c1230]">
        Image failed to load or decode. The base64 data may be incomplete or corrupted.
      </div>
    )
  }

  return (
    <img
      src={normalizedSrc}
      alt={alt || ''}
      title={title}
      width={width}
      height={height}
      loading="lazy"
      decoding="async"
      onError={() => setFailed(true)}
      className={`block max-h-[620px] max-w-full rounded-lg border border-line bg-white object-contain ${className}`}
    />
  )
}

function ImageUnit({ src, alt, title }) {
  return (
    <figure className="my-6 overflow-hidden rounded-xl border border-line bg-white p-4 shadow-sm">
      <div className="flex justify-center overflow-auto">
        <SafeImage src={src} alt={alt} title={title} />
      </div>
    </figure>
  )
}

const markdownComponents = {
  img: ({ node, src = '', alt = '', title, width, height }) => (
    <SafeImage
      src={src}
      alt={alt}
      title={title}
      width={width}
      height={height}
    />
  ),

  a: ({ node, href = '', children, ...props }) => {
    const isExternal = /^https?:\/\//i.test(href)

    return (
      <a
        href={href}
        target={isExternal ? '_blank' : undefined}
        rel={isExternal ? 'noreferrer noopener' : undefined}
        className="font-semibold text-blue underline underline-offset-2 hover:opacity-80"
        {...props}
      >
        {children}
      </a>
    )
  },

  table: ({ children }) => (
    <div className="my-5 overflow-x-auto rounded-lg border border-line">
      <table className="w-full border-collapse text-sm">
        {children}
      </table>
    </div>
  ),

  thead: ({ children, ...props }) => (
    <thead className="bg-soft" {...props}>
      {children}
    </thead>
  ),

  tbody: ({ children, ...props }) => (
    <tbody {...props}>
      {children}
    </tbody>
  ),

  tr: ({ children, ...props }) => (
    <tr className="border-b border-line last:border-b-0" {...props}>
      {children}
    </tr>
  ),

  th: ({ children, ...props }) => (
    <th
      className="border-r border-line bg-soft px-3 py-2 text-left font-bold last:border-r-0"
      {...props}
    >
      {children}
    </th>
  ),

  td: ({ children, ...props }) => (
    <td
      className="border-r border-line px-3 py-2 align-top last:border-r-0"
      {...props}
    >
      {children}
    </td>
  ),

  code: ({ node, inline, className = '', children, ...props }) => {
    if (inline) {
      return (
        <code
          className="rounded bg-soft px-1.5 py-0.5 font-mono text-[0.9em]"
          {...props}
        >
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

  pre: ({ children, ...props }) => (
    <pre
      className="my-4 overflow-x-auto rounded-lg border border-line bg-[#0f172a] p-4 text-sm text-white"
      {...props}
    >
      {children}
    </pre>
  ),

  blockquote: ({ children, ...props }) => (
    <blockquote
      className="my-4 border-l-4 border-blue/40 bg-blue/5 px-4 py-2 text-muted"
      {...props}
    >
      {children}
    </blockquote>
  ),
}

function MarkdownChunk({ markdown }) {
  if (!markdown) return null

  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[
        rehypeRaw,
        [rehypeSanitize, markdownSchema],
      ]}
      components={markdownComponents}
    >
      {markdown}
    </ReactMarkdown>
  )
}

function MarkdownRenderer({ markdown }) {
  const parts = useMemo(
    () => splitMarkdownByImageUnits(markdown || ''),
    [markdown],
  )

  return (
    <>
      {parts.map((part, index) => {
        if (part.type === 'image') {
          return (
            <ImageUnit
              key={`image-${index}`}
              src={part.src}
              alt={part.alt}
              title={part.title}
            />
          )
        }

        return (
          <MarkdownChunk
            key={`markdown-${index}`}
            markdown={part.content}
          />
        )
      })}
    </>
  )
}

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
          <span
            className={`inline-flex items-center gap-[6px] border px-[8px] py-[5px] font-bold ${
              isEditing
                ? 'border-blue/20 bg-blue/10 text-[#244a9d]'
                : badgeClass
            }`}
          >
            {isEditing ? 'Editing' : dirty ? 'Unsaved edits' : doc.badge}
          </span>

          <span>
            {dirty ? 'Review the changes, then confirm them.' : doc.meta}
          </span>
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
          <SmallBtn
            onClick={onStartEdit}
            active={isEditing}
            disabled={!editable}
          >
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

          <SmallBtn onClick={onShowGraph}>
            Show in graph
          </SmallBtn>

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
                <MarkdownRenderer markdown={draft.markdown} />
              </article>
            </div>
          </div>
        ) : (
          <article className="md mx-auto max-w-[860px] px-[36px] pb-[90px] pt-[36px]">
            <MarkdownRenderer markdown={draft.markdown} />
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
    <button
      className={`${base} ${tone}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}
