<template>
  <div class="following-page">
    <h2 class="page-title">我的关注</h2>

    <!-- Tab切换 -->
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="全部关注" name="all">
        <div v-loading="loading" class="user-list">
          <div v-for="user in userList" :key="user.id" class="user-item" :class="{ 'special-user': user.isSpecial }">
            <el-avatar :size="48" :src="user.avatar">
              {{ user.nickname?.charAt(0) }}
            </el-avatar>
            <div class="user-info">
              <div class="user-name">
                <el-icon v-if="user.isSpecial" color="#FFD700"><StarFilled /></el-icon>
                {{ user.nickname }}
              </div>
              <div class="user-bio">{{ user.bio || '这个人很懒~' }}</div>
            </div>
            <div class="user-actions">
              <el-button 
                :type="user.isSpecial ? 'warning' : 'default'" 
                size="small"
                @click="toggleSpecial(user)"
              >
                <el-icon><StarFilled v-if="user.isSpecial" /><Star v-else /></el-icon>
                {{ user.isSpecial ? '取消星标' : '设为星标' }}
              </el-button>
              <el-button type="danger" size="small" @click="handleUnfollow(user)">
                取消关注
              </el-button>
            </div>
          </div>

          <el-empty v-if="!loading && userList.length === 0" description="暂无关注" />

          <!-- 分页 -->
          <el-pagination
            v-if="total > 0"
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :total="total"
            layout="prev, pager, next"
            @current-change="loadFollowing"
          />
        </div>
      </el-tab-pane>

      <el-tab-pane label="特别关注" name="special">
        <div v-loading="loading" class="user-list">
          <div v-for="user in specialUsers" :key="user.id" class="user-item special-user">
            <el-avatar :size="48" :src="user.avatar">
              {{ user.nickname?.charAt(0) }}
            </el-avatar>
            <div class="user-info">
              <div class="user-name">
                <el-icon color="#FFD700"><StarFilled /></el-icon>
                {{ user.nickname }}
              </div>
              <div class="user-bio">{{ user.bio || '这个人很懒~' }}</div>
            </div>
            <div class="user-actions">
              <el-button type="warning" size="small" @click="toggleSpecial(user)">
                <el-icon><Star /></el-icon>
                取消星标
              </el-button>
              <el-button type="danger" size="small" @click="handleUnfollow(user)">
                取消关注
              </el-button>
            </div>
          </div>

          <el-empty v-if="!loading && specialUsers.length === 0" description="暂无特别关注" />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { authApi } from '@/api'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'

const loading = ref(false)
const activeTab = ref('all')
const userList = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 计算特别关注用户
const specialUsers = computed(() => {
  return userList.value.filter(user => user.isSpecial)
})

const loadFollowing = async () => {
  loading.value = true
  try {
    const res = await authApi.getFollowingList({ page: page.value, pageSize: pageSize.value })
    userList.value = res.data.list || []
    total.value = res.data.total || 0
  } catch (error) {
    ElMessage.error('加载关注列表失败')
  } finally {
    loading.value = false
  }
}

const handleTabChange = (tab) => {
  // 切换tab时可以重新加载数据
  console.log('切换到:', tab)
}

const toggleSpecial = async (user) => {
  try {
    if (user.isSpecial) {
      await authApi.unsetSpecialFollow(user.id)
      user.isSpecial = false
      ElMessage.success('已取消星标')
    } else {
      await authApi.setSpecialFollow(user.id)
      user.isSpecial = true
      ElMessage.success('已设为星标')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleUnfollow = async (user) => {
  try {
    await authApi.unfollowUser(user.id)
    ElMessage.success('已取消关注')
    loadFollowing()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadFollowing()
})
</script>

<style scoped>
.following-page {
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
  transition: all 0.3s;
}

.user-item.special-user {
  border-color: #FFD700;
  background: linear-gradient(135deg, #FFF9E6 0%, #FFFFFF 100%);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.user-bio {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.user-actions {
  display: flex;
  gap: 8px;
}
</style>