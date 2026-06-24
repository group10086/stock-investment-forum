# 股票基金投资论坛 - 后端API接口文档

## OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: 股票基金投资论坛 API
  description: 股票基金投资论坛后端RESTful API接口文档
  version: 1.0.0
  contact:
    name: 开发团队
    email: dev@stockforum.com

servers:
  - url: http://localhost:8000/api
    description: 本地开发服务器

tags:
  - name: 用户系统
    description: 用户注册、认证、资料管理
  - name: 内容系统
    description: 板块、帖子、评论管理
  - name: 社交系统
    description: 关注、群组、私信
  - name: 信息整合
    description: 热榜、搜索、推荐
  - name: 管理运营
    description: 审核、用户管理、数据分析

paths:
  /users/register:
    post:
      summary: 用户注册
      tags: [用户系统]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  minLength: 3
                  maxLength: 64
                password:
                  type: string
                  minLength: 6
                email:
                  type: string
                  format: email
                phone:
                  type: string
                auth_type:
                  type: string
                  enum: [email, phone, wechat, weibo]
                auth_provider:
                  type: string
      responses:
        '201':
          description: 注册成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    example: 201
                  message:
                    type: string
                    example: 注册成功
                  data:
                    $ref: '#/components/schemas/User'
        '400':
          description: 参数错误
        '409':
          description: 用户已存在

  /users/login:
    post:
      summary: 用户登录
      tags: [用户系统]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                phone:
                  type: string
                password:
                  type: string
                auth_type:
                  type: string
                  enum: [email, phone, wechat, weibo]
      responses:
        '200':
          description: 登录成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    example: 200
                  message:
                    type: string
                    example: 登录成功
                  data:
                    type: object
                    properties:
                      user:
                        $ref: '#/components/schemas/User'
                      token:
                        type: string
                        example: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        '401':
          description: 账号或密码错误

  /users/{user_id}:
    get:
      summary: 获取用户详情
      tags: [用户系统]
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    example: 200
                  data:
                    $ref: '#/components/schemas/UserProfile'
        '404':
          description: 用户不存在

    put:
      summary: 更新用户资料
      tags: [用户系统]
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                nickname:
                  type: string
                bio:
                  type: string
                avatar_url:
                  type: string
                experience_tags:
                  type: string
                focus_markets:
                  type: string
                risk_preference:
                  type: integer
                  minimum: 1
                  maximum: 4
                privacy_settings:
                  type: object
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限

  /users/{user_id}/certifications:
    post:
      summary: 提交认证申请
      tags: [用户系统]
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                cert_type:
                  type: string
                  enum: [basic, real_name, professional]
                cert_data:
                  type: object
      responses:
        '200':
          description: 提交成功
        '400':
          description: 参数错误

    get:
      summary: 获取用户认证信息
      tags: [用户系统]
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/UserCertification'

  /users/{user_id}/achievements:
    get:
      summary: 获取用户成就
      tags: [用户系统]
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/UserAchievement'

  /users/{user_id}/risk-assessment:
    post:
      summary: 提交风险评估问卷
      tags: [用户系统]
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                answers:
                  type: array
                  items:
                    type: integer
      responses:
        '200':
          description: 提交成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  message:
                    type: string
                  data:
                    type: object
                    properties:
                      score:
                        type: integer
                      risk_level:
                        type: string

  /sections:
    get:
      summary: 获取板块列表
      tags: [内容系统]
      parameters:
        - name: parent_id
          in: query
          schema:
            type: integer
        - name: status
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Section'

    post:
      summary: 创建板块
      tags: [内容系统]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                code:
                  type: string
                parent_id:
                  type: integer
                description:
                  type: string
                icon_url:
                  type: string
                sort_order:
                  type: integer
      responses:
        '201':
          description: 创建成功
        '403':
          description: 无权限

  /sections/{section_id}:
    get:
      summary: 获取板块详情
      tags: [内容系统]
      parameters:
        - name: section_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/Section'
        '404':
          description: 板块不存在

    put:
      summary: 更新板块
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: section_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                description:
                  type: string
                icon_url:
                  type: string
                sort_order:
                  type: integer
                status:
                  type: integer
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限

    delete:
      summary: 删除板块
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: section_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 删除成功
        '403':
          description: 无权限

  /posts:
    get:
      summary: 获取帖子列表
      tags: [内容系统]
      parameters:
        - name: section_id
          in: query
          schema:
            type: integer
        - name: user_id
          in: query
          schema:
            type: integer
        - name: post_type
          in: query
          schema:
            type: string
            enum: [normal, article, poll, discussion]
        - name: is_essence
          in: query
          schema:
            type: integer
        - name: is_top
          in: query
          schema:
            type: integer
        - name: status
          in: query
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Post'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: 创建帖子
      tags: [内容系统]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                section_id:
                  type: integer
                  required: true
                title:
                  type: string
                  required: true
                content:
                  type: string
                  required: true
                post_type:
                  type: string
                  enum: [normal, article, poll, discussion]
                  default: normal
                vote_options:
                  type: array
                  items:
                    type: string
                is_multi_select:
                  type: boolean
                  default: false
                vote_end_time:
                  type: string
                  format: date-time
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/Post'
        '400':
          description: 参数错误

  /posts/{post_id}:
    get:
      summary: 获取帖子详情
      tags: [内容系统]
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/PostDetail'
        '404':
          description: 帖子不存在

    put:
      summary: 更新帖子
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                content:
                  type: string
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限

    delete:
      summary: 删除帖子
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 删除成功
        '403':
          description: 无权限

  /posts/{post_id}/views:
    post:
      summary: 增加浏览量
      tags: [内容系统]
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 成功

  /posts/{post_id}/likes:
    post:
      summary: 点赞/取消点赞
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 操作成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: object
                    properties:
                      liked:
                        type: boolean
                      like_count:
                        type: integer

  /posts/{post_id}/favorites:
    post:
      summary: 收藏/取消收藏
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 操作成功

  /posts/{post_id}/shares:
    post:
      summary: 转发帖子
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                content:
                  type: string
      responses:
        '201':
          description: 转发成功

  /posts/{post_id}/votes:
    post:
      summary: 参与投票
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                selected_options:
                  type: array
                  items:
                    type: integer
      responses:
        '200':
          description: 投票成功
        '400':
          description: 投票已结束或参数错误

  /posts/{post_id}/attachments:
    post:
      summary: 上传附件
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: post_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
      responses:
        '201':
          description: 上传成功
        '400':
          description: 文件格式不支持

  /comments:
    get:
      summary: 获取评论列表
      tags: [内容系统]
      parameters:
        - name: post_id
          in: query
          required: true
          schema:
            type: integer
        - name: parent_id
          in: query
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Comment'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: 创建评论
      tags: [内容系统]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                post_id:
                  type: integer
                  required: true
                parent_id:
                  type: integer
                content:
                  type: string
                  required: true
                mentioned_users:
                  type: array
                  items:
                    type: integer
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/Comment'

  /comments/{comment_id}:
    put:
      summary: 更新评论
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: comment_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                content:
                  type: string
                  required: true
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限

    delete:
      summary: 删除评论
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: comment_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 删除成功
        '403':
          description: 无权限

  /comments/{comment_id}/likes:
    post:
      summary: 评论点赞
      tags: [内容系统]
      security:
        - BearerAuth: []
      parameters:
        - name: comment_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 操作成功

  /follows:
    get:
      summary: 获取关注列表
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: query
          schema:
            type: integer
        - name: type
          in: query
          schema:
            type: string
            enum: [following, followers]
          default: following
        - name: is_star
          in: query
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Follow'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: 关注/取消关注用户
      tags: [社交系统]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                followee_id:
                  type: integer
                  required: true
                is_star:
                  type: boolean
                  default: false
      responses:
        '200':
          description: 操作成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: object
                    properties:
                      followed:
                        type: boolean

  /groups:
    get:
      summary: 获取群组列表
      tags: [社交系统]
      parameters:
        - name: privacy_type
          in: query
          schema:
            type: string
            enum: [public, private, approval]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Group'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: 创建群组
      tags: [社交系统]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  required: true
                description:
                  type: string
                avatar_url:
                  type: string
                privacy_type:
                  type: string
                  enum: [public, private, approval]
                  default: public
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/Group'

  /groups/{group_id}:
    get:
      summary: 获取群组详情
      tags: [社交系统]
      parameters:
        - name: group_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/GroupDetail'
        '404':
          description: 群组不存在

    put:
      summary: 更新群组
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: group_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                description:
                  type: string
                avatar_url:
                  type: string
                privacy_type:
                  type: string
                  enum: [public, private, approval]
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限

    delete:
      summary: 删除群组
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: group_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 删除成功
        '403':
          description: 无权限

  /groups/{group_id}/members:
    get:
      summary: 获取群组成员列表
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: group_id
          in: path
          required: true
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/GroupMember'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: 加入群组
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: group_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 申请成功
        '400':
          description: 已在群组中或申请待处理

  /groups/{group_id}/members/{user_id}:
    put:
      summary: 处理入群申请/设置角色
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: group_id
          in: path
          required: true
          schema:
            type: integer
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: integer
                  enum: [0, 1, 2]
                role:
                  type: string
                  enum: [member, admin, owner]
      responses:
        '200':
          description: 操作成功
        '403':
          description: 无权限

    delete:
      summary: 移除群成员
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: group_id
          in: path
          required: true
          schema:
            type: integer
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 移除成功
        '403':
          description: 无权限

  /private-messages:
    get:
      summary: 获取私信列表
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: receiver_id
          in: query
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/PrivateMessage'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: 发送私信
      tags: [社交系统]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                receiver_id:
                  type: integer
                  required: true
                content:
                  type: string
                image_urls:
                  type: array
                  items:
                    type: string
      responses:
        '201':
          description: 发送成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/PrivateMessage'

  /private-messages/{message_id}:
    put:
      summary: 标记已读
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: message_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 成功

    delete:
      summary: 撤回消息
      tags: [社交系统]
      security:
        - BearerAuth: []
      parameters:
        - name: message_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 撤回成功
        '400':
          description: 超过撤回时间

  /hot-topics:
    get:
      summary: 获取热榜
      tags: [信息整合]
      parameters:
        - name: period
          in: query
          schema:
            type: string
            enum: [daily, weekly, monthly]
            default: daily
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/HotTopic'

  /feed:
    get:
      summary: 获取个性化Feed
      tags: [信息整合]
      security:
        - BearerAuth: []
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Post'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

  /search:
    get:
      summary: 全文搜索
      tags: [信息整合]
      parameters:
        - name: keyword
          in: query
          required: true
          schema:
            type: string
        - name: type
          in: query
          schema:
            type: string
            enum: [all, post, user, stock]
            default: all
        - name: section_id
          in: query
          schema:
            type: integer
        - name: time_range
          in: query
          schema:
            type: string
            enum: [all, today, week, month]
        - name: is_essence
          in: query
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 搜索成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: object
                    properties:
                      posts:
                        type: array
                        items:
                          $ref: '#/components/schemas/Post'
                      users:
                        type: array
                        items:
                          $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

  /search/suggest:
    get:
      summary: 搜索联想
      tags: [信息整合]
      parameters:
        - name: keyword
          in: query
          required: true
          schema:
            type: string
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        type:
                          type: string
                        value:
                          type: string
                        label:
                          type: string

  /reports:
    get:
      summary: 获取举报列表
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: status
          in: query
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Report'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '403':
          description: 无权限

    post:
      summary: 提交举报
      tags: [管理运营]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                target_type:
                  type: string
                  enum: [post, comment, user]
                  required: true
                target_id:
                  type: integer
                  required: true
                report_type:
                  type: string
                  enum: [spam, harassment, fraud, other]
                  required: true
                reason:
                  type: string
      responses:
        '201':
          description: 提交成功
        '400':
          description: 参数错误

  /reports/{report_id}:
    get:
      summary: 获取举报详情
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: report_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    $ref: '#/components/schemas/ReportDetail'
        '403':
          description: 无权限

    put:
      summary: 处理举报
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: report_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: integer
                  enum: [1, 2, 3]
                  required: true
                action_type:
                  type: string
                  enum: [approve, reject, delete, warn, ban]
                action_reason:
                  type: string
      responses:
        '200':
          description: 处理成功
        '403':
          description: 无权限

  /moderations:
    get:
      summary: 获取审核记录
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: admin_id
          in: query
          schema:
            type: integer
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Moderation'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '403':
          description: 无权限

  /sensitive-words:
    get:
      summary: 获取敏感词列表
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/SensitiveWord'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '403':
          description: 无权限

    post:
      summary: 添加敏感词
      tags: [管理运营]
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                word:
                  type: string
                  required: true
                category:
                  type: string
                replace_with:
                  type: string
                  default: '*'
      responses:
        '201':
          description: 添加成功
        '403':
          description: 无权限

  /sensitive-words/{word_id}:
    put:
      summary: 更新敏感词
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: word_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                word:
                  type: string
                category:
                  type: string
                replace_with:
                  type: string
                status:
                  type: integer
      responses:
        '200':
          description: 更新成功
        '403':
          description: 无权限

    delete:
      summary: 删除敏感词
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: word_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: 删除成功
        '403':
          description: 无权限

  /analytics/activity:
    get:
      summary: 获取活跃度统计
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: start_date
          in: query
          schema:
            type: string
            format: date
        - name: end_date
          in: query
          schema:
            type: string
            format: date
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: object
                    properties:
                      total_users:
                        type: integer
                      active_users:
                        type: integer
                      new_users:
                        type: integer
                      total_posts:
                        type: integer
                      total_comments:
                        type: integer
                      daily_trend:
                        type: array
                        items:
                          type: object
                          properties:
                            date:
                              type: string
                            posts:
                              type: integer
                            comments:
                              type: integer
        '403':
          description: 无权限

  /analytics/hot-topics:
    get:
      summary: 获取热门话题分析
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: period
          in: query
          schema:
            type: string
            enum: [daily, weekly, monthly]
            default: weekly
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        topic:
                          type: string
                        type:
                          type: string
                        hot_score:
                          type: integer
                        discussion_count:
                          type: integer
        '403':
          description: 无权限

  /analytics/user-participation:
    get:
      summary: 获取用户参与度报告
      tags: [管理运营]
      security:
        - BearerAuth: []
      parameters:
        - name: start_date
          in: query
          schema:
            type: string
            format: date
        - name: end_date
          in: query
          schema:
            type: string
            format: date
      responses:
        '200':
          description: 获取成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  data:
                    type: object
                    properties:
                      avg_posts_per_user:
                        type: number
                      avg_comments_per_user:
                        type: number
                      active_user_ratio:
                        type: number
                      retention_rate:
                        type: number
                      top_users:
                        type: array
                        items:
                          type: object
                          properties:
                            user_id:
                              type: integer
                            username:
                              type: string
                            post_count:
                              type: integer
                            comment_count:
                              type: integer
        '403':
          description: 无权限

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
        phone:
          type: string
        avatar_url:
          type: string
        auth_type:
          type: string
        verification_level:
          type: integer
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    UserProfile:
      type: object
      properties:
        user:
          $ref: '#/components/schemas/User'
        nickname:
          type: string
        bio:
          type: string
        experience_tags:
          type: string
        focus_markets:
          type: string
        risk_preference:
          type: integer
        privacy_settings:
          type: object

    UserCertification:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: integer
        cert_type:
          type: string
        cert_status:
          type: integer
        cert_data:
          type: object
        verified_at:
          type: string
          format: date-time
        created_at:
          type: string
          format: date-time

    UserAchievement:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: integer
        post_count:
          type: integer
        essence_count:
          type: integer
        influence_score:
          type: integer
        medals:
          type: string
        level:
          type: integer
        points:
          type: integer

    Section:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        code:
          type: string
        parent_id:
          type: integer
        description:
          type: string
        icon_url:
          type: string
        sort_order:
          type: integer
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    Post:
      type: object
      properties:
        id:
          type: integer
        user_id:
          type: integer
        username:
          type: string
        user_avatar:
          type: string
        section_id:
          type: integer
        section_name:
          type: string
        title:
          type: string
        content:
          type: string
        post_type:
          type: string
        is_essence:
          type: integer
        is_top:
          type: integer
        view_count:
          type: integer
        like_count:
          type: integer
        comment_count:
          type: integer
        share_count:
          type: integer
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    PostDetail:
      type: object
      properties:
        post:
          $ref: '#/components/schemas/Post'
        vote:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            options:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  text:
                    type: string
                  count:
                    type: integer
            is_multi_select:
              type: boolean
            end_time:
              type: string
              format: date-time
            status:
              type: integer

    Comment:
      type: object
      properties:
        id:
          type: integer
        post_id:
          type: integer
        user_id:
          type: integer
        username:
          type: string
        user_avatar:
          type: string
        parent_id:
          type: integer
        content:
          type: string
        like_count:
          type: integer
        mentioned_users:
          type: array
          items:
            type: integer
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    Follow:
      type: object
      properties:
        id:
          type: integer
        follower_id:
          type: integer
        followee_id:
          type: integer
        followee:
          $ref: '#/components/schemas/User'
        is_star:
          type: boolean
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    Group:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
        avatar_url:
          type: string
        privacy_type:
          type: string
        creator_id:
          type: integer
        creator_name:
          type: string
        member_count:
          type: integer
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    GroupDetail:
      type: object
      properties:
        group:
          $ref: '#/components/schemas/Group'
        is_member:
          type: boolean
        member_role:
          type: string
        member_status:
          type: integer

    GroupMember:
      type: object
      properties:
        id:
          type: integer
        group_id:
          type: integer
        user_id:
          type: integer
        username:
          type: string
        user_avatar:
          type: string
        role:
          type: string
        status:
          type: integer
        joined_at:
          type: string
          format: date-time

    PrivateMessage:
      type: object
      properties:
        id:
          type: integer
        sender_id:
          type: integer
        sender_name:
          type: string
        sender_avatar:
          type: string
        receiver_id:
          type: integer
        content:
          type: string
        image_urls:
          type: array
          items:
            type: string
        is_read:
          type: boolean
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    HotTopic:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        topic_type:
          type: string
        target_id:
          type: integer
        hot_score:
          type: integer
        rank:
          type: integer
        period:
          type: string
        created_at:
          type: string
          format: date-time

    Report:
      type: object
      properties:
        id:
          type: integer
        reporter_id:
          type: integer
        reporter_name:
          type: string
        target_type:
          type: string
        target_id:
          type: integer
        report_type:
          type: string
        reason:
          type: string
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    ReportDetail:
      type: object
      properties:
        report:
          $ref: '#/components/schemas/Report'
        target_data:
          type: object

    Moderation:
      type: object
      properties:
        id:
          type: integer
        admin_id:
          type: integer
        admin_name:
          type: string
        report_id:
          type: integer
        target_type:
          type: string
        target_id:
          type: integer
        action_type:
          type: string
        action_reason:
          type: string
        created_at:
          type: string
          format: date-time

    SensitiveWord:
      type: object
      properties:
        id:
          type: integer
        word:
          type: string
        category:
          type: string
        replace_with:
          type: string
        status:
          type: integer
        created_at:
          type: string
          format: date-time

    Pagination:
      type: object
      properties:
        page:
          type: integer
        size:
          type: integer
        total:
          type: integer
        total_pages:
          type: integer
```
