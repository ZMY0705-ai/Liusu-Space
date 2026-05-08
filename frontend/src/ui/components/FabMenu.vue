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
    icon: 'book',
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

.fab-button {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--green-primary);
  box-shadow: 0 4px 12px rgba(100, 163, 134, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.fab-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(100, 163, 134, 0.5);
}

.fab-button:active {
  transform: scale(0.95);
}
</style>
