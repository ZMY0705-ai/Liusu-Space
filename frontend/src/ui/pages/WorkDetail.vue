<template>
  <div class="work-detail-container">
    <!-- 顶部导航栏 -->
    <div class="detail-header">
      <van-icon name="arrow-left" size="20" @click="goBack" />
      <h1>作品详情</h1>
      <div v-if="canEdit" class="header-actions">
        <van-icon name="edit" size="20" @click="handleEdit" />
      </div>
      <div v-else style="width: 20px;"></div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <van-loading type="spinner" size="24px" color="#64A386" />
      <p>加载中...</p>
    </div>

    <!-- 作品详情内容 -->
    <div v-else-if="work" class="work-content">
      <!-- 封面图片 -->
      <div v-if="work.cover_image" class="work-cover">
        <img :src="getCoverUrl(work.cover_image)" :alt="work.title" />
      </div>

      <!-- 作品信息 -->
      <div class="work-info">
        <h2 class="work-title">{{ work.title }}</h2>
        
        <!-- 作者信息 -->
        <div class="author-section">
          <div class="author-avatar" @click="goToAuthorProfile">
            {{ getAuthorInitial(work.author?.nickname || 'A') }}
          </div>
          <div class="author-details">
            <span class="author-name" @click="goToAuthorProfile">{{ work.author?.nickname || '匿名' }}</span>
            <span class="publish-time">{{ formatTime(work.created_at) }}</span>
          </div>
        </div>

        <!-- 统计数据 -->
        <div class="work-stats">
          <div class="stat-item">
            <van-icon name="eye-o" />
            <span>{{ work.view_count || 0 }}</span>
          </div>
          <div 
            class="stat-item clickable" 
            :class="{ active: isLiked }"
            @click="handleLike"
          >
            <van-icon :name="isLiked ? 'like' : 'like-o'" />
            <span>{{ work.like_count || 0 }}</span>
          </div>
          <div 
            class="stat-item clickable" 
            :class="{ active: isFavorited }"
            @click="handleFavorite"
          >
            <van-icon :name="isFavorited ? 'star' : 'star-o'" />
            <span>{{ work.favorite_count || 0 }}</span>
          </div>
        </div>

        <!-- 作品内容 -->
        <div class="work-body">
          <div class="content-text" v-html="formatContent(work.content)"></div>
        </div>
      </div>

      <!-- 评论区 -->
      <CommentSection :target-id="workId" target-type="work" />
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-state">
      <p>作品不存在或已被删除</p>
      <van-button type="primary" @click="goBack" color="#64A386">
        返回首页
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getWorkById, toggleLike, toggleFavorite, getInteractionStatus } from '@/api/work'
import { showToast } from 'vant'
import type { Work } from '@/types/api'
import CommentSection from '@/ui/components/CommentSection.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 作品ID
const workId = computed(() => Number(route.params.id))

// 数据状态
const work = ref<Work | null>(null)
const loading = ref(false)
const isLiked = ref(false)
const isFavorited = ref(false)

// 是否可以编辑（仅作者）
const canEdit = computed(() => {
  return authStore.isAuthenticated && work.value?.author_id === authStore.user?.id
})

// 获取封面URL
const getCoverUrl = (coverImage: string | null) => {
  if (!coverImage) return ''
  if (coverImage.startsWith('http')) {
    return coverImage
  }
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
  return `${baseUrl}${coverImage}`
}

// 获取作者首字母
const getAuthorInitial = (name: string) => {
  return name.charAt(0).toUpperCase()
}

// 格式化时间
const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 格式化内容（简单处理换行）
const formatContent = (content: string) => {
  if (!content) return ''
  // 将换行符转换为<br>
  return content.replace(/\n/g, '<br>')
}

// 加载作品详情
async function loadWorkDetail() {
  loading.value = true
  try {
    const response = await getWorkById(workId.value)
    work.value = response.data
    
    // 如果用户已登录，获取互动状态
    if (authStore.isAuthenticated) {
      await loadInteractionStatus()
    }
  } catch (error) {
    console.error('加载作品失败:', error)
    showToast({ type: 'fail', message: '加载作品失败' })
  } finally {
    loading.value = false
  }
}

// 加载用户互动状态
async function loadInteractionStatus() {
  try {
    const response = await getInteractionStatus(workId.value)
    const status = response.data
    isLiked.value = status.is_liked
    isFavorited.value = status.is_favorited
  } catch (error) {
    console.error('获取互动状态失败:', error)
  }
}

// 点赞/取消点赞
async function handleLike() {
  if (!authStore.isAuthenticated) {
    showToast({ type: 'fail', message: '请先登录' })
    router.push({ name: 'Login', query: { redirect: route.fullPath } })
    return
  }
  
  try {
    const response = await toggleLike(workId.value)
    const newCount = response.data.count
    
    // 更新点赞数和状态
    if (work.value) {
      work.value.like_count = newCount
      isLiked.value = !isLiked.value
    }
    
    showToast({ 
      type: 'success', 
      message: isLiked.value ? '点赞成功' : '取消点赞' 
    })
  } catch (error) {
    console.error('点赞失败:', error)
    showToast({ type: 'fail', message: '操作失败' })
  }
}

// 收藏/取消收藏
async function handleFavorite() {
  if (!authStore.isAuthenticated) {
    showToast({ type: 'fail', message: '请先登录' })
    router.push({ name: 'Login', query: { redirect: route.fullPath } })
    return
  }
  
  try {
    const response = await toggleFavorite(workId.value)
    const newCount = response.data.count
    
    // 更新收藏数和状态
    if (work.value) {
      work.value.favorite_count = newCount
      isFavorited.value = !isFavorited.value
    }
    
    showToast({ 
      type: 'success', 
      message: isFavorited.value ? '收藏成功' : '取消收藏' 
    })
  } catch (error) {
    console.error('收藏失败:', error)
    showToast({ type: 'fail', message: '操作失败' })
  }
}

// 编辑作品
function handleEdit() {
  router.push(`/editor/${workId.value}`)
}

// 跳转到作者主页
function goToAuthorProfile() {
  if (!work.value?.author?.id) return
  router.push(`/user/${work.value.author.id}`)
}

// 返回
function goBack() {
  router.back()
}

// 初始化
onMounted(() => {
  loadWorkDetail()
})
</script>

<style scoped>
.work-detail-container {
  min-height: 100vh;
  background: var(--paper-white);
  padding-bottom: 20px;
}

/* 顶部导航栏 */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #F5F5F5;
  position: sticky;
  top: 0;
  z-index: 10;
}

.detail-header h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-dark);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .van-icon {
  cursor: pointer;
  color: var(--matcha-green);
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 60px 0;
  color: var(--text-secondary);
}

.loading-state p {
  margin-top: 12px;
  font-size: 14px;
}

/* 错误状态 */
.error-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.error-state p {
  margin-bottom: 20px;
  font-size: 16px;
}

/* 作品封面 */
.work-cover {
  width: 100%;
  height: 240px;
  overflow: hidden;
}

.work-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 作品信息 */
.work-info {
  padding: 24px 20px;
  background: var(--pure-white);
  margin: 16px;
  border-radius: 20px;
  box-shadow: var(--shadow-soft);
}

.work-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--ink-dark);
  margin-bottom: 16px;
  line-height: 1.4;
}

/* 作者信息 */
.author-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #F5F5F5;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--matcha-green);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
  cursor: pointer;
  transition: all 0.2s;
}

.author-avatar:active {
  transform: scale(0.95);
  opacity: 0.8;
}

.author-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-name {
  font-size: 15px;
  font-weight: 500;
  color: var(--matcha-green);
  cursor: pointer;
  transition: all 0.2s;
}

.author-name:active {
  opacity: 0.7;
}

.publish-time {
  font-size: 13px;
  color: var(--text-light);
}

/* 统计数据 */
.work-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-item.clickable {
  cursor: pointer;
  transition: all 0.2s;
}

.stat-item.clickable:active {
  transform: scale(0.95);
}

.stat-item.active {
  color: var(--matcha-green);
}

.stat-item.active .van-icon {
  color: var(--matcha-green);
}

/* 作品内容 - 纸质书体验 */
.work-body {
  margin-top: 20px;
}

.content-text {
  font-family: 'Noto Serif SC', serif;
  font-size: 17px;
  line-height: 2;
  color: var(--ink-dark);
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 评论区 */
.comments-section {
  margin-top: 30px;
  padding: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-dark);
  margin-bottom: 20px;
  padding-left: 8px;
  border-left: 4px solid var(--lemon-yellow);
}

/* 评论列表 - 聊天气泡风格 */
.comments-list {
  margin-bottom: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--light-matcha);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.comment-bubble {
  background: var(--pure-white);
  padding: 12px 16px;
  border-radius: 16px;
  border-top-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.comment-author {
  font-size: 14px;
  font-weight: 600;
  color: var(--matcha-green);
}

.comment-time {
  font-size: 12px;
  color: var(--text-light);
}

.comment-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-primary);
  margin: 0;
}

/* 空评论状态 */
.empty-comments {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.empty-comments p {
  font-size: 14px;
}

/* 评论输入区 */
.comment-input-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #F5F5F5;
}

.comment-input-section :deep(.van-field) {
  padding: 0;
  background: transparent;
}

.comment-input-section :deep(.van-button) {
  margin-top: 12px;
  height: 44px;
  font-size: 15px;
  border-radius: 22px;
}
</style>
