import http from '@/api/http'
import type { Work, ApiResponse } from '@/types/api'

// 获取作品列表
export function getWorks(skip: number = 0, limit: number = 20) {
  return http.get<Work[]>('/works/', {
    params: { skip, limit }
  })
}

// 获取作品详情
export function getWorkById(workId: number) {
  return http.get<Work>(`/works/${workId}`)
}

// 创建作品
export function createWork(data: {
  title: string
  content: string
  cover_image?: string | null
  status?: number
  is_published?: boolean
}) {
  return http.post<Work>('/works/', data)
}

// 更新作品
export function updateWork(workId: number, data: {
  title?: string
  content?: string
  cover_image?: string | null
  status?: number
  is_published?: boolean
}) {
  return http.put<Work>(`/works/${workId}`, data)
}

// 删除作品
export function deleteWork(workId: number) {
  return http.delete<ApiResponse<{ message: string }>>(`/works/${workId}`)
}

// 上传封面图片
export function uploadCover(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  // 后端直接返回 { filename, url },不使用ApiResponse包装
  return http.post<{ filename: string; url: string }>('/works/upload-cover', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 点赞/取消点赞
export function toggleLike(workId: number) {
  return http.post<{ message: string; count: number }>(`/works/${workId}/like`)
}

// 收藏/取消收藏
export function toggleFavorite(workId: number) {
  return http.post<{ message: string; count: number }>(`/works/${workId}/favorite`)
}

// 获取作品评论列表
export function getWorkComments(workId: number) {
  return http.get<any[]>(`/works/${workId}/comments`)
}

// 发表评论
export function createWorkComment(workId: number, data: { content: string }) {
  return http.post<any>(`/works/${workId}/comments`, data)
}

// 获取用户互动状态
export function getInteractionStatus(workId: number) {
  return http.get<{ is_liked: boolean; is_favorited: boolean; like_count: number; favorite_count: number }>(`/works/${workId}/interaction-status`)
}

// 获取我的收藏列表
export function getMyFavorites() {
  return http.get<Work[]>('/favorites')
}

// ==================== 论坛相关 API ====================

// 获取帖子列表
export function getForumPosts(skip: number = 0, limit: number = 20) {
  return http.get<any[]>('/forum/posts', {
    params: { skip, limit }
  })
}

// 获取帖子详情
export function getForumPostById(postId: number) {
  return http.get<any>(`/forum/posts/${postId}`)
}

// 创建帖子
export function createForumPost(data: { title: string; content: string }) {
  return http.post<any>('/forum/posts', data)
}

// 获取帖子回复列表
export function getPostComments(postId: number) {
  return http.get<any[]>(`/forum/posts/${postId}/comments`)
}

// 发表回复
export function createPostComment(postId: number, data: { content: string; parent_id?: number | null }) {
  return http.post<any>(`/forum/posts/${postId}/comments`, data)
}

// ==================== 消息通知相关 API ====================

// 获取我的通知列表
export function getNotifications() {
  return http.get<any[]>('/notifications/')
}

// 标记通知为已读
export function markNotificationAsRead(notificationId: number) {
  return http.put<{ message: string }>(`/notifications/${notificationId}/read`)
}

// 全部标记为已读
export function markAllAsRead() {
  return http.put<{ message: string }>('/notifications/read-all')
}
