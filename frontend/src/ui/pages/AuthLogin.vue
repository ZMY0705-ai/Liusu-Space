<template>
  <div class="auth-container">
    <!-- 几何波浪背景 -->
    <div class="wave-background">
      <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="#85AD8A" fill-opacity="1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
      <svg viewBox="0 0 1440 320" preserveAspectRatio="none" class="wave-2">
        <path fill="#FCE48D" fill-opacity="0.6" d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
    </div>

    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title">流俗地</h1>
        <p class="auth-subtitle">在文字的世界里，遇见更好的自己</p>
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
  position: relative;
  overflow: hidden;
}

.wave-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 35%;
  z-index: 0;
}

.wave-background svg {
  position: absolute;
  width: 100%;
  height: 100%;
}

.wave-2 {
  opacity: 0.8;
  transform: translateY(20px);
}

.auth-card {
  background: var(--pure-white);
  border-radius: 24px;
  padding: 40px 30px;
  width: 100%;
  max-width: 420px;
  box-shadow: var(--shadow-soft);
  position: relative;
  z-index: 1;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-size: 36px;
  color: var(--matcha-green);
  margin-bottom: 8px;
  letter-spacing: 2px;
}

.auth-subtitle {
  font-size: 14px;
  color: var(--text-light);
}

.auth-tabs {
  display: flex;
  margin-bottom: 30px;
  background: #F5F5F5;
  border-radius: 12px;
  padding: 4px;
}

.auth-tab {
  flex: 1;
  padding: 10px;
  text-align: center;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all 0.3s ease;
  border-radius: 8px;
}

.auth-tab.active {
  background: var(--pure-white);
  color: var(--matcha-green);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
  padding: 14px 16px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.2s ease;
  background: #FAFAFA;
}

.form-input:focus {
  outline: none;
  border-color: var(--matcha-green);
  background: var(--pure-white);
  box-shadow: 0 0 0 4px rgba(133, 173, 138, 0.1);
}

.btn {
  padding: 14px;
  border: none;
  border-radius: 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--matcha-green);
  color: white;
  box-shadow: 0 4px 12px rgba(133, 173, 138, 0.3);
}

.btn-primary:hover:not(:disabled) {
  background: #769e7b;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  text-align: center;
  font-size: 14px;
  padding: 10px;
  border-radius: 12px;
}

.message.success {
  background: #E8F5E9;
  color: #2E7D32;
}

.message.error {
  background: #FFEBEE;
  color: #C62828;
}
</style>
