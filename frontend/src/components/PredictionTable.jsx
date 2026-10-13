import RiskBadge from './RiskBadge'
import { formatDate, formatConfidence, truncateText } from '../utils/formatters'
import { getCategoryConfig } from '../utils/riskConfig'
import { Trash2, Eye } from 'lucide-react'

export default function PredictionTable({ predictions, onView, onDelete, isLoading }) {
  if (isLoading) {
    return <div className="table-loading">Loading predictions...</div>
  }

  if (!predictions || predictions.length === 0) {
    return (
      <div className="table-empty">
        <p>No predictions found. Analyze a message to get started.</p>
      </div>
    )
  }

  return (
    <div className="table-container">
      <table className="prediction-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Message</th>
            <th>Category</th>
            <th>Risk</th>
            <th>Confidence</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {predictions.map((pred) => {
            const catConfig = getCategoryConfig(pred.predicted_class)
            return (
              <tr key={pred.id}>
                <td>{pred.id}</td>
                <td className="message-cell" title={pred.message}>
                  {truncateText(pred.message, 60)}
                </td>
                <td>
                  <span
                    className="category-badge"
                    style={{ color: catConfig.color, backgroundColor: catConfig.bgColor }}
                  >
                    {catConfig.label}
                  </span>
                </td>
                <td>
                  <RiskBadge riskLevel={pred.risk_level} />
                </td>
                <td>{formatConfidence(pred.confidence)}</td>
                <td>{formatDate(pred.created_at)}</td>
                <td>
                  <div className="table-actions">
                    <button
                      className="btn btn-icon"
                      onClick={() => onView && onView(pred)}
                      title="View details"
                    >
                      <Eye size={16} />
                    </button>
                    <button
                      className="btn btn-icon btn-danger"
                      onClick={() => onDelete && onDelete(pred.id)}
                      title="Delete"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
