<template>
  <div class="forum-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <h1 class="page-title">💬 校园论坛</h1>
    </div>

    <!-- 帖子列表 -->
    <div class="posts-section">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <van-loading type="spinner" size="24px" color="#64A386" />
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="posts.length === 0" class="empty-state">
        <p>暂无帖子，快来发表第一个话题吧！</p>
      </div>

      <!-- 帖子列表 -->
      <div v-else class="posts-list">
        <div 
          v-for="(post, index) in posts" 
          :key="post.id" 
          class="post-card"
          :class="index % 2 === 0 ? 'style-a' : 'style-b'"
          @click="handlePostClick(post.id)"
        >
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-excerpt">{{ getExcerpt(post.content) }}</p>
          
          <!-- 作者信息 -->
          <div class="post-author">
            <div class="author-avatar">
              {{ getAuthorInitial(post.author?.nickname || 'U') }}
            </div>
            <div class="author-info">
              <span class="author-name">{{ post.author?.nickname || '匿名' }}</span>
              <span class="post-time">{{ formatTime(post.created_at) }}</span>
            </div>
          </div>

          <!-- 统计数据 -->
          <div class="post-stats">
            <span class="stat-item">
              💬 {{ post.comment_count || 0 }} 回复
            </span>
          </div>
        </div>
      </div>

      <!-- 加载更多 -->
      <div v-if="hasMore && !loading" class="load-more">
        <van-button 
          type="default" 
          size="small"
          @click="loadMore" 
          :loading="loadingMore"
          loading-text="加载中..."
        >
          加载更多
        </van-button>
      </div>
    </div>

    <!-- 加号浮动按钮 -->
    <FabMenu />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getForumPosts } from '@/api/work'
import FabMenu from '@/ui/components/FabMenu.vue'

const router = useRouter()

// 帖子列表
const posts = ref<any[]>([])
const loading = ref(false)
const loadingMore = ref(false)
const skip = ref(0)
const limit = ref(10)
const hasMore = ref(true)

// 加载帖子列表
async function loadPosts(isLoadMore = false) {
  if (isLoadMore) {
    loadingMore.value = true
  } else {
    loading.value = true
  }

  try {
    const response = await getForumPosts(skip.value, limit.value)
    const newPosts = response.data || []
    
    if (isLoadMore) {
      posts.value.push(...newPosts)
    } else {
      posts.value = newPosts
    }
    
    // 判断是否还有更多数据
    hasMore.value = newPosts.length >= limit.value
    skip.value += newPosts.length
  } catch (error) {
    console.error('加载帖子失败:', error)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

// 加载更多
function loadMore() {
  loadPosts(true)
}

// 点击帖子
function handlePostClick(postId: number) {
  router.push(`/forum/post/${postId}`)
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

// 初始化加载
onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.forum-container {
  min-height: 100vh;
  background: transparent;
  padding-bottom: 20px;
}

/* 顶部标题栏 */
.header {
  background: var(--pure-white);
  padding: 16px 20px;
  border-bottom: 1px solid #F5F5F5;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--matcha-green);
  margin: 0;
}

/* 帖子列表区域 */
.posts-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.loading-state p {
  margin-top: 12px;
  font-size: 14px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 0;
  color: var(--text-secondary);
}

.empty-state p {
  font-size: 14px;
}

/* 帖子列表 - 网格布局 */
.posts-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

/* 帖子卡片 - 便签纸风格 */
.post-card {
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-soft);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(133, 173, 138, 0.2);
}

.post-card.style-a {
  background: #FFFDE7; /* 浅黄 */
}

.post-card.style-b {
  background: #E8F5E9; /* 浅绿 */
}

.post-card:active {
  transform: scale(0.98);
}

.post-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--ink-dark);
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-excerpt {
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
.post-author {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
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

.post-time {
  font-size: 12px;
  color: var(--text-light);
}

/* 统计数据 */
.post-stats {
  padding-top: 12px;
  border-top: 1px dashed rgba(0,0,0,0.1);
}

.stat-item {
  font-size: 13px;
  color: var(--text-secondary);
}

/* 加载更多 */
.load-more {
  text-align: center;
  padding: 16px 0;
}
</style>
