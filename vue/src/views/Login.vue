<template>
  <div class="container">
    <div class="login-card">
      <div class="title">欢迎来到郑在种助农工程</div>

      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input
            prefix-icon="el-icon-user"
            placeholder="请输入账号"
            v-model="form.username"
            clearable
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            prefix-icon="el-icon-lock"
            placeholder="请输入密码"
            show-password
            v-model="form.password"
          />
        </el-form-item>

        <el-form-item prop="role" class="role-select">
          <el-radio-group v-model="form.role">
            <el-radio label="ADMIN">管理员</el-radio>
            <el-radio label="USER">用户</el-radio>
            <el-radio label="FARMER">农户</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button class="login-btn" @click="login">
            登 录
          </el-button>
        </el-form-item>

        <div class="footer">
          还没有账号？<a href="/register">注册</a>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      form: {
        role: "ADMIN",
        username: "",
        password: "",
      },
      rules: {
        role: [{ required: true, message: "请选择角色", trigger: "change" }],
        username: [{ required: true, message: "请输入账号", trigger: "blur" }],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
    };
  },
  methods: {
    login() {
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          this.$request.post("/web/login", this.form).then((res) => {
            if (res.code === "200") {
              localStorage.setItem("xm-user", JSON.stringify(res.data));
              if (res.data.role === "ADMIN" || res.data.role === "FARMER") {
                this.$router.push("/admin/");
              } else {
                this.$router.push("/user/");
              }
              this.$message.success("登录成功");
            } else {
              this.$message.error(res.msg);
            }
          });
        }
      });
    },
  },
};
</script>

<style scoped>
.container {
  width: 100vw;
  height: 100vh;
  background-image: url("@/assets/imgs/bg.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  display: flex;
  align-items: center;

  /* 🔥 从 center 改成右对齐 */
  justify-content: flex-end;

  /* 🔥 控制离右边的距离（可继续加大） */
  padding-right: 23%;
}

/* 登录卡片 */
.login-card {
  width: 420px;
  padding: 35px 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);

  /* 🔥 关键：整体向右偏移 */
  transform: translateX(120px);
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 28px;
  letter-spacing: 2px;
  line-height: 1.4;

  /* 🔥 高级感核心 */
  background: linear-gradient(135deg, #2a60c9, #4f8dff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;

  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

/* 角色选择 */
.role-select {
  text-align: center;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  height: 42px;
  border-radius: 6px;
  font-size: 16px;
  color: #fff;
  background: linear-gradient(135deg, #2a60c9, #3f8cff);
  border: none;
}

.login-btn:hover {
  opacity: 0.9;
}

/* 底部 */
.footer {
  text-align: right;
  color: #666;
  font-size: 14px;
}

.footer a {
  color: #2a60c9;
}
</style>

