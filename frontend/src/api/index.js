import request from './request'

// 用户相关接口
export const authApi = {
  // 登录
  login: (data) => request.post('/auth/login', data),
  // 注册
  register: (data) => request.post('/auth/register', data),
  // 获取当前用户信息
  getUserInfo: () => request.get('/user/info'),
  // 更新用户信息
  updateUserInfo: (data) => request.put('/user/info', data),
  // 获取用户详情
  getUserDetail: (id) => request.get(`/user/${id}`),
  // 关注用户
  followUser: (id) => request.post(`/user/${id}/follow`),
  // 取消关注
  unfollowUser: (id) => request.delete(`/user/${id}/follow`),
  // 获取我的关注列表
  getFollowingList: (params) => request.get('/user/following', { params }),
  // 获取我的粉丝列表
  getFollowersList: (params) => request.get('/user/followers', { params })
}

// 帖子相关接口
export const postApi = {
  // 获取帖子列表
  getPostList: (params) => request.get('/posts', { params }),
  // 获取帖子详情
  getPostDetail: (id) => request.get(`/posts/${id}`),
  // 创建帖子
  createPost: (data) => request.post('/posts', data),
  // 更新帖子
  updatePost: (id, data) => request.put(`/posts/${id}`, data),
  // 删除帖子
  deletePost: (id) => request.delete(`/posts/${id}`),
  // 点赞帖子
  likePost: (id) => request.post(`/posts/${id}/like`),
  // 取消点赞
  unlikePost: (id) => request.delete(`/posts/${id}/like`),
  // 收藏帖子
  bookmarkPost: (id) => request.post(`/posts/${id}/bookmark`),
  // 取消收藏
  unbookmarkPost: (id) => request.delete(`/posts/${id}/bookmark`)
}

// 评论相关接口
export const commentApi = {
  // 获取评论列表
  getCommentList: (postId, params) => request.get(`/posts/${postId}/comments`, { params }),
  // 发表评论
  createComment: (postId, data) => request.post(`/posts/${postId}/comments`, data),
  // 删除评论
  deleteComment: (id) => request.delete(`/comments/${id}`),
  // 点赞评论
  likeComment: (id) => request.post(`/comments/${id}/like`)
}

// 私信相关接口
export const messageApi = {
  // 获取私信列表
  getMessageList: (userId, params) => request.get(`/messages/${userId}`, { params }),
  // 发送私信
  sendMessage: (data) => request.post('/messages', data),
  // 获取未读消息数量
  getUnreadCount: () => request.get('/messages/unread-count')
}

// 群组相关接口
export const groupApi = {
  // 获取群组列表
  getGroupList: (params) => request.get('/groups', { params }),
  // 创建群组
  createGroup: (data) => request.post('/groups', data),
  // 获取群组详情
  getGroupDetail: (id) => request.get(`/groups/${id}`),
  // 加入群组
  joinGroup: (id) => request.post(`/groups/${id}/join`),
  // 退出群组
  leaveGroup: (id) => request.delete(`/groups/${id}/leave`)
}

// 搜索接口
export const searchApi = {
  // 全局搜索
  search: (params) => request.get('/search', { params })
}
