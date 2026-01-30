SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS manager;
CREATE DATABASE manager;
USE manager;
-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '姓名',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '角色标识',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '电话',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '管理员' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of admin
-- ----------------------------
insert into manager.admin (id, username, password, name, avatar, role, phone, email)
values  (1, 'admin', '123456', '管理员', 'http://localhost:9090/static/files/1769765213940-8b70-kcysmrw5280926.jpg', 'ADMIN', '13677889922', 'admin@xm.com');

-- ----------------------------
-- Table structure for notice
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '标题',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '内容',
  `time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '创建时间',
  `user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '创建人',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '公告信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of notice
-- ----------------------------
insert into manager.notice (id, title, content, time, user)
values  (1, '系统正式上线通知', '系统已于近日正式上线运行，欢迎各位用户注册体验。如在使用过程中遇到问题，请及时反馈。', '2026-01-18', 'admin'),
        (2, '用户注册与登录功能说明', '当前系统已支持普通用户、农户等角色注册与登录，请在注册时正确选择角色。', '2026-01-19', 'admin'),
        (3, '系统功能持续优化中', '为提升系统稳定性与使用体验，开发团队将持续进行功能优化与性能调整。', '2026-01-21', 'admin'),
        (4, '新增公告与信息展示模块', '系统已新增公告管理与信息展示功能，重要通知将通过公告栏第一时间发布。', '2026-01-23', 'admin'),
        (5, '系统维护通知', '系统将于近期进行例行维护，维护期间部分功能可能受到影响，请提前做好相关安排。', '2026-01-26', 'admin'),
        (6, '欢迎提出宝贵意见', '欢迎各位用户在使用系统过程中提出宝贵意见与建议，帮助我们不断完善系统。', '2026-01-28', 'admin');

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------
-- Table structure for user
-- ----------------------------

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INT(11) AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    username VARCHAR(20) COMMENT '昵称',
    email VARCHAR(20) COMMENT '电子邮箱',
    name VARCHAR(20) COMMENT '姓名',
    phone VARCHAR(20) COMMENT '电话号码',
    password VARCHAR(20) DEFAULT '123456'  COMMENT '密码',
    role ENUM('ADMIN','USER','FARMER') DEFAULT 'USER' COMMENT '角色',
    avatar VARCHAR(500) COMMENT '头像'
);

-- ----------------------------
-- Records of user
-- ----------------------------

TRUNCATE TABLE user;
insert into manager.user (id, username, email, name, phone, password, role, avatar)
values  (1, 'user1', 'alice@example.com', 'Alice', '9561', '123456', 'USER', 'http://localhost:9090/static/files/1769765275327-下载 (11).jpg'),
        (2, 'user2', 'bob@example.com', 'Bob', '454', '123456', 'FARMER', 'http://localhost:9090/static/files/1769765313828-1732620500127-微信图片_20240714143928.jpg'),
        (3, 'user3', 'charlie@example.com', 'Charlie', '154', '123456', 'USER', 'http://localhost:9090/static/files/1769765291266-1732620479191-images (2).jpg'),
        (4, 'user4', 'david@example.com', 'David', '1556', '123456', 'FARMER', 'http://localhost:9090/static/files/1769765323345-1732620507671-微信图片_20240715205146.jpg'),
        (5, 'user5', 'eve@example.com', 'Eve', '35140', '123456', 'USER', 'http://localhost:9090/static/files/1769765301533-1732620489167-images (4).jpg');

-- ----------------------------
-- Table structure for news
-- ----------------------------

DROP TABLE IF EXISTS news;
CREATE TABLE news (
    id INT(11) AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    avatar VARCHAR(400) COMMENT '图片',
    title VARCHAR(100) COMMENT '标题',
    content VARCHAR(2000) COMMENT '内容'
);

-- ----------------------------
-- Records of news
-- ----------------------------

TRUNCATE TABLE news;

insert into manager.news (id, avatar, title, content)
values  (1, 'http://localhost:9090/static/files/1769787283744-downloaded-image (2).jpg', '“郑在种”助农工程正式启动，探索认养农业新模式', '近日，“郑在种”助农工程平台在郑州正式启动。项目以认养农业为核心模式，面向社区用户提供参与式农业体验，让消费者从“田间到餐桌”全程参与农作物的种植与成长过程。该平台积极响应郑州市乡村振兴战略，致力于为市民提供绿色、健康、安全的农产品，同时帮助周边农户实现稳定增收。'),
        (2, 'http://localhost:9090/static/files/1769787431416-downloaded-image (3).jpg', '社区用户参与投票，共同决定农作物种植计划', '在“郑在种”平台上，社区用户可以通过留言和投票的方式参与农业决策。平台根据郑州地区的气候与土壤条件，筛选出小麦、玉米、花生等适宜作物，由用户共同投票决定最终种植方案。这种互动式种植模式不仅提升了用户参与感，也让农业生产更加贴近真实需求。'),
        (3, 'http://localhost:9090/static/files/1769787544170-W020210630415047021837.jpg', '平台联合保险机构，为农户种植收益保驾护航', '为降低农业生产风险，“郑在种”平台与多家保险机构展开合作，为参与项目的农户提供农业保险服务。即使因自然灾害等不可抗力因素导致减产或绝收，农户也能获得相应赔付，有效保障农民收益，增强项目的可持续发展能力。'),
        (4, 'http://localhost:9090/static/files/1769787629685-downloaded-image (4).jpg', '“郑在种”助力城乡融合发展，推动绿色农业落地', '“郑在种”项目通过数字化平台连接城市社区与农村农田，构建稳定的农产品供需关系。项目不仅满足了城市居民对绿色健康食品的需求，也为农村地区引入了新的发展动力。未来，平台将持续优化功能，推动农业现代化与城乡融合发展，为乡村振兴注入新活力。');

-- ----------------------------
-- Table structure for cropType
-- ----------------------------
DROP Table IF EXISTS cropType;
CREATE TABLE cropType(
    id INT(11) AUTO_INCREMENT COMMENT 'ID',
    avatar VARCHAR(400) COMMENT '图片',
    type VARCHAR(50) COMMENT '种类',
    classes VARCHAR(50) COMMENT '大类',
    PRIMARY KEY (id)
);

-- ----------------------------
-- Records of cropType
-- ----------------------------
TRUNCATE TABLE cropType;
insert into manager.croptype (id, avatar, type, classes)
values  (1, 'http://localhost:9090/static/files/1769765377118-1732619931731-3ac79f3df8dcd100baa1a8d437c05010b912c9fc81b9.png', '水稻', '谷物类'),
        (2, 'http://localhost:9090/static/files/1769765390569-1732619607561-小麦.jpg', '小麦', '谷物类'),
        (3, 'http://localhost:9090/static/files/1769765399100-1732619616846-玉米.jpg', '玉米', '谷物类'),
        (4, 'http://localhost:9090/static/files/1769765410493-1732619628188-大豆.jpg', '黄豆', '豆类'),
        (5, 'http://localhost:9090/static/files/1769765419654-1732620370476-R.jpg', '红豆', '豆类'),
        (6, 'http://localhost:9090/static/files/1769767189648-u=2236706874,2240406126&fm=253&fmt=auto&app=138&f=JPEG.webp', '白菜', '蔬菜类'),
        (7, 'http://localhost:9090/static/files/1769765450044-1732619715006-菠菜.jpg', '菠菜', '蔬菜类'),
        (8, 'http://localhost:9090/static/files/1769765558048-1732619654886-苹果.jpg', '苹果', '水果类'),
        (9, 'http://localhost:9090/static/files/1769765570260-1732619671805-柑橘.jpg', '橙子', '水果类'),
        (10, 'http://localhost:9090/static/files/1769766511392-u=3627031068,299567907&fm=253&app=138&f=JPEG.jpg', '葡萄', '水果类');

-- ----------------------------
-- Table structure for plants
-- ----------------------------

DROP TABLE IF EXISTS plants;
CREATE TABLE plants(
    id INT(11) AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    farmer_id INT(11) COMMENT '农户ID',
    crop_id INT(11) COMMENT '作物ID',
    evaluate VARCHAR(500) COMMENT '评价',
    likes INT(11) DEFAULT 0 COMMENT '好评程度',
    deadline DATE COMMENT '截止日期',
    sales INT(11) DEFAULT 0 COMMENT  '销量',
    status VARCHAR(200) DEFAULT '等待种植' COMMENT '状态',
    CONSTRAINT fk_plants_user
        FOREIGN KEY (farmer_id)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_plants_crop
        FOREIGN KEY (crop_id)
        REFERENCES cropType(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ----------------------------
-- Records of plants
-- ----------------------------

TRUNCATE TABLE plants;
insert into manager.plants (id, farmer_id, crop_id, evaluate, likes, deadline, sales, status)
values  (1, 1, 1, '这批作物质量非常好，口感鲜美，受到了顾客的热烈好评！', 120, 2026-10-30, 35, '等待种植'),
        (2, 2, 2, '作物生长状况良好，绿色无污染，顾客反馈很不错。', 85, 2026-01-00, 20, '等待种植'),
        (3, 3, 3, '产量高，品质优良，已经被多位商家长期订购。', 150, 2026-03-13, 50, '等待种植'),
        (4, 4, 4, '非常耐储存，运输过程中没有任何损坏，口感也非常棒。', 70, 2026-02-24, 15, '等待种植'),
        (5, 5, 5, '这批作物略有瑕疵，但整体质量还是很令人满意的。', 60, 2026-05-15, 10, '等待种植'),
        (6, 1, 2, '这批作物质量非常好，口感鲜美，受到了顾客的热烈好评！', 120, 2025-12-31, 35, '等待种植'),
        (7, 2, 3, '作物生长状况良好，绿色无污染，顾客反馈很不错。', 85, 2027-12-31, 20, '等待种植'),
        (8, 3, 4, '产量高，品质优良，已经被多位商家长期订购。', 150, 2026-06-09, 50, '等待种植'),
        (9, 4, 5, '非常耐储存，运输过程中没有任何损坏，口感也非常棒。', 70, 2026-09-30, 15, '等待种植'),
        (10, 5, 2, '这批作物略有瑕疵，但整体质量还是很令人满意的。', 60, 2024-01-01, 10, '等待种植');

-- ----------------------------
-- Table structure for orders
-- ----------------------------

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
    id INT(11) AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    user_id INT(11) COMMENT '用户ID',
    plants_id INT(11) COMMENT '种植编号',
    area INT(11) COMMENT '种植面积(亩)',
    plan_img VARCHAR(300) DEFAULT '' COMMENT '进度图片',
    predict DATE COMMENT '预计结束时间',
    insurance VARCHAR(20) DEFAULT '否' COMMENT '购买保险',
    status VARCHAR(200) DEFAULT '等待种植' COMMENT '状态',
    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_orders_plants
        FOREIGN KEY (plants_id)
        REFERENCES plants(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ----------------------------
-- Records of orders
-- ----------------------------

TRUNCATE TABLE orders;
insert into manager.orders (id, user_id, plants_id, area, plan_img, predict, insurance, status)
values  (1, 1, 2, 50, '', '2024-01-15', '否', '等待种植'),
        (2, 2, 4, 75, '', '2024-02-01', '否', '等待种植'),
        (3, 3, 1, 40, '', '2024-03-10', '否', '等待种植'),
        (4, 4, 9, 60, '', '2024-04-05', '否', '等待种植'),
        (5, 5, 6, 100, '', '2024-05-01', '否', '等待种植'),
        (6, 1, 4, 50, '', '2024-01-15', '否', '等待种植'),
        (7, 1, 5, 50, '', '2024-01-15', '否', '等待种植'),
        (8, 1, 3, 50, '', '2024-01-15', '否', '等待种植'),
        (9, 1, 7, 50, '', '2024-01-15', '否', '等待种植'),
        (10, 1, 1, 50, '', '2024-01-15', '否', '等待种植');

-- ----------------------------
-- Table structure for cards
-- ----------------------------

DROP TABLE IF EXISTS cards;
CREATE TABLE cards(
    id INT(11) AUTO_INCREMENT PRIMARY KEY COMMENT 'ID',
    user_id INT(11) COMMENT '用户编号',
    title VARCHAR(100) COMMENT '标题',
    content VARCHAR(500) COMMENT '内容',
    time DATETIME COMMENT '发布时间',
    avatar VARCHAR(300) COMMENT '头像',
    likes INT(11) DEFAULT 0 COMMENT '好评数量',
    dislikes INT(11) DEFAULT 0 COMMENT '差评数量',
    CONSTRAINT fk_cards_user
        FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- ----------------------------
-- Records of orders
-- ----------------------------
TRUNCATE TABLE cards;

insert into manager.cards (id, user_id, title, content, time, avatar, likes, dislikes)
values  (1, 1, '第一次体验认养农业，感觉很新奇', '第一次在“郑在种”平台上认养农作物，看着小麦从播种到生长的过程，感觉特别踏实。每天打开手机就能看到田里的变化，真的有一种参与感。', '2026-01-30 15:51:57', 'http://localhost:9090/static/files/1769788316034-1732619607561-小麦.jpg', 56, 1),
        (2, 2, '原来粮食是这样种出来的', '以前只知道吃粮食，从没真正了解过种植过程。通过郑在种平台，看到了农民的辛苦，也更懂得珍惜粮食了。', '2026-01-30 15:52:11', 'http://localhost:9090/static/files/1769788330353-1732623134823-cac3f4b8b3632f5b86eb2d41f1a84688.jpg', 83, 2),
        (3, 3, '参与投票决定种什么，很有成就感', '平台让大家投票选择种植作物，我参与选了玉米。后来真的种了，感觉自己也为农业出了一份力，这种体验挺棒的。', '2026-01-30 15:56:30', 'http://localhost:9090/static/files/1769788589118-1733830547855-屏幕截图 2024-12-10 193534.png', 72, 0),
        (4, 4, '收到认养的农产品，很新鲜', '前几天收到了认养的农产品，包装很用心，蔬菜特别新鲜，味道也比超市买的好。感觉吃得更放心了。', '2026-01-30 15:54:03', 'http://localhost:9090/static/files/1769788442241-1732619759033-大葱.jpg', 101, 3),
        (5, 5, '这种模式真的能帮到农民', '以前总觉得助农离自己很远，用了郑在种之后发现，其实每个人都能参与。希望这种模式能让更多农民受益。', '2026-01-30 15:54:30', 'http://localhost:9090/static/files/1769788469069-1733830502826-屏幕截图 2024-12-10 193444.png', 134, 4),
        (6, 1, '线上看农田，线下也想去看看', '通过平台看到农田实景之后，突然很想找时间去现场看看，感觉比单纯网购农产品有温度多了。', '2026-01-30 15:52:54', 'http://localhost:9090/static/files/1769788370810-1733830622178-屏幕截图 2024-12-10 193632.png', 67, 1),
        (7, 1, '有保险机制，农户更安心', '了解到平台给农户上了农业保险，感觉这个设计很贴心。种地本来风险就大，有保障大家才更放心参与。', '2026-01-30 15:55:53', 'http://localhost:9090/static/files/1769788552503-downloaded-image (5).jpg', 89, 0),
        (8, 1, '每天看看作物成长，挺治愈的', '工作之余打开郑在种，看看自己认养的作物长势如何，有种慢生活的感觉，挺解压的。', '2026-01-30 15:51:26', 'http://localhost:9090/static/files/1769788285743-1732619931731-3ac79f3df8dcd100baa1a8d437c05010b912c9fc81b9.png', 112, 2);
