import apiClient from './client'

/**
 * Predict a single message
 * @param {string} message - The message to classify
 * @returns {Promise<Object>} Prediction result
 */
export async function predictMessage(message) {
  const response = await apiClient.post('/predict', { message })
  return response.data
}

/**
 * Predict multiple messages in batch
 * @param {string[]} messages - Array of messages to classify
 * @returns {Promise<Object>} Batch prediction results
 */
export async function predictBatch(messages) {
  const response = await apiClient.post('/predict/batch', { messages })
  return response.data
}

/**
 * Get prediction history with optional filters
 * @param {Object} params - Query parameters
 * @returns {Promise<Object>} Paginated predictions
 */
export async function getPredictions(params = {}) {
  const response = await apiClient.get('/predictions', { params })
  return response.data
}

/**
 * Get a single prediction by ID
 * @param {number} id - Prediction ID
 * @returns {Promise<Object>} Prediction details
 */
export async function getPrediction(id) {
  const response = await apiClient.get(`/predictions/${id}`)
  return response.data
}

/**
 * Delete a prediction
 * @param {number} id - Prediction ID
 * @returns {Promise<Object>} Deletion confirmation
 */
export async function deletePrediction(id) {
  const response = await apiClient.delete(`/predictions/${id}`)
  return response.data
}

/**
 * Clear all prediction history
 * @returns {Promise<Object>} Deletion confirmation
 */
export async function clearHistory() {
  const response = await apiClient.delete('/predictions')
  return response.data
}

/**
 * Get analytics summary
 * @returns {Promise<Object>} Summary statistics
 */
export async function getAnalyticsSummary() {
  const response = await apiClient.get('/analytics/summary')
  return response.data
}

/**
 * Get category distribution
 * @returns {Promise<Object>} Category counts
 */
export async function getAnalyticsCategories() {
  const response = await apiClient.get('/analytics/categories')
  return response.data
}

/**
 * Get prediction trends
 * @returns {Promise<Object>} Trend data
 */
export async function getAnalyticsTrends() {
  const response = await apiClient.get('/analytics/trends')
  return response.data
}

/**
 * Get model info
 * @returns {Promise<Object>} Model metadata
 */
export async function getModelInfo() {
  const response = await apiClient.get('/model/info')
  return response.data
}

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export async function healthCheck() {
  const response = await apiClient.get('/health')
  return response.data
}

/**
 * Export predictions to CSV
 * @param {Object} params - Filter parameters
 * @returns {Promise<Blob>} CSV file blob
 */
export async function exportPredictions(params = {}) {
  const response = await apiClient.get('/predictions/export', {
    params,
    responseType: 'blob',
  })
  return response.data
}
