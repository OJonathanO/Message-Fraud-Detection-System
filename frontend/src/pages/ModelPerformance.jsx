import { useState, useEffect } from 'react'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import { getModelInfo } from '../api/predictions'

export default function ModelPerformance() {
  const [modelInfo, setModelInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadModelInfo()
  }, [])

  const loadModelInfo = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await getModelInfo()
      setModelInfo(data)
    } catch (err) {
      setError(err.message || 'Failed to load model information')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner message="Loading model info..." />
  if (error) return <ErrorMessage message={error} onRetry={loadModelInfo} />
  if (!modelInfo) return null

  const evalData = modelInfo.evaluation
  const metadata = modelInfo.training_metadata

  return (
    <div className="page model-performance-page">
      <div className="page-header">
        <h1>Model Performance</h1>
        <p>Evaluation metrics and training information</p>
      </div>

      <div className="model-info-grid">
        <div className="info-card">
          <h3>Model Information</h3>
          <div className="info-row">
            <span className="info-label">Version:</span>
            <span className="info-value">{modelInfo.model_version}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Classes:</span>
            <span className="info-value">{modelInfo.classes?.join(', ')}</span>
          </div>
          {metadata && (
            <>
              <div className="info-row">
                <span className="info-label">Training Date:</span>
                <span className="info-value">{metadata.training_date}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Dataset:</span>
                <span className="info-value">{metadata.dataset}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Train Size:</span>
                <span className="info-value">{metadata.train_size}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Test Size:</span>
                <span className="info-value">{metadata.test_size}</span>
              </div>
            </>
          )}
        </div>

        {evalData && (
          <div className="info-card">
            <h3>Evaluation Metrics</h3>
            <div className="metrics-grid">
              <div className="metric">
                <span className="metric-value">{(evalData.accuracy * 100).toFixed(1)}%</span>
                <span className="metric-label">Accuracy</span>
              </div>
              <div className="metric">
                <span className="metric-value">{(evalData.precision * 100).toFixed(1)}%</span>
                <span className="metric-label">Precision</span>
              </div>
              <div className="metric">
                <span className="metric-value">{(evalData.recall * 100).toFixed(1)}%</span>
                <span className="metric-label">Recall</span>
              </div>
              <div className="metric">
                <span className="metric-value">{(evalData.f1_score * 100).toFixed(1)}%</span>
                <span className="metric-label">F1 Score</span>
              </div>
            </div>
          </div>
        )}

        {evalData?.classification_report && (
          <div className="info-card info-card-wide">
            <h3>Per-Class Metrics</h3>
            <table className="metrics-table">
              <thead>
                <tr>
                  <th>Class</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1-Score</th>
                  <th>Support</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(evalData.classification_report)
                  .filter(([key]) => key !== 'accuracy' && key !== 'macro avg' && key !== 'weighted avg')
                  .map(([className, metrics]) => (
                    <tr key={className}>
                      <td>{className === 'spam' ? 'Spam' : 'Legitimate'}</td>
                      <td>{(metrics.precision * 100).toFixed(1)}%</td>
                      <td>{(metrics.recall * 100).toFixed(1)}%</td>
                      <td>{(metrics['f1-score'] * 100).toFixed(1)}%</td>
                      <td>{metrics.support}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        )}

        {metadata?.limitations && (
          <div className="info-card info-card-wide">
            <h3>Known Limitations</h3>
            <ul className="limitations-list">
              {metadata.limitations.map((limitation, idx) => (
                <li key={idx}>{limitation}</li>
              ))}
            </ul>
          </div>
        )}

        {metadata?.pipeline_steps && (
          <div className="info-card info-card-wide">
            <h3>Pipeline Architecture</h3>
            <ol className="pipeline-list">
              {metadata.pipeline_steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ol>
          </div>
        )}
      </div>
    </div>
  )
}
