import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/api'
import { login, register, getCurrentUser } from '@/api/user'
import type { LoginRequest, RegisterRequest } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string>(localStorage.getItem('access_token') || '')
  const isLoading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)

  // 方法
  // 登录
  async function loginAction(loginData: LoginRequest) {
    isLoading.value = true
    try {
      const response = await login(loginData)
      token.value = response.data.access_token
      localStorage.setItem('access_token', token.value)
      
      // 获取用户信息
      await fetchUser()
      
      return { success: true, message: '登录成功' }
    } catch (error: any) {
      const message = error.response?.data?.detail || '登录失败，请检查账号密码'
      return { success: false, message }
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  async function registerAction(registerData: RegisterRequest) {
    isLoading.value = true
    try {
      await register(registerData)
      return { success: true, message: '注册成功，请登录' }
    } catch (error: any) {
      const message = error.response?.data?.detail || '注册失败'
      return { success: false, message }
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户信息
  async function fetchUser() {
    try {
      const response = await getCurrentUser()
      user.value = response.data
      localStorage.setItem('user_info', JSON.stringify(user.value))
      return true
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return false
    }
  }

  // 登出
  function logout() {
    user.value = null
    token.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
  }

  // 初始化 - 从本地存储恢复状态
  function initAuth() {
    const savedToken = localStorage.getItem('access_token')
    const savedUser = localStorage.getItem('user_info')
    
    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
    }
  }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    loginAction,
    registerAction,
    fetchUser,
    logout,
    initAuth
  }
})
