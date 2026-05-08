<template>
  <div class="me-container">
    <!-- 用户信息卡片 -->
    <div class="user-card">
      <div class="user-avatar">
        {{ getAuthorInitial(authStore.user?.nickname || 'U') }}
      </div>
      <div class="user-info">
        <h2 class="user-name">{{ authStore.user?.nickname || '未登录' }}</h2>
        <p class="user-detail">{{ authStore.user?.account || '' }}</p>
        <p v-if="authStore.user?.signature" class="user-signature">{{ authStore.user.signature }}</p>
      </div>
      <van-button 
        v-if="authStore.isAuthenticated"
        size="small" 
        type="default"
        @click="handleLogout"
      >
        退出登录
      </van-button>
      <router-link 
        v-else 
        to="/login"
        class="btn-login"
      >
        登录/注册
      </router-link>
    </div>

    <!-- 功能菜单 -->
    <div v-if="authStore.isAuthenticated" class="menu-section">
      <div class="menu-item" @click="activeTab = 'works'">
        <van-icon name="notes-o" size="24" color="#64A386" class="menu-icon" />
        <span>我的作品</span>
      </div>
      <div class="menu-item" @click="activeTab = 'drafts'">
        <van-icon name="edit" size="24" color="#BCDDBE" class="menu-icon" />
        <span>我的草稿</span>
      </div>
      <div class="menu-item" @click="activeTab = 'favorites'">
        <van-icon name="star-o" size="24" color="#FFD93D" class="menu-icon" />
        <span>我的收藏</span>
      </div>
    </div>

    <!-- 我的作品列表 -->
    <div v-if="authStore.isAuthenticated && activeTab === 'works'" class="content-section">
      <h3 class="section-title">📚 我的作品</h3>
      
      <!-- 调试信息 -->
      <div style="background: #fff3cd; padding: 10px; margin: 10px 0; border-radius: 8px; font-size: 12px;">
        <p style="margin: 0;">myWorks.length: {{ myWorks.length }}</p>
        <p style="margin: 0;">myWorks数据: {{ JSON.stringify(myWorks.map(w => ({id: w.id, title: w.title}))) }}</p>
      </div>
      
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
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getWorks, deleteWork, getMyFavorites } from '@/api/work'
import { showToast, showDialog } from 'vant'
import { Icon as VanIcon } from 'vant'
import type { Work } from '@/types/api'

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
</script>

<style scoped>
.me-container {
  min-height: 100vh;
  background: #FAF9F6;
  padding-bottom: 20px;
}

/* 用户信息卡片 */
.user-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 20px;
  background: linear-gradient(135deg, #BCDDBE, #CDE2EB);
  color: white;
}

.user-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.user-detail {
  font-size: 14px;
  opacity: 0.9;
  margin: 0 0 4px 0;
}

.user-signature {
  font-size: 13px;
  opacity: 0.8;
  margin: 0;
}

.btn-login {
  padding: 8px 16px;
  background: white;
  color: #64A386;
  border-radius: 20px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

/* 功能菜单 */
.menu-section {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background: white;
  margin: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-item:active {
  transform: scale(0.95);
}

.menu-item span {
  font-size: 14px;
  color: var(--text-primary);
}

.menu-icon {
  display: block;
  margin-bottom: 8px;
}

/* 内容区域 */
.content-section {
  padding: 0 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 24px 0 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #f0f0f0;
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

/* 信息框 */
.info-box {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 12px;
  margin-top: 16px;
}

.info-box p {
  font-size: 14px;
  color: var(--text-secondary);
}

/* 作品列表 */
.works-list {
  margin-bottom: 24px;
}

.work-item {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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
  border-top: 1px solid #f0f0f0;
}

.work-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
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
  background: #f0f0f0;
  border-radius: 4px;
  color: var(--text-secondary);
}

.work-status.published {
  background: #BCDDBE;
  color: #64A386;
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
  background: #64A386;
  color: white;
  border-radius: 24px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
}
</style>
