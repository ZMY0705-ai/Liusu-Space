<template>
  <div class="editor-container">
    <!-- 顶部导航栏 -->
    <div class="editor-header">
      <van-icon name="arrow-left" size="20" @click="goBack" />
      <h1>{{ isEdit ? '编辑作品' : '创作作品' }}</h1>
      <div style="width: 20px;"></div>
    </div>

    <form @submit.prevent class="editor-form">
      <!-- 封面上传 -->
      <div class="form-group">
        <label class="required">封面图片</label>
        <div class="cover-upload">
          <div v-if="previewUrl" class="cover-preview">
            <img :src="previewUrl" alt="封面预览" />
            <van-icon name="cross" @click="removeCover" class="remove-icon" />
          </div>
          <div v-else class="upload-placeholder" @click="triggerFileInput">
            <van-icon name="photograph" size="40" color="#999" />
            <p>点击上传封面</p>
          </div>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileChange"
            style="display: none"
          />
        </div>
      </div>

      <!-- 标题输入 -->
      <div class="form-group">
        <label class="required">作品标题</label>
        <van-field
          v-model="formData.title"
          placeholder="请输入作品标题"
          maxlength="100"
          show-word-limit
        />
      </div>

      <!-- 内容编辑 -->
      <div class="form-group">
        <label>正文内容</label>
        <van-field
          v-model="formData.content"
          type="textarea"
          placeholder="开始你的创作..."
          rows="10"
          autosize
          show-word-limit
          maxlength="10000"
        />
      </div>

      <!-- 底部按钮 -->
      <div class="form-actions">
        <!-- 编辑模式：三个按钮 -->
        <template v-if="isEdit">
          <van-button 
            type="default" 
            @click="handleSaveDraft"
            :loading="submitting"
          >
            储存草稿
          </van-button>
          <van-button 
            type="primary" 
            @click="handleSaveWork"
            :loading="submitting"
            color="#BCDDBE"
          >
            保存作品
          </van-button>
          <van-button 
            type="primary" 
            @click="handlePublish"
            :loading="submitting"
            color="#64A386"
          >
            发表作品
          </van-button>
        </template>
        
        <!-- 新建-储存作品模式 -->
        <template v-else-if="entryMode === 'draft'">
          <van-button 
            type="default" 
            @click="handleSaveDraft"
            :loading="submitting"
          >
            保存草稿
          </van-button>
          <van-button 
            type="primary" 
            @click="handleSaveWork"
            :loading="submitting"
            color="#64A386"
          >
            保存作品
          </van-button>
        </template>
        
        <!-- 新建-发表作品模式 -->
        <template v-else-if="entryMode === 'publish'">
          <van-button 
            type="default" 
            @click="handleSaveDraft"
            :loading="submitting"
          >
            储存草稿
          </van-button>
          <van-button 
            type="primary" 
            @click="handlePublish"
            :loading="submitting"
            color="#64A386"
          >
            发表作品
          </van-button>
        </template>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { createWork, updateWork, uploadCover, getWorkById } from '@/api/work'
import { showToast, showDialog } from 'vant'

const router = useRouter()
const route = useRoute()

// 是否为编辑模式
const isEdit = computed(() => !!route.params.id)
const workId = computed(() => route.params.id ? Number(route.params.id) : null)

// 进入模式：'draft'（储存作品）或 'publish'（发表作品）
const entryMode = computed(() => {
  const mode = route.query.mode as string
  return mode === 'draft' || mode === 'publish' ? mode : 'publish'
})

// 表单数据
const formData = ref({
  title: '',
  content: '',
  cover_image: null as string | null,
  status: 1 // 1: 发布, 0: 草稿
})

// 文件相关
const fileInput = ref<HTMLInputElement | null>(null)
const previewUrl = ref<string>('')
const selectedFile = ref<File | null>(null)

// 提交状态
const submitting = ref(false)

// 触发文件选择
function triggerFileInput() {
  fileInput.value?.click()
}

// 处理文件选择
async function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    showToast({ type: 'fail', message: '请选择图片文件' })
    return
  }
  
  // 验证文件大小（最大5MB）
  if (file.size > 5 * 1024 * 1024) {
    showToast({ type: 'fail', message: '图片大小不能超过5MB' })
    return
  }
  
  selectedFile.value = file
  
  // 创建预览URL
  previewUrl.value = URL.createObjectURL(file)
}

// 移除封面
function removeCover() {
  previewUrl.value = ''
  selectedFile.value = null
  formData.value.cover_image = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 上传封面
async function uploadCoverImage(): Promise<string | null> {
  if (!selectedFile.value) {
    return formData.value.cover_image
  }
  
  try {
    const response = await uploadCover(selectedFile.value)
    // Axios响应结构: response.data 是后端返回的数据
    return response.data.url
  } catch (error) {
    console.error('上传封面失败:', error)
    showToast({ type: 'fail', message: '上传封面失败,请重试' })
    return null
  }
}

// 提交表单
async function handleSubmit(isPublished: boolean = false) {
  if (!formData.value.title.trim()) {
    showToast({ type: 'fail', message: '请输入作品标题' })
    return
  }
  
  if (!formData.value.content.trim()) {
    showToast({ type: 'fail', message: '请输入作品内容' })
    return
  }
  
  submitting.value = true
  
  try {
    // 先上传封面（如果有）
    let coverUrl = formData.value.cover_image
    if (selectedFile.value) {
      coverUrl = await uploadCoverImage()
      if (!coverUrl) {
        submitting.value = false
        return
      }
    }
    
    // 提交作品数据
    const workData = {
      title: formData.value.title,
      content: formData.value.content,
      cover_image: coverUrl,
      status: formData.value.status,
      is_published: isPublished  // 由调用者决定是否发表
    }
    
    if (isEdit.value && workId.value) {
      // 编辑模式
      await updateWork(workId.value, workData)
      showToast({ type: 'success', message: '作品更新成功！' })
    } else {
      // 创建模式
      const response = await createWork(workData)
      console.log('创建作品成功:', response.data)
      showToast({ type: 'success', message: isPublished ? '作品发表成功！' : (formData.value.status === 1 ? '作品保存成功！' : '草稿保存成功！') })
    }
    
    // 根据状态决定跳转位置
    if (isPublished && formData.value.status === 1) {
      // 发表作品跳转到首页并强制刷新
      router.push({ path: '/home', query: { refresh: Date.now().toString() } })
    } else if (formData.value.status === 0) {
      // 保存草稿跳转到“我的”页面的草稿标签
      router.push({ path: '/me', query: { tab: 'drafts' } })
    } else {
      // 保存作品跳转到“我的”页面的作品标签
      router.push({ path: '/me', query: { tab: 'works' } })
    }
  } catch (error: any) {
    console.error('提交失败:', error)
    const message = error.response?.data?.detail || '提交失败，请重试'
    showToast({ type: 'fail', message })
  } finally {
    submitting.value = false
  }
}

// 加载作品数据（编辑模式）
async function loadWorkData() {
  if (!isEdit.value || !workId.value) return
  
  try {
    const response = await getWorkById(workId.value)
    const work = response.data
    
    formData.value = {
      title: work.title,
      content: work.content,
      cover_image: work.cover_image,
      status: work.status
    }
    
    // 设置封面预览
    if (work.cover_image) {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
      previewUrl.value = work.cover_image.startsWith('http') 
        ? work.cover_image 
        : `${baseUrl}${work.cover_image}`
    }
  } catch (error) {
    console.error('加载作品失败:', error)
    showToast({ type: 'fail', message: '加载作品失败' })
    router.push('/home')
  }
}

// 返回
function goBack() {
  if (formData.value.title || formData.value.content) {
    showDialog({
      title: '提示',
      message: '有未保存的内容，确定要离开吗？',
    }).then(() => {
      router.back()
    }).catch(() => {
      // 取消离开
    })
  } else {
    router.back()
  }
}

// 保存草稿（status=0，私密保存）
async function handleSaveDraft() {
  formData.value.status = 0
  await handleSubmit(false)  // is_published=false
}

// 保存作品（status=1，公开到我的作品，但不在首页显示）
async function handleSaveWork() {
  formData.value.status = 1
  await handleSubmit(false)  // is_published=false
}

// 发表作品（status=1，公开到首页和我的作品）
async function handlePublish() {
  formData.value.status = 1
  await handleSubmit(true)  // is_published=true
}

// 初始化
onMounted(() => {
  loadWorkData()
})
</script>

<style scoped>
.editor-container {
  min-height: 100vh;
  background: transparent;
  padding-bottom: 80px;
}

/* 头部 */
.editor-header {
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

.editor-header h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

/* 表单 */
.editor-form {
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

/* 封面上传 */
.cover-upload {
  margin-top: 8px;
}

.cover-preview {
  position: relative;
  width: 100%;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #64A386;
}

.cover-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.remove-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.upload-placeholder {
  width: 100%;
  height: 200px;
  border: 2px dashed #e8e8e8;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.upload-placeholder:active {
  border-color: #64A386;
  background: #FBFCCD;
}

.upload-placeholder p {
  font-size: 14px;
  color: #999;
  margin-top: 8px;
}

/* 操作按钮 */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 30px;
}

.form-actions :deep(.van-button) {
  flex: 1;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
}

.form-actions :deep(.van-button--default) {
  background: #BCDDBE;
  border: none;
  color: var(--text-primary);
}

.form-actions :deep(.van-button--primary) {
  background: #64A386;
  border: none;
}
</style>
