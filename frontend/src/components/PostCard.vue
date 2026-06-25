<template>
  <div class="post-card" @click="goDetail">
    <div class="post-body">
      <div class="post-header">
        <span class="author-name">{{ post.author_name || '匿名用户' }}</span>
        <span class="post-time">{{ post.created_at }}</span>
        <span v-if="post.is_top" class="tag-top">置顶</span>
        <span v-if="post.is_essence" class="tag-essence">精华</span>
      </div>
      <h3 class="post-title">{{ post.title }}</h3>
      <p class="post-summary">{{ post.summary || post.content?.slice(0, 80) }}</p>
      <div class="post-actions">
        <span>❤️ {{ post.like_count || 0 }}</span>
        <span>💬 {{ post.comment_count || 0 }}</span>
        <span>⭐ {{ post.collect_count || 0 }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  post: { type: Object, required: true }
})

const router = useRouter()
const goDetail = () => {
  router.push(`/post/${props.post.id}`)
}
</script>

<style scoped>
.post-card {
  padding: 16px 20px;
  background: #fff;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}
.post-card:hover { background: #f8f9fa; }
.post-header { font-size: 14px; color: #999; margin-bottom: 6px; }
.author-name { color: #333; font-weight: bold; margin-right: 12px; }
.post-title { margin: 6px 0; font-size: 18px; color: #1a1a1a; }
.post-summary { color: #666; font-size: 14px; margin: 4px 0 10px; }
.post-actions { display: flex; gap: 20px; font-size: 14px; color: #888; }
.tag-top { color: red; font-size: 12px; margin-left: 8px; }
.tag-essence { color: orange; font-size: 12px; margin-left: 8px; }
</style>