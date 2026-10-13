/**
 * Risk level configuration for UI display
 */
export const RISK_CONFIG = {
  low: {
    label: 'Low',
    color: '#10b981',
    bgColor: '#064e3b',
    borderColor: '#059669',
    description: 'Message appears safe',
  },
  medium: {
    label: 'Medium',
    color: '#f59e0b',
    bgColor: '#78350f',
    borderColor: '#d97706',
    description: 'Exercise caution',
  },
  high: {
    label: 'High',
    color: '#ef4444',
    bgColor: '#7f1d1d',
    borderColor: '#dc2626',
    description: 'Likely suspicious',
  },
  critical: {
    label: 'Critical',
    color: '#dc2626',
    bgColor: '#450a0a',
    borderColor: '#b91c1c',
    description: 'Strong spam indicators',
  },
}

/**
 * Category configuration for UI display
 */
export const CATEGORY_CONFIG = {
  spam: {
    label: 'Spam',
    color: '#ef4444',
    bgColor: '#450a0a',
  },
  ham: {
    label: 'Legitimate',
    color: '#10b981',
    bgColor: '#064e3b',
  },
  fraud: {
    label: 'Fraudulent',
    color: '#dc2626',
    bgColor: '#450a0a',
  },
  phishing: {
    label: 'Phishing',
    color: '#f59e0b',
    bgColor: '#78350f',
  },
}

/**
 * Get risk config for a given risk level
 * @param {string} riskLevel - Risk level
 * @returns {Object} Risk configuration
 */
export function getRiskConfig(riskLevel) {
  return RISK_CONFIG[riskLevel] || RISK_CONFIG.medium
}

/**
 * Get category config for a given category
 * @param {string} category - Category name
 * @returns {Object} Category configuration
 */
export function getCategoryConfig(category) {
  return CATEGORY_CONFIG[category] || { label: category, color: '#6b7280', bgColor: '#1f2937' }
}
