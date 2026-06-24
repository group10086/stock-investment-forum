<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <el-icon :size="48" color="#1890FF"><TrendCharts /></el-icon>
        <h2>股票投资论坛</h2>
        <p>手机号注册</p>
      </div>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        size="large"
        @submit.prevent="handleRegister"
      >
        <el-form-item prop="phone">
          <el-input
            v-model="formData.phone"
            placeholder="请输入手机号"
            :prefix-icon="Iphone"
            maxlength="11"
          />
        </el-form-item>

        <el-form-item prop="code">
          <div class="code-input">
            <el-input
              v-model="formData.code"
              placeholder="请输入验证码"
              :prefix-icon="Key"
              maxlength="6"
            />
            <el-button
              :disabled="countdown > 0"
              @click="sendCode"
              style="margin-left: 8px;"
            >
              {{ countdown > 0 ? `${countdown}s后重试` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="设置密码（至少6位）"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input
            v-model="formData.confirmPassword"
            type="password"
            placeholder="确认密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="formData.agree">
            我已阅读并同意 <a href="#">《用户协议》</a> 和 <a href="#">《隐私政策》</a>
          </el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" style="width: 100%">
            注册
          </el-button>
        </el-form-item>

        <div class="auth-links">
          <router-link to="/login">已有账号？立即登录</router-link>
          <router-link to="/register">使用邮箱注册</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api'
import { ElMessage } from 'element-plus'
import { TrendCharts, Iphone, Key, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const countdown = ref(0)

const formData = reactive({
  phone: '',
  code: '',
  password: '',
  confirmPassword: '',
  agree: false
})

let timer = null

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== formData.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为6位数字', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback(new Error('请同意用户协议'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

const sendCode = async () => {
  if (!formData.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  
  if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
    ElMessage.warning('请输入有效的手机号')
    return
  }

  try {
    await authApi.sendSmsCode(formData.phone)
    ElMessage.success('验证码已发送')
    
    countdown.value = 60
    timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '发送失败')
  }
}

const handleRegister = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      const res = await authApi.registerByPhone({
        phone: formData.phone,
        code: formData.code,
        password: formData.password
      })
      userStore.setLoginState(res.data.user, res.data.token)
      ElMessage.success('注册成功！')
      router.push('/')
    } catch (error) {
      ElMessage.error(error.response?.data?.message || '注册失败，请重试')
    } finally {
      loading.value = false
      if (timer) clearInterval(timer)
    }
  })
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #E6F7FF 0%, #FFFFFF 100%);
}

.auth-container {
  width: 400px;
  padding: 40px;
  background: #FFFFFF;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h2 {
  font-size: 24px;
  color: var(--text-primary);
  margin: 16px 0 8px;
}

.auth-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.code-input {
  display: flex;
  gap: 8px;
}

.code-input .el-input {
  flex: 1;
}

.auth-links {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

.auth-links a {
  color: var(--primary-color);
  font-size: 14px;
}
</style>