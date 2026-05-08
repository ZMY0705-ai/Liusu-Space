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
