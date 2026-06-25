<template>
  <div style="background:#fff;padding:20px;border-radius:8px;">
    <h2>📋 举报管理</h2>
    <table style="width:100%;border-collapse:collapse;margin-top:15px;">
      <thead>
        <tr style="background:#f5f5f5;">
          <th style="padding:10px;border:1px solid #ddd;">ID</th>
          <th style="padding:10px;border:1px solid #ddd;">举报人</th>
          <th style="padding:10px;border:1px solid #ddd;">原因</th>
          <th style="padding:10px;border:1px solid #ddd;">状态</th>
          <th style="padding:10px;border:1px solid #ddd;">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in list" :key="item.id">
          <td style="padding:10px;border:1px solid #ddd;">{{ item.id }}</td>
          <td style="padding:10px;border:1px solid #ddd;">{{ item.reporter_name }}</td>
          <td style="padding:10px;border:1px solid #ddd;">{{ item.reason }}</td>
          <td style="padding:10px;border:1px solid #ddd;">
            <span v-if="item.status === 'pending'" style="color:orange;">待处理</span>
            <span v-else style="color:green;">已处理</span>
          </td>
          <td style="padding:10px;border:1px solid #ddd;">
            <button v-if="item.status === 'pending'" @click="handleApprove(item.id)" style="margin-right:5px;">✅ 通过</button>
            <button v-if="item.status === 'pending'" @click="handleReject(item.id)">❌ 驳回</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getReports, approveReport, rejectReport } from '@/api/admin'

const list = ref([])

const loadData = async () => {
  const res = await getReports()
  list.value = res.data.data || res.data || []
}

const handleApprove = async (id) => {
  await approveReport(id)
  await loadData()
}

const handleReject = async (id) => {
  await rejectReport(id)
  await loadData()
}

onMounted(loadData)
</script>