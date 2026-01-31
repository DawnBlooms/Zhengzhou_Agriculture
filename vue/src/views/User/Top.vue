<template>
  <div id="news-carousel">
    <!-- 新闻轮播 -->
    <el-carousel :interval="3000" arrow="always" height="400px">
      <el-carousel-item v-for="newsItem in newsList" :key="newsItem.id">
        <div class="news-item">
          <img :src="newsItem.avatar || 'https://via.placeholder.com/800x400'" alt="News Avatar" class="news-image" />
          <div class="news-title">
            <h3>{{ newsItem.title }}</h3>
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>

    <!-- 热门推荐作物 -->
    <div class="mall-page">
      <h2>热门推荐作物</h2>
      <div class="plants-grid">
        <div class="plant-card" v-for="plant in recommendedPlants" :key="plant.id" @click="navigateToPlantDetail(plant.id)">
          <img :src="plant.crop_avatar || 'https://via.placeholder.com/300'" alt="Plant Image" />
          <h3>{{ plant.type }}</h3>
          <p>来源农户: {{ plant.username }}</p>
          <p>{{ plant.evaluate }}</p>
          <p>👍 {{ plant.likes }} | 销量: {{ plant.sales }}</p>
          <p>截止时间：{{ plant.deadline }}</p>
        </div>
      </div>

      <!-- 分页控件 -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
        <span>第 {{ currentPage }} 页</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Top",
  data() {
    return {
      newsList: [], // 存储新闻数据
      recommendedPlants: [], // 存储热门推荐作物数据
      currentPage: 1, // 当前页数
      pageSize: 8, // 每页显示数量
      totalPlants: 0 // 总作物数量
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalPlants / this.pageSize);
    },
  },
  mounted() {
    this.fetchNews();
    this.fetchRecommendedPlants(); // 获取推荐作物数据
  },
  methods: {
    // 获取新闻数据
    fetchNews() {
      this.$request.get("/news/selectPage", {
        params: {
          pageNum: 1,
          pageSize: 5,
        },
      })
          .then(response => {
            if (response.code === "200") {
              this.newsList = response.data.list;
            } else {
              this.$message.error(response.msg);
            }
          })
          .catch(error => {
            this.$message.error(error);
          });
    },
    // 获取热门推荐作物数据
    fetchRecommendedPlants() {
      this.$request.get("/plants/selectPage", {
        params: {
          pageNum: this.currentPage,
          pageSize: this.pageSize,
        },
      })
          .then(response => {
            if (response.code === "200") {
              this.recommendedPlants = response.data.list;
              this.totalPlants =response.data.total ; // 设置总作物数量
              console.log(this.totalPlants);
              console.log(this.currentPage);
            } else {
              this.$message.error(response.msg);
            }
          })
          .catch(error => {
            this.$message.error(error);
          });
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchRecommendedPlants(); // 获取当前页的推荐作物
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchRecommendedPlants(); // 获取当前页的推荐作物
      }
    },
    navigateToPlantDetail(plantId) {
      this.$router.push(`/user/plantDetails/${plantId}`);
    }
  },
}
</script>

<style scoped>
#news-carousel {
  width: 100%;
  margin: 20px auto;
}

/* 新闻部分 */
.news-item {
  position: relative;
  cursor: pointer;
}

.news-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 10px;
}

.news-title {
  position: absolute;
  bottom: 20px;
  left: 20px;
  color: white;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 12px 25px;
  border-radius: 10px;
  font-size: 20px;
}

.news-title h3 {
  margin: 0;
  font-size: 28px;
  font-weight: bold;
}

/* 热门推荐作物部分 */
.mall-page {
  padding: 40px 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.mall-page h2 {
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 30px;
  color: #333;
  border-bottom: 3px solid #409eff;
  display: inline-block;
  padding: 5px 20px;
  border-radius: 5px;
}

/* 卡片网格布局 */
.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* 每列最小250px，自动调整列数 */
  gap: 25px;
  justify-items: center; /* 卡片居中 */
}

.plant-card {
  width: 100%;
  max-width: 280px;
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  text-align: center;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.plant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.plant-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.plant-card h3 {
  margin: 15px 0 10px;
  font-size: 20px;
  color: #333;
}

.plant-card p {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}

.plant-card p:first-of-type {
  font-weight: bold;
  color: #409eff;
}

/* 分页部分 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
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

