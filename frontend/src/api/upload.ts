import axios from 'axios'
import type { ApiResponse } from '@/types/api'

// Use direct backend URL for file uploads in dev (Vite proxy has issues with multipart)
// In production, this is handled by Nginx which properly proxies multipart requests
const baseURL = import.meta.env.DEV ? 'http://localhost:5000/api/v1' : '/api/v1'

export function uploadImage(file: File): Promise<ApiResponse<{ url: string }>> {
  const formData = new FormData()
  formData.append('file', file)

  const token = localStorage.getItem('access_token')
  return axios.post(`${baseURL}/upload/image`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  }).then(res => res.data)
}

export function deleteImage(filename: string): Promise<ApiResponse<null>> {
  const token = localStorage.getItem('access_token')
  return axios.delete(`${baseURL}/upload/image/${filename}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  }).then(res => res.data)
}
