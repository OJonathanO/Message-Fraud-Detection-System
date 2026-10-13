import { useState } from 'react'
import MessageInput from '../components/MessageInput'
import PredictionResult from '../components/PredictionResult'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import { predictMessage } from '../api/predictions'

export default function Analyzer() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (message) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const prediction = await predictMessage(message)
      setResult(prediction)
    } catch (err) {
      setError(err.message || 'Failed to analyze message')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page analyzer-page">
      <div className="page-header">
        <h1>Message Analyzer</h1>
        <p>Enter a message to check for spam or fraud indicators</p>
      </div>

      <div className="analyzer-container">
        <div className="analyzer-input">
          <MessageInput onAnalyze={handleAnalyze} isLoading={loading} />
        </div>

        {loading && <LoadingSpinner message="Analyzing message..." />}

        {error && <ErrorMessage message={error} />}

        {result && !loading && <PredictionResult result={result} />}
      </div>

      <div className="analyzer-info">
        <h3>How it works</h3>
        <p>
          The system uses a machine learning model trained on the UCI SMS Spam Collection
          dataset. It analyzes text patterns using TF-IDF vectorization and Logistic
          Regression to classify messages as spam or legitimate.
        </p>
        <p className="info-disclaimer">
          <strong>Note:</strong> This is a binary classifier (spam vs. legitimate).
          It does not detect fraud or phishing specifically. Results are based on
          patterns learned from the training dataset and should not be considered
          definitive proof of a message's nature.
        </p>
      </div>
    </div>
  )
}
