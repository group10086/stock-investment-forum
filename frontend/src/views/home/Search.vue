<template>
  <div class="search-page">
    <h2>搜索结果</h2>
    <el-input v-model="keyword" placeholder="搜索帖子..." @keyup.enter="doSearch" clearable />
    <div v-loading="loading" style="margin-top: 16px">
      <div v-if="posts.length">
        <div v-for="post in posts" :key="post.id" class="post-item" @click="$router.push(`/post/${post.id}`)">
          <h3>{{ post.title }}</h3>
          <p>{{ post.summary }}</p>
          <span>{{ post.user?.nickname }} · {{ post.created_at?.slice(0,10) }}</span>
        </div>
      </div>
      <el-empty v-else description="未找到相关帖子" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { searchApi } from '@/api'

const route = useRoute()
const keyword = ref(route.query.keyword || '')
const posts = ref([])
const loading = ref(false)

const doSearch = async () => {
  if (!keyword.value.trim()) return
  loading.value = true
  try {
    const res = await searchApi.search({ keyword: keyword.value })
    posts.value = res.data?.posts || []
  } finally {
    loading.value = false
  }
}

onMounted(() => { if (keyword.value) doSearch() })
</script>

<style scoped>
.search-page { padding: 20px }
.post-item { cursor: pointer; padding: 12px; border: 1px solid #eee; border-radius: 8px; margin: 8px 0 }
.post-item:hover { border-color: #409EFF }
.post-item h3 { margin: 0 0 4px }
.post-item p { color: #666; margin: 0 0 4px }
.post-item span { font-size: 12px; color: #999 }
</style>
