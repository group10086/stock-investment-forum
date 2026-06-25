<template>
  <div class="main-layout">
    <!-- 顶部导航栏 -->
    <header class="navbar">
      <div class="navbar-content">
        <!-- Logo -->
        <router-link to="/" class="logo">
          <el-icon :size="24"><TrendCharts /></el-icon>
          <span>股票投资论坛</span>
        </router-link>

        <!-- 搜索框 -->
        <div class="search-box">
          <el-autocomplete
            v-model="searchKeyword"
            :fetch-suggestions="querySearch"
            placeholder="搜索帖子、用户、股票代码..."
            :prefix-icon="Search"
            clearable
            @keyup.enter="handleSearch"
            @select="handleSelect"
            popper-class="search-suggestions"
          >
            <template #default="{ item }">
              <div class="suggestion-item">
                <el-icon><component :is="item.icon" /></el-icon>
                <span>{{ item.value }}</span>
                <el-tag size="small" type="info">{{ item.type }}</el-tag>
              </div>
            </template>
          </el-autocomplete>
          
          <!-- 热门搜索 -->
          <div v-if="!searchKeyword && showHotSearch" class="hot-search">
            <span class="hot-label">热搜：</span>
            <el-tag
              v-for="(tag, index) in hotSearchTags"
              :key="index"
              size="small"
              @click="searchKeyword = tag"
              style="cursor: pointer; margin-right: 4px;"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <!-- 右侧操作区 -->
        <div class="navbar-actions">
          <!-- 消息通知 -->
          <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="notification-bell">
            <el-button circle @click="$router.push('/messages')">
              <el-icon><Bell /></el-icon>
            </el-button>
          </el-badge>

          <!-- 未登录 -->
          <template v-if="!userStore.isLoggedIn">
            <el-button type="primary" @click="$router.push('/login')">登录</el-button>
            <el-button @click="$router.push('/register')">注册</el-button>
          </template>

          <!-- 已登录 -->
          <template v-else>
            <el-dropdown @command="handleUserMenu">
              <div class="user-info">
                <el-avatar :size="32" :src="userStore.currentUser.avatar">
                  {{ userStore.currentUser.nickname?.charAt(0) }}
                </el-avatar>
                <span class="username">{{ userStore.currentUser.nickname }}</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon> 个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="myPosts">
                    <el-icon><Document /></el-icon> 我的帖子
                  </el-dropdown-item>
                  <el-dropdown-item command="bookmarks">
                    <el-icon><Star /></el-icon> 我的收藏
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon> 退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </div>
      </div>
    </header>

    <!-- 主体内容区 -->
    <div class="main-container">
      <!-- 左侧边栏 -->
      <aside class="left-sidebar">
        <el-menu :default-active="activeMenu" router @select="handleMenuSelect">
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页/热榜</span>
          </el-menu-item>
          <el-menu-item index="/following" v-if="userStore.isLoggedIn">
            <el-icon><UserFilled /></el-icon>
            <span>关注动态</span>
          </el-menu-item>
          <el-menu-item index="/stock-discuss">
            <el-icon><DataAnalysis /></el-icon>
            <span>自选股讨论</span>
          </el-menu-item>
          <el-menu-item index="/my-groups" v-if="userStore.isLoggedIn">
            <el-icon><ChatDotRound /></el-icon>
            <span>我的群组</span>
          </el-menu-item>
          <el-menu-item index="/bookmarks" v-if="userStore.isLoggedIn">
            <el-icon><StarFilled /></el-icon>
            <span>收藏夹</span>
          </el-menu-item>
          <el-menu-item index="/my-posts" v-if="userStore.isLoggedIn">
            <el-icon><Document /></el-icon>
            <span>我的帖子</span>
          </el-menu-item>
        </el-menu>
      </aside>

      <!-- 中间内容区 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <!-- 右侧边栏 -->
      <aside class="right-sidebar">
        <!-- 今日股市概览 -->
        <div class="sidebar-card">
          <h3>今日股市概览</h3>
          <div class="stock-index">
            <div class="index-item">
              <span class="index-name">上证指数</span>
              <span class="index-value up">3,285.62 +1.25%</span>
            </div>
            <div class="index-item">
              <span class="index-name">深证成指</span>
              <span class="index-value up">10,678.34 +0.89%</span>
            </div>
            <div class="index-item">
              <span class="index-name">创业板指</span>
              <span class="index-value down">2,156.78 -0.32%</span>
            </div>
          </div>
        </div>

        <!-- 热门话题 -->
        <div class="sidebar-card">
          <h3>热门话题</h3>
          <div class="hot-topics">
            <el-tag v-for="topic in hotTopics" :key="topic" class="topic-tag">
              #{{ topic }}
            </el-tag>
          </div>
        </div>

        <!-- 推荐用户（待后端推荐接口完成后启用） -->
        <!--
        <div class="sidebar-card" v-if="userStore.isLoggedIn">
          <h3>推荐关注</h3>
          <div class="recommended-users">
            <div v-for="user in recommendedUsers" :key="user.id" class="user-item">
              ...
            </div>
          </div>
        </div>
        -->
      </aside>
    </div>

    <!-- 底部信息栏 -->
    <footer class="footer">
      <div class="footer-content">
        <p>© 2026 股票投资论坛 | 课程设计项目</p>
        <p>友情链接：东方财富 | 雪球 | 同花顺</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Search, Bell, User, Document, Star, SwitchButton, 
  TrendCharts, HomeFilled, UserFilled, DataAnalysis, ChatDotRound, StarFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { authApi, messageApi } from '@/api'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')
const showHotSearch = ref(false)
const unreadCount = ref(0)

// 获取未读消息数
const fetchUnreadCount = async () => {
  if (!userStore.isLoggedIn) return
  try {
    const res = await messageApi.getUnreadCount()
    unreadCount.value = res.data.count || 0
  } catch {
    // 静默失败
  }
}

// 路由变化时刷新未读数
watch(() => route.path, (path) => {
  if (path.startsWith('/messages')) {
    setTimeout(fetchUnreadCount, 500) // 等消息标记已读后再刷新
  } else {
    fetchUnreadCount()
  }
})

onMounted(() => {
  fetchUnreadCount()
})

const hotTopics = ref([
  'A股', '港股', '美股', '基金定投', '价值投资', '技术分析', '财报分析'
])
// 搜索建议数据（模拟）
const searchSuggestions = ref([
  { value: '阿里巴巴', type: '股票', icon: 'TrendCharts' },
  { value: '阿里云', type: '概念', icon: 'DataAnalysis' },
  { value: '阿里健康', type: '股票', icon: 'TrendCharts' },
  { value: '巴菲特', type: '用户', icon: 'UserFilled' },
  { value: '价值投资策略', type: '帖子', icon: 'Document' },
  { value: '贵州茅台', type: '股票', icon: 'TrendCharts' },
  { value: '腾讯控股', type: '股票', icon: 'TrendCharts' },
  { value: '新能源基金', type: '基金', icon: 'StarFilled' }
])

const recommendedUsers = ref([
  { id: 1, nickname: '投资达人', bio: '10年投资经验', avatar: '' },
  { id: 2, nickname: '量化分析师', bio: '专注量化交易', avatar: '' },
  { id: 3, nickname: '价值投资者', bio: '长期价值投资', avatar: '' }
])

const activeMenu = computed(() => {
  if (route.path.startsWith('/following')) return '/following'
  if (route.path.startsWith('/stock-discuss')) return '/stock-discuss'
  if (route.path.startsWith('/my-groups')) return '/my-groups'
  if (route.path.startsWith('/bookmarks')) return '/bookmarks'
  if (route.path.startsWith('/my-posts')) return '/my-posts'
  return '/'
})

const handleSearch = () => {
  const kw = searchKeyword.value.trim()
  if (!kw) return
  router.push(`/search?keyword=${encodeURIComponent(kw)}`)
}

// 搜索联想 - 防抖处理
let searchTimer = null
const querySearch = (queryString, cb) => {
  clearTimeout(searchTimer)
  
  searchTimer = setTimeout(() => {
    if (!queryString) {
      cb([])
      return
    }
    
    const keyword = queryString.toLowerCase()
    const results = searchSuggestions.value.filter(item => 
      item.value.toLowerCase().includes(keyword)
    )
    
    cb(results)
  }, 300)
}

const handleSelect = (item) => {
  searchKeyword.value = item.value
  handleSearch()
}

const handleUserMenu = (command) => {
  switch (command) {
    case 'profile':
      router.push(`/user/${userStore.currentUser.id}`)
      break
    case 'myPosts':
      ElMessage.info('我的帖子功能开发中')
      break
    case 'bookmarks':
      ElMessage.info('收藏功能开发中')
      break
    case 'logout':
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
      break
  }
}

const handleFollowRecommend = async (user) => {
  try {
    await authApi.followUser(user.id)
    ElMessage.success(`已关注 ${user.nickname}`)
  } catch (error) {
    if (error.response?.status === 401) {
      ElMessage.warning('请先登录后关注')
    } else {
      ElMessage.error(error.response?.data?.detail || '关注失败')
    }
  }
}

const handleMenuSelect = (index) => {
  if (index === '/' || index === '/following' || index === '/bookmarks' || index === '/my-posts'
    || index === '/stock-discuss' || index === '/my-groups') return
  ElMessage.info('功能开发中，敬请期待')
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏 */
.navbar {
  height: 64px;
  background: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-content {
  max-width: 1440px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--primary-color);
  font-weight: bold;
  font-size: 20px;
  flex-shrink: 0;
  text-decoration: none;
}

.search-box {
  flex: 1;
  max-width: 500px;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.notification-bell {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.search-box {
  flex: 1;
  max-width: 500px;
  position: relative;
}

.hot-search {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.hot-label {
  margin-right: 4px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
}

.suggestion-item .el-icon {
  color: var(--primary-color);
}

.suggestion-item span {
  flex: 1;
}
.user-info:hover {
  background: var(--primary-light);
}

.username {
  font-size: 14px;
  color: var(--text-primary);
}

/* 主体容器 */
.main-container {
  flex: 1;
  max-width: 1440px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  gap: 24px;
  padding: 24px;
  background: var(--bg-color);
  min-height: calc(100vh - 64px - 120px);
}

/* 左侧边栏 */
.left-sidebar {
  width: 200px;
  flex-shrink: 0;
  background: #FFFFFF;
  border-radius: 8px;
  height: fit-content;
  position: sticky;
  top: 88px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.left-sidebar .el-menu {
  border-right: none;
}

.left-sidebar .el-menu-item.is-active {
  background-color: var(--primary-light) !important;
  color: var(--primary-color) !important;
  font-weight: 600;
}

/* 中间内容区 */
.main-content {
  flex: 1;
  min-width: 600px;
}

/* 右侧边栏 */
.right-sidebar {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-card {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.sidebar-card h3 {
  font-size: 16px;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.stock-index {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.index-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.index-name {
  color: var(--text-secondary);
}

.index-value {
  font-weight: 500;
}

.index-value.up {
  color: var(--success-color);
}

.index-value.down {
  color: var(--error-color);
}

.hot-topics {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.topic-tag {
  cursor: pointer;
}

.recommended-users {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-item .user-info {
  flex: 1;
  padding: 0;
}

.user-item .user-name {
  font-size: 14px;
  color: var(--text-primary);
}

.user-item .user-desc {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 底部信息栏 */
.footer {
  background: #FFFFFF;
  padding: 24px;
  margin-top: auto;
}

.footer-content {
  max-width: 1440px;
  margin: 0 auto;
  text-align: center;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.8;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
