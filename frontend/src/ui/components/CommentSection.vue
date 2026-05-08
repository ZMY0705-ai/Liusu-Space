<template>
  <div class="comment-section">
    <!-- 标题 -->
    <h3 class="section-title">💬 {{ targetType === 'work' ? '评论' : '回复' }} ({{ totalComments }})</h3>
    
    <!-- 评论列表 -->
    <div v-if="comments.length > 0" class="comments-list">
      <CommentItem 
        v-for="comment in comments" 
        :key="comment.id"
        :comment="comment"
        :target-id="targetId"
        :target-type="targetType"
        @reply-success="handleReplySuccess"
      />
    </div>
    
    <!-- 空状态 -->
    <div v-else class="empty-comments">
      <p>暂无{{ targetType === 'work' ? '评论' : '回复' }}，快来发表第一个{{ targetType === 'work' ? '评论' : '回复' }}吧！</p>
    </div>

    <!-- 发表评论 -->
    <div class="comment-input-section">
      <van-field
        v-model="commentContent"
        type="textarea"
        :placeholder="`写下你的${targetType === 'work' ? '想法' : '回复'}...`"
        rows="3"
        autosize
        maxlength="500"
        show-word-limit
      />
      <van-button 
        type="primary" 
        size="small"
        @click="handleSubmitComment"
        :loading="submittingComment"
        color="#64A386"
        block
      >
        发表{{ targetType === 'work' ? '评论' : '回复' }}
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getWorkComments, createWorkComment, getPostComments, createPostComment } from '@/api/work'
import { showToast } from 'vant'
import CommentItem from './CommentItem.vue'

const props = defineProps<{
  targetId: number
  targetType: 'work' | 'post'
}>()

const router = useRouter()
const authStore = useAuthStore()

// 数据状态
const comments = ref<any[]>([])
const commentContent = ref('')
const submittingComment = ref(false)

// 总评论数（包括所有嵌套回复）
const totalComments = computed(() => {
  function countComments(list: any[]): number {
    let count = 0
    for (const item of list) {
      count += 1 + countComments(item.replies || [])
    }
    return count
  }
  return countComments(comments.value)
})

// 加载评论列表
async function loadComments() {
  try {
    let response
    if (props.targetType === 'work') {
      response = await getWorkComments(props.targetId)
    } else {
      response = await getPostComments(props.targetId)
    }
    comments.value = response.data || []
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

// 发表评论
async function handleSubmitComment() {
  if (!authStore.isAuthenticated) {
    showToast({ type: 'fail', message: '请先登录' })
    router.push({ name: 'Login', query: { redirect: window.location.pathname } })
    return
  }
  
  if (!commentContent.value.trim()) {
    showToast({ type: 'fail', message: '请输入评论内容' })
    return
  }
  
  submittingComment.value = true
  try {
    if (props.targetType === 'work') {
      await createWorkComment(props.targetId, { content: commentContent.value })
    } else {
      await createPostComment(props.targetId, { content: commentContent.value })
    }
    
    showToast({ type: 'success', message: '评论成功' })
    commentContent.value = ''
    
    // 重新加载评论列表
    await loadComments()
  } catch (error) {
    console.error('评论失败:', error)
    showToast({ type: 'fail', message: '评论失败' })
  } finally {
    submittingComment.value = false
  }
}

// 处理回复成功事件
function handleReplySuccess() {
  loadComments()
}

// 初始化
onMounted(() => {
  loadComments()
})
</script>

<style scoped>
.comment-section {
  margin-top: 30px;
  padding: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-dark);
  margin-bottom: 20px;
  padding-left: 8px;
  border-left: 4px solid var(--lemon-yellow);
}

.comments-list {
  margin-bottom: 20px;
}

.empty-comments {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.empty-comments p {
  font-size: 14px;
}

.comment-input-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #F5F5F5;
}

.comment-input-section :deep(.van-field) {
  padding: 0;
  background: transparent;
}

.comment-input-section :deep(.van-button) {
  margin-top: 12px;
  height: 44px;
  font-size: 15px;
  border-radius: 22px;
}
</style>
