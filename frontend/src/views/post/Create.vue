<template>
  <div class="post-create">
    <h2 class="page-title">发布帖子</h2>

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
          placeholder="请输入帖子标题（必填）"
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
          placeholder="多个标签用逗号分隔，如：A股,价值投资"
        />
      </el-form-item>

      <el-divider />

      <el-form-item label="是否开启投票">
        <el-switch v-model="formData.enableVote" />
      </el-form-item>

      <template v-if="formData.enableVote">
        <el-form-item label="投票选项">
          <div v-for="(option, index) in formData.voteOptions" :key="index" class="vote-option">
            <el-input
              v-model="formData.voteOptions[index]"
              :placeholder="`选项 ${index + 1}`"
              style="flex: 1;"
            />
            <el-button
              v-if="formData.voteOptions.length > 2"
              type="danger"
              :icon="Delete"
              circle
              @click="removeVoteOption(index)"
              style="margin-left: 8px;"
            />
          </div>
          <el-button
            v-if="formData.voteOptions.length < 10"
            type="primary"
            plain
            :icon="Plus"
            @click="addVoteOption"
            style="margin-top: 8px;"
          >
            添加选项
          </el-button>
        </el-form-item>

        <el-form-item label="投票截止时间">
          <el-date-picker
            v-model="formData.voteDeadline"
            type="datetime"
            placeholder="选择投票截止时间"
            :disabled-date="disabledDate"
            style="width: 100%;"
          />
        </el-form-item>

        <el-form-item label="匿名投票">
          <el-switch v-model="formData.isAnonymous" />
        </el-form-item>
      </template>

      <el-divider />

      <el-form-item label="附件上传（支持 PDF/Excel）">
        <el-upload
          :file-list="fileList"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :before-upload="beforeUpload"
          accept=".pdf,.xlsx,.xls"
          multiple
          drag
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            拖拽文件到此处或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 pdf/xlsx/xls 格式，单个文件不超过 10MB
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" size="large" :loading="loading" @click="handlePublish">
          发布帖子
        </el-button>
        <el-button size="large" @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, shallowRef, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '@/api'
import { ElMessage } from 'element-plus'
import { UploadFilled, Delete, Plus } from '@element-plus/icons-vue'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

const router = useRouter()

const formRef = ref(null)
const loading = ref(false)
const editorRef = shallowRef()

const formData = reactive({
  title: '',
  content: '',
  category: '',
  tags: '',
  enableVote: false,
  voteOptions: ['', ''],
  voteDeadline: null,
  isAnonymous: false
})

const fileList = ref([])

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

const addVoteOption = () => {
  if (formData.voteOptions.length < 10) {
    formData.voteOptions.push('')
  }
}

const removeVoteOption = (index) => {
  formData.voteOptions.splice(index, 1)
}

const disabledDate = (time) => {
  return time.getTime() < Date.now()
}

const beforeUpload = (file) => {
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB!')
    return false
  }
  return true
}

const handleFileChange = (file, files) => {
  fileList.value = files
}

const handleFileRemove = (file, files) => {
  fileList.value = files
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

const handlePublish = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      const data = {
        title: formData.title,
        content: formData.content,
        category: formData.category,
        tags: formData.tags ? formData.tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        enable_vote: formData.enableVote,
        is_anonymous: formData.isAnonymous
      }

      if (formData.enableVote) {
        data.vote_options = formData.voteOptions.filter(opt => opt.trim())
        data.vote_deadline = formData.voteDeadline
      }

      if (fileList.value.length > 0) {
        data.attachments = fileList.value.map(file => ({
          name: file.name,
          url: file.url || URL.createObjectURL(file.raw),
          type: file.name.split('.').pop()
        }))
      }

      await postApi.createPost(data)
      ElMessage.success('发布成功！')
      router.push('/')
    } catch (error) {
      ElMessage.error(error.response?.data?.message || '发布失败，请重试')
    } finally {
      loading.value = false
    }
  })
}

onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})
</script>

<style scoped>
.post-create {
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

.vote-option {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.el-upload__tip {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 8px;
}
</style>