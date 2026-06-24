# 股票基金投资论坛 - 数据库设计文档

## 1. 数据库概述

本数据库设计用于支撑股票基金投资论坛的核心业务，包括用户管理、内容管理、社交互动、信息整合和管理运营五大系统。

### 1.1 数据库环境

| 项目 | 说明 |
|------|------|
| 数据库类型 | MySQL 8.0+ |
| 字符集 | utf8mb4 |
| 排序规则 | utf8mb4_unicode_ci |
| 存储引擎 | InnoDB |

---

## 2. 核心实体与关系

### 2.1 实体关系图 (ERD)

```mermaid
erDiagram
    USERS ||--o{ USER_PROFILES : has
    USERS ||--o{ USER_CERTIFICATIONS : has
    USERS ||--o{ USER_ACHIEVEMENTS : has
    USERS ||--o{ POSTS : creates
    USERS ||--o{ COMMENTS : creates
    USERS ||--o{ FOLLOWS : follows
    USERS ||--o{ GROUP_MEMBERS : joins
    SECTIONS ||--o{ POSTS : contains
    POSTS ||--o{ COMMENTS : has
    POSTS ||--o{ ATTACHMENTS : has
    POSTS ||--o{ VOTES : has
    GROUPS ||--o{ GROUP_MEMBERS : has
    MODERATIONS ||--o{ REPORTS : handles
```

---

## 3. 数据表设计

### 3.1 用户系统表

#### 3.1.1 users（用户基础信息表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 用户唯一标识 |
| username | VARCHAR(64) | NOT NULL, UNIQUE | 用户名 |
| email | VARCHAR(128) | UNIQUE | 邮箱 |
| phone | VARCHAR(20) | UNIQUE | 手机号 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| avatar_url | VARCHAR(512) | | 头像URL |
| auth_type | ENUM | NOT NULL, DEFAULT 'email' | 注册方式: email/phone/wechat/weibo |
| auth_provider | VARCHAR(32) | | 第三方账号标识 |
| verification_level | TINYINT | NOT NULL, DEFAULT 0 | 认证等级: 0-未认证,1-基础,2-实名,3-专业 |
| risk_assessment_score | INT | | 风险评估分数 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态: 0-禁用,1-正常,2-封禁 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.1.2 user_profiles（用户资料表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 用户ID |
| nickname | VARCHAR(64) | | 昵称 |
| bio | TEXT | | 个人简介 |
| experience_tags | VARCHAR(512) | | 投资经验标签(逗号分隔) |
| focus_markets | VARCHAR(256) | | 关注领域(A股/港股/美股/基金等) |
| risk_preference | TINYINT | DEFAULT 2 | 风险偏好:1-保守,2-稳健,3-积极,4-激进 |
| privacy_settings | JSON | | 隐私设置JSON |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.1.3 user_certifications（用户认证表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 用户ID |
| cert_type | ENUM | NOT NULL | 认证类型: basic/real_name/professional |
| cert_status | TINYINT | NOT NULL, DEFAULT 0 | 认证状态:0-待审核,1-通过,2-拒绝 |
| cert_data | JSON | | 认证资料(JSON格式) |
| verified_at | DATETIME | | 认证通过时间 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.1.4 user_achievements（用户成就表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 用户ID |
| post_count | INT | NOT NULL, DEFAULT 0 | 发帖数 |
|精华_count | INT | NOT NULL, DEFAULT 0 | 精华帖数 |
| influence_score | INT | NOT NULL, DEFAULT 0 | 影响力值 |
| medals | VARCHAR(512) | | 荣誉勋章(逗号分隔) |
| level | INT | NOT NULL, DEFAULT 1 | 用户等级 |
| points | INT | NOT NULL, DEFAULT 0 | 积分 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

---

### 3.2 内容系统表

#### 3.2.1 sections（板块表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 板块ID |
| name | VARCHAR(64) | NOT NULL | 板块名称 |
| code | VARCHAR(32) | NOT NULL, UNIQUE | 板块编码 |
| parent_id | BIGINT | FOREIGN KEY(sections.id) | 父板块ID |
| description | VARCHAR(512) | | 板块描述 |
| icon_url | VARCHAR(512) | | 板块图标 |
| sort_order | INT | NOT NULL, DEFAULT 0 | 排序顺序 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-禁用,1-启用 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.2.2 posts（帖子表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 帖子ID |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 作者ID |
| section_id | BIGINT | NOT NULL, FOREIGN KEY(sections.id) | 板块ID |
| title | VARCHAR(256) | NOT NULL | 帖子标题 |
| content | LONGTEXT | NOT NULL | 帖子内容 |
| post_type | ENUM | NOT NULL, DEFAULT 'normal' | 帖子类型:normal/article/poll/discussion |
| is_essence | TINYINT | NOT NULL, DEFAULT 0 | 是否精华:0-否,1-是 |
| is_top | TINYINT | NOT NULL, DEFAULT 0 | 是否置顶:0-否,1-是 |
| view_count | INT | NOT NULL, DEFAULT 0 | 浏览量 |
| like_count | INT | NOT NULL, DEFAULT 0 | 点赞数 |
| comment_count | INT | NOT NULL, DEFAULT 0 | 评论数 |
| share_count | INT | NOT NULL, DEFAULT 0 | 转发数 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-待审核,1-正常,2-隐藏,3-删除 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.2.3 comments（评论表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 评论ID |
| post_id | BIGINT | NOT NULL, FOREIGN KEY(posts.id) | 帖子ID |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 评论者ID |
| parent_id | BIGINT | FOREIGN KEY(comments.id) | 父评论ID(楼中楼) |
| content | TEXT | NOT NULL | 评论内容 |
| like_count | INT | NOT NULL, DEFAULT 0 | 点赞数 |
| mentioned_users | VARCHAR(512) | | @提及用户ID列表 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-待审核,1-正常,2-隐藏,3-删除 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.2.4 attachments（附件表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 附件ID |
| post_id | BIGINT | FOREIGN KEY(posts.id) | 关联帖子ID |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 上传者ID |
| file_name | VARCHAR(255) | NOT NULL | 文件名 |
| file_path | VARCHAR(512) | NOT NULL | 文件路径 |
| file_size | BIGINT | NOT NULL | 文件大小(字节) |
| file_type | VARCHAR(64) | | 文件类型 |
| status | TINYINT | NOT NULL, DEFAULT 0 | 状态:0-待审核,1-通过,2-拒绝 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 3.2.5 votes（投票表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 投票ID |
| post_id | BIGINT | NOT NULL, FOREIGN KEY(posts.id), UNIQUE | 关联帖子ID |
| title | VARCHAR(256) | NOT NULL | 投票标题 |
| options | JSON | NOT NULL | 投票选项(JSON数组) |
| is_multi_select | TINYINT | NOT NULL, DEFAULT 0 | 是否多选:0-单选,1-多选 |
| end_time | DATETIME | | 投票结束时间 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-关闭,1-开启 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 3.2.6 vote_records（投票记录表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 记录ID |
| vote_id | BIGINT | NOT NULL, FOREIGN KEY(votes.id) | 投票ID |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 投票用户ID |
| selected_options | VARCHAR(512) | NOT NULL | 选中选项ID列表 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

---

### 3.3 社交与关系系统表

#### 3.3.1 follows（关注关系表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| follower_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 关注者ID |
| followee_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 被关注者ID |
| is_star | TINYINT | NOT NULL, DEFAULT 0 | 是否特别关注:0-否,1-是 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-取消,1-关注 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.3.2 groups（群组表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 群组ID |
| name | VARCHAR(64) | NOT NULL | 群组名称 |
| description | VARCHAR(512) | | 群组描述 |
| avatar_url | VARCHAR(512) | | 群组头像 |
| privacy_type | ENUM | NOT NULL, DEFAULT 'public' | 隐私类型:public/private/approval |
| creator_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 创建者ID |
| member_count | INT | NOT NULL, DEFAULT 0 | 成员数量 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-禁用,1-正常 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.3.3 group_members（群组成员表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| group_id | BIGINT | NOT NULL, FOREIGN KEY(groups.id) | 群组ID |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 用户ID |
| role | ENUM | NOT NULL, DEFAULT 'member' | 角色:member/admin/owner |
| status | TINYINT | NOT NULL, DEFAULT 0 | 状态:0-待审核,1-通过,2-拒绝 |
| joined_at | DATETIME | | 加入时间 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.3.4 private_messages（私信表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 消息ID |
| sender_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 发送者ID |
| receiver_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 接收者ID |
| content | TEXT | NOT NULL | 消息内容 |
| image_urls | VARCHAR(1024) | | 图片URL列表(逗号分隔) |
| is_read | TINYINT | NOT NULL, DEFAULT 0 | 是否已读:0-未读,1-已读 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-撤回,1-正常 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

---

### 3.4 信息整合系统表

#### 3.4.1 hot_topics（热榜表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| title | VARCHAR(256) | NOT NULL | 热榜标题 |
| topic_type | ENUM | NOT NULL | 类型:post/stock/discussion |
| target_id | BIGINT | NOT NULL | 关联目标ID |
| hot_score | INT | NOT NULL, DEFAULT 0 | 热度分数 |
| rank | INT | NOT NULL, DEFAULT 0 | 排名 |
| period | ENUM | NOT NULL, DEFAULT 'daily' | 周期:daily/weekly/monthly |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.4.2 favorites（收藏表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 用户ID |
| post_id | BIGINT | NOT NULL, FOREIGN KEY(posts.id) | 帖子ID |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 3.4.3 likes（点赞表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| user_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 用户ID |
| target_type | ENUM | NOT NULL | 目标类型:post/comment |
| target_id | BIGINT | NOT NULL | 目标ID |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

---

### 3.5 管理运营系统表

#### 3.5.1 reports（举报表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| reporter_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 举报者ID |
| target_type | ENUM | NOT NULL | 目标类型:post/comment/user |
| target_id | BIGINT | NOT NULL | 目标ID |
| report_type | ENUM | NOT NULL | 举报类型:spam/harassment/fraud/other |
| reason | TEXT | | 举报理由 |
| status | TINYINT | NOT NULL, DEFAULT 0 | 状态:0-待处理,1-已受理,2-已解决,3-已驳回 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新时间 |

#### 3.5.2 moderations（审核记录表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| admin_id | BIGINT | NOT NULL, FOREIGN KEY(users.id) | 处理管理员ID |
| report_id | BIGINT | FOREIGN KEY(reports.id) | 关联举报ID |
| target_type | ENUM | NOT NULL | 目标类型:post/comment/user/attachment |
| target_id | BIGINT | NOT NULL | 目标ID |
| action_type | ENUM | NOT NULL | 操作类型:approve/reject/delete/warn/ban |
| action_reason | VARCHAR(512) | | 操作理由 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 3.5.3 sensitive_words（敏感词表）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| word | VARCHAR(64) | NOT NULL, UNIQUE | 敏感词 |
| category | VARCHAR(32) | | 分类 |
| replace_with | VARCHAR(64) | DEFAULT '*' | 替换内容 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态:0-禁用,1-启用 |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 3.5.4 audit_logs（操作审计日志）

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | 主键 |
| user_id | BIGINT | FOREIGN KEY(users.id) | 操作用户ID |
| action | VARCHAR(64) | NOT NULL | 操作类型 |
| target_type | VARCHAR(32) | | 目标类型 |
| target_id | BIGINT | | 目标ID |
| detail | TEXT | | 操作详情 |
| ip_address | VARCHAR(45) | | 操作IP |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

---

## 4. 索引设计

### 4.1 用户系统索引

| 表名 | 索引名 | 字段 | 类型 |
|------|--------|------|------|
| users | idx_users_email | email | UNIQUE |
| users | idx_users_phone | phone | UNIQUE |
| users | idx_users_status | status | NORMAL |
| users | idx_users_auth_type | auth_type | NORMAL |
| user_profiles | idx_user_profiles_user_id | user_id | UNIQUE |
| user_certifications | idx_cert_user_id_type | user_id, cert_type | UNIQUE |
| user_achievements | idx_achievements_user_id | user_id | UNIQUE |

### 4.2 内容系统索引

| 表名 | 索引名 | 字段 | 类型 |
|------|--------|------|------|
| sections | idx_sections_parent_id | parent_id | NORMAL |
| sections | idx_sections_status | status | NORMAL |
| posts | idx_posts_section_id | section_id | NORMAL |
| posts | idx_posts_user_id | user_id | NORMAL |
| posts | idx_posts_status | status | NORMAL |
| posts | idx_posts_is_essence | is_essence | NORMAL |
| posts | idx_posts_created_at | created_at | NORMAL |
| comments | idx_comments_post_id | post_id | NORMAL |
| comments | idx_comments_user_id | user_id | NORMAL |
| comments | idx_comments_parent_id | parent_id | NORMAL |

### 4.3 社交系统索引

| 表名 | 索引名 | 字段 | 类型 |
|------|--------|------|------|
| follows | idx_follows_follower | follower_id | NORMAL |
| follows | idx_follows_followee | followee_id | NORMAL |
| follows | idx_follows_follower_followee | follower_id, followee_id | UNIQUE |
| groups | idx_groups_creator_id | creator_id | NORMAL |
| group_members | idx_group_members_group_id | group_id | NORMAL |
| group_members | idx_group_members_user_id | user_id | NORMAL |
| group_members | idx_group_members_group_user | group_id, user_id | UNIQUE |

### 4.4 信息整合索引

| 表名 | 索引名 | 字段 | 类型 |
|------|--------|------|------|
| hot_topics | idx_hot_topics_period | period | NORMAL |
| hot_topics | idx_hot_topics_rank | rank | NORMAL |
| favorites | idx_favorites_user_post | user_id, post_id | UNIQUE |
| likes | idx_likes_user_target | user_id, target_type, target_id | UNIQUE |

### 4.5 管理系统索引

| 表名 | 索引名 | 字段 | 类型 |
|------|--------|------|------|
| reports | idx_reports_status | status | NORMAL |
| reports | idx_reports_reporter_id | reporter_id | NORMAL |
| moderations | idx_moderations_admin_id | admin_id | NORMAL |
| sensitive_words | idx_sensitive_words_word | word | UNIQUE |

---

## 5. 数据库初始化脚本

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS stock_forum CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE stock_forum;

-- 用户基础信息表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(128) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(512),
    auth_type ENUM('email', 'phone', 'wechat', 'weibo') NOT NULL DEFAULT 'email',
    auth_provider VARCHAR(32),
    verification_level TINYINT NOT NULL DEFAULT 0,
    risk_assessment_score INT,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_phone (phone),
    INDEX idx_users_status (status),
    INDEX idx_users_auth_type (auth_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户资料表
CREATE TABLE user_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    nickname VARCHAR(64),
    bio TEXT,
    experience_tags VARCHAR(512),
    focus_markets VARCHAR(256),
    risk_preference TINYINT DEFAULT 2,
    privacy_settings JSON,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE INDEX idx_user_profiles_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户认证表
CREATE TABLE user_certifications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    cert_type ENUM('basic', 'real_name', 'professional') NOT NULL,
    cert_status TINYINT NOT NULL DEFAULT 0,
    cert_data JSON,
    verified_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE INDEX idx_cert_user_id_type (user_id, cert_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户成就表
CREATE TABLE user_achievements (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    post_count INT NOT NULL DEFAULT 0,
    essence_count INT NOT NULL DEFAULT 0,
    influence_score INT NOT NULL DEFAULT 0,
    medals VARCHAR(512),
    level INT NOT NULL DEFAULT 1,
    points INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE INDEX idx_achievements_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 板块表
CREATE TABLE sections (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    code VARCHAR(32) NOT NULL UNIQUE,
    parent_id BIGINT,
    description VARCHAR(512),
    icon_url VARCHAR(512),
    sort_order INT NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES sections(id) ON DELETE SET NULL,
    INDEX idx_sections_parent_id (parent_id),
    INDEX idx_sections_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 帖子表
CREATE TABLE posts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    section_id BIGINT NOT NULL,
    title VARCHAR(256) NOT NULL,
    content LONGTEXT NOT NULL,
    post_type ENUM('normal', 'article', 'poll', 'discussion') NOT NULL DEFAULT 'normal',
    is_essence TINYINT NOT NULL DEFAULT 0,
    is_top TINYINT NOT NULL DEFAULT 0,
    view_count INT NOT NULL DEFAULT 0,
    like_count INT NOT NULL DEFAULT 0,
    comment_count INT NOT NULL DEFAULT 0,
    share_count INT NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE,
    INDEX idx_posts_section_id (section_id),
    INDEX idx_posts_user_id (user_id),
    INDEX idx_posts_status (status),
    INDEX idx_posts_is_essence (is_essence),
    INDEX idx_posts_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 评论表
CREATE TABLE comments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    parent_id BIGINT,
    content TEXT NOT NULL,
    like_count INT NOT NULL DEFAULT 0,
    mentioned_users VARCHAR(512),
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
    INDEX idx_comments_post_id (post_id),
    INDEX idx_comments_user_id (user_id),
    INDEX idx_comments_parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 附件表
CREATE TABLE attachments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT,
    user_id BIGINT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(64),
    status TINYINT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 投票表
CREATE TABLE votes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL UNIQUE,
    title VARCHAR(256) NOT NULL,
    options JSON NOT NULL,
    is_multi_select TINYINT NOT NULL DEFAULT 0,
    end_time DATETIME,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 投票记录表
CREATE TABLE vote_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    vote_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    selected_options VARCHAR(512) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vote_id) REFERENCES votes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 关注关系表
CREATE TABLE follows (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    is_star TINYINT NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (followee_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_follows_follower (follower_id),
    INDEX idx_follows_followee (followee_id),
    UNIQUE INDEX idx_follows_follower_followee (follower_id, followee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 群组表
CREATE TABLE groups (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    description VARCHAR(512),
    avatar_url VARCHAR(512),
    privacy_type ENUM('public', 'private', 'approval') NOT NULL DEFAULT 'public',
    creator_id BIGINT NOT NULL,
    member_count INT NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_groups_creator_id (creator_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 群组成员表
CREATE TABLE group_members (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    group_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    role ENUM('member', 'admin', 'owner') NOT NULL DEFAULT 'member',
    status TINYINT NOT NULL DEFAULT 0,
    joined_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_group_members_group_id (group_id),
    INDEX idx_group_members_user_id (user_id),
    UNIQUE INDEX idx_group_members_group_user (group_id, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 私信表
CREATE TABLE private_messages (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    sender_id BIGINT NOT NULL,
    receiver_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    image_urls VARCHAR(1024),
    is_read TINYINT NOT NULL DEFAULT 0,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 热榜表
CREATE TABLE hot_topics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(256) NOT NULL,
    topic_type ENUM('post', 'stock', 'discussion') NOT NULL,
    target_id BIGINT NOT NULL,
    hot_score INT NOT NULL DEFAULT 0,
    rank INT NOT NULL DEFAULT 0,
    period ENUM('daily', 'weekly', 'monthly') NOT NULL DEFAULT 'daily',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_hot_topics_period (period),
    INDEX idx_hot_topics_rank (rank)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 收藏表
CREATE TABLE favorites (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    UNIQUE INDEX idx_favorites_user_post (user_id, post_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 点赞表
CREATE TABLE likes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    target_type ENUM('post', 'comment') NOT NULL,
    target_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE INDEX idx_likes_user_target (user_id, target_type, target_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 举报表
CREATE TABLE reports (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    reporter_id BIGINT NOT NULL,
    target_type ENUM('post', 'comment', 'user') NOT NULL,
    target_id BIGINT NOT NULL,
    report_type ENUM('spam', 'harassment', 'fraud', 'other') NOT NULL,
    reason TEXT,
    status TINYINT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reporter_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_reports_status (status),
    INDEX idx_reports_reporter_id (reporter_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 审核记录表
CREATE TABLE moderations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    admin_id BIGINT NOT NULL,
    report_id BIGINT,
    target_type ENUM('post', 'comment', 'user', 'attachment') NOT NULL,
    target_id BIGINT NOT NULL,
    action_type ENUM('approve', 'reject', 'delete', 'warn', 'ban') NOT NULL,
    action_reason VARCHAR(512),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE SET NULL,
    INDEX idx_moderations_admin_id (admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 敏感词表
CREATE TABLE sensitive_words (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(64) NOT NULL UNIQUE,
    category VARCHAR(32),
    replace_with VARCHAR(64) DEFAULT '*',
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sensitive_words_word (word)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 操作审计日志
CREATE TABLE audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    action VARCHAR(64) NOT NULL,
    target_type VARCHAR(32),
    target_id BIGINT,
    detail TEXT,
    ip_address VARCHAR(45),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 6. 数据字典

### 6.1 枚举类型定义

| 枚举名称 | 值 | 说明 |
|----------|----|------|
| auth_type | email/phone/wechat/weibo | 用户注册方式 |
| verification_level | 0/1/2/3 | 认证等级:0-未认证,1-基础,2-实名,3-专业 |
| cert_type | basic/real_name/professional | 认证类型 |
| cert_status | 0/1/2 | 认证状态:0-待审核,1-通过,2-拒绝 |
| post_type | normal/article/poll/discussion | 帖子类型 |
| privacy_type | public/private/approval | 群组隐私类型 |
| role | member/admin/owner | 群组成员角色 |
| topic_type | post/stock/discussion | 热榜类型 |
| period | daily/weekly/monthly | 热榜周期 |
| target_type | post/comment/user/attachment | 目标类型 |
| report_type | spam/harassment/fraud/other | 举报类型 |
| action_type | approve/reject/delete/warn/ban | 审核操作类型 |

---

## 7. 数据库安全

### 7.1 访问控制

- 应用程序使用专用数据库账号，最小权限原则
- 禁止直接暴露数据库端口到公网
- 定期轮换数据库密码

### 7.2 数据加密

- 用户密码使用 bcrypt 哈希存储
- 敏感信息（如身份证号）加密存储
- 传输层使用 SSL/TLS

### 7.3 备份策略

- 每日全量备份
- 每小时增量备份
- 备份文件加密存储
