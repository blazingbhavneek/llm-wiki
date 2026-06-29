// Thin client over the wiki-view backend (app2.py).
// Base URL configurable via VITE_WIKI_API_URL; defaults to the app2 dev port.

const BASE = import.meta.env.VITE_WIKI_API_URL || 'http://localhost:8788'

async function req(path, opts) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  })
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText)
    throw new Error(`${res.status}: ${detail}`)
  }
  return res.json()
}

export const wikiApi = {
  health: () => req('/api/health'),
  tree: () => req('/api/wiki/tree'),
  navigation: () => req('/api/wiki/navigation'),
  source: (docId) => req(`/api/wiki/source/${encodeURIComponent(docId)}`),
  page: (path) => req(`/api/wiki/page?path=${encodeURIComponent(path)}`),
  rebuild: () => req('/api/wiki/rebuild', { method: 'POST' }),
}
