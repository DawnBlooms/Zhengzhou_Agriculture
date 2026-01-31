<template>
  <div class="mall-container">
    <!-- 搜索框 -->
    <div class="search-bar">
      <el-input
          v-model="type"
          placeholder="搜索你喜欢的农作物类型吧"
          class="search-input"
          @keyup.native.enter="onEnterSearch"
          prefix-icon="el-icon-search"
          clearable></el-input>
    </div>

    <div class="content">
      <!-- 分类按钮区域 -->
      <div class="category-box">
        <h3>农作物分类</h3>
        <div class="category-container">
          <div
              class="category-item"
              :class="{ active: selectedCategory === null }"
              @click="filterByCategory(null)">
            全部
          </div>
          <div
              class="category-item"
              v-for="category in cropTypes"
              :key="category.id"
              :class="{ active: selectedCategory === category.classes }"
              @click="filterByCategory(category.classes)">
            {{ category.classes }}
          </div>
        </div>
      </div>

      <!-- 右侧商品展示 -->
      <div class="product-box">
        <div
            class="product-card"
            v-for="plant in plants"
            :key="plant.id"
            @click="navigateToPlantDetail(plant.id)">
          <img
              :src="plant.crop_avatar || 'https://via.placeholder.com/150'"
              alt="Crop Image"/>
          <h4>{{ plant.type }}</h4>
          <p>种植者: {{ plant.username }}</p>
          <p>评价: {{ plant.evaluate }}</p>
          <p>👍 {{ plant.likes }} | 销量: {{ plant.sales }}</p>
          <p>截止日期: {{ plant.deadline }}</p>
        </div>

        <!-- 分页控件 -->
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
          <span>第 {{ currentPage }} 页</span>
          <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Mall",
  data() {
    return {
      type: null,
      cropTypes: [],
      plants: [],
      selectedCategory: null,
      currentPage: 1,
      pageSize: 6,
      totalPages: null,
      classes: null,
    };
  },
  created() {
    this.fetchCropTypes();
    this.fetchPlants();
  },
  methods: {
    onEnterSearch(){
      console.log("回车键按下，搜索触发");
      this.plants = []; // 清空当前卡片列表
      this.classes = null
      this.currentPage = 1; // 重置页码
      this.fetchPlants(); // 重新加载数据
    },
    fetchCropTypes() {
      this.$request
          .get("/cropType/classes")
          .then((response) => {
            this.cropTypes = response.data;
          })
          .catch((error) => {
            console.error("加载分类失败:", error);
          });
    },
    fetchPlants() {
      this.$request
          .get("/plants/selectByClass", {
            params: {
              pageNum: this.currentPage,
              pageSize: this.pageSize,
              classes: this.classes,
              type: this.type
            },
          })
          .then((response) => {
            this.plants = response.data.list;
            this.totalPages = response.data.total;
            this.totalPages = Math.ceil(this.totalPages / this.pageSize)
          })
          .catch((error) => {
            console.error("加载农作物失败:", error);
          });
    },
    filterByCategory(classes) {
      this.selectedCategory = classes;
      this.classes = classes;
      this.fetchPlants();
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchPlants();
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchPlants();
      }
    },
    navigateToPlantDetail(plantId) {
      this.$router.push(`/user/plantDetails/${plantId}`);
    },
  },
};
</script>

<style scoped>
.mall-container {
  padding: 20px;
}

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

.content {
  display: flex;
  gap: 20px;
}

/* 分类盒子 */
.category-box {
  flex: 1;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  height: auto;
  max-height: 80vh;
  overflow-y: auto;
}

.category-box h3 {
  margin-bottom: 15px;
  font-size: 18px;
  text-align: center;
}

.category-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.category-item {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
  cursor: pointer;
  background-color: #f9f9f9;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.category-item.active {
  background-color: #38b72e;
  color: #fff;
  font-weight: bold;
}

.category-item:hover:not(.active) {
  background-color: #f0f0f0;
}

/* 商品展示 */
.product-box {
  flex: 4;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  justify-content: space-between;
}

.product-card {
  width: calc(33.33% - 20px); /* 每行显示三个卡片 */
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  text-align: center; /* 文字居中 */
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.product-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  margin-bottom: 10px;
}

.product-card h4 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.product-card p {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

/* 分页部分 */
.pagination {
  width: 100%; /* 确保分页器独占一行 */
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 15px;
  margin: 0 10px;
  font-size: 16px;
  border: none;
  background-color: #409eff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #66b1ff;
}

.pagination span {
  font-size: 16px;
  color: #333;
}
</style>
