<template>
  <div class="order-container">
    <!-- 搜索框 -->
    <div class="search-bar">
      <input
          type="text"
          v-model="type"
          placeholder="搜索订单..."
      />
    </div>

    <h2 class="title">我的作物</h2>

    <!-- 订单列表 -->
    <ul class="order-list">
      <li
          v-for="order in orders"
          :key="order.id"
          class="order-item"
          @click="goToOrderDetail(order.id)"
      >
        <!-- 图片 -->
        <div class="image-container">
          <img :src="order.crop_avatar" alt="Crop Avatar" />
        </div>
        <!-- 信息 -->
        <div class="info-container">
          <h3>{{ order.type }}</h3>
          <p>农户名: {{ order.farmer_name }}</p>
          <p>种植面积: {{ order.area }} 亩</p>
          <p>预计成熟时间: {{ order.predict }}</p>
          <p>状态: {{ order.status }}</p>
        </div>
      </li>
    </ul>

    <!-- 分页器 -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>第 {{ currentPage }} 页</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Orders",
  data() {
    return {
      orders: [],
      paginatedOrders: [],
      type: null,
      currentPage: 1,
      pageSize: 5,
      user: JSON.parse(localStorage.getItem("xm-user") || "{}"),
      totalPages: 0,
    };
  },
  methods: {
    fetchOrders() {
      this.$request
          .get("/orders/selectUserId", {
            params: {
              pageNum: this.currentPage,
              pageSize: this.pageSize,
              user_id: this.user.id,
              type: this.type,
            },
          })
          .then((response) => {
            this.orders = response.data.list;
            this.totalPages = Math.ceil(response.data.total / this.pageSize);
          });
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchOrders();
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchOrders();
      }
    },
    goToOrderDetail(orderID) {
      this.$router.push(`/user/orderDetails/${orderID}`);
    },
  },
  mounted() {
    this.fetchOrders();
  },
};
</script>


<style scoped>
.order-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.search-bar {
  text-align: center;
  margin-bottom: 20px;
}

.search-bar input {
  width: 80%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.order-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.order-item {
  display: flex;
  align-items: flex-start;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  background-color: #fff;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  cursor: pointer;
}

.order-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.image-container {
  flex: 0 0 80px;
  height: 80px;
  overflow: hidden;
  border-radius: 8px;
  margin-right: 16px;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info-container {
  flex: 1;
}

.info-container h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #333;
}

.info-container p {
  margin: 4px 0;
  font-size: 14px;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  border: none;
  background-color: #007bff;
  color: white;
  padding: 8px 16px;
  margin: 0 8px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #0056b3;
}

.pagination span {
  font-size: 16px;
  color: #333;
}
</style>
