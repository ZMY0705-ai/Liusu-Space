<template>
  <div class="mobile-layout">
    <!-- 大面积波浪背景装饰 -->
    <div class="wave-bg-decoration">
      <svg class="wave-left" viewBox="0 0 400 800" preserveAspectRatio="none">
        <path d="M0 0 Q100 100 0 200 Q80 300 0 400 Q120 500 0 600 Q60 700 0 800" fill="#FEEE9A" opacity="0.3"/>
        <path d="M0 50 Q80 150 0 250 Q60 350 0 450 Q100 550 0 650 Q40 750 0 800" fill="#8EB89C" opacity="0.25"/>
      </svg>
      <svg class="wave-right" viewBox="0 0 400 800" preserveAspectRatio="none">
        <path d="M400 0 Q300 100 400 200 Q320 300 400 400 Q280 500 400 600 Q340 700 400 800" fill="#8EB89C" opacity="0.2"/>
        <path d="M400 80 Q320 180 400 280 Q340 380 400 480 Q300 580 400 680 Q360 750 400 800" fill="#FEEE9A" opacity="0.25"/>
      </svg>
    </div>
    
    <div class="content">
      <router-view />
    </div>
    <van-tabbar v-model="active" route active-color="#85AD8A" inactive-color="#999" class="custom-tabbar">
      <van-tabbar-item icon="home-o" to="/home">首页</van-tabbar-item>
      <van-tabbar-item icon="comment-o" to="/forum">论坛</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/me">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

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

<style scoped>
.mobile-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--paper-white);
  position: relative;
  overflow: hidden;
}

/* 波浪背景装饰 */
.wave-bg-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.wave-left {
  position: absolute;
  left: -50px;
  top: 0;
  width: 150px;
  height: 100%;
}

.wave-right {
  position: absolute;
  right: -50px;
  top: 0;
  width: 150px;
  height: 100%;
}

.content {
  flex: 1;
  padding-bottom: 50px;
  position: relative;
  z-index: 1;
}

.custom-tabbar :deep(.van-tabbar) {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-top: 1px solid #F5F5F5;
}

.custom-tabbar :deep(.van-tabbar-item--active) {
  color: var(--matcha-green);
}
</style>
