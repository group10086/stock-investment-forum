-- ============================================
-- 股票基金投资论坛 - 测试数据
-- ============================================

-- 插入敏感词
INSERT INTO sensitive_words (word, replacement) VALUES
('赌博', '***'),
('色情', '***'),
('毒品', '***'),
('暴力', '***'),
('诈骗', '***');

-- 插入管理员用户（密码：admin123）
INSERT INTO users (username, email, password_hash, nickname, bio, is_admin, is_verified) VALUES
('admin', 'admin@stockforum.com', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5Yx5L5x5L5x5L5x5L5O', '管理员', '论坛管理员', TRUE, TRUE);

-- 插入测试用户（密码：test123）
INSERT INTO users (username, email, password_hash, nickname, bio, investment_preference, is_verified) VALUES
('investor1', 'investor1@test.com', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5Yx5L5x5L5x5L5x5L5O', '投资达人', '10年股市老韭菜', '["a_stock", "fund"]', TRUE),
('investor2', 'investor2@test.com', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5Yx5L5x5L5x5L5x5L5O', '量化分析师', '专注量化交易', '["us_stock", "technical"]', TRUE),
('newbie', 'newbie@test.com', '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Qlq5GzGq5Yx5L5x5L5x5L5x5L5O', '股市小白', '刚入市，请多指教', '["fund"]', FALSE);

-- 插入测试帖子
INSERT INTO posts (user_id, title, content, summary, category, tags, is_essence, is_hot, view_count, like_count, comment_count) VALUES
(2, '2026年A股中期投资策略分析', '<p>2026年已经过半，回顾上半年A股市场走势...</p><p>从宏观经济角度看，GDP增速保持在5%左右...</p>', '2026年A股中期策略分析：关注科技创新和消费升级两大主线', 'a_stock', '["A股","策略分析","2026"]', TRUE, TRUE, 1520, 89, 23),
(2, '港股打新经验分享：如何提高中签率', '<p>打新是港股投资的重要方式之一...</p><p>经过多年的实战经验，我总结出以下几点提高中签率的方法...</p>', '分享港股打新提高中签率的实战经验和技巧', 'hk_stock', '["港股","打新","经验分享"]', TRUE, FALSE, 856, 45, 12),
(3, '纳斯达克指数技术分析：双顶形态是否形成', '<p>从技术面来看，纳斯达克指数当前处于关键位置...</p><p>MACD指标出现顶背离信号，RSI处于超买区域...</p>', '纳斯达克指数技术面分析，探讨双顶形态的可能性', 'us_stock', '["美股","技术分析","纳斯达克"]', FALSE, TRUE, 2340, 120, 34),
(4, '新手买基金入门指南', '<p>很多新手朋友问我：''月薪5000怎么开始理财？''</p><p>我的建议是先了解基金的种类：货币基金、债券基金、股票基金...</p>', '为理财新手准备的基金投资入门指南', 'fund', '["基金","入门","理财"]', FALSE, FALSE, 3200, 200, 56),
(2, '价值投资 vs 成长投资：哪种策略更适合当前市场', '<p>在当前的宏观经济环境下，价值投资和成长投资各有什么优劣？</p><p>本文将从多个维度进行对比分析...</p>', '对比分析价值投资与成长投资在当前市场的适用性', 'value', '["价值投资","成长投资","策略对比"]', TRUE, TRUE, 1890, 156, 45);

-- 插入测试评论
INSERT INTO comments (post_id, user_id, content) VALUES
(1, 3, '好文章！非常赞同作者关于科技创新主线的观点。'),
(1, 4, '请问作者对半导体板块怎么看？'),
(2, 4, '感谢分享，打新确实需要技巧。'),
(3, 2, '技术分析很到位，但建议结合基本面一起看。'),
(4, 2, '写得很详细，对新手很有帮助！'),
(4, 3, '补充一点：定投是很好的入门方式。');

-- 插入楼中楼评论
INSERT INTO comments (post_id, user_id, parent_id, content) VALUES
(1, 2, 2, '半导体板块我长期看好，尤其是AI芯片方向。');

-- 插入关注关系
INSERT INTO follows (follower_id, followed_id) VALUES
(2, 3),
(3, 2),
(4, 2),
(4, 3);

-- 插入点赞记录
INSERT INTO post_likes (user_id, post_id) VALUES
(2, 5),
(3, 1),
(4, 1),
(4, 4);

-- 插入收藏记录
INSERT INTO bookmarks (user_id, post_id) VALUES
(4, 1),
(4, 5);

-- 插入私信
INSERT INTO messages (sender_id, receiver_id, content, is_read) VALUES
(2, 3, '你好，看了你在纳斯达克分析文章，写得很好！', TRUE),
(3, 2, '谢谢！对美股有研究的话可以多交流。', TRUE),
(2, 3, '好的，以后多交流。', FALSE);
