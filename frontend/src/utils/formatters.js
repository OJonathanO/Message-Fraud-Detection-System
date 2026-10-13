/**
 * Format a timestamp for display
 * @param {string} timestamp - ISO timestamp
 * @returns {string} Formatted date string
 */
export function formatDate(timestamp) {
  if (!timestamp) return 'N/A'
  const date = new Date(timestamp)
  return date.toLocaleString()
}

/**
 * Format a confidence score as percentage
 * @param {number} confidence - Confidence score (0-1)
 * @returns {string} Formatted percentage
 */
export function formatConfidence(confidence) {
  if (confidence == null) return 'N/A'
  return `${(confidence * 100).toFixed(1)}%`
}

/**
 * Format a class label for display
 * @param {string} className - Class label
 * @returns {string} Formatted label
 */
export function formatClassName(className) {
  if (!className) return 'Unknown'
  const labels = {
    spam: 'Spam',
    ham: 'Legitimate',
    fraud: 'Fraudulent',
    phishing: 'Phishing',
  }
  return labels[className] || className.charAt(0).toUpperCase() + className.slice(1)
}

/**
 * Format a risk level for display
 * @param {string} riskLevel - Risk level
 * @returns {string} Formatted risk level
 */
export function formatRiskLevel(riskLevel) {
  if (!riskLevel) return 'Unknown'
  return riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1)
}

/**
 * Truncate text to a maximum length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export function truncateText(text, maxLength = 100) {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
