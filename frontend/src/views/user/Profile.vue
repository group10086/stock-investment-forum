<template>
  <div class="profile-page" v-loading="loading">
    <template v-if="user">
      <!-- 用户头部 -->
      <div class="profile-header">
        <div class="cover-image"></div>
        <div class="profile-info">
          <el-avatar :size="80" :src="user.avatar">
            {{ user.nickname?.charAt(0) }}
          </el-avatar>
          <div class="user-details">
            <h2 class="user-name">
              {{ user.nickname }}
              <el-tag v-if="user.is_verified" type="success" size="small">认证</el-tag>
            </h2>
            <p class="user-bio">{{ user.bio || '这个人很懒，什么都没有留下~' }}</p>
          </div>
          <div v-if="userStore.currentUser?.id !== user.id" class="profile-actions">
            <el-button
              :type="user.is_following ? 'default' : 'primary'"
              @click="handleFollow"
            >
              {{ user.is_following ? '已关注' : '关注' }}
            </el-button>
            <el-button @click="startChat">
              <el-icon><ChatDotRound /></el-icon> 私信
            </el-button>
          </div>
          <div v-else class="profile-actions">
            <el-button type="primary" @click="$router.push('/profile/edit')">
              <el-icon><Edit /></el-icon> 编辑资料
            </el-button>
          </div>
        </div>
        <!-- 统计数据 -->
        <div class="profile-stats">
          <div class="stat-item">
            <span class="stat-value">{{ user.post_count || 0 }}</span>
            <span class="stat-label">帖子</span>
          </div>
          <div class="stat-item" @click="$router.push('/following')">
            <span class="stat-value">{{ user.following_count || 0 }}</span>
            <span class="stat-label">关注</span>
          </div>
          <div class="stat-item" @click="$router.push('/followers')">
            <span class="stat-value">{{ user.follower_count || 0 }}</span>
            <span class="stat-label">粉丝</span>
          </div>
        </div>
      </div>

      <!-- 内容标签页 -->
      <div class="profile-content">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="他的帖子" name="posts">
            <div v-if="userPosts.length > 0" class="post-list">
              <div
                v-for="post in userPosts"
                :key="post.id"
                class="post-item"
                @click="$router.push(`/post/${post.id}`)"
              >
                <h3 class="post-title">{{ post.title }}</h3>
                <p class="post-summary">{{ post.summary }}</p>
                <div class="post-meta">
                  <span>{{ post.like_count }} 点赞</span>
                  <span>{{ post.comment_count }} 评论</span>
                  <span>{{ formatTime(post.created_at) }}</span>
                </div>
              </div>
            </div>
            <el-empty v-else description="暂无帖子" />
          </el-tab-pane>

          <el-tab-pane label="他的收藏" name="bookmarks">
            <div v-if="bookmarks.length > 0" class="post-list">
              <div
                v-for="post in bookmarks"
                :key="post.id"
                class="post-item"
                @click="$router.push(`/post/${post.id}`)"
              >
                <h3 class="post-title">{{ post.title }}</h3>
                <p class="post-summary">{{ post.summary }}</p>
              </div>
            </div>
            <el-empty v-else description="暂无收藏" />
          </el-tab-pane>

          <el-tab-pane label="关于" name="about">
            <div class="about-section">
              <div class="info-item">
                <span class="info-label">注册时间</span>
                <span class="info-value">{{ formatDate(user.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">投资偏好</span>
                <span class="info-value">{{ user.investment_preference?.join('、') || '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">GitHub</span>
                <a v-if="user.github" :href="user.github" target="_blank">{{ user.github }}</a>
                <span v-else class="info-value">未绑定</span>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { authApi, postApi } from '@/api'
import { ElMessage } from 'element-plus'
import { Edit, ChatDotRound } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const user = ref(null)
const userPosts = ref([])
const bookmarks = ref([])
const activeTab = ref('posts')

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const diff = Date.now() - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleDateString()
}

const formatDate = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleDateString('zh-CN')
}

const loadUserProfile = async () => {
  loading.value = true
  try {
    const res = await authApi.getUserDetail(route.params.id)
    user.value = res.data
  } catch (error) {
    ElMessage.error('加载用户信息失败')
  } finally {
    loading.value = false
  }
}

const loadUserPosts = async () => {
  try {
    const res = await postApi.getPostList({ user_id: route.params.id, page: 1, pageSize: 10 })
    userPosts.value = res.data.list || []
  } catch (error) {
    console.error('加载用户帖子失败', error)
  }
}

const handleFollow = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    if (user.value.is_following) {
      await authApi.unfollowUser(user.value.id)
      user.value.is_following = false
      user.value.follower_count--
      ElMessage.success('已取消关注')
    } else {
      await authApi.followUser(user.value.id)
      user.value.is_following = true
      user.value.follower_count++
      ElMessage.success('关注成功')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const startChat = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  router.push(`/messages/${user.value.id}`)
}

onMounted(() => {
  loadUserProfile()
  loadUserPosts()
})
</script>

<style scoped>
.profile-page {
  background: #FFFFFF;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.profile-header {
  position: relative;
}

.cover-image {
  height: 120px;
  background: linear-gradient(135deg, #1890FF 0%, #096DD9 100%);
}

.profile-info {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  padding: 0 24px;
  margin-top: -40px;
  position: relative;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-bio {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.profile-actions {
  display: flex;
  gap: 8px;
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  padding: 24px;
  border-top: 1px solid #F0F0F0;
}

.stat-item {
  text-align: center;
  cursor: pointer;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.profile-content {
  padding: 24px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-item {
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #F0F0F0;
  cursor: pointer;
  transition: all 0.2s;
}

.post-item:hover {
  border-color: var(--primary-color);
  background: var(--primary-light);
}

.post-title {
  font-size: 16px;
  margin: 0 0 8px;
}

.post-summary {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0 0 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: var(--text-secondary);
}

.about-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #F0F0F0;
}

.info-label {
  color: var(--text-secondary);
}

.info-value {
  color: var(--text-primary);
}
</style>
