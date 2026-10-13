export default function ErrorMessage({ message, onRetry }) {
  if (!message) return null

  return (
    <div className="error-message" role="alert">
      <div className="error-content">
        <span className="error-icon">⚠</span>
        <p className="error-text">{message}</p>
      </div>
      {onRetry && (
        <button className="error-retry-btn" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  )
}
