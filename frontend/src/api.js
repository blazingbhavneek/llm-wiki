// Thin client over the FastAPI backend (app.py).
// Base URL configurable via VITE_API_URL; defaults to the dev server port.

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8787'

async function req(path, opts) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  })
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText)
    throw new Error(`${res.status}: ${detail}`)
  }
  return res.status === 204 ? null : res.json()
}

export const api = {
  graph: () => req('/api/graph'),
  health: (nodeId) => req(`/api/health${nodeId ? `?node_id=${encodeURIComponent(nodeId)}` : ''}`),
  recluster: (resolution = 1.0) => req(`/api/recluster?resolution=${resolution}`, { method: 'POST' }),

  node: (id) => req(`/api/node/${encodeURIComponent(id)}`),
  links: (id, direction = 'both', label) =>
    req(`/api/node/${encodeURIComponent(id)}/links?direction=${direction}${label ? `&label=${encodeURIComponent(label)}` : ''}`),
  updateNode: (id, body) =>
    req(`/api/node/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify({ body }) }),
  deleteNode: (id) => req(`/api/node/${encodeURIComponent(id)}`, { method: 'DELETE' }),

  search: (q, limit) =>
    req(`/api/search?q=${encodeURIComponent(q)}${limit ? `&limit=${limit}` : ''}`),
  ask: (question) => req('/api/ask', { method: 'POST', body: JSON.stringify({ question }) }),

  // Stream step-level agent progress via SSE. Calls onEvent(ev) per event;
  // resolves when the stream ends. Falls back to throwing on a non-OK response.
  askStream: async (question, onEvent) => {
    const res = await fetch(`${BASE}/api/ask/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    })
    if (!res.ok || !res.body) {
      const detail = await res.text().catch(() => res.statusText)
      throw new Error(`${res.status}: ${detail}`)
    }

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      let sep
      while ((sep = buffer.indexOf('\n\n')) !== -1) {
        const frame = buffer.slice(0, sep)
        buffer = buffer.slice(sep + 2)

        for (const line of frame.split('\n')) {
          if (!line.startsWith('data:')) continue // skip ": ping"/comments
          const payload = line.slice(5).trim()
          if (!payload) continue
          let ev
          try {
            ev = JSON.parse(payload)
          } catch {
            continue // ignore malformed frame
          }
          onEvent(ev) // throws here propagate to the caller
        }
      }
    }
  },
  createExogenous: (body, sourceNodeIds, origin) =>
    req('/api/exogenous', {
      method: 'POST',
      body: JSON.stringify({ body, source_node_ids: sourceNodeIds, origin }),
    }),
}
