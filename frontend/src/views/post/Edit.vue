<template>
  <div class="post-edit" v-loading="loading">
    <h2 class="page-title">编辑帖子</h2>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-position="top"
      size="large"
    >
      <el-form-item label="标题" prop="title">
        <el-input
          v-model="formData.title"
          placeholder="请输入帖子标题"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="板块" prop="category">
        <el-select v-model="formData.category" placeholder="请选择板块" style="width: 100%">
          <el-option label="A股讨论" value="a_stock" />
          <el-option label="港股讨论" value="hk_stock" />
          <el-option label="美股讨论" value="us_stock" />
          <el-option label="基金投资" value="fund" />
          <el-option label="技术分析" value="technical" />
          <el-option label="价值投资" value="value" />
          <el-option label="其他" value="other" />
        </el-select>
      </el-form-item>

      <el-form-item label="内容" prop="content">
        <div style="border: 1px solid #DCDFE6; border-radius: 4px;">
          <Toolbar
            style="border-bottom: 1px solid #DCDFE6;"
            :editor="editorRef"
            :defaultConfig="toolbarConfig"
            mode="default"
          />
          <Editor
            style="height: 400px; overflow-y: hidden;"
            v-model="formData.content"
            :defaultConfig="editorConfig"
            mode="default"
            @onCreated="handleCreated"
          />
        </div>
      </el-form-item>

      <el-form-item label="标签（可选）">
        <el-input
          v-model="formData.tags"
          placeholder="多个标签用逗号分隔"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" size="large" :loading="submitting" @click="handleUpdate">
          保存修改
        </el-button>
        <el-button size="large" @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, shallowRef, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '@/api'
import { ElMessage } from 'element-plus'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

const route = useRoute()
const router = useRouter()

const formRef = ref(null)
const loading = ref(false)
const submitting = ref(false)
const editorRef = shallowRef()

const formData = reactive({
  title: '',
  content: '',
  category: '',
  tags: ''
})

const toolbarConfig = {}
const editorConfig = {
  placeholder: '分享你的投资观点和分析...',
  MENU_CONF: {
    uploadImage: {
      server: '/api/upload/image',
      fieldName: 'file',
      maxFileSize: 5 * 1024 * 1024,
      allowedFileTypes: ['image/*']
    }
  }
}

const handleCreated = (editor) => {
  editorRef.value = editor
}

const rules = {
  title: [
    { required: true, message: '请输入帖子标题', trigger: 'blur' },
    { min: 5, max: 100, message: '标题长度为5-100个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入帖子内容', trigger: 'blur' },
    { 
      validator: (rule, value, callback) => {
        if (!value || value === '<p><br></p>') {
          callback(new Error('内容不能为空'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  category: [
    { required: true, message: '请选择板块', trigger: 'change' }
  ]
}

const loadPost = async () => {
  loading.value = true
  try {
    const res = await postApi.getPostDetail(route.params.id)
    const post = res.data
    formData.title = post.title
    formData.content = post.content
    formData.category = post.category
    formData.tags = post.tags?.join(', ') || ''
  } catch (error) {
    ElMessage.error('加载帖子失败')
  } finally {
    loading.value = false
  }
}

const handleUpdate = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    try {
      const data = {
        ...formData,
        tags: formData.tags ? formData.tags.split(',').map(t => t.trim()).filter(Boolean) : []
      }
      await postApi.updatePost(route.params.id, data)
      ElMessage.success('更新成功！')
      router.push(`/post/${route.params.id}`)
    } catch (error) {
      ElMessage.error(error.response?.data?.message || '更新失败，请重试')
    } finally {
      submitting.value = false
    }
  })
}

onMounted(() => {
  loadPost()
})

onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})
</script>

<style scoped>
.post-edit {
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
</style>