<template>
  <div class="mobile-layout">
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
}

.content {
  flex: 1;
  padding-bottom: 50px; /* 为底部导航栏预留空间 */
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
