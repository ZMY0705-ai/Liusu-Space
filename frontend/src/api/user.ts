import { post, get, put } from '@/api/http'
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  User,
  UserUpdate
} from '@/types/api'

// 用户登录
export function login(data: LoginRequest) {
  return post<LoginResponse>('/users/login', data)
}

// 用户注册
export function register(data: RegisterRequest) {
  return post<User>('/users/register', data)
}

// 获取当前用户信息
export function getCurrentUser() {
  return get<User>('/users/me')
}

// 更新用户信息
export function updateUser(data: UserUpdate) {
  return put<User>('/users/me', data)
}

// 上传头像
export function uploadAvatar(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  
  // 获取 token（注意：实际存储的 key 是 'access_token'）
  const token = localStorage.getItem('access_token')
  console.log('[上传头像] Token:', token ? `${token.substring(0, 20)}...` : 'null')
  
  if (!token) {
    return Promise.reject({ detail: '未登录，请先登录' })
  }
  
  // 使用原生 fetch 以支持 multipart/form-data
  return fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/users/avatar`, {
    method: 'POST',
    headers: {
      // 注意：不要手动设置 Content-Type，浏览器会自动添加 boundary
      'Authorization': `Bearer ${token}`
    },
    body: formData
  }).then(response => {
    console.log('[上传头像] 响应状态:', response.status)
    if (!response.ok) {
      return response.json().then(err => {
        console.error('[上传头像] 错误详情:', err)
        return Promise.reject(err)
      })
    }
    return response.json()
  })
}
