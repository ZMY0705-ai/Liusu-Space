import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/ui/pages/AuthLogin.vue'),
      meta: { requiresAuth: false, layout: 'fullscreen' }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/ui/pages/AuthRegister.vue'),
      meta: { requiresAuth: false, layout: 'fullscreen' }
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('@/ui/pages/HomeFeed.vue'),
      meta: { requiresAuth: false, layout: 'mobile' }
    },
    {
      path: '/work/:id',
      name: 'WorkDetail',
      component: () => import('@/ui/pages/WorkDetail.vue'),
      meta: { requiresAuth: false, layout: 'mobile' }
    },
    {
      path: '/editor',
      name: 'Editor',
      component: () => import('@/ui/pages/EditorWork.vue'),
      meta: { requiresAuth: true, layout: 'mobile' }
    },
    {
      path: '/editor/:id',
      name: 'EditorEdit',
      component: () => import('@/ui/pages/EditorWork.vue'),
      meta: { requiresAuth: true, layout: 'mobile' }
    },
    {
      path: '/forum',
      name: 'Forum',
      component: () => import('@/ui/pages/ForumList.vue'),
      meta: { requiresAuth: false, layout: 'mobile' }
    },
    {
      path: '/forum/post/:id',
      name: 'ForumDetail',
      component: () => import('@/ui/pages/ForumDetail.vue'),
      meta: { requiresAuth: false, layout: 'mobile' }
    },
    {
      path: '/forum/create',
      name: 'ForumCreate',
      component: () => import('@/ui/pages/ForumCreate.vue'),
      meta: { requiresAuth: true, layout: 'mobile' }
    },
    {
      path: '/me',
      name: 'Me',
      component: () => import('@/ui/pages/MeCenter.vue'),
      meta: { requiresAuth: true, layout: 'mobile' }
    },
    {
      path: '/user/:id',
      name: 'UserProfile',
      component: () => import('@/ui/pages/UserProfile.vue'),
      meta: { requiresAuth: false, layout: 'mobile' }
    },
    {
      path: '/profile/edit',
      name: 'EditProfile',
      component: () => import('@/ui/pages/EditProfile.vue'),
      meta: { requiresAuth: true, layout: 'mobile' }
    },
    {
      path: '/notifications',
      name: 'Notifications',
      component: () => import('@/ui/pages/Notifications.vue'),
      meta: { requiresAuth: true, layout: 'mobile' }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 初始化认证状态
  if (!authStore.token) {
    authStore.initAuth()
  }
  
  // 需要登录的页面
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && authStore.isAuthenticated) {
    // 已登录用户访问登录页，重定向到首页
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
