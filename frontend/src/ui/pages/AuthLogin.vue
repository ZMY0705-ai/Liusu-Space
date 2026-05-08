<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title"> 流俗地</h1>
        <p class="auth-subtitle">校园文学创作平台</p>
      </div>

      <div class="auth-tabs">
        <div 
          class="auth-tab" 
          :class="{ active: activeTab === 'login' }"
          @click="activeTab = 'login'"
        >
          登录
        </div>
        <div 
          class="auth-tab" 
          :class="{ active: activeTab === 'register' }"
          @click="activeTab = 'register'"
        >
          注册
        </div>
      </div>

      <!-- 登录表单 -->
      <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="form-label">账号</label>
          <input 
            v-model="loginForm.account"
            type="text" 
            class="form-input" 
            placeholder="请输入账号"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <input 
            v-model="loginForm.password"
            type="password" 
            class="form-input" 
            placeholder="请输入密码"
            required
          />
        </div>

        <button 
          type="submit" 
          class="btn btn-primary" 
          :disabled="authStore.isLoading"
        >
          {{ authStore.isLoading ? '登录中...' : '登录' }}
        </button>

        <p v-if="message" :class="['message', messageType]">{{ message }}</p>
      </form>

      <!-- 注册表单 -->
      <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label class="form-label">账号 *</label>
          <input 
            v-model="registerForm.account"
            type="text" 
            class="form-input" 
            placeholder="请输入账号"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">密码 *</label>
          <input 
            v-model="registerForm.password"
            type="password" 
            class="form-input" 
            placeholder="请输入密码（至少6位）"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">昵称 *</label>
          <input 
            v-model="registerForm.nickname"
            type="text" 
            class="form-input" 
            placeholder="请输入昵称"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label">姓名</label>
          <input 
            v-model="registerForm.real_name"
            type="text" 
            class="form-input" 
            placeholder="请输入真实姓名（可选）"
          />
        </div>

        <div class="form-group">
          <label class="form-label">学号</label>
          <input 
            v-model="registerForm.student_id"
            type="text" 
            class="form-input" 
            placeholder="请输入学号（可选）"
          />
        </div>

        <div class="form-group">
          <label class="form-label">专业</label>
          <input 
            v-model="registerForm.major"
            type="text" 
            class="form-input" 
            placeholder="请输入专业（可选）"
          />
        </div>

        <button 
          type="submit" 
          class="btn btn-primary" 
          :disabled="authStore.isLoading"
        >
          {{ authStore.isLoading ? '注册中...' : '注册' }}
        </button>

        <p v-if="message" :class="['message', messageType]">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('login')
const message = ref('')
const messageType = ref('')

const loginForm = reactive({
  account: '',
  password: ''
})

const registerForm = reactive({
  account: '',
  password: '',
  nickname: '',
  real_name: '',
  student_id: '',
  major: ''
})

const handleLogin = async () => {
  message.value = ''
  const result = await authStore.loginAction(loginForm)
  
  if (result.success) {
    message.value = result.message
    messageType.value = 'success'
    
    // 登录成功后跳转到首页或重定向页面
    setTimeout(() => {
      const redirect = router.currentRoute.value.query.redirect as string
      router.push(redirect || '/home')
    }, 500)
  } else {
    message.value = result.message
    messageType.value = 'error'
  }
}

const handleRegister = async () => {
  message.value = ''
  
  if (registerForm.password.length < 6) {
    message.value = '密码长度至少为6位'
    messageType.value = 'error'
    return
  }
  
  const result = await authStore.registerAction(registerForm)
  
  if (result.success) {
    message.value = result.message
    messageType.value = 'success'
    
    // 注册成功后切换到登录表单
    setTimeout(() => {
      activeTab.value = 'login'
      loginForm.account = registerForm.account
      message.value = ''
    }, 1000)
  } else {
    message.value = result.message
    messageType.value = 'error'
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.auth-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-size: 32px;
  color: var(--green-primary);
  margin-bottom: 8px;
}

.auth-subtitle {
  font-size: 14px;
  color: var(--text-light);
}

.auth-tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 2px solid var(--border-color);
}

.auth-tab {
  flex: 1;
  padding: 12px;
  text-align: center;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  color: var(--text-light);
  transition: all 0.3s ease;
  position: relative;
}

.auth-tab.active {
  color: var(--green-primary);
}

.auth-tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--green-primary);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
}

.form-input {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
  background: var(--paper-bg);
}

.form-input:focus {
  outline: none;
  border-color: var(--green-primary);
  background: white;
  box-shadow: 0 0 0 3px rgba(100, 163, 134, 0.1);
}

.btn {
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--green-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #5a9478;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 163, 134, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  text-align: center;
  font-size: 14px;
  padding: 10px;
  border-radius: 8px;
}

.message.success {
  background: #e8f5e9;
  color: #2e7d32;
}

.message.error {
  background: #ffebee;
  color: #c62828;
}
</style>
