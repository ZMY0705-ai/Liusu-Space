<template>
  <div class="notifications-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <h1 class="page-title">🔔 消息通知</h1>
      <van-button 
        v-if="unreadCount > 0"
        size="small" 
        type="default"
        @click="handleMarkAllRead"
      >
        全部已读
      </van-button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <van-loading type="spinner" size="24px" color="#64A386" />
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="notifications.length === 0" class="empty-state">
      <p>暂无消息通知</p>
    </div>

    <!-- 通知列表 -->
    <div v-else class="notifications-list">
      <div 
        v-for="notification in notifications" 
        :key="notification.id" 
        class="notification-item"
        :class="{ unread: !notification.is_read }"
        @click="handleNotificationClick(notification)"
      >
        <div class="notification-icon">
          <van-icon :name="getNotificationIcon(notification.type)" size="24" :color="getNotificationColor(notification.type)" />
        </div>
        <div class="notification-content">
          <div class="notification-header">
            <span class="notification-title">{{ getNotificationTitle(notification) }}</span>
            <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
          </div>
          <p class="notification-text">{{ notification.content || '你有新的消息' }}</p>
        </div>
        <div v-if="!notification.is_read" class="unread-dot"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getNotifications, markNotificationAsRead, markAllAsRead } from '@/api/work'
import { showToast } from 'vant'

const router = useRouter()

// 通知列表
const notifications = ref<any[]>([])
const loading = ref(false)

// 未读数量
const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length
})

// 加载通知列表
async function loadNotifications() {
  loading.value = true
  try {
    const response = await getNotifications()
    notifications.value = response.data || []
  } catch (error) {
    console.error('加载通知失败:', error)
    showToast({ type: 'fail', message: '加载通知失败' })
  } finally {
    loading.value = false
  }
}

// 获取通知图标
function getNotificationIcon(type: string) {
  switch (type) {
    case 'like':
      return 'star'
    case 'comment':
      return 'chat'
    case 'favorite':
      return 'like'
    case 'reply':
      return 'comment'
    default:
      return 'bell'
  }
}

// 获取通知颜色
function getNotificationColor(type: string) {
  switch (type) {
    case 'like':
      return '#FF6B6B'
    case 'comment':
      return '#4ECDC4'
    case 'favorite':
      return '#FFD93D'
    case 'reply':
      return '#6BCB77'
    default:
      return '#64A386'
  }
}

// 获取通知标题
function getNotificationTitle(notification: any) {
  switch (notification.type) {
    case 'like':
      return '点赞'
    case 'comment':
      return '评论'
    case 'favorite':
      return '收藏'
    case 'reply':
      return '回复'
    default:
      return '通知'
  }
}

// 格式化时间
const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 点击通知
async function handleNotificationClick(notification: any) {
  // 标记为已读
  if (!notification.is_read) {
    try {
      await markNotificationAsRead(notification.id)
      notification.is_read = true
    } catch (error) {
      console.error('标记已读失败:', error)
    }
  }
  
  // 跳转到相关页面
  if (notification.target_type === 'work') {
    router.push(`/work/${notification.target_id}`)
  } else if (notification.target_type === 'post') {
    router.push(`/forum/post/${notification.target_id}`)
  }
}

// 全部标记为已读
async function handleMarkAllRead() {
  try {
    await markAllAsRead()
    showToast({ type: 'success', message: '已全部标记为已读' })
    
    // 更新本地状态
    notifications.value.forEach(n => {
      n.is_read = true
    })
  } catch (error) {
    console.error('标记全部已读失败:', error)
    showToast({ type: 'fail', message: '操作失败' })
  }
}

// 初始化加载
onMounted(() => {
  loadNotifications()
})
</script>

<style scoped>
.notifications-container {
  min-height: 100vh;
  background: transparent;
  padding-bottom: 20px;
}

/* 顶部标题栏 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
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

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 0;
  color: var(--text-secondary);
}

.empty-state p {
  font-size: 14px;
}

/* 通知列表 */
.notifications-list {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px 16px;
}

/* 通知项 */
.notification-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
}

.notification-item:active {
  transform: scale(0.98);
}

.notification-item.unread {
  background: linear-gradient(135deg, #FBFCCD, #BCDDBE);
}

.notification-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.notification-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.notification-time {
  font-size: 12px;
  color: var(--text-light);
}

.notification-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
}

/* 未读标记 */
.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ee0a24;
  position: absolute;
  top: 16px;
  right: 16px;
}
</style>
