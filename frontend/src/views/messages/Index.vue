<template>
  <div class="messages-page">
    <div class="messages-container">
      <!-- 左侧：联系人列表 -->
      <div class="conversation-list">
        <h3 class="section-title">消息</h3>
        <div
          v-for="conv in conversations"
          :key="conv.user.id"
          class="conversation-item"
          :class="{ active: currentUserId === conv.user.id }"
          @click="selectUser(conv.user)"
        >
          <el-avatar :size="40" :src="conv.user.avatar">
            {{ conv.user.nickname?.charAt(0) }}
          </el-avatar>
          <div class="conversation-info">
            <div class="conversation-name">{{ conv.user.nickname }}</div>
            <div class="conversation-last">{{ conv.lastMessage }}</div>
          </div>
          <div v-if="conv.unread" class="unread-badge">{{ conv.unread }}</div>
        </div>
        <el-empty v-if="conversations.length === 0" description="暂无消息" />
      </div>

      <!-- 右侧：聊天区域 -->
      <div class="chat-area">
        <template v-if="chatUser">
          <!-- 聊天头部 -->
          <div class="chat-header">
            <el-avatar :size="32" :src="chatUser.avatar">
              {{ chatUser.nickname?.charAt(0) }}
            </el-avatar>
            <span class="chat-name">{{ chatUser.nickname }}</span>
            <span class="chat-status" :class="chatUser.online ? 'online' : 'offline'">
              {{ chatUser.online ? '在线' : '离线' }}
            </span>
          </div>

          <!-- 消息列表 -->
          <div class="message-list" ref="messageListRef">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="message-item"
              :class="msg.isMine ? 'message-mine' : 'message-other'"
            >
              <el-avatar v-if="!msg.isMine" :size="32" :src="msg.user.avatar">
                {{ msg.user.nickname?.charAt(0) }}
              </el-avatar>
              <div class="message-bubble">
                <div class="message-text">{{ msg.content }}</div>
                <div class="message-time">{{ formatTime(msg.created_at) }}</div>
              </div>
              <el-avatar v-if="msg.isMine" :size="32" :src="userStore.currentUser?.avatar">
                {{ userStore.currentUser?.nickname?.charAt(0) }}
              </el-avatar>
            </div>
            <el-empty v-if="messages.length === 0" description="暂无消息，打个招呼吧" />
          </div>

          <!-- 输入框 -->
          <div class="chat-input">
            <el-input
              v-model="messageContent"
              type="textarea"
              :rows="2"
              placeholder="输入消息... (Enter发送, Shift+Enter换行)"
              resize="none"
              @keydown="handleKeyDown"
            />
            <el-button type="primary" :disabled="!messageContent.trim()" @click="sendMessage">
              发送
            </el-button>
          </div>
        </template>
        <el-empty v-else description="选择一个联系人开始聊天" style="height: 100%" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onMounted as onMount } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { messageApi } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const userStore = useUserStore()

const conversations = ref([])

const currentUserId = ref(route.params.userId || null)
const chatUser = ref(null)
const messages = ref([])
const messageContent = ref('')
const messageListRef = ref(null)

// 加载会话列表
const loadConversations = async () => {
  try {
    const res = await messageApi.getConversations()
    conversations.value = (res.data || []).map(conv => ({
      user: conv.user,
      lastMessage: conv.last_message,
      lastTime: conv.last_time,
      unread: conv.unread_count
    }))
  } catch (error) {
    console.error('加载会话失败', error)
  }
}

const selectUser = (user) => {
  currentUserId.value = user.id
  chatUser.value = user
  loadMessages()
}

const loadMessages = async () => {
  if (!currentUserId.value) return
  try {
    const res = await messageApi.getMessageList(currentUserId.value, { page: 1, pageSize: 50 })
    messages.value = (res.data.list || []).map(msg => ({
      ...msg,
      isMine: msg.is_mine,
      created_at: msg.created_at
    }))
    scrollToBottom()
  } catch (error) {
    console.error('加载消息失败', error)
  }
}

const sendMessage = async () => {
  if (!messageContent.value.trim() || !currentUserId.value) return
  
  try {
    await messageApi.sendMessage({
      receiver_id: currentUserId.value,
      content: messageContent.value
    })
    messages.value.push({
      id: Date.now(),
      content: messageContent.value,
      isMine: true,
      created_at: new Date().toISOString(),
      user: userStore.currentUser
    })
    messageContent.value = ''
    scrollToBottom()
    loadConversations() // 刷新会话列表
  } catch (error) {
    const msg = error?.response?.data?.detail || '发送失败'
    ElMessage.error(msg)
  }
}

const handleKeyDown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
}

onMounted(async () => {
  await loadConversations()
  if (route.params.userId) {
    const conv = conversations.value.find(c => c.user.id == route.params.userId)
    if (conv) selectUser(conv.user)
  }
})
</script>

<style scoped>
.messages-page {
  height: calc(100vh - 160px);
}

.messages-container {
  display: flex;
  height: 100%;
  background: #FFFFFF;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.conversation-list {
  width: 280px;
  border-right: 1px solid #F0F0F0;
  display: flex;
  flex-direction: column;
}

.section-title {
  padding: 16px;
  margin: 0;
  font-size: 16px;
  border-bottom: 1px solid #F0F0F0;
}

.conversation-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.2s;
  position: relative;
}

.conversation-item:hover {
  background: #F5F5F5;
}

.conversation-item.active {
  background: var(--primary-light);
}

.conversation-info {
  flex: 1;
  overflow: hidden;
}

.conversation-name {
  font-size: 14px;
  font-weight: 500;
}

.conversation-last {
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.unread-badge {
  background: #FF4D4F;
  color: white;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #F0F0F0;
}

.chat-name {
  flex: 1;
  font-weight: 500;
}

.chat-status {
  font-size: 12px;
}

.chat-status.online {
  color: var(--success-color);
}

.chat-status.offline {
  color: var(--text-secondary);
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-item {
  display: flex;
  gap: 8px;
  max-width: 70%;
}

.message-mine {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-bubble {
  padding: 10px 14px;
  border-radius: 12px;
  background: #F5F5F5;
}

.message-mine .message-bubble {
  background: var(--primary-color);
  color: white;
}

.message-text {
  font-size: 14px;
  line-height: 1.5;
  word-break: break-word;
}

.message-time {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.message-mine .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.chat-input {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-top: 1px solid #F0F0F0;
  align-items: flex-end;
}

.chat-input .el-textarea {
  flex: 1;
}

.chat-input .el-button {
  align-self: flex-end;
}
</style>
