import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/components/layout/MainLayout.vue'),
    children: [
      // 首页
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/home/Index.vue'),
        meta: { title: '首页' }
      },
      // 帖子详情
      {
        path: 'post/:id',
        name: 'PostDetail',
        component: () => import('@/views/post/Detail.vue'),
        meta: { title: '帖子详情' }
      },
      // 发帖
      {
        path: 'post/create',
        name: 'PostCreate',
        component: () => import('@/views/post/Create.vue'),
        meta: { title: '发布帖子', requiresAuth: true }
      },
      // 编辑帖子
      {
        path: 'post/:id/edit',
        name: 'PostEdit',
        component: () => import('@/views/post/Edit.vue'),
        meta: { title: '编辑帖子', requiresAuth: true }
      },
      // 用户中心
      {
        path: 'user/:id',
        name: 'UserProfile',
        component: () => import('@/views/user/Profile.vue'),
        meta: { title: '用户中心' }
      },
      // 个人资料编辑
      {
        path: 'profile/edit',
        name: 'ProfileEdit',
        component: () => import('@/views/user/EditProfile.vue'),
        meta: { title: '编辑资料', requiresAuth: true }
      },
      // 关注列表
      {
        path: 'following',
        name: 'Following',
        component: () => import('@/views/user/Following.vue'),
        meta: { title: '我的关注', requiresAuth: true }
      },
      // 粉丝列表
      {
        path: 'followers',
        name: 'Followers',
        component: () => import('@/views/user/Followers.vue'),
        meta: { title: '我的粉丝', requiresAuth: true }
      },
      // 私信
      {
        path: 'messages/:userId?',
        name: 'Messages',
        component: () => import('@/views/messages/Index.vue'),
        meta: { title: '私信', requiresAuth: true }
      }
    ]
  },
  // 登录
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: '登录' }
  },
  // 注册
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { title: '注册' }
  },
  // 手机号注册
  {
    path: '/register-phone',
    name: 'RegisterPhone',
    component: () => import('@/views/auth/RegisterPhone.vue'),
    meta: { title: '手机号注册' }
  },
  // 分级认证
  {
    path: '/authentication',
    name: 'Authentication',
    component: () => import('@/views/auth/Authentication.vue'),
    meta: { title: '身份认证', requiresAuth: true }
  },
  // 投资者适当性问卷
  {
    path: '/questionnaire',
    name: 'Questionnaire',
    component: () => import('@/views/auth/Questionnaire.vue'),
    meta: { title: '风险评估问卷', requiresAuth: true }
  },
  // 成就系统
  {
    path: '/achievement',
    name: 'Achievement',
    component: () => import('@/views/user/Achievement.vue'),
    meta: { title: '成就中心', requiresAuth: true }
  },
  // 搜索
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/home/Search.vue'),
    meta: { title: '搜索结果' }
  },
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面不存在' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 股票投资论坛` : '股票投资论坛'

  const userStore = useUserStore()

  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // 已登录用户访问登录/注册页，重定向到首页
  if ((to.name === 'Login' || to.name === 'Register' || to.name === 'RegisterPhone') && userStore.isLoggedIn) {
    next({ name: 'Home' })
    return
  }
  next()
})

export default router
