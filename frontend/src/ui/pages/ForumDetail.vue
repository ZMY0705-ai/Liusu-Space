<template>
  <div class="forum-detail-container">
    <!-- 顶部导航栏 -->
    <div class="detail-header">
      <van-icon name="arrow-left" size="20" @click="goBack" />
      <h1>帖子详情</h1>
      <div style="width: 20px;"></div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <van-loading type="spinner" size="24px" color="#64A386" />
      <p>加载中...</p>
    </div>

    <!-- 帖子详情内容 -->
    <div v-else-if="post" class="post-content">
      <!-- 帖子信息 -->
      <div class="post-info">
        <h2 class="post-title">{{ post.title }}</h2>
        
        <!-- 作者信息 -->
        <div class="author-section">
          <div class="author-avatar">
            {{ getAuthorInitial(post.author?.nickname || 'U') }}
          </div>
          <div class="author-details">
            <span class="author-name">{{ post.author?.nickname || '匿名' }}</span>
            <span class="publish-time">{{ formatTime(post.created_at) }}</span>
          </div>
        </div>

        <!-- 帖子内容 -->
        <div class="post-body">
          <div class="content-text" v-html="formatContent(post.content)"></div>
        </div>
      </div>

      <!-- 回复区 -->
      <CommentSection :target-id="postId" target-type="post" />
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-state">
      <p>帖子不存在或已被删除</p>
      <van-button type="primary" @click="goBack" color="#64A386">
        返回论坛
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getForumPostById } from '@/api/work'
import { showToast } from 'vant'
import CommentSection from '@/ui/components/CommentSection.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 帖子ID
const postId = computed(() => Number(route.params.id))

// 数据状态
const post = ref<any>(null)
const loading = ref(false)

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

// 加载帖子详情
async function loadPostDetail() {
  loading.value = true
  try {
    const response = await getForumPostById(postId.value)
    post.value = response.data
  } catch (error) {
    console.error('加载帖子失败:', error)
    showToast({ type: 'fail', message: '加载帖子失败' })
  } finally {
    loading.value = false
  }
}

// 返回
function goBack() {
  router.back()
}

// 初始化
onMounted(() => {
  loadPostDetail()
})
</script>

<style scoped>
.forum-detail-container {
  min-height: 100vh;
  background: transparent;
  padding-bottom: 20px;
}

/* 顶部导航栏 */
.detail-header {
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

.detail-header h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
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

/* 帖子信息 */
.post-info {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 20px;
}

.post-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
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
  border-bottom: 1px solid #f0f0f0;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--light-green);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
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
  color: var(--green-primary);
}

.publish-time {
  font-size: 13px;
  color: var(--text-light);
}

/* 帖子内容 */
.post-body {
  margin-top: 20px;
}

.content-text {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 回复区 */
.comments-section {
  margin-top: 30px;
  padding: 20px;
  background: white;
  border-top: 1px solid #f0f0f0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}

/* 回复列表 */
.comments-list {
  margin-bottom: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--light-green);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.comment-content {
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
  font-weight: 500;
  color: var(--green-primary);
}

.comment-time {
  font-size: 12px;
  color: var(--text-light);
}

.comment-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-primary);
  margin: 0;
}

/* 空回复状态 */
.empty-comments {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.empty-comments p {
  font-size: 14px;
}

/* 回复输入区 */
.comment-input-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.comment-input-section :deep(.van-field) {
  padding: 0;
  background: transparent;
}

.comment-input-section :deep(.van-button) {
  margin-top: 12px;
  height: 40px;
  font-size: 14px;
}
</style>
