<template>
  <div class="achievement-page">
    <div class="container">
      <!-- 用户等级卡片 -->
      <el-card class="level-card">
        <div class="level-header">
          <el-avatar :size="80" :src="userStore.currentUser?.avatar">
            {{ userStore.currentUser?.nickname?.charAt(0) }}
          </el-avatar>
          <div class="level-info">
            <h3>{{ userStore.currentUser?.nickname }}</h3>
            <el-tag type="warning" size="large">Lv.{{ currentLevel }}</el-tag>
            <p class="level-title">{{ levelTitle }}</p>
          </div>
        </div>
        
        <div class="exp-progress">
          <span>经验值：{{ currentExp }}/{{ nextLevelExp }}</span>
          <el-progress :percentage="levelProgress" :format="() => `${currentExp}/${nextLevelExp} EXP`" />
        </div>
      </el-card>

      <!-- 成就徽章 -->
      <el-card style="margin-top: 24px;">
        <template #header>
          <h3>成就徽章</h3>
        </template>
        
        <div class="achievement-grid">
          <el-card v-for="achievement in achievements" :key="achievement.id" class="achievement-item" :class="{ unlocked: achievement.unlocked }">
            <el-icon :size="48" :color="achievement.unlocked ? '#FFD700' : '#C0C0C0'">
              <component :is="achievement.icon" />
            </el-icon>
            <h4>{{ achievement.name }}</h4>
            <p>{{ achievement.description }}</p>
            <el-tag v-if="achievement.unlocked" type="success" size="small">已解锁</el-tag>
            <el-tag v-else type="info" size="small">未解锁</el-tag>
          </el-card>
        </div>
      </el-card>

      <!-- 积分排行榜 -->
      <el-card style="margin-top: 24px;">
        <template #header>
          <h3>积分排行榜 TOP 10</h3>
        </template>
        
        <el-table :data="leaderboard" stripe>
          <el-table-column prop="rank" label="排名" width="80" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.rank === 1" type="warning" effect="dark">{{ row.rank }}</el-tag>
              <el-tag v-else-if="row.rank === 2" type="warning">{{ row.rank }}</el-tag>
              <el-tag v-else-if="row.rank === 3" type="warning">{{ row.rank }}</el-tag>
              <span v-else>{{ row.rank }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="nickname" label="用户" />
          <el-table-column prop="points" label="积分" width="120" align="right" />
          <el-table-column prop="level" label="等级" width="100" align="center" />
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { Trophy, Star, Medal, Collection, TrendCharts } from '@element-plus/icons-vue'

const userStore = useUserStore()

const currentLevel = ref(5)
const currentExp = ref(450)
const nextLevelExp = ref(600)

const levelTitle = computed(() => {
  const titles = ['新手', '入门', '初级', '中级', '高级', '专家', '大师', '宗师', '传奇', '神话']
  return titles[currentLevel.value - 1] || '未知'
})

const levelProgress = computed(() => {
  return Math.round((currentExp.value / nextLevelExp.value) * 100)
})

const achievements = ref([
  { id: 1, name: '新手上路', description: '完成首次登录', icon: 'Trophy', unlocked: true },
  { id: 2, name: '发帖达人', description: '发布10篇帖子', icon: 'Star', unlocked: true },
  { id: 3, name: '精华作者', description: '获得10个精华帖', icon: 'Medal', unlocked: false },
  { id: 4, name: '社交达人', description: '关注50个用户', icon: 'Collection', unlocked: false },
  { id: 5, name: '投资专家', description: '通过高级认证', icon: 'TrendCharts', unlocked: false }
])

const leaderboard = ref([
  { rank: 1, nickname: '巴菲特研究院', points: 9999, level: 10 },
  { rank: 2, nickname: '量化交易大师', points: 8888, level: 9 },
  { rank: 3, nickname: '价值投资者', points: 7777, level: 8 },
  { rank: 4, nickname: '技术分析专家', points: 6666, level: 7 },
  { rank: 5, nickname: '基金定投王', points: 5555, level: 6 },
  { rank: 6, nickname: '短线高手', points: 4444, level: 5 },
  { rank: 7, nickname: '长线持有者', points: 3333, level: 4 },
  { rank: 8, nickname: '新股民', points: 2222, level: 3 },
  { rank: 9, nickname: '学习中的小白', points: 1111, level: 2 },
  { rank: 10, nickname: '刚注册的用户', points: 100, level: 1 }
])
</script>

<style scoped>
.achievement-page {
  min-height: 100vh;
  background: var(--bg-color);
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.level-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.level-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.level-info h3 {
  margin: 0 0 8px 0;
  font-size: 24px;
}

.level-title {
  margin: 8px 0 0 0;
  opacity: 0.9;
}

.exp-progress {
  margin-top: 24px;
}

.exp-progress span {
  display: block;
  margin-bottom: 8px;
}

.achievement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.achievement-item {
  text-align: center;
  padding: 24px;
  transition: all 0.3s;
}

.achievement-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.achievement-item.unlocked {
  border: 2px solid #FFD700;
}

.achievement-item h4 {
  margin: 16px 0 8px 0;
}

.achievement-item p {
  color: var(--text-secondary);
  font-size: 12px;
  margin-bottom: 12px;
}
</style>