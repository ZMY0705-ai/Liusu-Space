<template>
  <div class="me-container">
    <!-- 小红书风格的个人主页头部 -->
    <div class="profile-header">
      <!-- 背景封面 -->
      <div class="cover-banner">
        <div class="cover-gradient"></div>
      </div>

      <!-- 头像和信息区域 -->
      <div class="profile-info-section">
        <!-- 头像（一半在背景上，一半在白色区域） -->
        <div class="avatar-wrapper">
          <div class="user-avatar">
            <img 
              v-if="authStore.user?.avatar" 
              :src="getFullAvatarUrl(authStore.user.avatar)" 
              alt="头像"
              class="avatar-img"
            />
            <span v-else class="avatar-placeholder">{{ getAuthorInitial(authStore.user?.nickname || 'U') }}</span>
          </div>
        </div>

        <!-- 用户信息 -->
        <div class="user-details">
          <!-- 昵称 -->
          <h2 class="nickname">{{ authStore.user?.nickname || '未登录' }}</h2>
          
          <!-- 专业标签（胶囊样式） -->
          <div v-if="authStore.user?.is_major_public && authStore.user?.major" class="tags-row">
            <span class="tag-pill"> {{ authStore.user.major }}</span>
          </div>

          <!-- 个性签名 -->
          <p v-if="authStore.user?.bio || authStore.user?.signature" class="bio-text">
            {{ authStore.user?.bio || authStore.user?.signature }}
          </p>

          <!-- 姓名和专业信息气泡 -->
          <div v-if="authStore.user?.is_real_name_public && authStore.user?.real_name" class="info-bubble">
            <span class="bubble-label">姓名：</span>
            <span class="bubble-value">{{ authStore.user.real_name }}</span>
          </div>
          <div v-if="authStore.user?.is_major_public && authStore.user?.major" class="info-bubble">
            <span class="bubble-label">专业：</span>
            <span class="bubble-value">{{ authStore.user.major }}</span>
          </div>
        </div>

        <!-- 编辑资料按钮 -->
        <van-button 
          v-if="authStore.isAuthenticated"
          size="small"
          @click="handleEditProfile"
          class="edit-profile-btn"
        >
          编辑资料
        </van-button>
      </div>

      <!-- 数据统计栏 -->
      <div v-if="authStore.isAuthenticated" class="stats-bar">
        <div class="stat-item">
          <span class="stat-number">{{ myWorks.length }}</span>
          <span class="stat-label">作品</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ myDrafts.length }}</span>
          <span class="stat-label">草稿</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ myFavorites.length }}</span>
          <span class="stat-label">收藏</span>
        </div>
      </div>
    </div>

    <!-- 退出登录按钮（在功能菜单下方） -->
    <div v-if="authStore.isAuthenticated" class="logout-section">
      <van-button 
        block
        plain
        type="default"
        @click="handleLogout"
        class="logout-btn-full"
      >
        退出登录
      </van-button>
    </div>

    <!-- 功能菜单 - 大网格卡片风格 -->
    <div v-if="authStore.isAuthenticated" class="menu-section">
      <div class="menu-grid-item" @click="activeTab = 'works'">
        <div class="grid-icon-wrapper works-bg">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
        </div>
        <span>我的作品</span>
      </div>
      <div class="menu-grid-item" @click="activeTab = 'drafts'">
        <div class="grid-icon-wrapper drafts-bg">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19l7-7 3 3-7 7-3-3z"></path><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"></path><path d="M2 2l7.586 7.586"></path><circle cx="11" cy="11" r="2"></circle></svg>
        </div>
        <span>我的草稿</span>
      </div>
      <div class="menu-grid-item" @click="activeTab = 'favorites'">
        <div class="grid-icon-wrapper fav-bg">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        </div>
        <span>我的收藏</span>
      </div>
    </div>

    <!-- 我的作品列表 -->
    <div v-if="authStore.isAuthenticated && activeTab === 'works'" class="content-section">
      <h3 class="section-title">📚 我的作品</h3>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <van-loading type="spinner" size="24px" color="#64A386" />
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="myWorks.length === 0" class="empty-state">
        <p>暂无作品，快去创作吧！</p>
      </div>

      <!-- 作品列表 -->
      <div v-else class="works-list">
        <div 
          v-for="work in myWorks" 
          :key="work.id" 
          class="work-item"
        >
          <div class="work-content-wrapper" @click="handleWorkClick(work.id)">
            <van-icon name="book-o" size="20" color="#64A386" style="margin-right: 8px;" />
            <div class="work-info">
              <h4 class="work-title">{{ work.title }}</h4>
              <p class="work-excerpt">{{ getExcerpt(work.content) }}</p>
              <div class="work-meta">
                <span class="work-status published">已发布</span>
                <span class="work-time">{{ formatTime(work.created_at) }}</span>
              </div>
            </div>
          </div>
          <div class="work-actions">
            <van-button size="mini" type="default" @click.stop="handleEditWork(work.id)">
              编辑
            </van-button>
            <van-button size="mini" type="danger" @click.stop="handleDeleteWork(work.id)">
              删除
            </van-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 我的草稿列表 -->
    <div v-if="authStore.isAuthenticated && activeTab === 'drafts'" class="content-section">
      <h3 class="section-title">📝 我的草稿</h3>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <van-loading type="spinner" size="24px" color="#64A386" />
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="myDrafts.length === 0" class="empty-state">
        <p>暂无草稿</p>
      </div>

      <!-- 草稿列表 -->
      <div v-else class="works-list">
        <div 
          v-for="work in myDrafts" 
          :key="work.id" 
          class="work-item"
          @click="handleEditWork(work.id)"
        >
          <van-icon name="edit" size="20" color="#BCDDBE" style="margin-right: 8px;" />
          <h4 class="work-title">{{ work.title }}</h4>
          <p class="work-excerpt">{{ getExcerpt(work.content) }}</p>
          <div class="work-meta">
            <span class="work-status">草稿</span>
            <span class="work-time">{{ formatTime(work.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 我的收藏列表 -->
    <div v-if="authStore.isAuthenticated && activeTab === 'favorites'" class="content-section">
      <h3 class="section-title">⭐ 我的收藏</h3>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <van-loading type="spinner" size="24px" color="#64A386" />
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="myFavorites.length === 0" class="empty-state">
        <p>暂无收藏，快去发现好作品吧！</p>
      </div>

      <!-- 收藏列表 -->
      <div v-else class="works-list">
        <div 
          v-for="work in myFavorites" 
          :key="work.id" 
          class="work-item"
          @click="handleWorkClick(work.id)"
        >
          <van-icon name="star-o" size="20" color="#FFD93D" style="margin-right: 8px;" />
          <h4 class="work-title">{{ work.title }}</h4>
          <p class="work-excerpt">{{ getExcerpt(work.content) }}</p>
          <div class="work-meta">
            <span class="work-author">作者: {{ work.author?.nickname || '匿名' }}</span>
            <span class="work-time">{{ formatTime(work.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 未登录提示 -->
    <div v-if="!authStore.isAuthenticated" class="not-login">
      <p>请先登录后查看个人中心</p>
      <router-link to="/login" class="btn-go-login">去登录</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onActivated } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getWorks, deleteWork, getMyFavorites } from '@/api/work'
import { showToast, showDialog } from 'vant'
import { Icon as VanIcon } from 'vant'
import type { Work } from '@/types/api'

// 组件名称（用于 keep-alive）
defineOptions({
  name: 'MeCenter'
})

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 当前激活的标签
const activeTab = ref('works')

// 数据状态
const myWorks = ref<Work[]>([])
const myDrafts = ref<Work[]>([])
const myFavorites = ref<Work[]>([])
const loading = ref(false)

// 获取完整头像URL
const getFullAvatarUrl = (url: string | undefined) => {
  if (!url) return ''
  // 如果是相对路径，拼接后端地址
  if (url.startsWith('/')) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}${url}`
  }
  return url
}

// 获取作者首字母
const getAuthorInitial = (name: string) => {
  return name.charAt(0).toUpperCase()
}

// 获取摘要（截取前50字符）
const getExcerpt = (content: string) => {
  if (!content) return ''
  const text = content.replace(/<[^>]*>/g, '') // 去除HTML标签
  return text.length > 50 ? text.substring(0, 50) + '...' : text
}

// 格式化时间
const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 加载我的作品和草稿
async function loadMyContent() {
  if (!authStore.isAuthenticated) return
  
  loading.value = true
  try {
    // 这里需要后端提供一个获取当前用户作品的接口
    // 暂时使用通用接口，前端过滤
    const response = await getWorks(0, 100)
    const allWorks = response.data || []
    
    console.log('=== 调试信息 ===')
    console.log('当前用户ID:', authStore.user?.id)
    console.log('后端返回的作品总数:', allWorks.length)
    console.log('所有作品详情:', allWorks.map(w => ({
      id: w.id,
      title: w.title,
      author_id: w.author_id,
      status: w.status,
      published_at: w.published_at
    })))
    
    // 过滤出当前用户的作品
    const userId = authStore.user?.id
    myWorks.value = allWorks.filter(w => w.author_id === userId && w.status === 1)
    myDrafts.value = allWorks.filter(w => w.author_id === userId && w.status === 0)
    
    console.log('过滤后的我的作品数:', myWorks.value.length)
    console.log('过滤后的草稿数:', myDrafts.value.length)
    console.log('================')
    
    // 加载收藏列表
    await loadFavorites()
  } catch (error) {
    console.error('加载内容失败:', error)
  } finally {
    loading.value = false
  }
}

// 加载收藏列表
async function loadFavorites() {
  try {
    const response = await getMyFavorites()
    myFavorites.value = response.data || []
  } catch (error) {
    console.error('加载收藏失败:', error)
  }
}

// 点击作品
function handleWorkClick(workId: number) {
  router.push(`/work/${workId}`)
}

// 编辑作品
function handleEditWork(workId: number) {
  router.push(`/editor/${workId}`)
}

// 删除作品
async function handleDeleteWork(workId: number) {
  try {
    await showDialog({
      title: '确认删除',
      message: '确定要删除这个作品吗？删除后无法恢复。',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      confirmButtonColor: '#ee0a24'
    })
    
    await deleteWork(workId)
    showToast({ type: 'success', message: '删除成功' })
    
    // 重新加载列表
    await loadMyContent()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      showToast({ type: 'fail', message: '删除失败' })
    }
  }
}

// 编辑资料
function handleEditProfile() {
  router.push('/profile/edit')
}

// 退出登录
function handleLogout() {
  authStore.logout()
  showToast({ type: 'success', message: '已退出登录' })
  router.push('/home')
}

// 初始化加载
onMounted(() => {
  // 检查URL参数，如果有tab参数则切换到对应标签
  const tabParam = route.query.tab as string
  if (tabParam && ['works', 'drafts', 'favorites'].includes(tabParam)) {
    activeTab.value = tabParam
  }
  
  loadMyContent()
})

// 当页面被激活时（从其他页面返回），重新获取用户信息
onActivated(async () => {
  console.log('[MeCenter] 页面被激活，刷新用户信息')
  await authStore.fetchUser()
})
</script>

<style scoped>
.me-container {
  min-height: 100vh;
  background: var(--paper-white);
  padding-bottom: 20px;
}

/* === 小红书风格个人主页头部 === */
.profile-header {
  position: relative;
  background: var(--pure-white);
  padding-bottom: 20px;
}

/* 背景封面 */
.cover-banner {
  position: relative;
  width: 100%;
  height: 140px;
  overflow: hidden;
}

.cover-gradient {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #64A386 0%, #A8D5A1 50%, #F5B342 100%);
  position: relative;
}

.cover-gradient::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.2) 0%, transparent 40%);
}

/* 头像和信息区域 */
.profile-info-section {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 0 20px;
  margin-top: -45px; /* 让头像浮层效果 */
}

.avatar-wrapper {
  position: relative;
  z-index: 10;
  flex-shrink: 0;
}

.user-avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: var(--pure-white);
  border: 4px solid var(--pure-white);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 32px;
  font-weight: 600;
  color: var(--matcha-green);
}

/* 用户信息 */
.user-details {
  flex: 1;
  padding-top: 50px; /* 为头像留出空间 */
  min-width: 0;
}

.nickname {
  font-size: 20px;
  font-weight: 700;
  color: var(--ink-dark);
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
}

.tag-pill {
  display: inline-block;
  padding: 4px 12px;
  background: #F5F5F5;
  color: var(--text-secondary);
  font-size: 12px;
  border-radius: 12px;
  font-weight: 500;
}

.bio-text {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 信息气泡 */
.info-bubble {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: rgba(100, 163, 134, 0.1);
  border-radius: 12px;
  margin-right: 8px;
  margin-bottom: 6px;
  font-size: 12px;
  transition: all 0.2s ease;
}

.info-bubble:hover {
  background: rgba(100, 163, 134, 0.15);
  transform: translateY(-1px);
}

.bubble-label {
  color: #999;
  font-weight: 500;
}

.bubble-value {
  color: var(--text-primary);
  font-weight: 500;
}

/* 编辑资料按钮 */
.edit-profile-btn {
  margin-top: 50px; /* 为头像留出空间 */
  flex-shrink: 0;
  background: var(--pure-white);
  border: 1px solid #E0E0E0;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  border-radius: 16px;
  padding: 6px 16px;
  height: auto;
  min-width: 70px;
}

.edit-profile-btn:active {
  background: #F5F5F5;
}

/* 数据统计栏 */
.stats-bar {
  display: flex;
  justify-content: space-around;
  padding: 16px 20px 0;
  border-top: 1px solid #F0F0F0;
  margin-top: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.stat-item:active {
  transform: scale(0.95);
}

.stat-number {
  font-size: 18px;
  font-weight: 700;
  color: var(--ink-dark);
  line-height: 1;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 400;
}

/* 功能菜单 - 大网格 */
.menu-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 20px;
}

.menu-grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-grid-item:active {
  transform: scale(0.95);
}

.grid-icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.works-bg { background: #E8F5E9; color: var(--matcha-green); }
.drafts-bg { background: #FFFDE7; color: #FBC02D; }
.fav-bg { background: #FFF8E1; color: var(--warm-yellow); }

.menu-grid-item span {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

/* 内容区域 */
.content-section {
  padding: 0 16px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-dark);
  margin: 24px 0 16px;
  padding-left: 8px;
  border-left: 4px solid var(--lemon-yellow);
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

/* 作品列表 */
.works-list {
  margin-bottom: 24px;
}

.work-item {
  background: var(--pure-white);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: var(--shadow-soft);
  transition: all 0.2s;
}

.work-content-wrapper {
  display: flex;
  cursor: pointer;
  margin-bottom: 12px;
}

.work-content-wrapper:active {
  opacity: 0.7;
}

.work-info {
  flex: 1;
  min-width: 0;
}

.work-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  padding-top: 12px;
  border-top: 1px solid #F5F5F5;
}

.work-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--ink-dark);
  margin: 0 0 8px 0;
}

.work-excerpt {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 12px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.work-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.work-status {
  font-size: 12px;
  padding: 4px 8px;
  background: #F5F5F5;
  border-radius: 4px;
  color: var(--text-secondary);
}

.work-status.published {
  background: #E8F5E9;
  color: var(--matcha-green);
}

.work-author {
  font-size: 12px;
  color: var(--text-light);
}

.work-time {
  font-size: 12px;
  color: var(--text-light);
}

/* 未登录提示 */
.not-login {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.not-login p {
  margin-bottom: 20px;
  font-size: 16px;
}

.btn-go-login {
  display: inline-block;
  padding: 12px 32px;
  background: var(--matcha-green);
  color: white;
  border-radius: 24px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 600;
}
</style>