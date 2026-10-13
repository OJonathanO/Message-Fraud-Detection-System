import { formatConfidence } from '../utils/formatters'

export default function ConfidenceIndicator({ confidence }) {
  if (confidence == null) return null

  const percentage = confidence * 100
  let color = '#10b981' // green
  if (percentage < 50) color = '#ef4444' // red
  else if (percentage < 70) color = '#f59e0b' // amber

  return (
    <div className="confidence-indicator">
      <div className="confidence-header">
        <span className="confidence-label">Model Confidence</span>
        <span className="confidence-value" style={{ color }}>
          {formatConfidence(confidence)}
        </span>
      </div>
      <div className="confidence-bar-container">
        <div
          className="confidence-bar"
          style={{
            width: `${percentage}%`,
            backgroundColor: color,
          }}
        />
      </div>
    </div>
  )
}
