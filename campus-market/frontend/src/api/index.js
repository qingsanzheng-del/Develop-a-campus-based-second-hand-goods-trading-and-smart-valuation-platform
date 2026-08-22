import axios from 'axios'
import { toast } from '../utils/toast'

const api = axios.create({ baseURL: '/api', timeout: 120000 })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const detail = err.response?.data?.detail
    const msg = typeof detail === 'string' ? detail : err.message || '请求失败'
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.dispatchEvent(new Event('app:unauthorized'))
    }
    toast(msg, 'error')
    return Promise.reject(err)
  }
)

export default api
