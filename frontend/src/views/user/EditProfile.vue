<template>
  <div class="edit-profile-page">
    <h2 class="page-title">编辑个人资料</h2>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-position="top"
      size="large"
      style="max-width: 600px"
    >
      <el-form-item label="头像">
        <div class="avatar-upload">
          <el-avatar :size="80" :src="formData.avatar">
            {{ formData.nickname?.charAt(0) }}
          </el-avatar>
          <el-button size="small" @click="uploadAvatar">更换头像</el-button>
        </div>
      </el-form-item>

      <el-form-item label="昵称" prop="nickname">
        <el-input v-model="formData.nickname" placeholder="请输入昵称" maxlength="20" show-word-limit />
      </el-form-item>

      <el-form-item label="个人简介" prop="bio">
        <el-input
          v-model="formData.bio"
          type="textarea"
          :rows="4"
          placeholder="介绍一下自己吧..."
          maxlength="200"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="投资偏好">
        <el-select v-model="formData.investment_preference" placeholder="选择投资偏好" multiple style="width: 100%">
          <el-option label="A股" value="a_stock" />
          <el-option label="港股" value="hk_stock" />
          <el-option label="美股" value="us_stock" />
          <el-option label="基金" value="fund" />
          <el-option label="期货" value="futures" />
        </el-select>
      </el-form-item>

      <el-form-item label="社交链接">
        <el-input v-model="formData.github" placeholder="GitHub 链接" :prefix-icon="Link" />
      </el-form-item>

      <el-form-item label="隐私设置">
        <el-switch v-model="formData.email_public" active-text="公开邮箱" />
        <el-switch v-model="formData.allow_messages" active-text="允许私信" style="margin-left: 24px" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" size="large" :loading="loading" @click="handleSave">
          保存修改
        </el-button>
        <el-button size="large" @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api'
import { ElMessage } from 'element-plus'
import { Link } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)

const formData = reactive({
  nickname: '',
  bio: '',
  avatar: '',
  investment_preference: [],
  github: '',
  email_public: true,
  allow_messages: true
})

const rules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度为2-20个字符', trigger: 'blur' }
  ]
}

const loadUserInfo = async () => {
  try {
    const res = await authApi.getUserInfo()
    const user = res.data
    formData.nickname = user.nickname || ''
    formData.bio = user.bio || ''
    formData.avatar = user.avatar || ''
    formData.investment_preference = user.investment_preference || []
    formData.github = user.github || ''
    formData.email_public = user.email_public ?? true
    formData.allow_messages = user.allow_messages ?? true
  } catch (error) {
    ElMessage.error('加载用户信息失败')
  }
}

const uploadAvatar = () => {
  ElMessage.info('头像上传功能待实现')
  // TODO: 实现头像上传
}

const handleSave = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await authApi.updateUserInfo(formData)
      // 更新本地用户状态
      userStore.currentUser = { ...userStore.currentUser, ...formData }
      ElMessage.success('保存成功！')
      router.push(`/user/${userStore.currentUser.id}`)
    } catch (error) {
      ElMessage.error(error.response?.data?.message || '保存失败，请重试')
    } finally {
      loading.value = false
    }
  })
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped>
.edit-profile-page {
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

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>
