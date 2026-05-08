<template>
  <div class="home-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <h1 class="app-title"> 流俗地</h1>
    </div>

    <!-- 欢迎区域 -->
    <div v-if="authStore.isAuthenticated" class="welcome-section">
      <h2>欢迎回来, {{ authStore.user?.nickname || '文艺青年' }}!</h2>
      <p class="welcome-text">在文字的世界里，遇见更好的自己</p>
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
  background: #FAF9F6;
  padding-bottom: 20px;
}

/* 顶部标题栏 */
.header {
  background: #fff;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

/* 欢迎区域 */
.welcome-section {
  text-align: center;
  padding: 24px 16px;
  margin: 16px;
  background: linear-gradient(135deg, #BCDDBE, #CDE2EB);
  border-radius: 12px;
  color: white;
}

.welcome-section h2 {
  font-size: 20px;
  margin-bottom: 8px;
}

.welcome-text {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 16px;
}

.btn-login {
  display: inline-block;
  padding: 10px 24px;
  background: white;
  color: #64A386;
  border-radius: 20px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

/* 作品列表区域 */
.works-section {
  padding: 0 16px;
}

.section-title {
  font-size: 16px;
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
