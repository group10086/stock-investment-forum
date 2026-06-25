<template>
  <div class="groups-page">
    <div class="page-header">
      <h2 class="page-title">我的群组</h2>
      <el-button type="primary" @click="showCreate = true">创建群组</el-button>
    </div>

    <div v-loading="loading" class="group-list">
      <div v-for="group in groups" :key="group.id" class="group-card" @click="$router.push(`/group/${group.id}`)">
        <div class="group-info">
          <h3 class="group-name">{{ group.name }}</h3>
          <p class="group-desc">{{ group.description || '暂无简介' }}</p>
          <div class="group-meta">
            <span>群主：{{ group.owner?.nickname }}</span>
            <span>{{ group.member_count }} 名成员</span>
            <span>{{ formatTime(group.created_at) }} 创建</span>
          </div>
        </div>
        <div class="group-actions" @click.stop>
          <el-button v-if="group.owner_id !== userStore.currentUser?.id" type="danger" size="small" @click="handleLeave(group)">
            退出
          </el-button>
          <el-tag v-else type="warning" size="small">群主</el-tag>
        </div>
      </div>
      <el-empty v-if="!loading && groups.length === 0" description="还未加入群组">
        <el-button type="primary" @click="showCreate = true">创建第一个群组</el-button>
      </el-empty>
    </div>

    <!-- 创建群组对话框 -->
    <el-dialog v-model="showCreate" title="创建群组" width="420px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="群组名称">
          <el-input v-model="form.name" maxlength="50" placeholder="输入群组名称" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.desc" type="textarea" :rows="3" maxlength="200" placeholder="介绍群组主题" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreate = false">取消</el-button>
        <el-button type="primary" :disabled="!form.name.trim()" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { groupApi } from '@/api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const loading = ref(false)
const groups = ref([])
const showCreate = ref(false)
const form = reactive({ name: '', desc: '' })

const loadGroups = async () => {
  loading.value = true
  try {
    const res = await groupApi.getGroupList({ my: true })
    groups.value = res.data?.list || []
  } catch (e) {
    console.error('加载群组失败', e)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  try {
    await groupApi.createGroup({ name: form.name, description: form.desc, is_public: true })
    ElMessage.success('创建成功')
    showCreate.value = false
    form.name = ''
    form.desc = ''
    loadGroups()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '创建失败')
  }
}

const handleLeave = async (group) => {
  try {
    await groupApi.leaveGroup(group.id)
    ElMessage.success('已退出群组')
    loadGroups()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleDateString('zh-CN')
}

onMounted(() => { loadGroups() })
</script>

<style scoped>
.groups-page { background:#fff; border-radius:8px; padding:24px; box-shadow:0 2px 4px rgba(0,0,0,.05); }
.page-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; }
.page-title { font-size:20px; font-weight:600; color:#303133; }
.group-list { display:flex; flex-direction:column; gap:12px; }
.group-card { display:flex; justify-content:space-between; align-items:center; padding:16px; border:1px solid #ebeef5; border-radius:8px; cursor:pointer; }
.group-card:hover { border-color:#409eff; }
.group-info { flex:1; }
.group-name { font-size:16px; margin:0 0 4px; color:#303133; }
.group-desc { color:#999; font-size:13px; margin:0 0 8px; }
.group-meta { display:flex; gap:16px; color:#999; font-size:12px; }
.group-actions { margin-left:16px; }
</style>
