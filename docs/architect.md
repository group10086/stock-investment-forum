# 架构与类设计

## 一、系统架构

### 整体架构（三层架构）

```
┌─────────────────────────────────────────────────┐
│                  前端 (Vue3)                      │
│    Element Plus · Vue Router · Pinia · Axios     │
└─────────────────────┬───────────────────────────┘
                      │ HTTP / JSON
                      ▼
┌─────────────────────────────────────────────────┐
│           后端 API (FastAPI + Python)             │
│  ┌───────────┐ ┌──────────┐ ┌────────────────┐  │
│  │  Routers   │ │ Services │ │    Models      │  │
│  │ (路由层)   │→│ (业务层)  │→│  (数据模型)    │  │
│  └───────────┘ └──────────┘ └────────────────┘  │
└─────────────────────┬───────────────────────────┘
                      │ SQLAlchemy ORM
                      ▼
┌─────────────────────────────────────────────────┐
│              PostgreSQL 数据库                     │
│       用户表 · 帖子表 · 评论表 · 收藏表 · ...     │
└─────────────────────────────────────────────────┘
```

### 后端模块划分

```
backend/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置文件
│   ├── database.py          # 数据库连接
│   ├── middleware.py         # JWT认证中间件
│   ├── models/              # SQLAlchemy 数据模型
│   │   ├── __init__.py
│   │   ├── user.py          # 用户模型
│   │   ├── post.py          # 帖子模型
│   │   ├── comment.py       # 评论模型
│   │   ├── message.py       # 私信模型
│   │   └── report.py        # 举报/敏感词模型
│   ├── schemas/             # Pydantic 数据校验
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── message.py
│   ├── routers/             # API 路由
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证相关
│   │   ├── user.py          # 用户管理
│   │   ├── post.py          # 帖子管理
│   │   ├── comment.py       # 评论管理
│   │   ├── message.py       # 私信管理
│   │   ├── group.py         # 群组管理
│   │   ├── search.py        # 搜索
│   │   └── admin.py         # 管理运营
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── post_service.py
│   │   ├── comment_service.py
│   │   ├── message_service.py
│   │   ├── group_service.py
│   │   ├── search_service.py
│   │   └── admin_service.py
│   ├── utils/               # 工具类
│   │   ├── __init__.py
│   │   ├── jwt_handler.py   # JWT 工具
│   │   ├── sensitive_filter.py  # 敏感词过滤
│   │   └── pagination.py    # 分页工具
│   └── tests/               # 单元测试
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_post.py
│       ├── test_comment.py
│       └── test_admin.py
└── requirements.txt
```

---

## 二、类设计

### 2.1 数据模型（SQLAlchemy Models）

#### User 用户模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 用户ID |
| username | String(50) | 用户名，唯一 |
| email | String(100) | 邮箱，唯一 |
| password_hash | String(255) | 密码哈希 |
| nickname | String(50) | 昵称 |
| avatar | String(255) | 头像URL |
| bio | Text | 个人简介 |
| investment_preference | JSON | 投资偏好数组 |
| github | String(255) | GitHub链接 |
| email_public | Boolean | 是否公开邮箱 |
| allow_messages | Boolean | 是否允许私信 |
| is_verified | Boolean | 是否实名认证 |
| is_admin | Boolean | 是否为管理员 |
| is_muted | Boolean | 是否被禁言 |
| muted_until | DateTime | 禁言截止时间 |
| created_at | DateTime | 注册时间 |
| updated_at | DateTime | 更新时间 |

#### Post 帖子模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 帖子ID |
| user_id | Integer (FK) | 作者ID |
| title | String(200) | 标题 |
| content | Text | 内容（富文本HTML） |
| summary | String(500) | 摘要 |
| category | String(50) | 板块分类 |
| images | JSON | 图片数组 |
| tags | JSON | 标签数组 |
| is_top | Boolean | 是否置顶 |
| is_essence | Boolean | 是否精华 |
| is_hot | Boolean | 是否热门 |
| view_count | Integer | 浏览量 |
| like_count | Integer | 点赞数 |
| comment_count | Integer | 评论数 |
| bookmark_count | Integer | 收藏数 |
| is_deleted | Boolean | 是否删除（软删除） |
| created_at | DateTime | 发布时间 |
| updated_at | DateTime | 更新时间 |

#### Comment 评论模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 评论ID |
| post_id | Integer (FK) | 所属帖子ID |
| user_id | Integer (FK) | 评论者ID |
| parent_id | Integer (FK, nullable) | 父评论ID（楼中楼） |
| content | Text | 评论内容 |
| like_count | Integer | 点赞数 |
| is_deleted | Boolean | 是否删除 |
| created_at | DateTime | 评论时间 |

#### Message 私信模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 私信ID |
| sender_id | Integer (FK) | 发送者ID |
| receiver_id | Integer (FK) | 接收者ID |
| content | Text | 内容 |
| is_read | Boolean | 是否已读 |
| created_at | DateTime | 发送时间 |

#### Follow 关注模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 记录ID |
| follower_id | Integer (FK) | 关注者ID |
| followed_id | Integer (FK) | 被关注者ID |
| created_at | DateTime | 关注时间 |

#### PostLike 帖子点赞模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 记录ID |
| user_id | Integer (FK) | 用户ID |
| post_id | Integer (FK) | 帖子ID |
| created_at | DateTime | 点赞时间 |

#### Bookmark 收藏模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 记录ID |
| user_id | Integer (FK) | 用户ID |
| post_id | Integer (FK) | 帖子ID |
| created_at | DateTime | 收藏时间 |

#### CommentLike 评论点赞模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 记录ID |
| user_id | Integer (FK) | 用户ID |
| comment_id | Integer (FK) | 评论ID |
| created_at | DateTime | 点赞时间 |

#### Report 举报模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 举报ID |
| reporter_id | Integer (FK) | 举报人ID |
| target_type | String(20) | 举报类型（post/comment/user） |
| target_id | Integer | 目标ID |
| reason | String(200) | 举报原因 |
| status | String(20) | 状态（pending/resolved/dismissed） |
| handled_by | Integer (FK, nullable) | 处理人ID |
| handled_at | DateTime (nullable) | 处理时间 |
| created_at | DateTime | 举报时间 |

#### SensitiveWord 敏感词模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 记录ID |
| word | String(100) | 敏感词 |
| replacement | String(100) | 替换词 |
| created_at | DateTime | 添加时间 |

#### Group 群组模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 群组ID |
| name | String(100) | 群组名 |
| description | Text | 群组描述 |
| owner_id | Integer (FK) | 创建者ID |
| is_public | Boolean | 是否公开 |
| created_at | DateTime | 创建时间 |

#### GroupMember 群组成员模型
| 属性 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 记录ID |
| group_id | Integer (FK) | 群组ID |
| user_id | Integer (FK) | 用户ID |
| role | String(20) | 角色（owner/admin/member） |
| created_at | DateTime | 加入时间 |

---

## 三、API路由设计

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/auth/login | 用户登录 | 否 |
| POST | /api/auth/register | 用户注册 | 否 |
| GET | /api/user/info | 获取当前用户信息 | 是 |
| PUT | /api/user/info | 更新用户信息 | 是 |
| GET | /api/user/{id} | 获取用户详情 | 否 |
| POST | /api/user/{id}/follow | 关注用户 | 是 |
| DELETE | /api/user/{id}/follow | 取消关注 | 是 |
| GET | /api/user/following | 获取关注列表 | 是 |
| GET | /api/user/followers | 获取粉丝列表 | 是 |
| GET | /api/posts | 获取帖子列表 | 否 |
| GET | /api/posts/{id} | 获取帖子详情 | 否 |
| POST | /api/posts | 创建帖子 | 是 |
| PUT | /api/posts/{id} | 更新帖子 | 是 |
| DELETE | /api/posts/{id} | 删除帖子 | 是 |
| POST | /api/posts/{id}/like | 点赞帖子 | 是 |
| DELETE | /api/posts/{id}/like | 取消点赞 | 是 |
| POST | /api/posts/{id}/bookmark | 收藏帖子 | 是 |
| DELETE | /api/posts/{id}/bookmark | 取消收藏 | 是 |
| GET | /api/posts/{postId}/comments | 获取评论列表 | 否 |
| POST | /api/posts/{postId}/comments | 创建评论 | 是 |
| DELETE | /api/comments/{id} | 删除评论 | 是 |
| POST | /api/comments/{id}/like | 点赞评论 | 是 |
| GET | /api/messages/{userId} | 获取私信列表 | 是 |
| POST | /api/messages | 发送私信 | 是 |
| GET | /api/messages/unread-count | 未读消息数 | 是 |
| GET | /api/groups | 获取群组列表 | 否 |
| POST | /api/groups | 创建群组 | 是 |
| GET | /api/groups/{id} | 获取群组详情 | 否 |
| POST | /api/groups/{id}/join | 加入群组 | 是 |
| DELETE | /api/groups/{id}/leave | 退出群组 | 是 |
| GET | /api/search | 全局搜索 | 否 |
| GET | /api/admin/reports | 获取举报列表 | 管理 |
| PUT | /api/admin/reports/{id} | 处理举报 | 管理 |
| POST | /api/admin/user/{id}/mute | 禁言用户 | 管理 |
| POST | /api/admin/user/{id}/unmute | 解除禁言 | 管理 |
| GET | /api/admin/sensitive-words | 获取敏感词列表 | 管理 |
| POST | /api/admin/sensitive-words | 添加敏感词 | 管理 |
| DELETE | /api/admin/sensitive-words/{id} | 删除敏感词 | 管理 |

---

## 四、关键业务流程

### 4.1 JWT认证流程
```
用户登录 → 验证凭证 → 生成JWT Token（含user_id, role） 
→ 返回Token → 前端存储到localStorage 
→ 每次请求携带Authorization: Bearer <token> 
→ 中间件验证 → 获取当前用户 → 放行/拒绝
```

### 4.2 敏感词过滤流程
```
用户发帖/评论 → 文本经过敏感词过滤器 
→ 使用DFA算法检测敏感词 → 替换为*** 
→ 存储过滤后的内容 → 同时记录命中日志
```

### 4.3 举报处理流程
```
用户举报 → 创建举报记录（状态:pending） 
→ 管理员审核 → 判断处理（删除内容/禁言用户/驳回）
→ 更新举报状态 → 通知举报人和被举报人
```

---

## 五、安全性设计

1. **密码安全**：使用 bcrypt 哈希存储
2. **JWT认证**：Token 过期机制，刷新机制
3. **输入校验**：Pydantic 模型校验所有输入
4. **防SQL注入**：SQLAlchemy ORM 参数化查询
5. **XSS防护**：HTML 转义输出
6. **速率限制**：API 调用频率限制
7. **软删除**：重要数据采用软删除策略
