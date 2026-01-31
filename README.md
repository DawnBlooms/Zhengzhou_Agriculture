# 一、项目背景与意义

​    随着我国乡村振兴战略的深入推进，农业现代化与数字化转型成为重要方向。《郑州市高质量推进乡村振兴加快农业农村现代化“十四五”规划》明确支持绿色农业企业与农业标准体系建设，为农业创新模式提供了政策支持。

​    “郑在种”项目正是在这一背景下诞生的。项目通过认养农业模式，为城市社区用户提供参与式农业体验，旨在：

- 缩短城市与农村的感知距离
- 满足城市用户对绿色健康食品的真实需求
- 帮助周边农户增加收入、减少农业风险
- 构建可持续的数字农业社区生态

​    该模式既具有社会价值，也符合毕业设计对于技术实现与现实意义的双重要求，是一项非常适合作为实践型项目的开发主题。

# 二、项目概述

平台主要包括以下功能模块：

### 核心功能

1. **用户注册与登录**
   - 支持普通用户 / 农户 / 管理员身份登录
   - 使用角色区分不同权限
2. **作物认养与投票机制**
   - 用户可参与作物投票，决定平台待种植品种
   - 实现用户参与式农业决策
3. **动态种植进度展示**
   - 用户可实时查看作物当前成长状态
   - 平台采用可视化交互看板提升用户体验
4. **系统公告与新闻**
   - 发布平台公告、农业资讯等内容
   - 用户可了解最新动态
5. **社区交流与分享**
   - 用户可发布个人心得与见闻
   - 包括点赞 / 点踩互动
6. **农业保障机制**
   - 引入保险机制分担自然灾害风险
   - 提升农户收益保障能力

### **业务流程图**

![img](https://i-blog.csdnimg.cn/direct/9a7b785852fd477387c69bd3395617a9.png)

# 三、技术架构与实现

项目采用**前后端分离架构**：

### 前端

- 使用 **Vue（Element UI）** 构建响应式界面
- 登录 / 注册 / 帖子广场 / 投票页面等组件化实现
- 通过 Axios 发送 HTTP 请求调用后端 API

### 后端

- 使用 **Flask 框架 + SQLAlchemy ORM**
- 提供标准 RESTful 接口
- 实现用户认证、数据 CRUD（创建、读取、更新、删除）
- 支持跨域、配置灵活、易于扩展

### 数据库

- 使用 **MySQL** 存储业务数据
- 表设计包括：`user` / `admin` / `plants` / `orders` / `news` / `notice` / `cards` 等
- 外键关联、级联更新 & 删除确保数据一致性

**数据库关系模型**

![img](https://i-blog.csdnimg.cn/direct/9e8eedc6579d43cc835fb9048e7b1447.png)

## 四、项目前端界面展示

```
编辑
```

![img](https://i-blog.csdnimg.cn/direct/ea6e0b62a2c847ec8542ee11a57a114c.png)



![img](https://i-blog.csdnimg.cn/direct/9e9961880faf438789ff0d96623d61b9.png)

![img](https://i-blog.csdnimg.cn/direct/f7ffa98eae9a4ba3afe384bd1c1a91cd.png)

![img](https://i-blog.csdnimg.cn/direct/75d4853ab5b14b83a22cf7ee146506ab.png)

![img](https://i-blog.csdnimg.cn/direct/ff5854922c4c45408f04c030fea283f7.png)

# ![img](https://i-blog.csdnimg.cn/direct/347f9827793e43ddbeb8127e7222b497.png)
## 五、附上源码



### [https://github.com/DawnBlooms/Zhengzhou_Agriculture.git![img](https://csdnimg.cn/release/blog_editor_html/release2.4.5/ckeditor/plugins/CsdnLink/icons/icon-default.png?t=PBP8)https://github.com/DawnBlooms/Zhengzhou_Agriculture.git](https://github.com/DawnBlooms/Zhengzhou_Agriculture.git)

# 六、部署与运行步骤

### 后端(根目录)：

1. 创建并激活虚拟环境

```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate      # Windows
```


2. 安装依赖（若仓库内有 requirements.txt）：

```bash
   pip install -r requirements.txt
```


3. 配置数据库与其他配置

   \- 编辑 `app/config.py` 或通过环境变量注入。

```python
#换成自己的用户名和密码
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/manager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```


4. 启动服务：

```bash
   python run.py
```


 \- 默认监听端口：9090（可在 run.py / config 中修改）
  \- 或使用 gunicorn 部署（生产环境）：

```bash
     gunicorn -w 4 -b 0.0.0.0:9090 run:app
```


### 前端（位于 `vue/` 目录）：

1. 进入前端目录并安装依赖：

```bash
   cd vue
   npm install
```


2. 启动开发服务器：

```bash
   npm run serve
```


  \- 默认端口：8080（由 vue/vue.config.js 指定）

# 七、项目总结与展望

“郑在种”是一个兼具**技术实现与现实价值**的农业数字化实践平台。它结合了前沿的 Web 技术与现实农业业务需求，从用户体验、农户利益保障、社区互动等角度进行了深度设计。

未来可以进一步扩展：

- 增加手机端应用支持（微信小程序 / 跨平台 App）
- 引入实时数据监测与 IoT 农业设备对接
- 加入 AI 作物生长预测与病虫害识别模块

