<template>
  <div class="questionnaire-page">
    <div class="container">
      <el-card>
        <template #header>
          <h2>投资者适当性风险评估问卷</h2>
          <p class="subtitle">请根据您的实际情况如实填写，我们将据此评估您的风险承受能力</p>
        </template>

        <el-progress :percentage="progress" :format="() => `已完成 ${answeredCount}/${questions.length} 题`" />

        <el-form ref="formRef" :model="answers" label-width="100%" style="margin-top: 32px;">
          <el-form-item v-for="(question, index) in questions" :key="index" :label="`${index + 1}. ${question.text}`">
            <el-radio-group v-model="answers[index]" @change="handleAnswerChange">
              <el-radio v-for="(option, optIndex) in question.options" :key="optIndex" :label="optIndex + 1">
                {{ option }}
              </el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitQuestionnaire" :disabled="!isComplete">
              提交问卷
            </el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>

        <!-- 结果展示 -->
        <el-alert v-if="riskLevel" :title="`您的风险等级：${riskLevelText}`" type="success" :closable="false" style="margin-top: 24px;">
          <p>{{ riskDescription }}</p>
        </el-alert>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const questions = [
  {
    text: '您的年龄是？',
    options: ['18-30岁', '31-45岁', '46-60岁', '60岁以上']
  },
  {
    text: '您的家庭年收入约为？',
    options: ['10万以下', '10-30万', '30-50万', '50万以上']
  },
  {
    text: '您有多少年的投资经验？',
    options: ['无经验', '1-3年', '3-5年', '5年以上']
  },
  {
    text: '您能接受的最大投资损失是？',
    options: ['5%以内', '5-10%', '10-20%', '20%以上']
  },
  {
    text: '您的投资目标是？',
    options: ['保本为主', '稳健增值', '平衡收益与风险', '追求高收益']
  }
]

const answers = ref({})
const riskLevel = ref('')

const answeredCount = computed(() => Object.keys(answers.value).length)
const progress = computed(() => Math.round((answeredCount.value / questions.length) * 100))
const isComplete = computed(() => answeredCount.value === questions.length)

const riskLevelText = computed(() => {
  const map = {
    conservative: '保守型',
    steady: '稳健型',
    balanced: '平衡型',
    growth: '成长型',
    aggressive: '进取型'
  }
  return map[riskLevel.value] || ''
})

const riskDescription = computed(() => {
  const descriptions = {
    conservative: '您属于保守型投资者，建议以低风险产品为主，如货币基金、国债等。',
    steady: '您属于稳健型投资者，可适当配置债券基金、银行理财等产品。',
    balanced: '您属于平衡型投资者，可均衡配置股票、债券等各类资产。',
    growth: '您属于成长型投资者，可适当增加股票、混合基金等权益类资产配置。',
    aggressive: '您属于进取型投资者，可积极参与股票、期货等高风险高收益投资。'
  }
  return descriptions[riskLevel.value] || ''
})

const handleAnswerChange = () => {
  if (isComplete.value) {
    calculateRiskLevel()
  }
}

const calculateRiskLevel = () => {
  const totalScore = Object.values(answers.value).reduce((sum, val) => sum + val, 0)
  
  if (totalScore <= 5) {
    riskLevel.value = 'conservative'
  } else if (totalScore <= 10) {
    riskLevel.value = 'steady'
  } else if (totalScore <= 15) {
    riskLevel.value = 'balanced'
  } else if (totalScore <= 20) {
    riskLevel.value = 'growth'
  } else {
    riskLevel.value = 'aggressive'
  }
}

const submitQuestionnaire = async () => {
  if (!isComplete.value) {
    ElMessage.warning('请完成所有题目')
    return
  }

  try {
    ElMessage.success('问卷提交成功！')
    setTimeout(() => {
      router.push('/authentication')
    }, 1500)
  } catch (error) {
    ElMessage.error('提交失败，请重试')
  }
}

const resetForm = () => {
  answers.value = {}
  riskLevel.value = ''
}
</script>

<style scoped>
.questionnaire-page {
  min-height: 100vh;
  background: var(--bg-color);
  padding: 40px 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin-top: 8px;
}

.el-form-item {
  margin-bottom: 32px;
}
</style>