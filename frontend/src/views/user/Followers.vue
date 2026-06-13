<template>
  <div class="followers-page">
    <h2 class="page-title">我的粉丝</h2>

    <div v-loading="loading" class="user-list">
      <div v-for="user in userList" :key="user.id" class="user-item">
        <el-avatar :size="48" :src="user.avatar">
          {{ user.nickname?.charAt(0) }}
        </el-avatar>
        <div class="user-info">
          <div class="user-name">{{ user.nickname }}</div>
          <div class="user-bio">{{ user.bio || '这个人很懒~' }}</div>
        </div>
        <el-button
          :type="user.is_following ? 'default' : 'primary'"
          size="small"
          @click="handleFollowBack(user)"
        >
          {{ user.is_following ? '已互关' : '回关' }}
        </el-button>
      </div>

      <el-empty v-if="!loading && userList.length === 0" description="暂无粉丝" />

      <!-- 分页 -->
      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadFollowers"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authApi } from '@/api'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const userList = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

const loadFollowers = async () => {
  loading.value = true
  try {
    const res = await authApi.getFollowersList({ page: page.value, pageSize: pageSize.value })
    userList.value = res.data.list || []
    total.value = res.data.total || 0
  } catch (error) {
    ElMessage.error('加载粉丝列表失败')
  } finally {
    loading.value = false
  }
}

const handleFollowBack = async (user) => {
  try {
    if (user.is_following) {
      await authApi.unfollowUser(user.id)
      user.is_following = false
      ElMessage.success('已取消关注')
    } else {
      await authApi.followUser(user.id)
      user.is_following = true
      ElMessage.success('关注成功')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadFollowers()
})
</script>

<style scoped>
.followers-page {
  background: #FFFFFF;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #F0F0F0;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
}

.user-bio {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}
</style>
