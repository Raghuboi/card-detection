import axios, { AxiosError } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // You can add global error handling here
    return Promise.reject(error)
  }
)

export interface ServerError {
  detail: string
  message?: string
}

export function getErrorMessage(error: AxiosError<ServerError>) {
  const message = error.response?.data?.detail || error.response?.data?.message || error.message || 'An unexpected error occurred'
  return {
    message,
    description: error.response?.status ? `Status: ${error.response.status}` : undefined,
  }
}
