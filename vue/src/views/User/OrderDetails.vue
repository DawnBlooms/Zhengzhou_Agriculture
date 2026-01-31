<template>
  <div class="order-detail-container">

    <!-- 作物信息和图片展示 -->
    <div class="image-and-info">
      <!-- 左侧：头像和作物种类 -->
      <div class="left-section">
        <div class="avatar-container">
          <img :src="order.crop_avatar || 'https://via.placeholder.com/100'" alt="Avatar" class="avatar-image" />
        </div>
        <p class="crop-type"><strong>作物种类:</strong> {{ order.type }}</p>
      </div>

      <!-- 右侧：主图片 -->
      <div class="right-section">
        <h1 class="order-title">进展展示</h1>
        <div class="main-image-container">
          <img :src="order.plan_img || order.crop_avatar || 'https://via.placeholder.com/300'" alt="Main Image" class="main-image" />
        </div>
      </div>
    </div>

    <!-- 订单详细信息 -->
    <div class="order-details">
      <div class="left-column">
        <p><strong>农户姓名:</strong> {{ order.farmer_name }}</p>
        <p><strong>农户邮箱:</strong> {{ order.farmer_email }}</p>
        <p><strong>是否购买保险:</strong> {{ order.insurance }}</p>
      </div>
      <div class="right-column">
        <p><strong>区域面积:</strong> {{ order.area }} 亩</p>
        <p><strong>种植状态:</strong> {{ order.status }}</p>
        <p><strong>预计结束时间:</strong> {{ order.predict }}</p>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="actions">
      <button
          :disabled="order.status === '已种植'"
          @click="openOrderDialog"
          class="button primary"
      >
        修改订单
      </button>
      <button
          :disabled="order.status === '已种植'"
          @click="del(order.id)"
          class="button danger"
      >
        取消订单
      </button>
    </div>

    <el-dialog title="订购作物" :visible.sync="dialogVisible">
      <el-form :model="form">
        <el-form-item label="种植面积(亩)" required>
          <el-input v-model="form.area" type="number" min="1"></el-input>
        </el-form-item>
        <el-form-item  label="购买保险" prop="insurance">
          <el-select v-model="form.insurance" placeholder="请选择是否购买" style="width: 100%">
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
  name: "OrderDetail",
  data() {
    return {
      order: {},
      dialogVisible: false,
      id: 0,
      form: {}
    };
  },
  mounted() {
    this.id = this.$route.params.id;
    this.fetchOrderDetails();
  },
  methods: {
    fetchOrderDetails() {
      this.$request
          .get("/orders/selectId", { params: { id: this.id } })
          .then((response) => {
            if (response.code === "200") {
              this.order = response.data;
            } else {
              this.$message.error("数据获取错误");
            }
          });
    },
    del(id) {   // 单个删除
      this.$confirm('您确定取消吗？', '确认删除', {type: "warning"}).then(response => {
        this.$request.delete('/orders/delete/' + id).then(res => {
          if (res.code === '200') {   // 表示操作成功
            this.$message.success('取消成功')
            this.$router.push('/user/orders');
          } else {
            this.$message.error(res.msg)  // 弹出错误的信息
          }
        })
      }).catch(() => {
      })
    },
    openOrderDialog() {
      this.dialogVisible = true; // 打开订购弹窗
      this.form = this.order
    },
    submitOrder() {
      const orderData = {
        id: this.order.id,
        area: this.form.area,
      };

      this.$request.put('/orders/update', orderData)
          .then(response => {
            if (response.code === "200") {
              this.$message.success("修改成功！");
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
  },
};
</script>

<style scoped>
.order-detail-container {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

/* 作物信息和图片区域布局 */
.image-and-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  margin-left: 25px;
}

.left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.avatar-container {
  width: 100px;
  height: 100px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ddd;
}

.crop-type {
  font-size: 16px;
  color: #333;
}

.right-section {
  flex: 1;
  text-align: center;
}

.order-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.main-image-container {
  width: 100%;
  max-width: 500px;
  height: 300px;
  margin: 0 auto;
  border-radius: 10px;
  overflow: hidden;
}

.main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: 2px solid #ddd;
}

/* 订单详情 */
.order-details {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.left-column,
.right-column {
  flex: 1;
  font-size: 16px;
  color: #555;
  line-height: 1.8;
}

.left-column p,
.right-column p {
  margin: 8px 0;
}

/* 按钮样式 */
.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
}

.button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.button.primary {
  background-color: #409eff;
}

.button.primary:hover {
  background-color: #66b1ff;
}

.button.danger {
  background-color: #f56c6c;
}

.button.danger:hover {
  background-color: #ff9999;
}
</style>


