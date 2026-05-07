# stock-investment-forum
股票基金投资论坛-软件工程课程设计

## 项目简介
本项目为软件工程课程设计选题三，实现一个股票基金投资论坛，支持用户系统、内容发布、社交互动、信息聚合、管理运营等功能。

## 负责人
- 李明轩（学号U202417321）

## 团队成员
|        班级        |   姓名  |     学号    |
|-------------------|---------|------------|
| 软件工程2401班     | 李明轩  | U202417321 |
| 软件工程2401班     | 蔡云飞  | U202417312 |
| 软件工程2401班     | 邓文博  | U202417313 |
| 软件工程2401班     | 高宁朔  | U202417314 |
| 软件工程2401班     | 刘安邦  | U202417322 |
| 软件工程2401班     | 杨仲晨  | U202417332 |
| 软件工程2401班     | 郭森垚  | U202417316 |
| 软件工程2401班     | 孟令腾  | U202417325 |

## 目录结构
stock-investment-forum/
│
├── docs/ # 全部文档
│ ├── user_stories.md # 用户故事
│ ├── use_cases.md # 交互场景
│ ├── architect.md # 架构与类设计
│ ├── ui_design.md # 前端UI设计
│ ├── backend_api.md # 后端API文档
│ ├── db.md # 数据库设计
│ ├── test.md # 测试报告
│ ├── install.md # 安装文档
│ ├── user_guid.md # 使用说明书
│ └── assign.md # 工作完成情况记录
│
├── backend/ # 后端代码（FastAPI + Python）
│ ├── app/
│ │ ├── main.py # 入口文件
│ │ ├── routers/ # 路由层
│ │ ├── models/ # 数据模型
│ │ └── services/ # 业务逻辑
│ └── requirements.txt # Python依赖
│
├── frontend/ # 前端代码（Vue3 + Vite）
│ ├── src/ # 源码
│ ├── public/ # 静态资源
│ └── package.json # npm依赖
│
├── sql/ # 数据库脚本
│ ├── init.sql # 建表脚本
│ └── sample_data.sql # 测试数据
│
├── ai_prompts/ # AI交互记录
│ └── ai.md # 所有AI使用记录
│
└── README.md # 本文件

## 技术栈（初定）
- 前端：Vue3 + Element Plus
- 后端：Python FastAPI
- 数据库：PostgreSQL + Redis
- 版本控制：Gitee

## 进度
- [x] 模块1：项目启动与需求分析（进行中）
- [ ] 模块2：AI辅助设计
- [ ] 模块3：AI辅助编码实现
- [ ] 模块4：AI辅助测试与调试
- [ ] 模块5：上线部署与报告撰写

## 仓库地址
https://github.com/group10086/stock-investment-forum.git