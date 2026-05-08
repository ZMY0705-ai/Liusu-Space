<template>
  <div class="app-container">
    <MobileLayout v-if="layout === 'mobile'">
      <router-view v-slot="{ Component }">
        <keep-alive :include="['MeCenter']">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </MobileLayout>
    <div v-else>
      <router-view v-slot="{ Component }">
        <keep-alive :include="['MeCenter']">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import MobileLayout from '@/ui/layouts/MobileLayout.vue'

const route = useRoute()
const authStore = useAuthStore()

// 根据路由元信息选择布局
const layout = computed(() => {
  if (route.meta.layout === 'mobile') {
    return 'mobile'
  }
  return 'default'
})

onMounted(() => {
  // 初始化认证状态
  authStore.initAuth()
})
</script>

<style>
@import '@/styles/theme.css';

.app-container {
  max-width: var(--mobile-max-width);
  margin: 0 auto;
  min-height: 100vh;
  background: var(--paper-bg);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}

/* 全屏布局（登录/注册页） */
.app-container:has(.auth-container) {
  max-width: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  box-shadow: none;
}

/* Vant 样式覆盖 */
:root {
  --van-primary-color: #64A386;
  --van-action-sheet-item-icon-size: 20px;
}
</style>
