<template>
  <div class="comment-item">
    <!-- 评论内容 -->
    <div class="comment-main">
      <div class="comment-avatar">
        {{ getAuthorInitial(comment.user?.nickname || 'U') }}
      </div>
      <div class="comment-bubble">
        <div class="comment-header">
          <span class="comment-author">{{ comment.user?.nickname || '匿名' }}</span>
          <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
        </div>
        <p class="comment-text">{{ comment.content }}</p>
        
        <!-- 操作按钮 -->
        <div class="comment-actions">
          <span class="action-btn" @click="toggleReply">
            {{ showReplyInput ? '取消' : '回复' }}
          </span>
        </div>
        
        <!-- 回复输入框 -->
        <div v-if="showReplyInput" class="reply-input-box">
          <van-field
            v-model="replyContent"
            type="textarea"
            placeholder="写下你的回复..."
            rows="2"
            autosize
            maxlength="500"
            show-word-limit
          />
          <van-button 
            type="primary" 
            size="mini"
            @click="handleReply"
            :loading="submittingReply"
            color="#64A386"
          >
            发送
          </van-button>
        </div>
      </div>
    </div>
    
    <!-- 嵌套回复列表 -->
    <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
      <div 
        v-for="reply in comment.replies" 
        :key="reply.id"
        class="reply-item-wrapper"
      >
        <CommentItem
          :comment="reply"
          :target-id="targetId"
          :target-type="targetType"
          @reply-success="handleReplySuccess"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { createWorkComment, createPostComment } from '@/api/work'
import { showToast } from 'vant'

const props = defineProps<{
  comment: any
  targetId: number
  targetType: 'work' | 'post'
}>()

const emit = defineEmits(['reply-success'])

const router = useRouter()
const authStore = useAuthStore()

// 状态
const showReplyInput = ref(false)
const replyContent = ref('')
const submittingReply = ref(false)

// 获取作者首字母
const getAuthorInitial = (name: string) => {
  return name.charAt(0).toUpperCase()
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

// 切换回复输入框
function toggleReply() {
  if (!authStore.isAuthenticated) {
    showToast({ type: 'fail', message: '请先登录' })
    router.push({ name: 'Login', query: { redirect: window.location.pathname } })
    return
  }
  showReplyInput.value = !showReplyInput.value
  if (!showReplyInput.value) {
    replyContent.value = ''
  }
}

// 发表回复
async function handleReply() {
  if (!replyContent.value.trim()) {
    showToast({ type: 'fail', message: '请输入回复内容' })
    return
  }
  
  submittingReply.value = true
  try {
    if (props.targetType === 'work') {
      await createWorkComment(props.targetId, { 
        content: replyContent.value,
        parent_id: props.comment.id
      })
    } else {
      await createPostComment(props.targetId, { 
        content: replyContent.value,
        parent_id: props.comment.id
      })
    }
    
    showToast({ type: 'success', message: '回复成功' })
    replyContent.value = ''
    showReplyInput.value = false
    
    // 通知父组件刷新
    emit('reply-success')
  } catch (error) {
    console.error('回复失败:', error)
    showToast({ type: 'fail', message: '回复失败' })
  } finally {
    submittingReply.value = false
  }
}

// 处理子组件回复成功
function handleReplySuccess() {
  emit('reply-success')
}
</script>

<style scoped>
.comment-item {
  margin-bottom: 16px;
}

.comment-main {
  display: flex;
  gap: 12px;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--light-matcha);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.comment-bubble {
  background: var(--pure-white);
  padding: 12px 16px;
  border-radius: 16px;
  border-top-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.comment-author {
  font-size: 14px;
  font-weight: 600;
  color: var(--matcha-green);
}

.comment-time {
  font-size: 12px;
  color: var(--text-light);
}

.comment-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.comment-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s;
}

.action-btn:hover {
  color: var(--matcha-green);
}

.reply-input-box {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #F5F5F5;
}

.reply-input-box :deep(.van-field) {
  padding: 0;
  background: transparent;
  margin-bottom: 8px;
}

.reply-input-box :deep(.van-button) {
  float: right;
}

/* 嵌套回复列表 */
.replies-list {
  margin-left: 48px;
  margin-top: 12px;
  padding-left: 12px;
  border-left: 2px solid #F0F0F0;
}

.reply-item-wrapper {
  margin-bottom: 12px;
}

.reply-item-wrapper:last-child {
  margin-bottom: 0;
}
</style>
