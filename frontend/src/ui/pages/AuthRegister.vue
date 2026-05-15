<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title"> 流俗地</h1>
        <p class="auth-subtitle">开启你的文学创作之旅</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
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
          <label class="form-label">确认密码 *</label>
          <input 
            v-model="registerForm.confirmPassword"
            type="password" 
            class="form-input" 
            placeholder="请再次输入密码"
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

        <div class="auth-switch">
          已有账号？
          <router-link to="/login" class="auth-switch-link">去登录</router-link>
        </div>
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

const message = ref('')
const messageType = ref('')

const registerForm = reactive({
  account: '',
  password: '',
  confirmPassword: '',
  nickname: '',
  real_name: '',
  student_id: '',
  major: ''
})

const handleRegister = async () => {
  message.value = ''
  
  if (registerForm.password.length < 6) {
    message.value = '密码长度至少为6位'
    messageType.value = 'error'
    return
  }
  
  if (registerForm.password !== registerForm.confirmPassword) {
    message.value = '两次密码输入不一致'
    messageType.value = 'error'
    return
  }
  
  const result = await authStore.registerAction({
    account: registerForm.account,
    password: registerForm.password,
    nickname: registerForm.nickname,
    real_name: registerForm.real_name || undefined,
    student_id: registerForm.student_id || undefined,
    major: registerForm.major || undefined
  })
  
  if (result.success) {
    message.value = result.message
    messageType.value = 'success'
    
    // 注册成功后跳转到登录页
    setTimeout(() => {
      router.push('/login')
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
  background: transparent;
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

.auth-switch {
  text-align: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.auth-switch-link {
  color: var(--green-primary);
  font-weight: 500;
  text-decoration: none;
}

.auth-switch-link:hover {
  text-decoration: underline;
}
</style>
