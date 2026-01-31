<template>
  <div id="card-list" ref="scrollContainer" @scroll="handleScroll">
    <!-- 搜索框和新增按钮 -->
    <div class="search-bar">
      <el-input
          v-model="title"
          placeholder="搜索你感兴趣的新鲜事"
          class="search-input"
          @keyup.native.enter="onEnterSearch"
          prefix-icon="el-icon-search"
          clearable></el-input>
    </div>
    <div class="add-post">
        <span @click="handleAdd">
          🌟点击我  **分享你的郑在种日常吧！** 🌈
        </span>
    </div>

    <!-- 卡片列表 -->
    <div class="card-container">
      <el-card
          v-for="card in cards"
          :key="card.id"
          class="card-item"
          shadow="hover">
        <div class="card-header">
          <img class="avatar" :src="card.user_avatar" alt="用户头像" />
          <div class="user-info">
            <span class="username">{{ card.username }}</span>
            <span class="role">{{ card.role }}</span>
            <span class="time">{{ card.time }}</span>
          </div>
        </div>

        <div class="card-content">
          <h2>{{ card.title }}</h2>
          <p>{{ card.content }}</p>
          <img
              v-if="card.avatar"
              class="card-image"
              :src="card.avatar"
              alt="卡片图片"/>
        </div>

        <div class="card-footer">
          <el-button type="text" size="mini" @click="like(card.id)">
            ❤️ {{ card.likes }}
          </el-button>
          <el-button type="text" size="mini" @click="comment(card.id)">
            💬 评论
          </el-button>
          <el-button type="text" size="mini" @click="save(card.id)">
            ⭐ 收藏
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 加载更多 -->
    <el-loading v-if="loading" text="正在加载更多内容..." />
    <div v-if="noMoreData" class="end-of-content">
      没有更多数据了~
    </div>

    <el-dialog title="我要发帖" :visible.sync="formVisible" width="40%" :close-on-click-modal="false" destroy-on-close>
      <el-form :model="form" label-width="100px" style="padding-right: 50px" :rules="rules" ref="formRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="标题"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" placeholder="内容"></el-input>
        </el-form-item>
        <el-form-item label="图片">
          <el-upload
              class="avatar-uploader"
              :action="$baseUrl + '/files/upload'"
              :headers="{ token: user.token }"
              list-type="picture"
              :on-success="handleAvatarSuccess"
          >
            <el-button type="primary">上传图片</el-button>
          </el-upload>
        </el-form-item>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="formVisible = false">取 消</el-button>
        <el-button type="primary" @click="addNew">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
export default {
  name: "Cards",
  data() {
    return {
      form:{},
      cards: [], // 卡片数据
      currentPage: 1, // 当前页码
      title:null,
      pageSize: 5, // 每页大小
      loading: false, // 是否正在加载
      noMoreData: false, // 是否还有更多数据
      formVisible: false,
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
    };
  },
  created() {
    this.fetchCards(); // 页面加载时加载第一批数据
  },
  methods: {
    onEnterSearch(){
      console.log("回车键按下，搜索触发");
      this.cards = []; // 清空当前卡片列表
      this.currentPage = 1; // 重置页码
      this.noMoreData = false; // 允许加载更多数据
      this.fetchCards(); // 重新加载数据
    },
    // 获取卡片数据
    fetchCards() {
      if (this.loading || this.noMoreData) return; // 防止重复加载
      this.loading = true;

      this.$request
          .get("/cards/selectPage", {
            params: {
              pageNum: this.currentPage,
              pageSize: this.pageSize,
              title: this.title,
            },
          })
          .then((response) => {
            console.log("接口返回的数据：", response.data.list); // 打印接口返回内容
            const list = response.data.list; // 获取列表数据
            if (list.length === 0) {
              this.noMoreData = true; // 没有更多数据了
            } else {
              this.cards = [...this.cards, ...list]; // 合并新数据
              this.currentPage++; // 页码自增
            }
            this.loading = false;
          })
          .catch((error) => {
            console.error("获取数据失败：", error);
            this.loading = false;
          });
    },
    // 监听滚动
    handleScroll() {
      const container = this.$refs.scrollContainer;
      if (
          container.scrollTop + container.clientHeight >=
          container.scrollHeight - 10
      ) {
        this.fetchCards(); // 滚动到底部时加载更多
      }
    },
    handleAdd(){
      this.form = {}
      this.formVisible = true
    },
    addNew(){
      this.form.user_id = this.user.id;
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          this.$request({
            url: '/cards/add',
            method: 'POST' ,
            data: this.form
          }).then(res => {
            if (res.code === '200') {  // 表示成功保存
              this.$message.success('保存成功')
              this.fetchCards()
              this.formVisible = false
            } else {
              this.$message.error(res.msg)  // 弹出错误的信息
            }
          })
        }
      })
    },
    handleAvatarSuccess(response, file, fileList) {
      // 把头像属性换成上传的图片的链接
      this.form.avatar = response.data
    },
    // 点赞
    like(cardId) {
      console.log("点赞卡片：", cardId);
    },
    // 评论
    comment(cardId) {
      console.log("评论卡片：", cardId);
    },
    // 收藏
    save(cardId) {
      console.log("收藏卡片：", cardId);
    },
  },

};
</script>

<style scoped>

/* 搜索栏容器 */
.search-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 10px 15px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

/* 搜索框 */
.search-input {
  flex: 1;
  margin-right: 15px;
  height: 45px; /* 调整搜索框高度 */
  border: 2px solid #ccc; /* 增加边框 */
  border-radius: 8px; /* 边框圆角 */
  padding: 5px 10px; /* 内边距 */
}

/* 新增文字 */
.add-post {
  font-size: 16px;
  font-weight: bold;
  color: #007aff;
  cursor: pointer;
  transition: color 0.3s ease, transform 0.3s ease;
  text-align: center; /* 文字居中 */
  display: block; /* 设置为块级元素 */
  margin: 0 auto; /* 居中 */
}

.add-post:hover {
  color: #0056b3;
  transform: scale(1.1);
}

/* 容器样式 */
#card-list {
  max-width: 800px;
  margin: 20px auto;
  height: 100vh; /* 设置高度，便于滚动测试 */
  overflow-y: auto; /* 保留滚动功能 */
  scrollbar-width: none; /* 隐藏 Firefox 滚动条 */
}

#card-list::-webkit-scrollbar {
  display: none; /* 隐藏 Chrome 滚动条 */
}

/* 卡片容器 */
.card-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 卡片样式 */
.card-item {
  padding: 20px;
  border: none; /* 去掉边框 */
  border-radius: 15px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  background: #ffffff;
  transition: transform 0.3s ease; /* 添加悬停动画 */
}

.card-item:hover {
  transform: translateY(-5px); /* 悬停上移 */
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
  font-size: 16px;
}

.role {
  font-size: 12px;
  color: #999;
}

.time {
  font-size: 12px;
  color: #999;
}

/* 卡片内容 */
.card-content h2 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.card-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 显示最多三行 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-image {
  width: 100%;
  height: 300px; /* 固定高度 */
  object-fit: cover; /* 填充图片 */
  border-radius: 10px;
  margin-top: 10px;
}

/* 卡片底部 */
.card-footer {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
}

.el-button {
  transition: transform 0.2s ease;
}

.el-button:hover {
  transform: scale(1.1); /* 鼠标悬停放大 */
}

/* 加载状态 */
.loading-indicator,
.end-of-content {
  text-align: center;
  font-size: 14px;
  color: #999;
  margin: 20px 0;
}

</style>
