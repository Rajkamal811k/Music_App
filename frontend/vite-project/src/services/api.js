import axios from 'axios'

const API_BASE_URL = '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach auth token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 responses globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// ── Auth endpoints ──────────────────────────────────────────────

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/me'),
}

// ── Song endpoints ──────────────────────────────────────────────

export const songsAPI = {
  getAll: (search = '') => {
    const params = search ? { search } : {}
    return api.get('/songs', { params })
  },
  getById: (id) => api.get(`/songs/${id}`),
  upload: (formData) =>
    api.post('/songs/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  delete: (id) => api.delete(`/songs/${id}`),
  getStreamUrl: (id) => `/api/v1/songs/${id}/stream`,
}

export default api
