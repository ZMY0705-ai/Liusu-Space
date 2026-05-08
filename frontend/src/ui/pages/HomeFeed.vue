<template>
  <div class="home-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <h1 class="app-title">流俗地</h1>
    </div>

    <!-- 欢迎区域 -->
    <div v-if="authStore.isAuthenticated" class="welcome-section">
      <svg class="wave-decoration" viewBox="0 0 1440 320" preserveAspectRatio="none">
        <path fill="#A8D5A1" fill-opacity="0.3" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
      <div class="welcome-content">
        <h2>欢迎回来，Writer！</h2>
        <p class="welcome-text">在文字的世界里，遇见更好的自己</p>
      </div>
    </div>
    <div v-else class="welcome-section">
      <h2>欢迎来到流俗地</h2>
      <p class="welcome-text">一个温暖的校园文学社区</p>
      <router-link to="/login" class="btn-login">登录 / 注册</router-link>
    </div>

    <!-- 作品列表 -->
    <div class="works-section">
      <h3 class="section-title">📚 最新作品</h3>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <van-loading type="spinner" size="24px" color="#64A386" />
        <p>加载中...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="works.length === 0" class="empty-state">
        <p>暂无作品，快来创作第一篇吧！</p>
      </div>

      <!-- 作品列表 -->
      <div v-else class="works-list">
        <WorkCard 
          v-for="work in works" 
          :key="work.id" 
          :work="work"
          @click="handleWorkClick"
        />
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
import { useRouter, useRoute, onBeforeRouteUpdate } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getWorks } from '@/api/work'
import WorkCard from '@/ui/components/WorkCard.vue'
import FabMenu from '@/ui/components/FabMenu.vue'
import type { Work } from '@/types/api'

const router = useRouter()
const authStore = useAuthStore()

// 作品列表
const works = ref<Work[]>([])
const loading = ref(false)
const loadingMore = ref(false)
const skip = ref(0)
const limit = ref(10)
const hasMore = ref(true)

// 加载作品列表
async function loadWorks(isLoadMore = false) {
  if (isLoadMore) {
    loadingMore.value = true
  } else {
    loading.value = true
  }

  try {
    const response = await getWorks(skip.value, limit.value)
    // 过滤出已发布的作品（status === 1）
    const newWorks = (response.data || []).filter(work => work.status === 1)
    
    if (isLoadMore) {
      works.value.push(...newWorks)
    } else {
      works.value = newWorks
    }
    
    // 判断是否还有更多数据
    hasMore.value = newWorks.length >= limit.value
    skip.value += newWorks.length
  } catch (error) {
    console.error('加载作品失败:', error)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

// 加载更多
function loadMore() {
  loadWorks(true)
}

// 点击作品
function handleWorkClick(workId: number) {
  router.push(`/work/${workId}`)
}

// 初始化加载
onMounted(() => {
  loadWorks()
})

// 监听路由变化，当从编辑器返回时重新加载数据
onBeforeRouteUpdate((to, from) => {
  // 如果是从编辑器页面返回，则重新加载作品列表
  if (from.path.startsWith('/editor') || to.path === '/home') {
    skip.value = 0
    hasMore.value = true
    loadWorks()
  }
})

// 监听查询参数变化，用于强制刷新
import { watch } from 'vue'
const route = useRoute()
watch(() => route.query.refresh, () => {
  // 当refresh参数变化时，重新加载作品列表
  skip.value = 0
  hasMore.value = true
  loadWorks()
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: var(--paper-white);
  padding-bottom: 20px;
}

/* 顶部标题栏 */
.header {
  background: var(--pure-white);
  padding: 16px 20px;
  border-bottom: 1px solid #F5F5F5;
}

.app-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--matcha-green);
  margin: 0;
  letter-spacing: 1px;
}

/* 欢迎区域 */
.welcome-section {
  position: relative;
  text-align: center;
  padding: 30px 20px;
  margin: 16px;
  background: linear-gradient(135deg, var(--light-matcha), #E8F5E9);
  border-radius: 24px;
  color: var(--ink-dark);
  overflow: hidden;
}

.wave-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60%;
  opacity: 0.5;
}

.welcome-content {
  position: relative;
  z-index: 1;
}

.welcome-section h2 {
  font-size: 22px;
  margin-bottom: 8px;
  color: var(--ink-dark);
}

.welcome-text {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 16px;
}

.btn-login {
  display: inline-block;
  padding: 10px 24px;
  background: var(--pure-white);
  color: var(--matcha-green);
  border-radius: 20px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(133, 173, 138, 0.2);
}

/* 作品列表区域 */
.works-section {
  padding: 0 16px;
}

.section-title {
  font-size: 18px;
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

/* 加载更多 */
.load-more {
  text-align: center;
  padding: 16px 0;
}
</style>
