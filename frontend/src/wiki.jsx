import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import WikiBrowser from './components/WikiBrowser.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <WikiBrowser />
  </StrictMode>,
)
