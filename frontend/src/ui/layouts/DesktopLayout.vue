<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = ref(0)

// 根据当前路由设置激活的tab
watch(
  () => route.path,
  (path) => {
    if (path === '/home') {
      active.value = 0
    } else if (path === '/forum' || path.startsWith('/forum/post') || path === '/forum/create') {
      active.value = 1
    } else if (path === '/me') {
      active.value = 2
    }
  },
  { immediate: true }
)
</script>

<template>
  <div class="desktop-layout">
    <!-- 顶部导航栏 -->
    <header class="top-header">
      <div class="header-content">
        <h1 class="logo">流俗地</h1>
        <nav class="main-nav">
          <router-link to="/home" class="nav-item" :class="{ active: active === 0 }">
            <van-icon name="home-o" />
            <span>首页</span>
          </router-link>
          <router-link to="/forum" class="nav-item" :class="{ active: active === 1 }">
            <van-icon name="comment-o" />
            <span>论坛</span>
          </router-link>
          <router-link to="/me" class="nav-item" :class="{ active: active === 2 }">
            <van-icon name="user-o" />
            <span>我的</span>
          </router-link>
        </nav>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.desktop-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: transparent;
}

/* 顶部导航栏 */
.top-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #F5F5F5;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 20px;
  }
  
  .main-nav {
    gap: 16px;
  }
  
  .nav-item span {
    display: none;
  }
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: var(--matcha-green);
  margin: 0;
  letter-spacing: 2px;
  font-family: 'Noto Serif SC', serif;
}

.main-nav {
  display: flex;
  gap: 32px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: rgba(133, 173, 138, 0.1);
  color: var(--matcha-green);
}

.nav-item.active {
  color: var(--matcha-green);
  background: rgba(133, 173, 138, 0.15);
}

.nav-item :deep(.van-icon) {
  font-size: 18px;
}

/* 主内容区 */
.main-content {
  flex: 1;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px 40px;
  position: relative;
}

@media (max-width: 768px) {
  .main-content {
    padding: 16px 20px;
  }
}
</style>
