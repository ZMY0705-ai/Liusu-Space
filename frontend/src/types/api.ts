// API响应基础类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 用户相关类型
export interface User {
  id: number
  account: string
  nickname: string
  real_name?: string
  student_id?: string
  major?: string
  avatar?: string
  signature?: string
  bio?: string
  is_real_name_public?: boolean
  is_major_public?: boolean
  role: number
  created_at: string
  updated_at: string
}

// 登录请求
export interface LoginRequest {
  account: string
  password: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  token_type: string
}

// 注册请求
export interface RegisterRequest {
  account: string
  password: string
  nickname: string
  real_name?: string
  student_id?: string
  major?: string
}

// 更新用户信息
export interface UserUpdate {
  nickname?: string
  real_name?: string
  student_id?: string
  major?: string
  avatar?: string
  signature?: string
  bio?: string
  is_real_name_public?: boolean
  is_major_public?: boolean
}

// 作品相关类型
export interface Work {
  id: number
  author_id: number
  title: string
  content: string
  cover_image: string | null
  status: number
  view_count: number
  like_count: number
  comment_count: number
  favorite_count: number
  created_at: string
  published_at: string | null
  author?: User
}

// 作品创建请求
export interface WorkCreate {
  title: string
  content: string
  cover_image?: string | null
  status?: number
}

// 作品更新请求
export interface WorkUpdate {
  title?: string
  content?: string
  cover_image?: string | null
  status?: number
}

// 作品评论
export interface WorkComment {
  id: number
  work_id: number
  user_id: number
  content: string
  created_at: string
  user?: User
}

// 论坛帖子
export interface ForumPost {
  id: number
  author_id: number
  title: string
  content: string
  comment_count: number
  created_at: string
  updated_at: string
  author?: User
}

// 帖子评论
export interface PostComment {
  id: number
  post_id: number
  user_id: number
  parent_id: number | null
  content: string
  created_at: string
  user?: User
}

// 通知
export interface Notification {
  id: number
  user_id: number
  type: string // like, comment, favorite, reply
  sender_id: number
  target_type: string // work, post
  target_id: number
  content: string | null
  is_read: boolean
  created_at: string
  sender?: User
}
