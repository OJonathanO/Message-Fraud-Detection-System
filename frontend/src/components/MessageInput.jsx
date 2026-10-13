import { useState } from 'react'

export default function MessageInput({ onAnalyze, isLoading }) {
  const [message, setMessage] = useState('')
  const maxLength = 5000

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !isLoading) {
      onAnalyze(message.trim())
    }
  }

  const handleClear = () => {
    setMessage('')
  }

  const charCount = message.length
  const isNearLimit = charCount > maxLength * 0.9

  return (
    <form onSubmit={handleSubmit} className="message-input-form">
      <label htmlFor="message-input" className="input-label">
        Enter message to analyze
      </label>
      <textarea
        id="message-input"
        className="message-textarea"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Paste or type a message, email, or notification to check for spam or fraud indicators..."
        maxLength={maxLength}
        rows={6}
        disabled={isLoading}
      />
      <div className="input-footer">
        <span className={`char-count ${isNearLimit ? 'near-limit' : ''}`}>
          {charCount} / {maxLength}
        </span>
        <div className="input-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleClear}
            disabled={isLoading || !message}
          >
            Clear
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isLoading || !message.trim()}
          >
            {isLoading ? 'Analyzing...' : 'Analyze Message'}
          </button>
        </div>
      </div>
    </form>
  )
}
