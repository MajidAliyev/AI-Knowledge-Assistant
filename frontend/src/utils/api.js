import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 120 seconds timeout for long operations (RAG can take time)
})

// Add request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      return Promise.reject(new Error('Request timeout. Please try again.'))
    }
    if (error.response) {
      // Server responded with error
      return Promise.reject(error)
    } else if (error.request) {
      // Request made but no response
      return Promise.reject(new Error('Cannot connect to server. Please ensure the backend is running.'))
    } else {
      // Something else happened
      return Promise.reject(error)
    }
  }
)

export const chatAPI = {
  sendMessage: async (message, conversationHistory = []) => {
    const response = await api.post('/api/chat', {
      message,
      conversation_history: conversationHistory,
    })
    return response.data
  },
}

export const searchAPI = {
  search: async (query, topK = 5) => {
    const response = await api.post('/api/search', {
      query,
      top_k: topK,
    })
    return response.data
  },
}

export const ingestAPI = {
  uploadFile: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/ingest', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
  
  ingestDirectory: async () => {
    const response = await api.post('/api/ingest/directory')
    return response.data
  },
}

export const statusAPI = {
  getStatus: async () => {
    const response = await api.get('/api/status')
    return response.data
  },
}

export default api

