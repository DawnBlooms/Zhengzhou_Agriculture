<template>
  <div class="user-page">
    <el-card class="user-card">
      <el-form :model="user" label-width="120px" class="user-form">
        <div class="avatar-container">
          <el-upload
              class="avatar-uploader"
              :action="'http://localhost:9090' + '/files/upload'"
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
          >
            <img v-if="user.avatar" :src="user.avatar" class="avatar" />
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </div>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="user.username" placeholder="请输入用户名" ></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="user.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="user.phone" placeholder="请输入电话"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="user.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <div class="form-footer">
          <el-button type="primary" @click="update">保存</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "UserPerson",
  data() {
    return {
      user: JSON.parse(localStorage.getItem('xm-user') || '{}')
    }
  },
  methods: {
    update() {
      this.$request.put('/user/update', this.user).then((res) => {
        if (res.code === '200') {
          this.$message.success('保存成功');
          localStorage.setItem('xm-user', JSON.stringify(this.user));
          this.$emit('update:user');
        } else {
          this.$message.error(res.msg);
        }
      });
    },
    handleAvatarSuccess(response) {
      this.$set(this.user, 'avatar', response.data);
    },
  },
};
</script>

<style scoped>
.user-page {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 改为顶部对齐 */
  height: 100vh;
  background-color: #f5f5f5;
  padding-top: 50px; /* 调整顶部间距 */
}

.user-card {
  width: 60%;
  max-width: 600px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  background-color: #ffffff;
}

.user-form {
  padding: 20px;
}

.avatar-container {
  margin: 20px 0;
  text-align: center;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
  width: 130px;
  height: 130px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
}

.avatar-uploader:hover .el-upload {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 32px;
  color: #8c939d;
  width: 130px;
  height: 130px;
  line-height: 130px;
  text-align: center;
}

.avatar {
  width: 130px;
  height: 130px;
  display: block;
  border-radius: 50%;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
}

.el-form-item__label {
  font-weight: bold;
}
</style>
