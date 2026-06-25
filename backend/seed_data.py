# -*- coding: utf-8 -*-
"""种子数据 - 初始化演示数据"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.message import Message
from app.models.follow import Follow
from app.models.star_follow import StarFollow
from app.models.group import Group, GroupMember
from passlib.hash import bcrypt
from datetime import datetime

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    # 检查是否已有种子数据
    existing = db.query(User).filter(User.username == "trader_wang").first()
    if existing:
        print("种子数据已存在，跳过")
        db.close()
        sys.exit(0)

    # ========== 演示用户 ==========
    demo_users = [
        {"username": "trader_wang", "nickname": "投资达人", "bio": "10年A股投资经验，专注价值投资", "email": "wang@test.com"},
        {"username": "quant_li", "nickname": "量化分析师", "bio": "量化交易策略研究，Python量化", "email": "li@test.com"},
        {"username": "fund_zhang", "nickname": "基金小张", "bio": "基金定投实践者，分享定投心得", "email": "zhang@test.com"},
        {"username": "tech_chen", "nickname": "科技股研究员", "bio": "专注科技板块，擅长基本面分析", "email": "chen@test.com"},
        {"username": "newbie_liu", "nickname": "韭菜小白", "bio": "新手入门，请大家多多指教", "email": "liu@test.com"},
    ]

    created_users = []
    for u in demo_users:
        user = User(
            username=u["username"],
            nickname=u["nickname"],
            email=u["email"],
            bio=u["bio"],
            password_hash=bcrypt.hash("123456"),
            is_verified=True,
            allow_messages=True,
            score=100,
            level=1,
            created_at=datetime.now(),
        )
        db.add(user)
        db.flush()
        created_users.append(user)
        print(f"创建用户: {u['nickname']} (id={user.id})")

    # ========== 帖子 ==========
    demo_posts = [
        {
            "user_idx": 0, "title": "2026年下半年A股投资策略分享",
            "content": "<h2>一、宏观经济展望</h2><p>2026年下半年，中国经济持续复苏，GDP增速预计维持在5%左右。政策面持续宽松，降准降息仍有空间。</p><h2>二、行业配置建议</h2><p>建议重点关注三大方向：</p><ol><li><strong>新能源产业链</strong>：光伏、储能、电动车</li><li><strong>半导体国产替代</strong>：芯片设计、设备材料</li><li><strong>消费复苏</strong>：白酒、家电、旅游</li></ol><h2>三、风险提示</h2><p>地缘政治风险、美联储政策转向、房地产行业不确定性仍需关注。</p>",
            "summary": "分析2026下半年A股投资机会，重点关注新能源、半导体和消费板块",
            "category": "stock", "tags": ["A股", "投资策略", "行业分析"],
        },
        {
            "user_idx": 1, "title": "量化交易入门：从零搭建你的第一个策略",
            "content": "<h2>什么是量化交易</h2><p>量化交易是利用数学模型和计算机程序来执行交易策略的方法。相比主观交易，量化交易更加客观、纪律性强。</p><h2>入门三步走</h2><ol><li><strong>数据获取</strong>：使用Tushare、AKShare等获取A股数据</li><li><strong>策略开发</strong>：从简单的均线交叉策略开始</li><li><strong>回测验证</strong>：使用Backtrader或Zipline进行历史回测</li></ol><p>今天我分享一个简单的双均线策略代码：</p><pre><code>def dual_ma_strategy(data, short=5, long=20):\n    data['ma_short'] = data['close'].rolling(short).mean()\n    data['ma_long'] = data['close'].rolling(long).mean()\n    data['signal'] = 0\n    data.loc[data['ma_short'] > data['ma_long'], 'signal'] = 1\n    data.loc[data['ma_short'] < data['ma_long'], 'signal'] = -1\n    return data</code></pre>",
            "summary": "分享量化交易入门知识，包含双均线策略示例代码",
            "category": "stock", "tags": ["量化交易", "Python", "策略"],
        },
        {
            "user_idx": 2, "title": "基金定投两年，收益率超30%的经验分享",
            "content": "<h2>我的定投之路</h2><p>从2024年开始定投，到现在已经两年多了。目前总收益率32.5%，年化约15%。</p><h2>定投标的选择</h2><p>我选择了三只基金：</p><ul><li><strong>沪深300指数基金</strong>（40%仓位）：跟踪大盘蓝筹</li><li><strong>中证500指数增强</strong>（35%仓位）：中小盘成长</li><li><strong>新能源主题基金</strong>（25%仓位）：赛道配置</li></ul><h2>定投纪律</h2><p>每月15号定投，无论涨跌坚持执行。大跌时偶尔加仓，但从不减少定投金额。坚持是最重要的！</p>",
            "summary": "分享基金定投两年的经验，年化收益率15%",
            "category": "fund", "tags": ["基金定投", "投资心得", "指数基金"],
        },
        {
            "user_idx": 3, "title": "半导体行业深度分析：国产替代加速",
            "content": "<h2>行业背景</h2><p>2025年中国半导体市场规模突破2万亿，国产化率从2020年的15%提升至2025年的30%。预计2026年国产化率将达到35%以上。</p><h2>重点细分领域</h2><ol><li><strong>芯片设计</strong>：华为海思、紫光展锐等持续突破</li><li><strong>晶圆制造</strong>：中芯国际14nm良率提升至95%</li><li><strong>封装测试</strong>：长电科技全球市占率前三</li><li><strong>设备材料</strong>：北方华创、中微公司国产替代加速</li></ol><h2>投资逻辑</h2><p>短期看库存周期，中期看国产替代，长期看AI算力需求。建议关注设备、材料环节龙头企业。</p>",
            "summary": "半导体行业国产替代加速，分析投资机会",
            "category": "stock", "tags": ["半导体", "国产替代", "科技股"],
        },
        {
            "user_idx": 4, "title": "新手求助：第一次买基金应该注意什么？",
            "content": "<p>大家好，我是投资小白，刚工作一年多攒了点钱，想开始买基金。看了很多帖子还是很迷茫，想请教几个问题：</p><ol><li>第一次买基金应该买什么类型的？指数基金还是主动基金？</li><li>一次买入还是定投比较好？</li><li>大概要投多少钱比较合适？</li><li>需要每天盯着看吗？</li></ol><p>感谢大家指点！</p>",
            "summary": "基金投资新手求助帖",
            "category": "fund", "tags": ["新手", "基金", "求助"],
        },
    ]

    post_objs = []
    for p in demo_posts:
        post = Post(
            user_id=created_users[p["user_idx"]].id,
            title=p["title"],
            content=p["content"],
            summary=p["summary"],
            category=p["category"],
            tags=p.get("tags", []),
            view_count=100,
            like_count=5,
            comment_count=2,
            created_at=datetime.now(),
        )
        db.add(post)
        db.flush()
        post_objs.append(post)
        print(f"创建帖子: {p['title'][:30]}...")

    # ========== 评论 ==========
    demo_comments = [
        {"post_idx": 0, "user_idx": 1, "content": "分析得很透彻！新能源确实是大方向，我最近也在关注储能板块。"},
        {"post_idx": 0, "user_idx": 2, "content": "同意消费复苏的观点，白酒板块估值已经比较合理了。"},
        {"post_idx": 1, "user_idx": 0, "content": "好文！双均线策略虽然简单但很实用，期待更多量化内容。"},
        {"post_idx": 2, "user_idx": 4, "content": "向大佬学习！我也是刚开始定投，希望能像你一样坚持下来。"},
        {"post_idx": 3, "user_idx": 2, "content": "半导体确实是好赛道，但我感觉估值偏高，现在入场会不会追高？"},
        {"post_idx": 4, "user_idx": 2, "content": "建议从沪深300指数基金开始，定投是最好的方式，不用每天看。"},
        {"post_idx": 4, "user_idx": 0, "content": "小白可以先拿月收入的10%-20%定投，保持平常心，不要追涨杀跌。"},
    ]

    for c in demo_comments:
        comment = Comment(
            post_id=post_objs[c["post_idx"]].id,
            user_id=created_users[c["user_idx"]].id,
            content=c["content"],
            created_at=datetime.now(),
        )
        db.add(comment)
    print(f"创建 {len(demo_comments)} 条评论")

    # ========== 私信 ==========
    # 获取 dubo2248 用户
    dubo = db.query(User).filter(User.username == "dubo2248").first()
    if dubo:
        demo_messages = [
            {"from_idx": 0, "content": "你好！看到你的帖子了，一起交流投资心得吧"},
            {"from_idx": 0, "content": "最近看好什么板块？"},
        ]
        for m in demo_messages:
            msg = Message(
                sender_id=created_users[m["from_idx"]].id,
                receiver_id=dubo.id,
                content=m["content"],
                is_read=False,
                created_at=datetime.now(),
            )
            db.add(msg)
        # 还有一条来自量化分析师
        msg2 = Message(
            sender_id=created_users[1].id,
            receiver_id=dubo.id,
            content="Hi，你对量化交易感兴趣吗？我们可以多交流",
            is_read=False,
            created_at=datetime.now(),
        )
        db.add(msg2)
        print(f"创建 {len(demo_messages) + 1} 条私信 → dubo2248")

    # 用户之间的互发消息
    inter_messages = [
        {"from_idx": 0, "to_idx": 1, "content": "李总，你的量化策略最近收益怎么样？"},
        {"from_idx": 1, "to_idx": 0, "content": "还不错，上个月收益8%，主要是抓住了新能源这波"},
        {"from_idx": 0, "to_idx": 1, "content": "厉害！有空帮我看看我的策略"},
    ]
    for m in inter_messages:
        msg = Message(
            sender_id=created_users[m["from_idx"]].id,
            receiver_id=created_users[m["to_idx"]].id,
            content=m["content"],
            is_read=True,
            created_at=datetime.now(),
        )
        db.add(msg)

    # ========== 关注关系 ==========
    if dubo:
        # dubo2248 关注几个用户
        for idx in [0, 1, 2]:
            follow = Follow(follower_id=dubo.id, followed_id=created_users[idx].id)
            db.add(follow)
        print(f"dubo2248 关注了 3 个用户")

    # 用户之间互关
    for i, j in [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 4)]:
        follow = Follow(follower_id=created_users[i].id, followed_id=created_users[j].id)
        db.add(follow)

    # ========== 群组 ==========
    demo_groups = [
        {"name": "A股价值投资交流", "description": "专注价值投资理念，分享基本面分析，长期持有优质企业", "owner_idx": 0},
        {"name": "量化交易策略研究", "description": "Python量化、机器学习选股、回测框架交流", "owner_idx": 1},
        {"name": "基金定投实战群", "description": "基金定投心得分享，每周复盘，互相鼓励坚持定投", "owner_idx": 2},
        {"name": "科技股研究小组", "description": "半导体、AI、新能源等科技赛道深度研究", "owner_idx": 3},
    ]
    group_objs = []
    for g in demo_groups:
        group = Group(
            name=g["name"],
            description=g["description"],
            owner_id=created_users[g["owner_idx"]].id,
            is_public=True,
            created_at=datetime.now(),
        )
        db.add(group)
        db.flush()
        group_objs.append(group)
        # 群主自动加入
        db.add(GroupMember(group_id=group.id, user_id=created_users[g["owner_idx"]].id, role="owner"))
        print(f"创建群组: {g['name']}")

    # dubo2248 加入几个群
    if dubo:
        for g in group_objs[:2]:
            db.add(GroupMember(group_id=g.id, user_id=dubo.id, role="member"))
        print("dubo2248 加入了 2 个群组")

    # 其他用户加入群组
    for g_idx, u_idx in [(0, 1), (0, 2), (0, 4), (1, 0), (1, 3), (2, 0), (2, 4), (3, 0), (3, 1)]:
        db.add(GroupMember(group_id=group_objs[g_idx].id, user_id=created_users[u_idx].id, role="member"))

    db.commit()
    print("\n✅ 种子数据初始化完成！")
    print(f"   - {len(created_users)} 个演示用户（密码: 123456）")
    print(f"   - {len(post_objs)} 篇帖子")
    print(f"   - {len(demo_comments)} 条评论")
    print(f"   - 多条私信和关注关系")

except Exception as e:
    db.rollback()
    print(f"❌ 错误: {e}")
    raise
finally:
    db.close()
