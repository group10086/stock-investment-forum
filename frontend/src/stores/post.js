import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/request'  // 调用你项目里已有的 axios 实例

export const usePostStore = defineStore('post', () => {
  const list = ref([])
  const loading = ref(false)

  // 获取帖子列表
  const fetchList = async (params = {}) => {
    loading.value = true
    try {
      const res = await api.get('/posts', { params })
      // 如果后端返回格式是 { code:200, data:[...] }
      list.value = res.data.data || res.data
    } catch (e) {
      console.error('加载失败', e)
    } finally {
      loading.value = false
    }
  }

  return { list, loading, fetchList }
})