<template>
  <div class="work-card" @click="handleClick">
    <!-- 封面图片 -->
    <div v-if="work.cover_image" class="card-cover">
      <img :src="getCoverUrl(work.cover_image)" :alt="work.title" />
    </div>
    <div v-else class="card-cover card-cover-placeholder">
      <span>📖</span>
    </div>

    <!-- 内容区域 -->
    <div class="card-content">
      <h3 class="card-title">{{ work.title }}</h3>
      
      <p class="card-excerpt">{{ getExcerpt(work.content) }}</p>
      
      <!-- 作者信息 -->
      <div class="card-author">
        <div class="author-avatar">
          {{ getAuthorInitial(work.author?.nickname || 'A') }}
        </div>
        <div class="author-info">
          <span class="author-name">{{ work.author?.nickname || '匿名' }}</span>
          <span class="publish-time">{{ formatTime(work.created_at) }}</span>
        </div>
      </div>

      <!-- 统计数据 -->
      <div class="card-stats">
        <span class="stat-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          {{ work.view_count || 0 }}
        </span>
        <span class="stat-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
          {{ work.like_count || 0 }}
        </span>
        <span class="stat-item">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          {{ work.favorite_count || 0 }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Work } from '@/types/api'

const props = defineProps<{
  work: Work
}>()

const emit = defineEmits<{
  click: [workId: number]
}>()

// 获取封URL
const getCoverUrl = (coverImage: string | null) => {
  if (!coverImage) return ''
  // 如果是完整URL直接返回，否则拼接后端地址
  if (coverImage.startsWith('http')) {
    return coverImage
  }
  // 使用环境变量或默认值
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
  return `${baseUrl}${coverImage}`
}

// 获取摘要（截取前100字符）
const getExcerpt = (content: string) => {
  if (!content) return ''
  const text = content.replace(/<[^>]*>/g, '') // 去除HTML标签
  return text.length > 100 ? text.substring(0, 100) + '...' : text
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

// 点击事件
const handleClick = () => {
  emit('click', props.work.id)
}
</script>

<style scoped>
.work-card {
  background: var(--pure-white);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow-soft);
  transition: all 0.3s;
  cursor: pointer;
  margin-bottom: 20px;
}

.work-card:active {
  transform: scale(0.98);
}

/* 封面图片 */
.card-cover {
  width: 100%;
  height: 180px;
  overflow: hidden;
  position: relative;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--light-matcha), #CDE2EB);
  font-size: 48px;
}

/* 内容区域 */
.card-content {
  padding: 20px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-dark);
  margin-bottom: 10px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-excerpt {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 作者信息 */
.card-author {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--matcha-green);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.author-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--matcha-green);
}

.publish-time {
  font-size: 12px;
  color: var(--text-light);
}

/* 统计数据 */
.card-stats {
  display: flex;
  gap: 20px;
  padding-top: 12px;
  border-top: 1px solid #F5F5F5;
}

.stat-item {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-item svg {
  color: var(--matcha-green);
}
</style>
