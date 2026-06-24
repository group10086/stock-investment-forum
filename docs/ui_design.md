# 前端 UI 设计文档

## 项目概述

**项目名称**: 股票基金投资论坛  
**技术栈**: Vue 3 + Element Plus + Axios + Pinia + Vue Router + WangEditor  
**负责人**: 前端A组  
**最后更新**: 2026-06-24

---

## 系统页面结构图
股票投资论坛
├── 首页 (/)
│ ├── 帖子列表（热门/最新/推荐）
│ ├── 搜索栏（带联想功能）
│ └── 侧边栏（热门标签、活跃用户）
│
├── 认证模块
│ ├── 登录页 (/login)
│ │ ├── 邮箱登录
│ │ ├── 手机号登录
│ │ └── 第三方登录（微信/QQ/GitHub）
│ │
│ ├── 注册页 (/register)
│ │ ├── 邮箱注册 (/register-email)
│ │ └── 手机号注册 (/register-phone)
│ │
│ ├── 分级认证页 (/authentication)
│ │ ├── 实名认证
│ │ ├── 投资者适当性问卷 (/questionnaire)
│ │ └── 认证状态展示
│ │
│ └── 成就系统页 (/achievement)
│ ├── 成就徽章展示
│ ├── 积分排行
│ └── 等级进度
│
├── 帖子模块
│ ├── 发帖页 (/post/create)
│ │ ├── 普通帖子
│ │ │ ├── 标题
│ │ │ ├── 富文本内容编辑器（WangEditor）
│ │ │ ├── 板块选择
│ │ │ ├── 标签
│ │ │ ── 附件上传（PDF/Excel）
│ │ │
│ │ └── 投票帖子
│ │ ├── 投票选项（2-10个）
│ │ ├── 投票截止时间
│ │ └── 是否匿名
│ │
│ ├── 帖子详情页 (/post/:id)
│ │ ├── 帖子内容（富文本渲染）
│ │ ├── 投票组件（看涨/看跌）
│ │ ├── 评论列表
│ │ ├── 点赞/收藏/分享
│ │ └── 附件下载
│ │
│ ├── 编辑帖子页 (/post/:id/edit)
│ └── 帖子列表页（首页集成）
│
── 社交模块
│ ├── 关注列表页 (/following)
│ │ ├── 特别关注（星标用户）
│ │ └── 普通关注
│ │
│ ├── 粉丝列表页 (/followers)
│ │
│ └── 私信页 (/messages/:userId?)
│ ├── 聊天列表（左侧）
│ └── 聊天窗口（右侧）
│ ├── 消息气泡
│ ├── 发送输入框
│ └── 表情/图片发送
│
├── 用户中心模块
│ ├── 个人主页 (/user/:id)
│ │ ├── 用户信息卡片
│ │ ├── 发布的帖子
│ │ ├── 收藏的帖子
│ │ └── 统计数据（关注/粉丝/帖子数）
│ │
│ └── 个人资料编辑页 (/profile/edit)
│ ├── 基本信息（昵称/头像/简介）
│ ├── 联系方式
│ └── 隐私设置
│
├── 搜索模块
│ ├── 搜索结果页 (/search)
│ └── 搜索联想（下拉建议）
│
└── 其他
├── 404 页面 (/:pathMatch(.))
└── 管理后台（预留）
---

## 页面详细设计

### 1. 登录页 (/login)

**功能**:
- 用户登录（邮箱/手机号）
- 记住密码
- 忘记密码
- 第三方登录入口

**组件**:
- el-input - 账号输入
- el-input (type="password") - 密码输入
- el-checkbox - 记住密码
- el-button - 登录按钮
- el-divider - 分割线
- 第三方登录图标按钮（微信/QQ/GitHub）

**交互**:
- 表单验证（必填项、格式校验）
- 登录成功跳转首页或重定向页面
- 登录失败显示错误提示

---

### 2. 注册页 (/register)

**功能**:
- 邮箱注册
- 手机号注册
- 验证码验证
- 用户协议勾选

**组件**:
- el-tabs - 切换邮箱/手机注册
- el-input - 邮箱/手机号输入
- el-input - 验证码输入
- el-button - 获取验证码/注册
- el-checkbox - 同意用户协议

**交互**:
- 实时验证邮箱/手机号格式
- 倒计时获取验证码
- 注册成功后自动登录并跳转

---

### 3. 分级认证页 (/authentication)

**功能**:
- 实名认证
- 投资者适当性评估
- 认证状态展示

**组件**:
- el-steps - 认证步骤指示器
- el-upload - 身份证上传
- el-form - 个人信息表单
- el-progress - 认证进度条

**状态**:
- 未认证
- 审核中
- 已认证（初级/中级/高级）

---

### 4. 投资者适当性问卷 (/questionnaire)

**功能**:
- 风险评估问卷
- 风险等级评定
- 投资建议匹配

**组件**:
- el-radio-group - 单选题
- el-checkbox-group - 多选题
- el-slider - 评分题
- el-progress - 答题进度

**结果**:
- 保守型 / 稳健型 / 平衡型 / 成长型 / 进取型

---

### 5. 成就系统页 (/achievement)

**功能**:
- 成就徽章展示
- 积分排行榜
- 等级进度

**组件**:
- el-card - 成就卡片
- el-badge - 徽章标识
- el-table - 排行榜
- el-progress - 等级进度条

**成就类型**:
- 新手上路、发帖达人、精华作者、投资专家等

---

### 6. 发帖页 (/post/create)

**功能**:
- 发布普通帖子
- 发布投票帖子
- 富文本编辑
- 附件上传

**组件**:
- el-input - 标题输入
- WangEditor - 富文本编辑器
- el-select - 板块选择
- el-tag - 标签输入
- el-upload - 附件上传（支持 PDF/XLS/XLSX）
- el-switch - 是否开启投票
- el-input - 投票选项（动态增减）
- el-date-picker - 投票截止时间

**富文本功能**:
- 加粗、斜体、下划线
- 标题层级（H1-H6）
- 列表（有序/无序）
- 引用块
- 超链接
- 图片插入
- 代码块

---

### 7. 帖子详情页 (/post/:id)

**功能**:
- 查看帖子内容
- 参与投票
- 发表评论
- 点赞/收藏/分享
- 下载附件

**组件**:
- 富文本内容渲染区
- el-radio-group - 投票选项（看涨/看跌/其他）
- el-progress - 投票结果展示
- el-comment - 评论列表
- el-button - 点赞/收藏/分享
- el-link - 附件下载

---

### 8. 关注列表页 (/following)

**功能**:
- 查看关注的用户
- 区分特别关注和普通关注
- 取消关注

**组件**:
- el-tabs - 切换全部/特别关注
- el-card - 用户卡片
- el-icon (Star) - 星标标识
- el-button - 取消关注/设为特别关注

**数据结构**:
{
  id: 1,
  username: '巴菲特研究院',
  avatar: 'url',
  isSpecial: true,
  bio: '价值投资理念传播者',
  followersCount: 10000
}

---

### 9. 私信页 (/messages/:userId?)

**功能**:
- 聊天列表
- 聊天窗口
- 发送消息
- 查看历史消息

**布局**:
- 左侧：聊天列表（30%宽度）
- 右侧：聊天窗口（70%宽度）

**组件**:
- el-scrollbar - 滚动容器
- el-avatar - 用户头像
- el-input - 消息输入
- el-button - 发送按钮
- 自定义消息气泡组件

**消息类型**:
- 文本消息
- 图片消息（预留）
- 系统通知

---

### 10. 搜索联想

**功能**:
- 输入时实时显示搜索建议
- 点击建议快速搜索

**实现方式**:
// 防抖处理
const handleSearch = debounce((keyword) => {
  if (!keyword) return
  searchApi.getSuggestions(keyword).then(res => {
    suggestions.value = res.data
  })
}, 300)

**UI**:
- el-autocomplete 或自定义下拉列表
- 显示热门搜索词
- 高亮匹配部分

---

## 技术选型说明

### 核心框架
- **Vue 3**: Composition API，更好的性能和开发体验
- **Vite**: 极速的开发服务器和构建工具

### UI 组件库
- **Element Plus**: 企业级 UI 组件库，丰富的组件和完善的文档

### 富文本编辑器
- **WangEditor**: 轻量、简洁、易用，适合中文场景
  - 优点：体积小、API 简单、支持 Vue 3
  - 替代方案：Quill、TinyMCE

### 状态管理
- **Pinia**: Vue 官方推荐的状态管理库，比 Vuex 更简洁

### HTTP 客户端
- **Axios**: 成熟的 HTTP 客户端，支持拦截器、请求/响应转换

### 路由管理
- **Vue Router 4**: 官方路由管理器，支持动态路由、路由守卫

### 图标
- **Element Plus Icons**: 与 Element Plus 完美集成

---

## 设计规范

### 颜色规范
--primary-color: #409EFF;      /* 主题蓝 */
--success-color: #67C23A;      /* 成功绿 */
--warning-color: #E6A23C;      /* 警告橙 */
--danger-color: #F56C6C;       /* 危险红 */
--text-primary: #303133;       /* 主要文字 */
--text-regular: #606266;       /* 常规文字 */
--text-secondary: #909399;     /* 次要文字 */
--border-color: #DCDFE6;       /* 边框色 */
--background-color: #F5F7FA;   /* 背景色 */

### 字体规范
- 主字体：-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial
- 字号：14px（基础）、16px（正文）、18px（小标题）、20px（标题）

### 间距规范
- 内边距：8px、16px、24px、32px
- 外边距：8px、16px、24px

### 圆角规范
- 小圆角：4px
- 中圆角：8px
- 大圆角：16px

---

## 响应式设计

### 断点
- 移动端：< 768px
- 平板端：768px - 1024px
- 桌面端：> 1024px

### 适配策略
- 使用 Element Plus 的响应式栅格系统
- 移动端隐藏侧边栏，使用抽屉菜单
- 图片和视频自适应容器宽度

---

## 性能优化

### 代码分割
- 路由懒加载：component: () => import('@/views/xxx.vue')
- 大型组件异步加载

### 图片优化
- 使用 WebP 格式
- 懒加载：loading="lazy"
- CDN 加速

### 缓存策略
- 静态资源长期缓存
- API 数据短期缓存（Pinia persist）

---

## 待办事项

### 高优先级 ⭐⭐⭐⭐⭐
- [x] UI 设计文档（本文档）
- [ ] 富文本编辑器集成（WangEditor）
- [ ] 私信页面完整实现
- [ ] 投票帖子功能
- [ ] 附件上传功能

### 中优先级 ⭐⭐⭐⭐
- [ ] 特别关注功能
- [ ] 搜索联想功能
- [ ] 手机号注册页面
- [ ] 第三方登录集成

### 低优先级 ⭐⭐⭐
- [ ] 成就系统页面（可先做静态展示）
- [ ] 投资者适当性问卷（可先做静态展示）
- [ ] 分级认证页面（可先做静态展示）

---

## 附录

### API 接口约定
详见 backend_api.md

### 组件复用清单
- UserCard.vue - 用户信息卡片
- PostCard.vue - 帖子卡片
- CommentItem.vue - 评论项
- MessageBubble.vue - 消息气泡
- VotePanel.vue - 投票面板

### 参考资源
- Element Plus 文档: https://element-plus.org/
- WangEditor 文档: https://www.wangeditor.com/
- Vue 3 官方文档: https://cn.vuejs.org/
- Pinia 官方文档: https://pinia.vuejs.org/zh/