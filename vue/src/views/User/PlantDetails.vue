<template>
  <div class="plant-details">
    <div class="header">
      <h1>{{ plant.type }}</h1>
    </div>
    <div class="plant-info">
      <div class="image-section">
        <img :src="plant.crop_avatar || 'https://via.placeholder.com/400'" alt="Plant Image" class="plant-image" />
      </div>
      <div class="content-section">
        <div class="user-info">
          <img :src="plant.farmer_avatar || 'https://via.placeholder.com/100'" alt="User Avatar" class="user-avatar" />
          <div class="user-details">
            <p class="username">{{ plant.username }}</p>
            <p class="email">{{ plant.email }}</p>
          </div>
        </div>
        <div class="plant-details-content">
          <p class="description"><strong>评价:</strong> {{ plant.evaluate }}</p>
          <p class="likes"><strong>好评数:</strong> ❤️ {{ plant.likes }}</p>
          <p class="sales"><strong>已售数量:</strong> {{ plant.sales }}</p>
          <p class="deadline"><strong>截止时间:</strong> {{ plant.deadline }}</p>
        </div>
      </div>
    </div>

    <div class="button-container">
      <!-- 添加 :disabled 来禁用按钮 -->
      <button @click="openOrderDialog" class="order-button" :disabled="isOrderButtonDisabled">订购</button>
      <button @click="handleBack" class="back-button">返回</button>
    </div>

    <!-- 订购弹窗 -->
    <el-dialog title="订购作物" :visible.sync="dialogVisible">
      <el-form :model="orderForm">
        <el-form-item label="种植面积(亩)" required>
          <el-input v-model="orderForm.area" type="number" min="1"></el-input>
        </el-form-item>
        <el-form-item  label="购买保险" prop="insurance">
          <el-select v-model="orderForm.insurance" placeholder="请选择是否购买" style="width: 100%">
            <el-option label="是" value="是"></el-option>
            <el-option label="否" value="否"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitOrder">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "PlantDetails",
  data() {
    return {
      plant: [], // 用于存储作物的详细信息
      dialogVisible: false, // 控制弹窗的显示
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      orderForm: { // 订购信息表单
        area: 1,
        begin_time: null,
        end_time: null,
      },
      isOrderButtonDisabled: false, // 按钮是否禁用
    };
  },
  mounted() {
    this.fetchPlantDetails();
  },
  methods: {
    fetchPlantDetails() {
      const plantId = this.$route.params.id; // 获取路由参数中的作物 ID
      this.$request.get("/plants/selectId", {
        params: {
          id: plantId,
        },
      }).then(response => {
        if (response.code === '200') {
          this.plant = response.data;
          this.checkDeadline(); // 获取作物详情后，检查截止日期
        } else {
          this.$message.error(response.msg);
        }
      })
          .catch(error => {
            this.$message.error("加载作物详情失败");
          });
    },
    openOrderDialog() {
      this.dialogVisible = true; // 打开订购弹窗
    },
    submitOrder() {
      const orderData = {
        user_id: this.user.id, // 假设从 Vuex 获取用户 ID
        plants_id: this.plant.id,
        area: this.orderForm.area,
      };

      console.log(orderData);

      // 提交订单请求
      this.$request.post('/orders/add', orderData)
          .then(response => {
            if (response.code === "200") {
              this.$message.success("订购成功！");
              this.dialogVisible = false; // 关闭弹窗
              this.resetOrderForm(); // 重置表单
            } else {
              this.$message.error(response.msg);
            }
          })
          .catch(error => {
            this.$message.error("订购失败，请重试");
          });
    },
    resetOrderForm() {
      this.orderForm = {
        area: 1,
        begin_time: null,
        end_time: null,
      };
    },
    handleBack() {
      this.$router.back(); // 返回上一页
    },
    checkDeadline() {
      const currentDate = new Date();
      const deadlineDate = new Date(this.plant.deadline);
      // 如果当前日期大于截止日期，禁用订购按钮
      this.isOrderButtonDisabled = currentDate > deadlineDate;
    }
  }
};
</script>

<style scoped>
.order-button:hover {
  background-color: #85ce61;
}

.plant-details {
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 40px auto;
  font-family: 'Arial', sans-serif;
}

.header h1 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #333;
}

.plant-info {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.image-section {
  flex: 1;
  min-width: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.plant-image {
  width: 100%;
  max-width: 400px;
  height: auto;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.content-section {
  flex: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid #409eff;
  object-fit: cover;
  margin-right: 15px;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
  font-size: 1.2rem;
  color: #555;
}

.email {
  font-size: 0.9rem;
  color: #777;
}

.plant-details-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.description,
.likes,
.deadline,
.sales {
  font-size: 1.1rem;
  color: #444;
  margin-bottom: 10px;
}

.back-button {
  display: block;
  width: 150px;
  margin: 30px auto 0;
  padding: 12px 20px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
  transition: background-color 0.3s;
}

.order-button {
  display: block;
  width: 150px;
  margin: 30px auto 0;
  padding: 12px 20px;
  background-color: #67c23a;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
  transition: background-color 0.3s;
}

.order-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.order-button:hover:enabled {
  background-color: #85ce61;
}
</style>
