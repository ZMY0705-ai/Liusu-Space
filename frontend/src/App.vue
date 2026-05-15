<template>
  <div class="app-container">
    <MobileLayout v-if="layout === 'mobile'">
      <router-view v-slot="{ Component }">
        <keep-alive :include="['MeCenter']">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </MobileLayout>
    <DesktopLayout v-else-if="layout === 'desktop'">
      <router-view v-slot="{ Component }">
        <keep-alive :include="['MeCenter']">
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </DesktopLayout>
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
import DesktopLayout from '@/ui/layouts/DesktopLayout.vue'

const route = useRoute()
const authStore = useAuthStore()

// 根据路由元信息选择布局
const layout = computed(() => {
  if (route.meta.layout === 'mobile') {
    return 'mobile'
  }
  if (route.meta.layout === 'desktop') {
    return 'desktop'
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
  width: 100%;
  min-height: 100vh;
  background: transparent;
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
