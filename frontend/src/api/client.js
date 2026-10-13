import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.message || 'An error occurred'
      console.error(`API Error ${error.response.status}: ${message}`)
      return Promise.reject(new Error(message))
    } else if (error.request) {
      // Request made but no response
      console.error('API Error: No response from server')
      return Promise.reject(new Error('No response from server. Is the backend running?'))
    } else {
      // Something else happened
      console.error('API Error:', error.message)
      return Promise.reject(error)
    }
  }
)

export default apiClient
