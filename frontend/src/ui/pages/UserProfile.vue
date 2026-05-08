<template>
  <div class="user-profile-container">
    <!-- 顶部导航栏 -->
    <div class="profile-header-nav">
      <van-icon name="arrow-left" size="20" @click="goBack" />
      <h1>个人主页</h1>
      <div style="width: 20px;"></div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <van-loading type="spinner" size="24px" color="#64A386" />
      <p>加载中...</p>
    </div>

    <!-- 用户信息 -->
    <div v-else-if="userProfile" class="profile-content">
      <!-- 小红书风格的个人主页头部 -->
      <div class="profile-header">
        <!-- 背景封面 -->
        <div class="cover-banner">
          <div class="cover-gradient"></div>
        </div>

        <!-- 头像和信息区域 -->
        <div class="profile-info-section">
          <!-- 头像 -->
          <div class="avatar-wrapper">
            <div class="user-avatar">
              <img 
                v-if="userProfile.avatar" 
                :src="getFullAvatarUrl(userProfile.avatar)" 
                alt="头像"
                class="avatar-img"
              />
              <span v-else class="avatar-placeholder">{{ getAuthorInitial(userProfile.nickname || 'U') }}</span>
            </div>
          </div>

          <!-- 用户信息 -->
          <div class="user-details">
            <!-- 昵称 -->
            <h2 class="nickname">{{ userProfile.nickname || '未知用户' }}</h2>

            <!-- 个性签名（优先显示bio，如果没有则显示signature） -->
            <p v-if="userProfile.bio" class="bio-text">
              {{ userProfile.bio }}
            </p>

            <!-- 姓名和专业信息气泡（根据用户隐私设置显示） -->
            <div class="info-bubbles">
              <div v-if="userProfile.real_name" class="info-bubble">
                <span class="bubble-label">姓名：</span>
                <span class="bubble-value">{{ userProfile.real_name }}</span>
              </div>
              <div v-if="userProfile.major" class="info-bubble">
                <span class="bubble-label">专业：</span>
                <span class="bubble-value">{{ userProfile.major }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 数据统计栏 -->
        <div class="stats-bar">
          <div class="stat-item">
            <span class="stat-number">{{ userProfile.works_count || 0 }}</span>
            <span class="stat-label">作品</span>
          </div>
        </div>
      </div>

      <!-- 作品列表 -->
      <div class="content-section">
        <h3 class="section-title">📚 作品</h3>
        
        <!-- 空状态 -->
        <div v-if="userProfile.published_works.length === 0" class="empty-state">
          <p>暂无作品</p>
        </div>

        <!-- 作品列表 -->
        <div v-else class="works-list">
          <div 
            v-for="work in userProfile.published_works" 
            :key="work.id" 
            class="work-item"
            @click="handleWorkClick(work.id)"
          >
            <div class="work-content-wrapper">
              <van-icon name="book-o" size="20" color="#64A386" style="margin-right: 8px;" />
              <div class="work-info">
                <h4 class="work-title">{{ work.title }}</h4>
                <p class="work-excerpt">{{ getExcerpt(work.content) }}</p>
                <div class="work-meta">
                  <span class="work-stats">
                    <van-icon name="like-o" size="12" /> {{ work.like_count || 0 }}
                  </span>
                  <span class="work-time">{{ formatTime(work.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-state">
      <p>用户不存在或已被删除</p>
      <van-button type="primary" @click="goBack" color="#64A386">
        返回首页
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getUserPublicProfile } from '@/api/work'
import { showToast } from 'vant'

const router = useRouter()
const route = useRoute()

// 用户ID
const userId = ref(Number(route.params.id))

// 数据状态
const userProfile = ref<any>(null)
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

// 加载用户信息
async function loadUserProfile() {
  loading.value = true
  try {
    const response = await getUserPublicProfile(userId.value)
    userProfile.value = response.data
  } catch (error) {
    console.error('加载用户信息失败:', error)
    showToast({ type: 'fail', message: '加载用户信息失败' })
  } finally {
    loading.value = false
  }
}

// 点击作品
function handleWorkClick(workId: number) {
  router.push(`/work/${workId}`)
}

// 返回
function goBack() {
  router.back()
}

// 初始化
onMounted(() => {
  loadUserProfile()
})
</script>

<style scoped>
.user-profile-container {
  min-height: 100vh;
  background: var(--paper-white);
  padding-bottom: 20px;
}

/* 顶部导航栏 */
.profile-header-nav {
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

.profile-header-nav h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-dark);
  margin: 0;
}

.profile-header-nav .van-icon {
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
  margin-top: -45px;
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
  padding-top: 50px;
  min-width: 0;
}

.nickname {
  font-size: 20px;
  font-weight: 700;
  color: var(--ink-dark);
  margin: 0 0 8px 0;
  line-height: 1.3;
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

/* 信息气泡容器 */
.info-bubbles {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

/* 信息气泡 */
.info-bubble {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  background: rgba(100, 163, 134, 0.08);
  border-radius: 16px;
  font-size: 13px;
  transition: all 0.2s ease;
}

.info-bubble:hover {
  background: rgba(100, 163, 134, 0.12);
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
  cursor: pointer;
}

.work-item:active {
  transform: scale(0.98);
  opacity: 0.9;
}

.work-content-wrapper {
  display: flex;
}

.work-info {
  flex: 1;
  min-width: 0;
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

.work-stats {
  font-size: 12px;
  color: var(--text-light);
  display: flex;
  align-items: center;
  gap: 4px;
}

.work-time {
  font-size: 12px;
  color: var(--text-light);
}
</style>
