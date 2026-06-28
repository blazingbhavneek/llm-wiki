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
  createExogenous: (body, sourceNodeIds, origin) =>
    req('/api/exogenous', {
      method: 'POST',
      body: JSON.stringify({ body, source_node_ids: sourceNodeIds, origin }),
    }),
}
