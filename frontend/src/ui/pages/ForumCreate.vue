<template>
  <div class="forum-create-container">
    <!-- 顶部导航栏 -->
    <div class="create-header">
      <van-icon name="arrow-left" size="20" @click="goBack" />
      <h1>发布话题</h1>
      <div style="width: 20px;"></div>
    </div>

    <form @submit.prevent="handleSubmit" class="create-form">
      <!-- 标题输入 -->
      <div class="form-group">
        <label class="required">话题标题</label>
        <van-field
          v-model="formData.title"
          placeholder="请输入话题标题"
          maxlength="100"
          show-word-limit
        />
      </div>

      <!-- 内容编辑 -->
      <div class="form-group">
        <label class="required">话题内容</label>
        <van-field
          v-model="formData.content"
          type="textarea"
          placeholder="分享你的想法..."
          rows="10"
          autosize
          show-word-limit
          maxlength="5000"
        />
      </div>

      <!-- 提交按钮 -->
      <div class="form-actions">
        <van-button 
          type="primary" 
          @click="handleSubmit"
          :loading="submitting"
          color="#64A386"
          block
        >
          发布话题
        </van-button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createForumPost } from '@/api/work'
import { showToast } from 'vant'

const router = useRouter()

// 表单数据
const formData = ref({
  title: '',
  content: ''
})

// 提交状态
const submitting = ref(false)

// 提交表单
async function handleSubmit() {
  if (!formData.value.title.trim()) {
    showToast({ type: 'fail', message: '请输入话题标题' })
    return
  }
  
  if (!formData.value.content.trim()) {
    showToast({ type: 'fail', message: '请输入话题内容' })
    return
  }
  
  submitting.value = true
  
  try {
    await createForumPost({
      title: formData.value.title,
      content: formData.value.content
    })
    
    showToast({ type: 'success', message: '话题发布成功！' })
    
    // 跳转到论坛列表
    router.push('/forum')
  } catch (error: any) {
    console.error('发布失败:', error)
    const message = error.response?.data?.detail || '发布失败，请重试'
    showToast({ type: 'fail', message })
  } finally {
    submitting.value = false
  }
}

// 返回
function goBack() {
  if (formData.value.title || formData.value.content) {
    router.back()
  } else {
    router.back()
  }
}
</script>

<style scoped>
.forum-create-container {
  min-height: 100vh;
  background: transparent;
  padding-bottom: 20px;
}

/* 顶部导航栏 */
.create-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: rgba(250, 249, 246, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e8e8e8;
  position: sticky;
  top: 0;
  z-index: 10;
}

.create-header h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

/* 表单 */
.create-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.form-group label.required::after {
  content: ' *';
  color: #ee0a24;
}

/* 操作按钮 */
.form-actions {
  margin-top: 30px;
}

.form-actions :deep(.van-button) {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
}
</style>
