<template>
  <div class="bookmarks-page">
    <h2 class="page-title">我的收藏</h2>
    <div v-loading="loading" class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-item" @click="$router.push(`/post/${post.id}`)">
        <div class="post-header">
          <el-avatar :size="32" :src="post.user?.avatar">{{ post.user?.nickname?.charAt(0) }}</el-avatar>
          <span class="post-author">{{ post.user?.nickname }}</span>
          <span class="post-time">{{ formatTime(post.created_at) }}</span>
        </div>
        <h3 class="post-title">{{ post.title }}</h3>
        <p class="post-summary">{{ post.summary || post.content?.replace(/<[^>]+>/g, '').substring(0, 150) }}</p>
        <div class="post-footer">
          <el-tag v-for="tag in (post.tags || [])" :key="tag" size="small" class="tag">{{ tag }}</el-tag>
          <div class="post-stats">
            <span><el-icon><View /></el-icon> {{ post.view_count || 0 }}</span>
            <span><el-icon><Star /></el-icon> {{ post.like_count || 0 }}</span>
            <span><el-icon><ChatDotRound /></el-icon> {{ post.comment_count || 0 }}</span>
          </div>
        </div>
      </div>
      <el-empty v-if="!loading && posts.length === 0" description="暂无收藏" />
      <el-pagination
        v-if="total > pageSize"
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadBookmarks"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { postApi } from '@/api'
import { View, Star, ChatDotRound } from '@element-plus/icons-vue'

const loading = ref(false)
const posts = ref([])
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const loadBookmarks = async () => {
  loading.value = true
  try {
    const res = await postApi.getPostList({ page: page.value, pageSize: pageSize.value, bookmarked: 1 })
    posts.value = res.data?.list || []
    total.value = res.data?.total || 0
  } catch (e) {
    console.error('加载收藏失败', e)
  } finally {
    loading.value = false
  }
}

const formatTime = (time) => {
  if (!time) return ''
  const d = new Date(time)
  const now = new Date()
  const diff = now - d
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return d.toLocaleDateString('zh-CN')
}

onMounted(() => { loadBookmarks() })
</script>

<style scoped>
.bookmarks-page { background:#fff; border-radius:8px; padding:24px; box-shadow:0 2px 4px rgba(0,0,0,.05); }
.page-title { font-size:20px; font-weight:600; margin-bottom:24px; color:#303133; }
.post-item { padding:16px 0; border-bottom:1px solid #f0f0f0; cursor:pointer; }
.post-item:hover { background:#fafafa; }
.post-header { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
.post-author { color:#409eff; font-size:14px; }
.post-time { color:#999; font-size:12px; margin-left:auto; }
.post-title { font-size:16px; margin:8px 0; color:#303133; }
.post-summary { color:#666; font-size:14px; line-height:1.6; }
.post-footer { display:flex; align-items:center; gap:8px; margin-top:8px; flex-wrap:wrap; }
.tag { margin-right:4px; }
.post-stats { display:flex; gap:16px; margin-left:auto; color:#999; font-size:13px; }
.post-stats span { display:flex; align-items:center; gap:4px; }
</style>
