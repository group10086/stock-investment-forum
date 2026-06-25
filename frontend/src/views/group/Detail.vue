<template>
  <div class="group-detail-page" v-loading="loading">
    <template v-if="group">
      <div class="group-header">
        <h2 class="group-name">{{ group.name }}</h2>
        <p class="group-desc">{{ group.description || '暂无简介' }}</p>
        <div class="group-meta">
          <span>群主：{{ group.owner?.nickname }}</span>
          <span>{{ group.member_count }} 名成员</span>
          <span>{{ formatTime(group.created_at) }} 创建</span>
        </div>
        <div class="group-actions">
          <el-button v-if="!group.is_member" type="primary" @click="handleJoin">加入群组</el-button>
          <el-button v-else-if="group.owner_id !== userStore.currentUser?.id" type="danger" @click="handleLeave">退出群组</el-button>
        </div>
      </div>

      <el-divider />

      <!-- 群聊区域 -->
      <h3>群聊消息</h3>
      <div class="chat-area" ref="chatRef">
        <div v-if="messages.length === 0" class="chat-empty">暂无消息，发一条吧</div>
        <div v-for="msg in messages" :key="msg.id" class="chat-msg" :class="{ mine: msg.user_id === userStore.currentUser?.id }">
          <el-avatar :size="28" :src="msg.user?.avatar">{{ msg.user?.nickname?.charAt(0) }}</el-avatar>
          <div class="msg-content">
            <span class="msg-author">{{ msg.user?.nickname }}</span>
            <span class="msg-time">{{ formatMsgTime(msg.created_at) }}</span>
            <div class="msg-text">{{ msg.content }}</div>
          </div>
        </div>
      </div>
      <div class="chat-input" v-if="group.is_member">
        <el-input v-model="inputText" placeholder="输入消息..." @keydown.enter.exact="sendMsg" />
        <el-button type="primary" :disabled="!inputText.trim()" @click="sendMsg">发送</el-button>
      </div>

      <el-divider />

      <h3>群组成员 ({{ group.member_count }})</h3>
      <div class="member-list">
        <div v-for="m in group.members" :key="m.id" class="member-item" @click="$router.push(`/user/${m.id}`)">
          <el-avatar :size="40" :src="m.avatar">{{ m.nickname?.charAt(0) }}</el-avatar>
          <div class="member-info">
            <span class="member-name">{{ m.nickname }}</span>
            <el-tag v-if="m.role === 'owner'" type="warning" size="small">群主</el-tag>
            <el-tag v-else-if="m.role === 'admin'" type="primary" size="small">管理员</el-tag>
          </div>
        </div>
      </div>
    </template>
    <el-empty v-else-if="!loading" description="群组不存在" />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { groupApi } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const userStore = useUserStore()
const loading = ref(true)
const group = ref(null)
const messages = ref([])
const inputText = ref('')
const chatRef = ref(null)

const loadGroup = async () => {
  loading.value = true
  try {
    const res = await groupApi.getGroupDetail(route.params.id)
    group.value = res.data
    if (group.value.is_member) loadMessages()
  } catch (e) {
    console.error('加载群组失败', e)
  } finally {
    loading.value = false
  }
}

const loadMessages = async () => {
  try {
    const res = await groupApi.getGroupMessages(route.params.id, { page: 1, pageSize: 100 })
    messages.value = res.data?.list || []
    scrollToBottom()
  } catch (e) {
    console.error('加载消息失败', e)
  }
}

const sendMsg = async () => {
  if (!inputText.value.trim()) return
  try {
    const res = await groupApi.sendGroupMessage(route.params.id, { content: inputText.value })
    messages.value.push(res.data)
    inputText.value = ''
    scrollToBottom()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '发送失败')
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatRef.value) chatRef.value.scrollTop = chatRef.value.scrollHeight
}

const handleJoin = async () => {
  try {
    await groupApi.joinGroup(group.value.id)
    ElMessage.success('已加入群组')
    loadGroup()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  }
}

const handleLeave = async () => {
  try {
    await groupApi.leaveGroup(group.value.id)
    ElMessage.success('已退出群组')
    loadGroup()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleDateString('zh-CN')
}

const formatMsgTime = (time) => {
  if (!time) return ''
  const d = new Date(time)
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => { loadGroup() })
</script>

<style scoped>
.group-detail-page { background:#fff; border-radius:8px; padding:24px; box-shadow:0 2px 4px rgba(0,0,0,.05); }
.group-header { margin-bottom:8px; }
.group-name { font-size:22px; font-weight:600; margin:0 0 8px; color:#303133; }
.group-desc { color:#666; font-size:14px; margin:0 0 12px; }
.group-meta { display:flex; gap:16px; color:#999; font-size:13px; margin-bottom:12px; }
.group-actions { margin-top:8px; }
.chat-area { max-height:400px; overflow-y:auto; border:1px solid #ebeef5; border-radius:8px; padding:12px; margin-bottom:12px; background:#fafafa; }
.chat-empty { text-align:center; color:#999; padding:40px; }
.chat-msg { display:flex; gap:8px; margin-bottom:12px; align-items:flex-start; }
.chat-msg.mine { flex-direction:row-reverse; }
.chat-msg.mine .msg-content { text-align:right; }
.msg-author { font-size:12px; color:#409eff; margin-right:8px; font-weight:500; }
.msg-time { font-size:11px; color:#ccc; }
.msg-text { background:#fff; padding:8px 12px; border-radius:8px; margin-top:4px; display:inline-block; max-width:80%; word-break:break-word; }
.mine .msg-text { background:#409eff; color:#fff; }
.chat-input { display:flex; gap:8px; }
.member-list { display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:12px; }
.member-item { display:flex; align-items:center; gap:12px; padding:10px; border-radius:8px; cursor:pointer; }
.member-item:hover { background:#f5f7fa; }
.member-info { display:flex; align-items:center; gap:8px; }
.member-name { font-weight:500; }
</style>
