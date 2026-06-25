import api from './request'  // 根据你实际存放 axios 实例的文件名调整

// 获取举报列表
export const getReports = (params) => api.get('/admin/reports', { params })

// 通过举报
export const approveReport = (id) => api.put(`/admin/reports/${id}/approve`)

// 驳回举报
export const rejectReport = (id) => api.put(`/admin/reports/${id}/reject`)

// 获取用户列表（管理员用）
export const getUsers = (params) => api.get('/admin/users', { params })

// 禁言用户
export const muteUser = (id, data) => api.post(`/admin/users/${id}/mute`, data)

// 获取敏感词列表
export const getSensitiveWords = () => api.get('/admin/words')

// 添加敏感词
export const addSensitiveWord = (word) => api.post('/admin/words', { word })

// 删除敏感词
export const deleteSensitiveWord = (id) => api.delete(`/admin/words/${id}`)