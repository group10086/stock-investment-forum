# stock-investment-forum
股票基金投资论坛-软件工程课程设计

## 项目简介
本项目为软件工程课程设计选题三，实现一个股票基金投资论坛，支持用户系统、内容发布、社交互动、信息聚合、管理运营等功能。

## 负责人
- 李明轩（学号U202417321）

## 团队成员

| 角色 | 姓名 | 学号 | 核心职责 | 负责模块 |
|------|------|:----:|---------|:--------:|
| 组长/项目经理 | 李明轩 | U202417321 | 总体进度把控、任务分配、组织会议、对外沟通、代码审查 | 全模块 |
| 后端开发A | 邓文博 | U202417313 | 用户系统与认证、内容系统、社交与数据功能 | 模块2,3,4 |
| 后端开发B | 蔡云飞 | U202417312 | 后端辅助开发、接口联调 | 模块2,3,4 |
| 前端开发A | 刘安邦 | U202417322 | 页面与交互工作 | 模块1,3 |
| 前端开发B | 孟令腾 | U202417325 | 组件与管理员页面 | 模块3 |
| 数据库与测试 | 杨仲晨 | U202417332 | 数据库设计、测试用例生成、单元测试 | 模块2,3,4 |
| 文档与AI协作 | 郭森垚 | U202417316 | AI提示词管理、文档编写、AI使用记录 | 模块1,2,3,4 |
| 运维与部署 | 高宁朔 | U202417314 | Git仓库管理、环境配置、部署上线、CI/CD | 模块1,5 |

## 目录结构

```
stock-investment-forum/
│
├── docs/                              # 全部文档
│   ├── user_stories.md                # 用户故事（26个）
│   ├── use_cases.md                   # 交互场景
│   ├── architect.md                   # 架构与类设计（12个数据模型）
│   ├── ui_design.md                   # 前端UI设计
│   ├── backend_api.md                 # 后端API文档
│   ├── db.md                          # 数据库设计
│   ├── test.md                        # 测试报告
│   ├── install.md                     # 安装文档
│   ├── user_guid.md                   # 使用说明书
│   └── assign.md                      # 工作完成情况记录
│
├── backend/                           # 后端代码（FastAPI + Python）
│   ├── app/
│   │   ├── main.py                    # FastAPI 入口，注册8个路由模块
│   │   ├── config.py                  # 配置（数据库URL、JWT、CORS）
│   │   ├── database.py                # 数据库连接（SQLAlchemy）
│   │   ├── models/                    # 数据模型（12个SQLAlchemy模型）
│   │   │   ├── user.py                # 用户模型
│   │   │   ├── post.py                # 帖子模型
│   │   │   ├── comment.py             # 评论模型
│   │   │   ├── follow.py              # 关注关系
│   │   │   ├── post_like.py           # 帖子点赞
│   │   │   ├── bookmark.py            # 收藏
│   │   │   ├── comment_like.py        # 评论点赞
│   │   │   ├── message.py             # 私信
│   │   │   ├── group.py               # 群组+群组成员
│   │   │   ├── report.py              # 举报
│   │   │   └── sensitive_word.py      # 敏感词
│   │   ├── schemas/                   # Pydantic 数据校验
│   │   │   ├── user.py                # 用户请求/响应Schema
│   │   │   ├── post.py                # 帖子请求/响应Schema
│   │   │   ├── comment.py             # 评论请求/响应Schema
│   │   │   └── message.py             # 私信请求/响应Schema
│   │   ├── conftest.py                  # 测试配置（fixtures）
│   ├── routers/                   # 路由层（8个路由模块）
│   │   │   ├── auth.py                # 认证（注册/登录）
│   │   │   ├── user.py                # 用户管理
│   │   │   ├── post.py                # 帖子CRUD
│   │   │   ├── comment.py             # 评论管理
│   │   │   ├── message.py             # 私信
│   │   │   ├── group.py               # 群组
│   │   │   ├── search.py              # 搜索
│   │   │   └── admin.py               # 管理运营
│   │   ├── services/                  # 业务逻辑层（8个服务）
│   │   │   ├── auth_service.py        # 认证服务
│   │   │   ├── user_service.py        # 用户服务
│   │   │   ├── post_service.py        # 帖子服务
│   │   │   ├── comment_service.py     # 评论服务
│   │   │   ├── message_service.py     # 私信服务
│   │   │   ├── group_service.py       # 群组服务
│   │   │   ├── search_service.py      # 搜索服务
│   │   │   └── admin_service.py       # 管理运营服务
│   │   ├── utils/                     # 工具类
│   │   │   ├── jwt_handler.py         # JWT认证工具
│   │   │   ├── sensitive_filter.py    # DFA敏感词过滤器
│   │   │   └── pagination.py          # 分页工具
│   │   └── tests/                     # 单元测试
│   │       ├── test_auth.py           # 认证模块测试
│   │       ├── test_post.py           # 帖子模块测试
│   │       ├── test_comment.py        # 评论模块测试
│   │       └── test_admin.py          # 管理模块测试
│   └── requirements.txt               # Python依赖
│
├── frontend/                          # 前端代码（Vue3 + Vite）
│   ├── src/
│   │   ├── api/                       # API接口层
│   │   ├── components/                # 公共组件
│   │   ├── router/                    # 路由配置
│   │   ├── stores/                    # Pinia状态管理
│   │   ├── views/                     # 页面组件
│   │   │   ├── auth/                  # 登录/注册
│   │   │   ├── home/                  # 首页
│   │   │   ├── post/                  # 帖子（详情/创建/编辑）
│   │   │   ├── user/                  # 用户中心/编辑/关注/粉丝
│   │   │   └── messages/              # 私信
│   │   └── assets/                    # 静态资源
│   ├── public/                        # 公共资源
│   └── package.json                   # npm依赖
│
├── sql/                               # 数据库脚本
│   ├── init.sql                       # 建表脚本（12张表+18个索引）
│   └── sample_data.sql                # 测试数据
│
├── ai_prompts/                        # AI交互记录
│   └── ai.md                          # 所有AI使用记录（模块1~4）
│
└── README.md                          # 本文件
```

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|:----:|
| 前端框架 | Vue 3 | ^3.5.34 |
| UI组件库 | Element Plus | ^2.14.0 |
| 构建工具 | Vite | ^8.0.12 |
| 状态管理 | Pinia | ^3.0.4 |
| 路由 | Vue Router | ^5.0.7 |
| HTTP客户端 | Axios | ^1.16.1 |
| 后端框架 | FastAPI | ^0.104.1 |
| ORM | SQLAlchemy | ^2.0.23 |
| 数据库 | PostgreSQL | — |
| 认证 | JWT (python-jose) | — |
| 密码加密 | bcrypt (passlib) | — |
| 测试 | pytest + httpx | — |
| 版本控制 | GitHub | — |

## 功能模块

### 1️⃣ 用户系统
- 多方式注册（邮箱/手机号）
- 用户登录（bcrypt加密 + JWT Token 7天有效期）
- 分级认证（基础认证/实名认证/专业认证加V）
- 投资者适当性评估问卷
- 个人资料查看/编辑（头像、昵称、简介、投资偏好）
- 隐私设置（邮箱公开、允许私信）
- 关注/取消关注、粉丝列表（含星标关注、分页）
- 积分与等级系统（发帖+5分，注册+10分，100分/级）
- 成就系统（发帖/评论/获赞里程碑）

### 2️⃣ 内容系统
- 帖子发布/编辑/删除（软删除）
- 富文本编辑器（wangeditor，支持图片和格式）
- 帖子列表多维度排序（最新/最热/精华/关注）
- 分类筛选（A股/港股/美股/基金/技术分析/价值投资）
- 评论系统（含楼中楼回复）
- 点赞/取消点赞、收藏/取消收藏
- 附件上传支持（PDF/Excel）

### 3️⃣ 社交与信息
- 私信系统（未读计数、会话列表）
- 群组创建/加入/退出
- 全局搜索（帖子+用户）
- 高级筛选（时间/热度/精华/市场维度）
- 搜索联想（自动补全）

### 4️⃣ 管理运营
- **敏感词过滤**：基于 DFA 算法的高效匹配
- **重复内容检测**：基于内容相似度
- **举报管理**：创建/审核/处理（删除/驳回）
- **用户禁言**：带时效的禁言/自动解除
- **数据分析**：DAU统计、活跃度、内容趋势

## 进度

| 模块 | 状态 | 时间 |
|:----:|:----:|:----:|
| ✅ 模块1：项目启动与需求分析 | 已完成 | 2026.4.30 - 2026.5.8 |
| ✅ 模块2：AI辅助设计 | 已完成 | 2026.5.8 - 2026.5.15 |
| ✅ 模块3：AI辅助编码实现 | 已完成 | 2026.5.15 - 2026.6.10 |
| ✅ 模块4：AI辅助测试与调试 | 已完成 | 2026.6.10 - 2026.6.13 |
| ⬜ 模块5：上线部署与报告撰写 | 待开始 | 2026.6.13 — |

## 测试结果

### 后端单元测试（33/33 ✅ 全部通过）

| 模块 | 测试文件 | 用例数 | 结果 |
|:----:|:--------|:------:|:----:|
| 🔐 认证 | `test_auth.py` | 9 | ✅ 全部通过 |
| 📝 帖子 | `test_post.py` | 9 | ✅ 全部通过 |
| 💬 评论 | `test_comment.py` | 5 | ✅ 全部通过 |
| ⚙️ 管理运营 | `test_admin.py` | 10 | ✅ 全部通过 |

### 前端构建测试

| 项目 | 结果 |
|:----|:----:|
| Vite 构建 | ✅ 成功（1677 modules，1.02s） |
| 编译错误 | ✅ 0 个 |
| 输出文件 | ✅ 40 个（20 JS + 20 CSS） |
| 页面路由 | ✅ 全部正常（含新增的成就/认证/问卷/手机注册页） |

## 快速启动

### 环境要求
- Python 3.9+
- Node.js 18+
- （可选）PostgreSQL（默认使用 SQLite）

### 1. 后端启动
```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 直接启动（默认 SQLite，自动建表）
python -m uvicorn app.main:app --reload --port 8000

# 初始化演示数据（首次运行）
python seed_data.py
```

### 2. 前端启动
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 3. 运行测试
```bash
cd backend

# 运行全部测试（33个用例）
pytest app/tests/ -v

# 运行单个模块
pytest app/tests/test_auth.py -v
pytest app/tests/test_post.py -v
pytest app/tests/test_comment.py -v
pytest app/tests/test_admin.py -v
```

### 4. 访问地址
| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:5173 |
| 后端 API | http://localhost:8000 |
| API 文档（Swagger） | http://localhost:8000/api/docs |
| API 文档（ReDoc） | http://localhost:8000/api/redoc |

### 5. 演示账号
| 用户名 | 密码 | 备注 |
|--------|------|------|
| dubo2248 | （已注册） | 当前用户 |
| trader_wang | 123456 | 投资达人 |
| quant_li | 123456 | 量化分析师 |
| fund_zhang | 123456 | 基金小张 |
| tech_chen | 123456 | 科技股研究员 |
| newbie_liu | 123456 | 韭菜小白 |

### 6. 切换数据库
```bash
# 默认 SQLite（无需配置）
# 切换到 PostgreSQL：
# 1. 安装 PostgreSQL 并创建数据库
# 2. 设置环境变量
set DATABASE_URL=postgresql://user:password@localhost:5432/stock_forum
# 3. 执行 sql/init.sql 建表
# 4. 重启后端
```

## 仓库地址
https://github.com/group10086/stock-investment-forum.git