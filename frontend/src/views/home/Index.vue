<template>
  <div class="home-page">
    <!-- 筛选标签 -->
    <div class="filter-tabs">
      <el-tabs v-model="activeTab" @tab-click="handleTabChange">
        <el-tab-pane label="最新" name="latest" />
        <el-tab-pane label="最热" name="hot" />
        <el-tab-pane label="精华" name="essence" />
        <el-tab-pane v-if="userStore.isLoggedIn" label="关注" name="following" />
      </el-tabs>
      <el-button type="primary" @click="$router.push('/post/create')">
        <el-icon><Plus /></el-icon>
        发布帖子
      </el-button>
    </div>

    <!-- 帖子列表 -->
    <div class="post-list" v-loading="loading">
      <div
        v-for="post in postList"
        :key="post.id"
        class="post-card"
        @click="goToPost(post.id)"
      >
        <!-- 帖子头部 -->
        <div class="post-header">
          <el-avatar :size="36" :src="post.user?.avatar">
            {{ post.user?.nickname?.charAt(0) }}
          </el-avatar>
          <div class="post-user-info">
            <div class="user-name">{{ post.user?.nickname }}</div>
            <div class="post-time">{{ formatTime(post.created_at) }}</div>
          </div>
          <div class="post-tags">
            <el-tag v-if="post.is_top" type="danger" size="small">置顶</el-tag>
            <el-tag v-if="post.is_essence" type="warning" size="small">精华</el-tag>
            <el-tag v-if="post.is_hot" type="primary" size="small">热门</el-tag>
          </div>
        </div>

        <!-- 帖子内容 -->
        <div class="post-content">
          <h3 class="post-title">{{ post.title }}</h3>
          <p class="post-summary">{{ post.summary }}</p>
          <div v-if="post.images?.length" class="post-images">
            <img
              v-for="(img, index) in post.images.slice(0, 3)"
              :key="index"
              :src="img"
              class="post-image"
            />
          </div>
        </div>

        <!-- 帖子底部 -->
        <div class="post-footer">
          <span class="post-action" @click.stop="handleLike(post)">
            <el-icon><component :is="post.is_liked ? 'StarFilled' : 'Star'" /></el-icon>
            <span :class="{ 'liked': post.is_liked }">{{ post.like_count }}</span>
          </span>
          <span class="post-action">
            <el-icon><ChatDotRound /></el-icon>
            <span>{{ post.comment_count }}</span>
          </span>
          <span class="post-action">
            <el-icon><View /></el-icon>
            <span>{{ post.view_count }}</span>
          </span>
          <span class="post-action" @click.stop="handleBookmark(post)">
            <el-icon><component :is="post.is_bookmarked ? 'StarFilled' : 'Star'" /></el-icon>
          </span>
        </div>
      </div>

      <!-- 空状态 -->
      <el-empty v-if="!loading && postList.length === 0" description="暂无帖子" />

      <!-- 加载更多 -->
      <div v-if="hasMore" class="load-more">
        <el-button @click="loadMore" :loading="loadingMore">
          {{ loadingMore ? '加载中...' : '加载更多' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { postApi } from '@/api'
import { ElMessage } from 'element-plus'
import { Plus, ChatDotRound, View } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('latest')
const postList = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const page = ref(1)
const pageSize = ref(10)
const hasMore = ref(true)

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  return date.toLocaleDateString()
}

const loadPosts = async (reset = false) => {
  if (reset) {
    page.value = 1
    postList.value = []
  }
  
  const params = {
    page: page.value,
    pageSize: pageSize.value,
    sort: activeTab.value === 'latest' ? 'newest' :
          activeTab.value === 'hot' ? 'hot' :
          activeTab.value === 'essence' ? 'essence' : 'following'
  }

  try {
    const res = await postApi.getPostList(params)
    if (reset) {
      postList.value = res.data.list
    } else {
      postList.value = [...postList.value, ...res.data.list]
    }
    hasMore.value = res.data.hasMore
  } catch (error) {
    ElMessage.error('加载帖子失败')
  }
}

const handleTabChange = () => {
  loadPosts(true)
}

const loadMore = () => {
  if (loadingMore.value || !hasMore.value) return
  loadingMore.value = true
  page.value++
  loadPosts(false).finally(() => {
    loadingMore.value = false
  })
}

const goToPost = (id) => {
  router.push(`/post/${id}`)
}

const handleLike = async (post) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    if (post.is_liked) {
      await postApi.unlikePost(post.id)
      post.is_liked = false
      post.like_count--
    } else {
      await postApi.likePost(post.id)
      post.is_liked = true
      post.like_count++
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleBookmark = async (post) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    if (post.is_bookmarked) {
      await postApi.unbookmarkPost(post.id)
      post.is_bookmarked = false
      ElMessage.success('已取消收藏')
    } else {
      await postApi.bookmarkPost(post.id)
      post.is_bookmarked = true
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadPosts(true)
})
</script>

<style scoped>
.home-page {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-tabs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 16px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  padding: 16px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s ease;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.post-user-info {
  flex: 1;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.post-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.post-tags {
  display: flex;
  gap: 6px;
}

.post-content {
  margin-bottom: 12px;
}

.post-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-summary {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-images {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.post-image {
  width: 120px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.post-footer {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-top: 12px;
  border-top: 1px solid #F0F0F0;
}

.post-action {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
}

.post-action:hover {
  color: var(--primary-color);
}

.post-action .liked {
  color: #FAAD14;
}

.load-more {
  text-align: center;
  padding-top: 20px;
}
</style>
