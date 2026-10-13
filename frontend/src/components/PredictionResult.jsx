import { useState } from 'react'
import RiskBadge from './RiskBadge'
import ConfidenceIndicator from './ConfidenceIndicator'
import { formatConfidence, formatDate } from '../utils/formatters'
import { getCategoryConfig } from '../utils/riskConfig'
import { Copy, Check } from 'lucide-react'

export default function PredictionResult({ result }) {
  const [copied, setCopied] = useState(false)

  if (!result) return null

  const categoryConfig = getCategoryConfig(result.predicted_class)

  const handleCopy = () => {
    const summary = `Prediction: ${result.predicted_class}\nRisk: ${result.risk_level}\nConfidence: ${formatConfidence(result.confidence)}\nRecommendation: ${result.recommendation}`
    navigator.clipboard.writeText(summary)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="prediction-result">
      <div className="result-header">
        <h3>Analysis Result</h3>
        <button className="btn btn-icon" onClick={handleCopy} title="Copy summary">
          {copied ? <Check size={16} /> : <Copy size={16} />}
        </button>
      </div>

      <div className="result-body">
        <div className="result-main">
          <div className="result-class" style={{ color: categoryConfig.color }}>
            {categoryConfig.label}
          </div>
          <RiskBadge riskLevel={result.risk_level} />
        </div>

        <ConfidenceIndicator confidence={result.confidence} />

        {result.indicators && result.indicators.length > 0 && (
          <div className="result-section">
            <h4>Key Indicators</h4>
            <ul className="indicators-list">
              {result.indicators.map((indicator, idx) => (
                <li key={idx}>{indicator}</li>
              ))}
            </ul>
          </div>
        )}

        {result.recommendation && (
          <div className="result-section">
            <h4>Recommendation</h4>
            <p className="recommendation-text">{result.recommendation}</p>
          </div>
        )}

        {result.explanation_disclaimer && (
          <p className="disclaimer-text">{result.explanation_disclaimer}</p>
        )}

        <div className="result-meta">
          <span>Model: {result.model_version}</span>
          {result.timestamp && <span> | {formatDate(result.timestamp)}</span>}
        </div>
      </div>
    </div>
  )
}
