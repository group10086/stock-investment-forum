<template>
  <div class="post-detail">
    <div v-loading="loading" class="post-main">
      <template v-if="post">
        <!-- 帖子头部 -->
        <div class="post-header">
          <el-page-header @back="$router.back()" title="返回列表" />
          <h1 class="post-title">{{ post.title }}</h1>
          <div class="post-meta">
            <el-avatar :size="40" :src="post.user?.avatar">
              {{ post.user?.nickname?.charAt(0) }}
            </el-avatar>
            <div class="meta-info">
              <div class="author-name">{{ post.user?.nickname }}</div>
              <div class="meta-time">
                {{ formatTime(post.created_at) }}
                <span v-if="post.updated_at !== post.created_at"> · 编辑于 {{ formatTime(post.updated_at) }}</span>
              </div>
            </div>
            <div v-if="userStore.currentUser?.id === post.user?.id" class="post-actions">
              <el-button size="small" @click="$router.push(`/post/${post.id}/edit`)">
                <el-icon><Edit /></el-icon> 编辑
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete">
                <el-icon><Delete /></el-icon> 删除
              </el-button>
            </div>
          </div>
        </div>

        <!-- 帖子内容 -->
        <div class="post-body">
          <div class="post-content" v-html="post.content"></div>
          <div v-if="post.images?.length" class="post-images">
            <el-image
              v-for="(img, index) in post.images"
              :key="index"
              :src="img"
              :preview-src-list="post.images"
              :initial-index="index"
              fit="cover"
            />
          </div>
        </div>
      <!-- 投票区域 -->
        <div v-if="post.enable_vote" class="vote-section">
          <h3 class="section-title">
            <el-icon><TrendCharts /></el-icon>
            投票：{{ post.vote_title || '市场观点' }}
          </h3>
          
          <div v-if="!hasVoted" class="vote-options">
            <el-radio-group v-model="selectedVoteOption" size="large">
              <el-radio
                v-for="(option, index) in post.vote_options"
                :key="index"
                :label="index"
                border
              >
                {{ option }}
              </el-radio>
            </el-radio-group>
            <el-button type="primary" @click="submitVote" style="margin-top: 16px;">
              提交投票
            </el-button>
          </div>

          <div v-else class="vote-results">
            <div v-for="(option, index) in post.vote_options" :key="index" class="vote-result-item">
              <div class="vote-option-label">{{ option }}</div>
              <el-progress
                :percentage="calculatePercentage(option.votes, totalVotes)"
                :status="getProgressStatus(calculatePercentage(option.votes, totalVotes))"
                :stroke-width="20"
              />
              <div class="vote-count">{{ option.votes }} 票 ({{ calculatePercentage(option.votes, totalVotes) }}%)</div>
            </div>
            <div class="vote-total">总票数：{{ totalVotes }}</div>
          </div>

          <div v-if="post.is_anonymous" class="vote-hint">
            <el-tag type="info" size="small">匿名投票</el-tag>
          </div>
        </div>

        <!-- 附件区域 -->
        <div v-if="post.attachments?.length" class="attachment-section">
          <h3 class="section-title">
            <el-icon><Document /></el-icon>
            附件下载
          </h3>
          <div class="attachment-list">
            <el-card
              v-for="(file, index) in post.attachments"
              :key="index"
              shadow="hover"
              class="attachment-item"
            >
              <div class="attachment-info">
                <el-icon :size="24" color="#409EFF">
                  <component :is="getFileIcon(file.type)" />
                </el-icon>
                <div class="attachment-details">
                  <div class="attachment-name">{{ file.name }}</div>
                  <div class="attachment-meta">{{ formatFileSize(file.size) }} · {{ file.type.toUpperCase() }}</div>
                </div>
              </div>
              <el-button type="primary" size="small" @click="downloadAttachment(file)">
                <el-icon><Download /></el-icon>
                下载
              </el-button>
            </el-card>
          </div>
        </div>

        <!-- 操作栏 -->
        <div class="action-bar">
          <el-button :type="post.is_liked ? 'warning' : ''" @click="handleLike">
            <el-icon><StarFilled v-if="post.is_liked" /><Star v-else /></el-icon>
            {{ post.like_count }} 点赞
          </el-button>
          <el-button :type="post.is_bookmarked ? 'primary' : ''" @click="handleBookmark">
            <el-icon><StarFilled v-if="post.is_bookmarked" /><Star v-else /></el-icon>
            {{ post.is_bookmarked ? '已收藏' : '收藏' }}
          </el-button>
          <el-button>
            <el-icon><Share /></el-icon> 分享
          </el-button>
          <el-button type="danger" plain>
            <el-icon><WarnTriangleFilled /></el-icon> 举报
          </el-button>
        </div>

        <!-- 评论区 -->
        <div class="comment-section">
          <h3 class="section-title">
            评论 ({{ post.comment_count }})
          </h3>

          <!-- 评论输入框 -->
          <div v-if="userStore.isLoggedIn" class="comment-input">
            <el-avatar :size="36" :src="userStore.currentUser?.avatar">
              {{ userStore.currentUser?.nickname?.charAt(0) }}
            </el-avatar>
            <div class="input-wrapper">
              <el-input
                v-model="commentContent"
                type="textarea"
                :rows="3"
                placeholder="写下你的评论..."
                resize="none"
              />
              <div class="input-actions">
                <el-button type="primary" size="small" @click="handleComment">
                  发表评论
                </el-button>
              </div>
            </div>
          </div>
          <el-alert v-else title="登录后才能评论" type="info" :closable="false" show-icon />

          <!-- 评论列表 -->
          <div class="comment-list">
            <div v-for="comment in commentList" :key="comment.id" class="comment-item">
              <el-avatar :size="32" :src="comment.user?.avatar">
                {{ comment.user?.nickname?.charAt(0) }}
              </el-avatar>
              <div class="comment-content">
                <div class="comment-header">
                  <span class="comment-author">{{ comment.user?.nickname }}</span>
                  <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
                </div>
                <div class="comment-text">{{ comment.content }}</div>
                <div class="comment-actions">
                  <span class="comment-action" @click="handleLikeComment(comment)">
                    <el-icon><component :is="comment.is_liked ? 'StarFilled' : 'Star'" /></el-icon>
                    {{ comment.like_count }}
                  </span>
                  <span class="comment-action">回复</span>
                </div>
              </div>
            </div>
            <el-empty v-if="commentList.length === 0" description="暂无评论，快来抢沙发吧" />
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { postApi, commentApi } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit, Delete, Star, StarFilled, Share, WarnTriangleFilled } from '@element-plus/icons-vue'
import { TrendCharts, Document, Download, Files, Reading, Picture } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const post = ref(null)
const commentList = ref([])
const commentContent = ref('')
const selectedVoteOption = ref(null)
const hasVoted = ref(false)
const totalVotes = ref(0)


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

const loadPost = async () => {
  loading.value = true
  try {
    const res = await postApi.getPostDetail(route.params.id)
    post.value = res.data
  } catch (error) {
    ElMessage.error('加载帖子失败')
  } finally {
    loading.value = false
  }
}

const loadComments = async () => {
  try {
    const res = await commentApi.getCommentList(route.params.id, { page: 1, pageSize: 20 })
    commentList.value = res.data.list || []
  } catch (error) {
    console.error('加载评论失败', error)
  }
}

const handleLike = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    if (post.value.is_liked) {
      await postApi.unlikePost(post.value.id)
      post.value.is_liked = false
      post.value.like_count--
    } else {
      await postApi.likePost(post.value.id)
      post.value.is_liked = true
      post.value.like_count++
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleBookmark = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    if (post.value.is_bookmarked) {
      await postApi.unbookmarkPost(post.value.id)
      post.value.is_bookmarked = false
      ElMessage.success('已取消收藏')
    } else {
      await postApi.bookmarkPost(post.value.id)
      post.value.is_bookmarked = true
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  try {
    await commentApi.createComment(post.value.id, { content: commentContent.value })
    ElMessage.success('评论成功')
    commentContent.value = ''
    loadComments()
    post.value.comment_count++
  } catch (error) {
    ElMessage.error('评论失败')
  }
}

const handleLikeComment = async (comment) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  try {
    await commentApi.likeComment(comment.id)
    comment.is_liked = !comment.is_liked
    comment.like_count += comment.is_liked ? 1 : -1
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个帖子吗？', '提示', {
      type: 'warning'
    })
    await postApi.deletePost(post.value.id)
    ElMessage.success('删除成功')
    router.back()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
const submitVote = async () => {
  if (selectedVoteOption.value === null) {
    ElMessage.warning('请选择一个选项')
    return
  }
  
  try {
    await postApi.submitVote(post.value.id, {
      option_index: selectedVoteOption.value
    })
    ElMessage.success('投票成功！')
    hasVoted.value = true
    loadPost()
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '投票失败')
  }
}

const calculatePercentage = (votes, total) => {
  if (total === 0) return 0
  return Math.round((votes / total) * 100)
}

const getProgressStatus = (percentage) => {
  if (percentage >= 50) return 'success'
  if (percentage >= 30) return 'warning'
  return 'exception'
}

const getFileIcon = (type) => {
  const iconMap = {
    pdf: 'Reading',
    xlsx: 'Files',
    xls: 'Files',
    doc: 'Reading',
    docx: 'Reading',
    default: 'Document'
  }
  return iconMap[type?.toLowerCase()] || iconMap.default
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const downloadAttachment = (file) => {
  if (file.url) {
    const link = document.createElement('a')
    link.href = file.url
    link.download = file.name
    link.click()
    ElMessage.success('开始下载...')
  } else {
    ElMessage.warning('文件链接无效')
  }
}

onMounted(() => {
  loadPost()
  loadComments()
})
</script>

<style scoped>
.post-detail {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.post-header {
  margin-bottom: 24px;
}

.post-title {
  font-size: 24px;
  font-weight: 600;
  margin: 16px 0;
  color: var(--text-primary);
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.meta-info {
  flex: 1;
}

.author-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.meta-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.post-actions {
  display: flex;
  gap: 8px;
}

.post-body {
  padding: 24px 0;
  border-top: 1px solid #F0F0F0;
  border-bottom: 1px solid #F0F0F0;
}

.post-content {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-primary);
}

.post-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-top: 20px;
}
.vote-section {
  margin-top: 24px;
  padding: 20px;
  background: #F5F7FA;
  border-radius: 8px;
}

.vote-options {
  margin-top: 16px;
}

.vote-results {
  margin-top: 16px;
}

.vote-result-item {
  margin-bottom: 16px;
}

.vote-option-label {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.vote-count {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.vote-total {
  text-align: right;
  font-size: 14px;
  color: var(--text-regular);
  margin-top: 12px;
}

.vote-hint {
  margin-top: 12px;
}

.attachment-section {
  margin-top: 24px;
  padding: 20px;
  background: #F5F7FA;
  border-radius: 8px;
}

.attachment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.attachment-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
}

.attachment-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.attachment-details {
  display: flex;
  flex-direction: column;
}

.attachment-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.attachment-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

.action-bar {
  display: flex;
  gap: 16px;
  padding: 16px 0;
}

.comment-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #F0F0F0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.comment-input {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.input-wrapper {
  flex: 1;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 8px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #FAFAFA;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.comment-author {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.comment-time {
  font-size: 12px;
  color: var(--text-secondary);
}

.comment-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.comment-actions {
  display: flex;
  gap: 16px;
}

.comment-action {
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.comment-action:hover {
  color: var(--primary-color);
}
</style>
