import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

const clampZoom = (v) => Math.max(0.05, Math.min(4.5, v))

export default function GraphCanvas({
  nodes,
  edges,
  clusters,
  worldW = 1200,
  worldH = 760,
  currentId,
  usedIds,
  focusIds,
  showConflict,
  showStale,
  onOpenNode,
}) {
  const svgRef = useRef(null)
  const wrapRef = useRef(null)
  const drag = useRef({ active: false, lastX: 0, lastY: 0 })
  const [view, setView] = useState({ scale: 1, panX: 0, panY: 0 })
  const [hover, setHover] = useState(null)

  const nodeById = useMemo(() => {
    const m = new Map()
    nodes.forEach((n) => m.set(n.id, n))
    return m
  }, [nodes])

  const clientToSvg = useCallback((clientX, clientY) => {
    const svg = svgRef.current
    if (!svg) return { x: clientX, y: clientY }
    const pt = svg.createSVGPoint()
    pt.x = clientX
    pt.y = clientY
    const m = svg.getScreenCTM()
    return m ? pt.matrixTransform(m.inverse()) : { x: clientX, y: clientY }
  }, [])

  const zoomAt = useCallback((svgX, svgY, factor) => {
    setView((v) => {
      const before = { x: (svgX - v.panX) / v.scale, y: (svgY - v.panY) / v.scale }
      const scale = clampZoom(v.scale * factor)
      return { scale, panX: svgX - before.x * scale, panY: svgY - before.y * scale }
    })
  }, [])

  // fit the whole world into the visible viewBox (which spans worldW x worldH)
  const fit = useCallback(() => {
    setView({ scale: 0.92, panX: worldW * 0.04, panY: worldH * 0.04 })
  }, [worldW, worldH])

  const reset = useCallback(() => setView({ scale: 1, panX: 0, panY: 0 }), [])

  // refit whenever the world size changes (new data loaded)
  useEffect(() => {
    fit()
  }, [fit])

  useEffect(() => {
    const svg = svgRef.current
    if (!svg) return
    const onWheel = (e) => {
      e.preventDefault()
      const p = clientToSvg(e.clientX, e.clientY)
      zoomAt(p.x, p.y, e.deltaY < 0 ? 1.12 : 0.88)
    }
    svg.addEventListener('wheel', onWheel, { passive: false })
    return () => svg.removeEventListener('wheel', onWheel)
  }, [clientToSvg, zoomAt])

  const onPointerDown = (e) => {
    if (e.target.dataset && e.target.dataset.node) return
    drag.current = { active: true, lastX: e.clientX, lastY: e.clientY }
    svgRef.current.setPointerCapture(e.pointerId)
  }
  const onPointerMove = (e) => {
    if (!drag.current.active) return
    const p0 = clientToSvg(drag.current.lastX, drag.current.lastY)
    const p1 = clientToSvg(e.clientX, e.clientY)
    drag.current.lastX = e.clientX
    drag.current.lastY = e.clientY
    setView((v) => ({ ...v, panX: v.panX + (p1.x - p0.x), panY: v.panY + (p1.y - p0.y) }))
  }
  const endDrag = (e) => {
    drag.current.active = false
    try {
      svgRef.current.releasePointerCapture(e.pointerId)
    } catch {
      /* noop */
    }
  }

  const moveHover = (e, n) => {
    const rect = wrapRef.current.getBoundingClientRect()
    setHover({ x: e.clientX - rect.left + 16, y: e.clientY - rect.top + 16, title: n.title, summary: n.summary })
  }

  const vp = {
    x: -view.panX / view.scale,
    y: -view.panY / view.scale,
    w: worldW / view.scale,
    h: worldH / view.scale,
  }

  const onMiniClick = (e) => {
    const mini = e.currentTarget
    const pt = mini.createSVGPoint()
    pt.x = e.clientX
    pt.y = e.clientY
    const m = mini.getScreenCTM()
    const p = m ? pt.matrixTransform(m.inverse()) : { x: worldW / 2, y: worldH / 2 }
    setView((v) => ({ ...v, panX: worldW / 2 - p.x * v.scale, panY: worldH / 2 - p.y * v.scale }))
  }

  const focusing = focusIds && focusIds.size > 0
  const transform = `translate(${view.panX} ${view.panY}) scale(${view.scale})`
  const gridSize = 42 * view.scale

  const nodeClass = (n) => {
    const cls = ['gnode', n.type]
    if (n.stale && showStale) cls.push('stale')
    if (n.conflict && showConflict) cls.push('conflict')
    if (usedIds && usedIds.has(n.id)) cls.push('used')
    if (n.id === currentId) cls.push('current')
    if (focusing && !focusIds.has(n.id) && n.id !== currentId) cls.push('dim')
    return cls.join(' ')
  }

  const nodeRadius = (n) =>
    n.id === currentId ? 11 : usedIds?.has(n.id) ? 8 : n.type === 'agent' ? 5.5 : 4.5

  return (
    <div ref={wrapRef} className="graph-grid relative h-full overflow-hidden" style={{ backgroundSize: `${gridSize}px ${gridSize}px`, backgroundPosition: `${view.panX}px ${view.panY}px` }}>
      <div className="absolute left-[18px] top-[18px] z-[3] w-[330px] border border-line bg-white/90 px-[14px] py-[13px] shadow-md backdrop-blur">
        <h2 className="m-0 text-[14px] font-bold tracking-tight">Infinite graph canvas</h2>
        <p className="mt-[5px] text-[12px] leading-[1.4] text-muted">
          Drag to pan, scroll to zoom. Notes grouped into dotted chapter regions. Zoom into a region to read it.
        </p>
      </div>

      <svg
        ref={svgRef}
        className={`graph-svg block h-full w-full${drag.current.active ? ' panning' : ''}`}
        viewBox={`0 0 ${worldW} ${worldH}`}
        preserveAspectRatio="xMidYMid meet"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={endDrag}
        onPointerLeave={endDrag}
      >
        <g transform={transform}>
          <g>
            {clusters.map((c) => (
              <g key={c.id}>
                <ellipse className="cluster-ring" cx={c.cx} cy={c.cy} rx={c.rx} ry={c.ry} stroke={c.color} fill={c.color + '10'} />
                <text className="cluster-label" x={c.cx} y={c.cy - c.ry - 8} textAnchor="middle">
                  {c.label}
                </text>
              </g>
            ))}
          </g>
          <g>
            {edges.map((edge, i) => {
              const a = nodeById.get(edge.a)
              const b = nodeById.get(edge.b)
              if (!a || !b) return null
              const cls = ['edge']
              if (edge.conflict && showConflict) cls.push('conflict')
              if (edge.stale && showStale) cls.push('stale')
              if (edge.support) cls.push('support')
              return <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} className={cls.join(' ')} />
            })}
          </g>
          <g>
            {nodes.map((n) => (
              <circle
                key={n.id}
                data-node={n.id}
                cx={n.x}
                cy={n.y}
                r={nodeRadius(n)}
                className={nodeClass(n)}
                onPointerEnter={(e) => moveHover(e, n)}
                onPointerMove={(e) => moveHover(e, n)}
                onPointerLeave={() => setHover(null)}
                onClick={(e) => {
                  e.stopPropagation()
                  onOpenNode(n)
                }}
              />
            ))}
          </g>
        </g>
      </svg>

      {hover && (
        <div
          className="pointer-events-none absolute z-[5] w-[250px] border border-line bg-white/95 p-[12px] shadow-md backdrop-blur"
          style={{ left: hover.x, top: hover.y }}
        >
          <strong className="mb-[4px] block text-[13px]">{hover.title}</strong>
          <p className="m-0 text-[12px] leading-[1.4] text-muted">{hover.summary}</p>
        </div>
      )}

      <div className="absolute left-[18px] top-[116px] z-[4] border border-line bg-white/90 px-[10px] py-[8px] text-[12px] text-muted shadow-md backdrop-blur">
        Drag to pan · Scroll to zoom · Click a note to open
      </div>

      <div className="absolute right-[18px] top-[18px] z-[4] w-[190px] border border-line bg-white/90 p-[10px] shadow-md backdrop-blur">
        <div className="mb-[7px] flex justify-between gap-2 text-[11px] font-extrabold uppercase tracking-wider text-muted">
          <span>Canvas map</span>
          <span>{nodes.length} notes</span>
        </div>
        <svg
          className="block h-[120px] w-full border border-line bg-soft"
          viewBox={`0 0 ${worldW} ${worldH}`}
          preserveAspectRatio="xMidYMid meet"
          onClick={onMiniClick}
        >
          {clusters.map((c) => (
            <ellipse key={c.id} cx={c.cx} cy={c.cy} rx={c.rx} ry={c.ry} fill={c.color + '14'} stroke={c.color} strokeWidth={Math.max(6, worldW / 220)} opacity={0.6} />
          ))}
          {nodes.map((n) => (
            <circle
              key={n.id}
              cx={n.x}
              cy={n.y}
              r={n.id === currentId ? worldW / 110 : worldW / 280}
              className={`mini-node ${n.type === 'agent' ? 'agent' : ''} ${n.id === currentId ? 'current' : ''}`}
            />
          ))}
          <rect className="mini-viewport" x={vp.x} y={vp.y} width={vp.w} height={vp.h} />
        </svg>
      </div>

      <div className="absolute bottom-[18px] right-[18px] z-[4] flex items-center gap-[7px] border border-line bg-white/90 p-[8px] shadow-md backdrop-blur">
        <button className="h-[32px] min-w-[34px] border border-line bg-white text-[12px] font-extrabold text-slate-700" onClick={() => zoomAt(worldW / 2, worldH / 2, 0.82)} title="Zoom out">−</button>
        <span className="min-w-[54px] text-center text-[12px] font-extrabold text-muted">{Math.round(view.scale * 100)}%</span>
        <button className="h-[32px] min-w-[34px] border border-line bg-white text-[12px] font-extrabold text-slate-700" onClick={() => zoomAt(worldW / 2, worldH / 2, 1.18)} title="Zoom in">+</button>
        <button className="h-[32px] min-w-[34px] border border-line bg-white text-[12px] font-extrabold text-slate-700" onClick={fit} title="Fit graph">Fit</button>
        <button className="h-[32px] min-w-[34px] border border-line bg-white text-[12px] font-extrabold text-slate-700" onClick={reset} title="Reset view">Reset</button>
      </div>

      <div className="absolute bottom-[18px] left-[18px] z-[3] flex max-w-[390px] flex-wrap gap-[8px] border border-line bg-white/90 p-[10px] shadow-md backdrop-blur">
        <LegendDot label="Opened note" style={{ width: 10, height: 10, background: '#111827', boxShadow: '0 0 0 6px rgba(57,119,246,.13)' }} />
        <LegendDot label="Source note" style={{ background: 'var(--color-blue)' }} />
        <LegendDot label="Agent note" style={{ background: 'var(--color-orange)' }} />
        <LegendDot label="Greyed old note" style={{ background: '#b6c0ce' }} />
        <LegendDot label="Conflict" style={{ background: 'var(--color-red)' }} />
      </div>
    </div>
  )
}

function LegendDot({ label, style }) {
  return (
    <span className="inline-flex items-center gap-[7px] text-[12px] text-muted">
      <span className="inline-block h-[8px] w-[8px]" style={style} />
      {label}
    </span>
  )
}
