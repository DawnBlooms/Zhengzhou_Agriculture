<template>
  <div id="app">
    <!-- 头部导航栏 -->
    <el-header>
      <div class="nav-bar">
        <div class="title">郑在种助农工程</div>
        <el-button
            :class="{ active: activeButton === 'home' }"
            @click="navigateTo('/user/top', 'home')"
        >
          系统首页
        </el-button>
        <el-button
            :class="{ active: activeButton === 'mall' }"
            @click="navigateTo('/user/mall', 'mall')"
        >
          郑在推
        </el-button>
        <el-button
            :class="{ active: activeButton === 'cards' }"
            @click="navigateTo('/user/cards', 'cards')"
        >
          郑在谈
        </el-button>
        <el-button
            :class="{ active: activeButton === 'orders' }"
            @click="navigateTo('/user/orders', 'orders')"
        >
          郑在养
        </el-button>

        <!-- 个人信息下拉菜单 -->
        <el-dropdown @command="handleCommand" class="personal-dropdown">
          <div class="dropdown-trigger">
            <img :src="user.avatar || defaultAvatar" alt="头像" class="avatar" />
            <span>{{ user.name || "个人信息" }}</span>
            <i class="el-icon-arrow-down"></i>
          </div>
          <el-dropdown-menu slot="dropdown" class="dropdown-menu">
            <el-dropdown-item command="space">我的空间</el-dropdown-item>
            <el-dropdown-item command="info">我的信息</el-dropdown-item>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-header>

    <!-- 主内容区域 -->
    <el-main class="main-content">
      <router-view></router-view>
    </el-main>
  </div>
</template>

<script>
export default {
  name: "UserFrame",
  data() {
    return {
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      defaultAvatar: "https://via.placeholder.com/40", // 默认头像
      activeButton: "" // 当前激活的按钮
    };
  },
  methods: {
    // 跳转到指定页面，并设置激活的按钮
    navigateTo(path, button) {
      this.activeButton = button; // 设置当前按钮为激活状态
      this.$router.push(path);
    },
    // 下拉菜单命令处理
    handleCommand(command) {
      if (command === "space") {
        this.$router.push("/user/space"); // 跳转到我的空间
      } else if (command === "info") {
        this.$router.push("/user/person"); // 跳转到我的信息
      } else if (command === "logout") {
        this.logout(); // 执行退出登录
      }
    },
    logout() {
      localStorage.removeItem("xm-user");
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background-color: #208922;
  color: white;
  padding: 10px;
}

.nav-bar .title {
  color: white;
  font-size: 22px;
  margin-right: 40px;
  padding-left: 150px;
}

.nav-bar .el-button {
  color: white;
  border: none;
  background-color: transparent;
  font-size: 16px;
  margin-right: 10px;
  padding: 10px;
  transition: background-color 0.3s;
}

.nav-bar .el-button:hover {
  background-color: #075720;
}

.nav-bar .el-button.active {
  background-color: #4CAF50; /* 高亮显示按钮的背景颜色 */
  color: white;
}

.personal-dropdown {
  margin-left: auto;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: white;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  color: white;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
  border: 2px solid #fff;
}

.dropdown-menu {
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 6px;
  overflow: hidden;
}

.dropdown-menu .el-dropdown-item {
  padding: 12px 20px;
  font-size: 14px;
  color: #333;
}

.dropdown-menu .el-dropdown-item:hover {
  background-color: #208922;
  color: white;
}

/* 主内容区域样式 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
