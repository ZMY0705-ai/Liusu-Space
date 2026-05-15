<template>
  <div class="fab-menu">
    <!-- 浮动加号按钮 -->
    <div class="fab-button" @click="showMenu = true">
      <van-icon name="plus" size="24" color="#fff" />
    </div>

    <!-- 弹出菜单 -->
    <van-action-sheet
      v-model:show="showMenu"
      :actions="actions"
      cancel-text="取消"
      close-on-click-action
      @select="onSelect"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showMenu = ref(false)

// 菜单选项
const actions = ref([
  {
    name: '储存作品',
    icon: 'edit',
    color: '#FBFCCD',
    value: 'draft'
  },
  {
    name: '发表作品',
    icon: 'fire-o',
    color: '#CDE2EB',
    value: 'publish'
  },
  {
    name: '发表讨论',
    icon: 'chat',
    color: '#BCDDBE',
    value: 'forum'
  }
])

// 处理菜单选择
function onSelect(action: any) {
  // 检查登录状态
  if (!authStore.isAuthenticated) {
    router.push({ name: 'Login', query: { redirect: router.currentRoute.value.fullPath } })
    return
  }

  // 根据选择跳转到不同页面
  switch (action.value) {
    case 'draft':
      // 储存作品链路
      router.push({ path: '/editor', query: { mode: 'draft' } })
      break
    case 'publish':
      // 发表作品链路
      router.push({ path: '/editor', query: { mode: 'publish' } })
      break
    case 'forum':
      router.push('/forum/create')
      break
  }
}
</script>

<style scoped>
.fab-menu {
  position: fixed;
  bottom: 70px; /* 在底部导航栏之上 */
  right: 20px;
  z-index: 100;
}

/* 桌面端适配：当使用DesktopLayout时，FAB按钮位置调整 */
@media (min-width: 769px) {
  .fab-menu {
    bottom: 40px;
    right: 40px;
  }
}

.fab-button {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #F5B342;
  box-shadow: 0 6px 16px rgba(47, 93, 80, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.fab-button:hover {
  transform: scale(1.15);
  box-shadow: 0 8px 24px rgba(47, 93, 80, 0.5);
}

.fab-button:active {
  transform: scale(0.95);
}

/* 弹出菜单样式优化 */
.fab-menu :deep(.van-action-sheet) {
  border-radius: 20px 20px 0 0;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.05);
}

/* 菜单项文字颜色改为深色 */
.fab-menu :deep(.van-action-sheet__item) {
  color: #2F4F4F !important;
  font-weight: 500;
  font-size: 16px;
  transition: all 0.2s;
}

/* 菜单项悬停/点击背景色 */
.fab-menu :deep(.van-action-sheet__item):hover,
.fab-menu :deep(.van-action-sheet__item):active {
  background-color: #F0F7F0 !important;
}

/* 取消按钮样式 */
.fab-menu :deep(.van-action-sheet__cancel) {
  color: #5C6B5D !important;
  font-weight: 500;
}

.fab-menu :deep(.van-action-sheet__cancel):hover,
.fab-menu :deep(.van-action-sheet__cancel):active {
  background-color: #F0F7F0 !important;
}
</style>
