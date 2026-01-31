<template>
  <div>
    <div class="search">
      <el-input placeholder="请输入用户账号查询" style="width: 200px" v-model="username"></el-input>
      <el-input placeholder="请输入作物类型查询" style="width: 200px; margin-left: 10px" v-model="type"></el-input>
      <el-button type="info" plain style="margin-left: 10px" @click="load(1)">查询</el-button>
      <el-button type="warning" plain style="margin-left: 10px" @click="reset">重置</el-button>
    </div>

    <div class="operation">
      <el-button type="danger" plain @click="delBatch">批量删除</el-button>
    </div>

    <div class="table">
      <el-table :data="tableData" strip @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="id" label="序号" width="70" align="center" sortable></el-table-column>
        <el-table-column prop="username" label="用户账号"></el-table-column>
        <el-table-column prop="user_phone" label="电话"></el-table-column>
        <el-table-column prop="farmer_name" label="农户账号"></el-table-column>
        <el-table-column prop="farmer_phone" label="电话"></el-table-column>
        <el-table-column prop="type" label="作物种类"></el-table-column>
        <el-table-column label="作物图片">
          <template v-slot="scope">
            <div style="display: flex; align-items: center">
              <el-image style="width: 40px; height: 40px; border-radius: 50%" v-if="scope.row.crop_avatar"
                        :src="scope.row.crop_avatar" :preview-src-list="[scope.row.crop_avatar]"></el-image>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="area" label="种植面积"></el-table-column>
        <el-table-column prop="predict" label="预计成熟日期"></el-table-column>
        <el-table-column prop="insurance" label="购买保险"></el-table-column>
        <el-table-column prop="status" label="状态"></el-table-column>
        <el-table-column label="进度图片">
          <template v-slot="scope">
            <div style="display: flex; align-items: center">
              <el-image style="width: 40px; height: 40px; border-radius: 50%" v-if="scope.row.plan_img"
                        :src="scope.row.plan_img" :preview-src-list="[scope.row.plan_img]"></el-image>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" align="center" width="240">
          <template v-slot="scope">
            <el-button size="mini" type="success" plain @click="delivery(scope.row)">发货</el-button>
            <el-button size="mini" type="primary" plain @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" plain @click="del(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>

      </el-table>

      <div class="pagination">
        <el-pagination
            background
            @current-change="handleCurrentChange"
            :current-page="pageNum"
            :page-sizes="[5, 10, 20]"
            :page-size="pageSize"
            layout="total, prev, pager, next"
            :total="total">
        </el-pagination>
      </div>
    </div>

    <el-dialog title="订单信息" :visible.sync="fromVisible" width="40%" :close-on-click-modal="false" destroy-on-close>
      <el-form :model="form" label-width="100px" style="padding-right: 50px" :rules="rules" ref="formRef">
        <el-form-item label="种植面积" prop="area">
          <el-input v-model="form.area" placeholder="种植面积"></el-input>
        </el-form-item>
        <el-form-item v-if="user.role === 'ADMIN'" label="购买保险" prop="insurance">
          <el-select v-model="form.insurance" placeholder="请选择是否购买" style="width: 100%">
            <el-option label="是" value="是"></el-option>
            <el-option label="否" value="否"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="等待种植" value="等待种植"></el-option>
            <el-option label="正在种植" value="正在种植"></el-option>
            <el-option label="已播种" value="已播种"></el-option>
            <el-option label="生长中" value="生长中"></el-option>
            <el-option label="开花授粉中" value="开花授粉中"></el-option>
            <el-option label="结果中" value="结果中"></el-option>
            <el-option label="正在收获" value="正在收获"></el-option>
            <el-option label="已收获" value="已收获"></el-option>
            <el-option label="等待发货" value="等待发货"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="预计结束日期" prop="predict">
          <el-date-picker
              v-model="form.predict"
              type="date"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              placeholder="选择结束日期"
              style="width: 100%">
          </el-date-picker>
        </el-form-item>
          <el-form-item label="进度图片">
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
        <el-button @click="fromVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
export default {
  name: "Orders",
  data() {
    return {
      tableData: [],  // 所有的数据
      pageNum: 1,   // 当前的页码
      pageSize: 5,  // 每页显示的个数
      total: 0,
      username: null,
      type: null,
      farmer_name: null,
      fromVisible: false,
      form: {},
      user: JSON.parse(localStorage.getItem('xm-user') || '{}'),
      rules: {
        username: [
          {required: true, message: '请输入用户账号', trigger: 'blur'},
        ],
        type: [
          {required: true, message: '请输入作物种类', trigger: 'blur'},
        ]
      },
      ids: []
    }
  },
  created() {
    this.load(1)
  },
  methods: {
    handleAvatarSuccess(response, file, fileList) {
      // 把头像属性换成上传的图片的链接
      this.form.plan_img = response.data
    },
    handleSelectionChange(rows) {   // 当前选中的所有的行数据
      this.ids = rows.map(v => v.id)
    },
    handleEdit(row) {   // 编辑数据
      this.form = JSON.parse(JSON.stringify(row))  // 给form对象赋值  注意要深拷贝数据
      this.fromVisible = true   // 打开弹窗
    },
    save() {   // 保存按钮触发的逻辑  它会触发新增或者更新
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          this.$request({
            url: '/orders/update',
            method: 'PUT' ,
            data: this.form
          }).then(res => {
            if (res.code === '200') {  // 表示成功保存
              this.$message.success('保存成功')
              this.load(1)
              this.fromVisible = false
            } else {
              this.$message.error(res.msg)  // 弹出错误的信息
            }
          })
        }
      })

    },
    delivery(row) {
      this.$confirm(
          '您确定要发货吗？',
          '确认发货',
          { type: 'warning' }
      ).then(() => {
        // 用户点击确定，执行发货逻辑
        this.form = JSON.parse(JSON.stringify(row)); // 深拷贝
        this.form.status = '已发货';

        this.$request({
          url: '/orders/update',
          method: 'PUT',
          data: this.form,
        }).then(res => {
          if (res.code === '200') { // 表示操作成功
            this.$message.success('发货成功');
            this.load(1); // 刷新列表
          } else {
            this.$message.error(res.msg); // 弹出错误信息
          }
        });
      }).catch(() => {
        // 用户点击取消
        this.$message.info('发货已取消');
      });
      this.form = null
    },

    del(id) {   // 单个删除
      this.$confirm('您确定删除吗？', '确认删除', {type: "warning"}).then(response => {
        this.$request.delete('/orders/delete/' + id).then(res => {
          if (res.code === '200') {   // 表示操作成功
            this.$message.success('操作成功')
            this.load(1)
          } else {
            this.$message.error(res.msg)  // 弹出错误的信息
          }
        })
      }).catch(() => {
      })
    },
    delBatch() {   // 批量删除
      if (!this.ids.length) {
        this.$message.warning('请选择数据')
        return
      }
      this.$confirm('您确定批量删除这些数据吗？', '确认删除', {type: "warning"}).then(response => {
        this.$request.delete('/orders/delete/batch', {data: this.ids}).then(res => {
          if (res.code === '200') {   // 表示操作成功
            this.$message.success('操作成功')
            this.load(1)
          } else {
            this.$message.error(res.msg)  // 弹出错误的信息
          }
        })
      }).catch(() => {
      })
    },

    load(pageNum) {  // 分页查询
      if (pageNum) this.pageNum = pageNum
      if(this.user.role === 'FARMER') {
        this.farmer_name = this.user.username
      }
      this.$request.get('/orders/selectPage', {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          username: this.username,
          type: this.type,
          farmer_name: this.farmer_name
        }
      }).then(res => {
        this.tableData = res.data?.list
        this.total = res.data?.total
      })
    },
    reset() {
      this.username = null
      this.type = null
      this.farmer_name = null
      this.load(1)
    },
    handleCurrentChange(pageNum) {
      this.load(pageNum)
    },
  }
}
</script>

<style scoped>

</style>