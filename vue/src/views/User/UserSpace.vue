<template>
  <div class="profile-page">
    <!-- 左侧用户信息面板 -->
    <div class="profile-info">
      <img :src="user.avatar || defaultAvatar" alt="用户头像" class="profile-avatar" />
      <div class="user-details">
        <h2>{{ user.username || "未设置用户名" }}</h2>
        <div class="user-stats">
          <p>角色: {{ user.role || "未设置角色" }}</p>
          <p>邮箱: {{ user.email || "未绑定邮箱" }}</p>
          <p>电话: {{ user.phone || "未绑定电话" }}</p>
        </div>
      </div>
    </div>

    <!-- 中间帖子内容区域 -->
    <div class="posts-container" ref="scrollContainer" @scroll="handleScroll">
      <el-card
          v-for="post in posts"
          :key="post.id"
          class="post-card"
          shadow="hover"
      >
        <div class="card-header">
          <img :src="post.user_avatar || defaultAvatar" alt="用户头像" class="avatar" />
          <div class="user-info">
            <span class="username">{{ post.username }}</span>
            <span class="role">{{ post.role || "普通用户" }}</span>
            <span class="time">{{ post.time || "刚刚" }}</span>
          </div>
        </div>

        <div class="post-info">
          <h4>{{ post.title }}</h4>
          <p class="post-content">{{ post.content }}</p>
          <img :src="post.avatar || defaultPostImage" alt="帖子图片" class="post-image" />
          <button class="edit-button" @click="editPost(post)">编辑</button>
        </div>

        <div class="card-footer">
          <el-button type="text" size="mini" @click="like(post.id)">
            ❤️ {{ post.likes }}
          </el-button>
          <el-button type="text" size="mini" @click="comment(post.id)">
            💬 评论
          </el-button>
          <el-button type="text" size="mini" @click="save(post.id)">
            ⭐ 收藏
          </el-button>
        </div>
      </el-card>
      <p v-if="noMoreData" class="end-of-content">没有更多帖子了</p>
    </div>

    <!-- 编辑帖子弹窗 -->
    <el-dialog
        title="编辑帖子"
        :visible.sync="formVisible"
        width="50%"
        :close-on-click-modal="false"
        destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入标题"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" placeholder="请输入内容"></el-input>
        </el-form-item>
        <el-form-item label="图片">
          <el-upload
              :action="uploadUrl"
              :headers="{ token: user.token }"
              list-type="picture-card"
              :on-success="handleAvatarSuccess"
          >
            <el-button type="primary">上传图片</el-button>
          </el-upload>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="formVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdit">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      defaultAvatar: "https://via.placeholder.com/100", // 默认头像
      defaultPostImage: "https://via.placeholder.com/500x250", // 默认帖子图片
      posts: [], // 帖子列表
      currentPage: 1,
      pageSize: 3,
      totalPosts: 0,
      loading: false,
      noMoreData: false,
      formVisible: false,
      form: {},
      uploadUrl: "/files/upload"
    };
  },
  mounted() {
    this.fetchPosts();
  },
  methods: {
    fetchPosts(page = 1) {
      if (this.loading || this.noMoreData) return;
      this.loading = true;
      this.$request
          .get('/cards/selectPage', {
            params: {
              pageNum: page,
              pageSize: this.pageSize ,
              user_id: this.user.id,
            } })
          .then((response) => {
            if (response.data) {
              const { list, total } = response.data;
              if (list && list.length > 0) {
                this.posts.push(...list);
              }
              this.totalPosts = total || 0;
              this.noMoreData = this.posts.length >= this.totalPosts;
            }
          })
          .catch(() => {
            this.$message.error("加载帖子失败");
          })
          .finally(() => {
            this.loading = false;
          });
    },
    handleScroll() {
      const container = this.$refs.scrollContainer;
      if (container.scrollTop + container.clientHeight >= container.scrollHeight - 10) {
        if (!this.loading && !this.noMoreData) {
          this.currentPage++;
          this.fetchPosts(this.currentPage);
        }
      }
    },
    editPost(post) {
      this.form = { ...post };
      this.formVisible = true;
    },
    submitEdit() {
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          this.$request.put('/cards/update', this.form).then((res) => {
            if (res.code === "200") {
              this.$message.success("修改成功");
              this.formVisible = false;
              this.fetchPosts();
            } else {
              this.$message.error(res.msg);
            }
          });
        }
      });
    },
    handleAvatarSuccess(response) {
      this.form.avatar = response.data;
    },
    like(id) {
      console.log("点赞帖子：", id);
    },
    comment(id) {
      console.log("评论帖子：", id);
    },
    save(id) {
      console.log("收藏帖子：", id);
    }
  }
};
</script>



<style scoped>
.profile-page {
  display: flex;
  gap: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.profile-info {
  flex-shrink: 0;
  width: 300px;
  padding: 20px;
  background: linear-gradient(135deg, #208922, #66cc99);
  color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  height: 500px;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

.user-details h2 {
  font-size: 24px;
  margin-bottom: 15px;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.user-stats {
  font-size: 14px;
  line-height: 1.8;
}

.posts-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  padding: 10px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.post-card {
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  width: 100%;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.post-info h4 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.post-content {
  margin: 10px 0;
  font-size: 14px;
  color: #555;
}

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

.post-image {
  width: 500px;
  height: 250px;
  object-fit: cover;
  border-radius: 10px 10px 0 0;
  margin-bottom: 80px;
}

.post-info {
  position: relative;
  padding: 15px;
  text-align: left;
}

.edit-button {
  position: absolute;
  top: 5px;
  right: 10px;
  background-color: rgba(169, 169, 169, 0.5);
  border: 1px solid #aaa;
  color: #333;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-button:hover {
  background-color: rgba(169, 169, 169, 0.8);
}

.end-of-content {
  text-align: center;
  font-size: 16px;
  color: #888;
  margin-top: 20px;
}

</style>
