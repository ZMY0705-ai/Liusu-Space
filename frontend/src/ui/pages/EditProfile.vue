<template>
  <div class="edit-profile-container">
    <!-- 顶部导航栏 -->
    <van-nav-bar
      title="编辑资料"
      left-arrow
      @click-left="handleBack"
    >
      <template #right>
        <span class="save-btn" @click="handleSave">保存</span>
      </template>
    </van-nav-bar>

    <!-- 表单内容 -->
    <div class="form-content">
      <!-- 头像上传 -->
      <div class="avatar-section">
        <div class="avatar-wrapper" @click="triggerFileInput">
          <img 
            v-if="previewAvatar || userForm.avatar" 
            :src="getFullAvatarUrl(previewAvatar || userForm.avatar)" 
            class="avatar-img"
            alt="头像"
          />
          <div v-else class="avatar-placeholder">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div class="avatar-overlay">
            <van-icon name="camera-o" size="24" color="#fff" />
          </div>
        </div>
        <p class="avatar-tip">点击更换头像</p>
        <input 
          ref="fileInput" 
          type="file" 
          accept="image/jpeg,image/png,image/webp" 
          style="display: none"
          @change="handleFileChange"
        />
      </div>

      <!-- 昵称 -->
      <van-field
        v-model="userForm.nickname"
        label="昵称"
        placeholder="请输入昵称"
        maxlength="30"
        show-word-limit
        required
      />

      <!-- 个性签名 -->
      <van-field
        v-model="userForm.bio"
        type="textarea"
        label="个性签名"
        placeholder="用一句话定义自己..."
        maxlength="150"
        show-word-limit
        rows="3"
        autosize
      />

      <!-- 真实姓名 -->
      <van-field
        v-model="userForm.real_name"
        label="真实姓名"
        placeholder="选填"
        maxlength="20"
      />

      <!-- 专业/学院 -->
      <van-field
        v-model="userForm.major"
        label="专业/学院"
        placeholder="选填"
        maxlength="50"
      />

      <!-- 隐私设置 -->
      <div class="privacy-section">
        <h3 class="section-title">隐私设置</h3>
        
        <van-cell-group inset>
          <van-cell center title="公开我的真实姓名">
            <template #right-icon>
              <van-switch 
                v-model="userForm.is_real_name_public" 
                size="24"
                active-color="#64A386"
              />
            </template>
          </van-cell>
          
          <van-cell center title="公开我的专业/学院">
            <template #right-icon>
              <van-switch 
                v-model="userForm.is_major_public" 
                size="24"
                active-color="#64A386"
              />
            </template>
          </van-cell>
        </van-cell-group>
        
        <p class="privacy-tip">关闭后，其他用户将无法看到您的这些信息</p>
      </div>
    </div>

    <!-- 加载遮罩 -->
    <van-loading v-if="saving" class="loading-overlay" vertical>
      保存中...
    </van-loading>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { updateUser, uploadAvatar } from '@/api/user'
import { showToast } from 'vant'
import type { UserUpdate } from '@/types/api'

const router = useRouter()
const authStore = useAuthStore()

// 表单数据
const userForm = ref<UserUpdate>({
  nickname: '',
  avatar: '',
  bio: '',
  real_name: '',
  major: '',
  is_real_name_public: false,
  is_major_public: false
})

// 预览头像（本地临时URL）
const previewAvatar = ref<string>('')

// 文件输入引用
const fileInput = ref<HTMLInputElement>()

// 保存状态
const saving = ref(false)

// 获取完整头像URL
const getFullAvatarUrl = (url: string | undefined) => {
  if (!url) return ''
  // 如果是相对路径，拼接后端地址
  if (url.startsWith('/')) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${url}`
  }
  return url
}

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileChange = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  // 验证文件大小（2MB）
  const maxSize = 2 * 1024 * 1024
  if (file.size > maxSize) {
    showToast({ type: 'fail', message: '图片大小不能超过2MB' })
    return
  }
  
  // 验证文件类型
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    showToast({ type: 'fail', message: '仅支持 JPG、PNG、WEBP 格式' })
    return
  }
  
  try {
    showToast({ type: 'loading', message: '上传中...', duration: 0 })
    
    // 上传头像
    const response = await uploadAvatar(file)
    
    // 更新表单中的头像URL
    userForm.value.avatar = response.avatar_url
    
    // 生成本地预览URL
    previewAvatar.value = URL.createObjectURL(file)
    
    showToast({ type: 'success', message: '头像上传成功' })
  } catch (error: any) {
    console.error('头像上传失败:', error)
    showToast({ 
      type: 'fail', 
      message: error.detail || '头像上传失败' 
    })
  }
}

// 返回上一页
const handleBack = () => {
  router.back()
}

// 保存资料
const handleSave = async () => {
  // 验证必填项
  if (!userForm.value.nickname || userForm.value.nickname.trim() === '') {
    showToast({ type: 'fail', message: '昵称不能为空' })
    return
  }
  
  saving.value = true
  
  try {
    await updateUser(userForm.value)
    
    // 更新 Pinia store 中的用户信息
    await authStore.fetchUser()
    
    showToast({ type: 'success', message: '保存成功' })
    
    // 延迟返回，让用户看到提示
    setTimeout(() => {
      router.back()
    }, 1000)
  } catch (error: any) {
    console.error('保存失败:', error)
    showToast({ 
      type: 'fail', 
      message: error.detail || '保存失败，请重试' 
    })
  } finally {
    saving.value = false
  }
}

// 初始化表单数据
onMounted(() => {
  const user = authStore.user
  if (user) {
    userForm.value = {
      nickname: user.nickname || '',
      avatar: user.avatar || '',
      bio: user.bio || '',
      real_name: user.real_name || '',
      major: user.major || '',
      is_real_name_public: user.is_real_name_public || false,
      is_major_public: user.is_major_public || false
    }
  }
})
</script>

<style scoped>
.edit-profile-container {
  min-height: 100vh;
  background: transparent;
}

/* 保存按钮 */
.save-btn {
  color: white;
  font-size: 15px;
  font-weight: 600;
  padding: 4px 12px;
  background: var(--matcha-green);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn:active {
  opacity: 0.8;
  transform: scale(0.95);
}

/* 表单内容 */
.form-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 16px;
}

/* 头像区域 */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 0;
  background: linear-gradient(135deg, rgba(100, 163, 134, 0.1), rgba(188, 221, 190, 0.1));
  border-radius: 20px;
  margin-bottom: 20px;
}

.avatar-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(100, 163, 134, 0.2);
  transition: all 0.3s;
}

.avatar-wrapper:active {
  transform: scale(0.95);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: var(--matcha-green);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40px;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.avatar-tip {
  margin-top: 12px;
  font-size: 14px;
  color: var(--text-secondary);
}

/* 隐私设置区域 */
.privacy-section {
  margin-top: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--ink-dark);
  margin: 0 0 12px 8px;
  padding-left: 8px;
  border-left: 3px solid var(--lemon-yellow);
}

.privacy-tip {
  font-size: 12px;
  color: var(--text-light);
  margin-top: 12px;
  padding: 0 8px;
}

/* 加载遮罩 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
</style>
