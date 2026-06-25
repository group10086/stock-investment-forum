<template>
  <div class="stock-discuss-page">
    <h2 class="page-title">自选股讨论</h2>
    <!-- 模拟股票行情条 -->
    <div class="stock-ticker">
      <div class="ticker-item" v-for="s in stocks" :key="s.code">
        <span class="ticker-name">{{ s.name }}</span>
        <span class="ticker-code">{{ s.code }}</span>
        <span class="ticker-price" :class="s.change >= 0 ? 'up' : 'down'">{{ s.price }}</span>
        <span class="ticker-change" :class="s.change >= 0 ? 'up' : 'down'">
          {{ s.change >= 0 ? '+' : '' }}{{ s.change }}%
        </span>
      </div>
    </div>
    <!-- 帖子列表：股票分类 -->
    <div v-loading="loading" class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-item" @click="$router.push(`/post/${post.id}`)">
        <div class="post-header">
          <el-avatar :size="32" :src="post.user?.avatar">{{ post.user?.nickname?.charAt(0) }}</el-avatar>
          <span class="post-author">{{ post.user?.nickname }}</span>
          <el-tag size="small" type="warning">{{ post.category === 'stock' ? '股票' : post.category }}</el-tag>
          <span class="post-time">{{ formatTime(post.created_at) }}</span>
        </div>
        <h3 class="post-title">{{ post.title }}</h3>
        <p class="post-summary">{{ post.summary || post.content?.replace(/<[^>]+>/g, '').substring(0, 150) }}</p>
        <div class="post-footer">
          <el-tag v-for="tag in (post.tags || [])" :key="tag" size="small">{{ tag }}</el-tag>
          <div class="post-stats">
            <span><el-icon><View /></el-icon>{{ post.view_count }}</span>
            <span><el-icon><Star /></el-icon>{{ post.like_count }}</span>
            <span><el-icon><ChatDotRound /></el-icon>{{ post.comment_count }}</span>
          </div>
        </div>
      </div>
      <el-empty v-if="!loading && posts.length === 0" description="暂无讨论" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { postApi } from '@/api'
import { View, Star, ChatDotRound } from '@element-plus/icons-vue'

const loading = ref(false)
const posts = ref([])

const stocks = [
  { name: '贵州茅台', code: '600519', price: '1,685.00', change: 2.35 },
  { name: '宁德时代', code: '300750', price: '218.50', change: -0.82 },
  { name: '中芯国际', code: '688981', price: '95.30', change: 5.67 },
  { name: '北方华创', code: '002371', price: '388.00', change: 1.23 },
  { name: '腾讯控股', code: 'HK0700', price: '385.60', change: -1.45 },
  { name: '比亚迪', code: '002594', price: '285.30', change: 3.12 },
]

const loadPosts = async () => {
  loading.value = true
  try {
    const res = await postApi.getPostList({ page: 1, pageSize: 20, category: 'stock', sort: 'newest' })
    posts.value = res.data?.list || []
  } catch (e) {
    console.error('加载失败', e)
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

onMounted(() => { loadPosts() })
</script>

<style scoped>
.stock-discuss-page { background:#fff; border-radius:8px; padding:24px; box-shadow:0 2px 4px rgba(0,0,0,.05); }
.page-title { font-size:20px; font-weight:600; margin-bottom:16px; color:#303133; }
.stock-ticker { display:flex; gap:8px; flex-wrap:wrap; padding:12px 16px; background:#f8f9fa; border-radius:8px; margin-bottom:20px; overflow-x:auto; }
.ticker-item { display:flex; align-items:center; gap:6px; padding:4px 12px; background:#fff; border-radius:6px; white-space:nowrap; box-shadow:0 1px 3px rgba(0,0,0,.08); }
.ticker-name { font-weight:600; font-size:13px; }
.ticker-code { color:#999; font-size:11px; }
.ticker-price { font-weight:500; font-size:13px; }
.ticker-change { font-size:12px; font-weight:500; }
.up { color:#e74c3c; }
.down { color:#27ae60; }
.post-item { padding:16px 0; border-bottom:1px solid #f0f0f0; cursor:pointer; }
.post-item:hover { background:#fafafa; }
.post-header { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
.post-author { color:#409eff; font-size:14px; }
.post-time { color:#999; font-size:12px; margin-left:auto; }
.post-title { font-size:16px; margin:8px 0; color:#303133; }
.post-summary { color:#666; font-size:14px; line-height:1.6; }
.post-footer { display:flex; align-items:center; gap:8px; margin-top:8px; flex-wrap:wrap; }
.post-stats { display:flex; gap:16px; margin-left:auto; color:#999; font-size:13px; }
.post-stats span { display:flex; align-items:center; gap:4px; }
</style>
