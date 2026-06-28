import { Component } from 'react'

// Catches render errors in a subtree so one broken view (e.g. a bad markdown doc)
// never blanks the whole app. Remounts when `resetKey` changes (tab/note switch).
export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidUpdate(prev) {
    if (prev.resetKey !== this.props.resetKey && this.state.error) {
      this.setState({ error: null })
    }
  }

  render() {
    if (this.state.error) {
      return (
        <div className="grid h-full place-items-center p-6">
          <div className="max-w-[420px] text-center">
            <p className="font-bold text-red">This view hit an error</p>
            <p className="mt-2 text-[13px] text-muted">{String(this.state.error.message || this.state.error)}</p>
            <p className="mt-3 text-[13px] text-muted">Switch tabs or open another note — the rest of the app still works.</p>
          </div>
        </div>
      )
    }
    return this.props.children
  }
}
