import axios from 'axios'
import type { ApiResponse } from '@/types/api'
import { ElMessage } from 'element-plus'

const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor: attach JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: handle token refresh + errors
let isRefreshing = false
let refreshQueue: Array<{ resolve: (token: string) => void; reject: (err: any) => void }> = []

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { config, response } = error

    // Token expired — try refresh
    if (response?.status === 401 && !config._retry && !config.url?.includes('/auth/')) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        redirectToLogin()
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          refreshQueue.push({ resolve, reject })
        }).then((token) => {
          config.headers.Authorization = `Bearer ${token}`
          return apiClient(config)
        })
      }

      isRefreshing = true
      config._retry = true

      try {
        const { data } = await axios.post('/api/v1/auth/refresh', {
          refresh_token: refreshToken,
        })
        const newToken = data.data.access_token
        localStorage.setItem('access_token', newToken)
        if (data.data.refresh_token) {
          localStorage.setItem('refresh_token', data.data.refresh_token)
        }

        refreshQueue.forEach(({ resolve }) => resolve(newToken))
        refreshQueue = []

        config.headers.Authorization = `Bearer ${newToken}`
        return apiClient(config)
      } catch (refreshError) {
        refreshQueue.forEach(({ reject }) => reject(refreshError))
        refreshQueue = []
        redirectToLogin()
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    // Normalize error message
    const message = response?.data?.message || error.message || '网络请求失败'
    if (response?.status !== 401) {
      ElMessage.error(message)
    }
    return Promise.reject(error)
  }
)

function redirectToLogin() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_info')
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

// Typed request helpers
export async function get<T>(url: string, params?: any): Promise<ApiResponse<T>> {
  const { data } = await apiClient.get(url, { params })
  return data
}

export async function post<T>(url: string, body?: any): Promise<ApiResponse<T>> {
  const { data } = await apiClient.post(url, body)
  return data
}

export async function put<T>(url: string, body?: any): Promise<ApiResponse<T>> {
  const { data } = await apiClient.put(url, body)
  return data
}

export async function del<T>(url: string): Promise<ApiResponse<T>> {
  const { data } = await apiClient.delete(url)
  return data
}

export default apiClient
