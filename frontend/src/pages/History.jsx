import { useState, useEffect, useCallback } from 'react'
import { Download, Trash2 } from 'lucide-react'
import PredictionTable from '../components/PredictionTable'
import FilterControls from '../components/FilterControls'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import ConfirmationDialog from '../components/ConfirmationDialog'
import { getPredictions, deletePrediction, clearHistory, exportPredictions } from '../api/predictions'

export default function History() {
  const [predictions, setPredictions] = useState([])
  const [pagination, setPagination] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showClearDialog, setShowClearDialog] = useState(false)
  const [selectedPrediction, setSelectedPrediction] = useState(null)

  const [filters, setFilters] = useState({
    search: '',
    category: '',
    riskLevel: '',
    dateFrom: '',
    dateTo: '',
  })
  const [page, setPage] = useState(1)

  const loadPredictions = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = {
        page,
        per_page: 10,
        ...filters,
      }
      const data = await getPredictions(params)
      setPredictions(data.predictions)
      setPagination(data.pagination)
    } catch (err) {
      setError(err.message || 'Failed to load predictions')
    } finally {
      setLoading(false)
    }
  }, [page, filters])

  useEffect(() => {
    loadPredictions()
  }, [loadPredictions])

  const handleFilterChange = (newFilters) => {
    setPage(1)
    setFilters(newFilters)
  }

  const handleClearFilters = () => {
    setPage(1)
    setFilters({ search: '', category: '', riskLevel: '', dateFrom: '', dateTo: '' })
  }

  const handleDelete = async (id) => {
    try {
      await deletePrediction(id)
      loadPredictions()
    } catch (err) {
      setError(err.message || 'Failed to delete prediction')
    }
  }

  const handleClearAll = async () => {
    try {
      await clearHistory()
      setShowClearDialog(false)
      loadPredictions()
    } catch (err) {
      setError(err.message || 'Failed to clear history')
    }
  }

  const handleExport = async () => {
    try {
      const blob = await exportPredictions(filters)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `predictions_export_${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      setError(err.message || 'Failed to export predictions')
    }
  }

  const handleView = (prediction) => {
    setSelectedPrediction(prediction)
  }

  return (
    <div className="page history-page">
      <div className="page-header">
        <h1>Prediction History</h1>
        <p>View and manage past message analysis results</p>
      </div>

      <div className="privacy-notice">
        <strong>Privacy Notice:</strong> Stored messages may contain personal or financial
        information. Do not share this history with unauthorized individuals.
      </div>

      <div className="history-controls">
        <FilterControls
          filters={filters}
          onFilterChange={handleFilterChange}
          onClear={handleClearFilters}
        />
        <div className="history-actions">
          <button className="btn btn-secondary" onClick={handleExport}>
            <Download size={16} />
            Export CSV
          </button>
          <button className="btn btn-danger" onClick={() => setShowClearDialog(true)}>
            <Trash2 size={16} />
            Clear History
          </button>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}

      {loading ? (
        <LoadingSpinner message="Loading history..." />
      ) : (
        <>
          <PredictionTable
            predictions={predictions}
            onView={handleView}
            onDelete={handleDelete}
          />

          {pagination && pagination.pages > 1 && (
            <div className="pagination">
              <button
                className="btn btn-secondary"
                disabled={!pagination.has_prev}
                onClick={() => setPage(page - 1)}
              >
                Previous
              </button>
              <span className="pagination-info">
                Page {pagination.page} of {pagination.pages} ({pagination.total} total)
              </span>
              <button
                className="btn btn-secondary"
                disabled={!pagination.has_next}
                onClick={() => setPage(page + 1)}
              >
                Next
              </button>
            </div>
          )}
        </>
      )}

      <ConfirmationDialog
        isOpen={showClearDialog}
        title="Clear Prediction History"
        message="Are you sure you want to delete all prediction history? This action cannot be undone."
        onConfirm={handleClearAll}
        onCancel={() => setShowClearDialog(false)}
        confirmLabel="Delete All"
        cancelLabel="Cancel"
      />

      {selectedPrediction && (
        <div className="modal-overlay" onClick={() => setSelectedPrediction(null)}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <h3>Prediction Details</h3>
            <div className="prediction-detail">
              <div className="detail-row">
                <strong>Message:</strong>
                <p>{selectedPrediction.message}</p>
              </div>
              <div className="detail-row">
                <strong>Category:</strong> {selectedPrediction.predicted_class}
              </div>
              <div className="detail-row">
                <strong>Risk Level:</strong> {selectedPrediction.risk_level}
              </div>
              <div className="detail-row">
                <strong>Confidence:</strong> {(selectedPrediction.confidence * 100).toFixed(1)}%
              </div>
              <div className="detail-row">
                <strong>Model Version:</strong> {selectedPrediction.model_version}
              </div>
              <div className="detail-row">
                <strong>Timestamp:</strong> {selectedPrediction.created_at}
              </div>
              {selectedPrediction.indicators && (
                <div className="detail-row">
                  <strong>Indicators:</strong>
                  <ul>
                    {JSON.parse(selectedPrediction.indicators).map((ind, i) => (
                      <li key={i}>{ind}</li>
                    ))}
                  </ul>
                </div>
              )}
              {selectedPrediction.recommendation && (
                <div className="detail-row">
                  <strong>Recommendation:</strong>
                  <p>{selectedPrediction.recommendation}</p>
                </div>
              )}
            </div>
            <button className="btn btn-secondary" onClick={() => setSelectedPrediction(null)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
