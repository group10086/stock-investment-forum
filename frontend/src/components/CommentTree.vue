<template>
  <div class="comment-tree">
    <div v-for="item in comments" :key="item.id" class="comment-item">
      <div class="comment-main">
        <strong>{{ item.username }}</strong>
        <span style="color:#999;font-size:13px;margin-left:10px;">{{ item.created_at }}</span>
        <p style="margin:4px 0 6px;">{{ item.content }}</p>
        <span style="color:#409eff;font-size:13px;cursor:pointer;" @click="emit('reply', item.id)">
          回复
        </span>
      </div>
      <!-- 如果有子评论，继续调用自己 -->
      <CommentTree 
        v-if="item.children && item.children.length" 
        :comments="item.children" 
        @reply="emit('reply', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  comments: { type: Array, required: true }
})
const emit = defineEmits(['reply'])
</script>

<style scoped>
.comment-item { margin-left: 20px; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.comment-main { padding: 4px 0; }
</style>