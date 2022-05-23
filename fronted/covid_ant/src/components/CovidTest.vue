<template>

  <a-row>
    <!--      上传两个文件-->
    <a-col :span="8">
      <h2>Step1:上传表格</h2>

      <div>
        <a-alert message="提示：建议上传XLS表格，否则不保留格式" type="info" show-icon/>
        <h3>上传学校报表</h3>
        <a-upload
            :action="HOST + '/upload?type=null'"
            :multiple="false"
            :file-list="fileList1"
            :before-upload="beforeUploadFile"
            accept='.xls,.xlsx'
            @change="handleChange1"
        >
          <a-button>
            <a-icon type="upload"/>
            Upload
          </a-button>
        </a-upload>
        <br>
        <br>
        <h3>上传医院报表</h3>

        <a-upload
            :action="HOST + '/upload?type=null'"
            :multiple="false"
            :file-list="fileList2"
            accept='.xls,.xlsx'
            @change="handleChange2"
        >
          <a-button>
            <a-icon type="upload"/>
            Upload
          </a-button>
        </a-upload>

      </div>

      <a-divider/>
      <div style="color: gray">
        *请确保学校表格第F列为学号
         <br>医院表格A列为姓名，C列为学号，H列为时间。
      </div>


    </a-col>
    <!--      /上传两个文件-->

    <a-col :span="8">
      <h2>Step2:处理表格</h2>
      <div>
        <a-alert message="工具仅提供便捷服务，具体以实际情况为准!" type="warning" show-icon/>

        <br>
        <br>

        <a-button type="primary" icon="logout" :loading="loading" @click="make_file">
          开始处理
        </a-button>
      </div>
    </a-col>
    <a-col :span="8">
      <h2>Step3:处理结果</h2>

      <div v-if="isSuccess">

        <a-tag color="green">
          成功:{{ this.ret_data['success_count'] }}
        </a-tag>

        <a-tag color="red">
          有误:{{ this.ret_data['err_count'] }}
        </a-tag>

        <br>
        <br>
        <a-button type="primary" block>
          <a :href="HOST+'/download/'+this.school_filename">下载文件</a>
        </a-button>

        <br>
        <br>
        <a-table :columns="columns" :data-source="table_data">

        </a-table>

        <a-divider/>
        <div style="color: gray">
          *提示：为保障个人信息安全，数据将在3分钟后自动销毁，服务器不保留任何个人数据，请及时下载！
        </div>


      </div>
      <div v-else>
        <a-empty/>
      </div>
    </a-col>
  </a-row>

</template>

<script>


import axios from "axios";


export default {
  beforeCreate: function () {
    this.isSuccess = false;
    this.HOST = process.env.VUE_APP_SERVER_URL;
  },
  methods: {
    handleChange1(info) {
      let fileList = [...info.fileList];
      fileList = fileList.slice(-1);       // 限制文件数量
      fileList = fileList.map(file => {
        if (file.response) {
          // eslint-disable-next-line no-unused-vars
          // window.school_filename = file.response;         //文件名
          this.school_filename = file.response;
          file.url = file.response.url;
        }
        return file;
      });
      this.fileList1 = fileList;
    },
    handleChange2(info) {
      let fileList = [...info.fileList];
      fileList = fileList.slice(-1);       // 限制文件数量
      fileList = fileList.map(file => {
        if (file.response) {
          // eslint-disable-next-line no-unused-vars
          // window.hospital_filename = file.response;         //文件名
          this.hospital_filename = file.response;
          file.url = file.response.url;
        }
        return file;
      });
      this.fileList2 = fileList;
    },
    beforeUploadFile(f) {
      const isLt50M = f.size / 1024 / 1024 < 50
      if (!isLt50M) {
        this.$message.error(f.name + '文件大小超出限制，请修改后重新上传')
        return false
      } else {
        return true
      }
    },
    make_file() {
      if (!this.school_filename || !this.hospital_filename) {
        this.$message.error('未上传文件或网络错误');
        return false
      }
      this.loading = true;
      axios.get(this.HOST + "/make", {
        params: {
          school_filename: this.school_filename,
          hospital_filename: this.hospital_filename
        }
      }).then(
          // 使用箭头函数this才会指代当前的Vue对象，如果使用的是function()，this指代的是window对象
          res => {
            // res 返回的参数包括很多内容，调用data才能获取到要展示的数据
            console.log(res.data)
            this.loading = false;
            // 处理成功标记
            this.isSuccess = true;
            this.ret_data = res.data;
            this.make_table();
          }
      ).catch(
          error => {
            this.$message.error('系统错误，请及时联系。');
            this.$message.error('错误信息：' + error);
          }
      )

    },
    make_table() {
      this.columns = [
        {
          title: '行号',
          dataIndex: 'idx',
          key: 'idx',
          width: '20%',
        },
        {
          title: '姓名',
          dataIndex: 'name',
          key: 'name',
          ellipsis: true,
        },
        {
          title: '学号',
          dataIndex: 'uid',
          key: 'uid',
          ellipsis: true,
        },

      ]

      this.table_data = []

      for (let idx = 0; idx < this.ret_data['not_in_db'].length; idx++) {
        this.table_data.push(
            {
              key: idx,
              idx: this.ret_data['not_in_db'][idx][0],
              uid: this.ret_data['not_in_db'][idx][1],
              name: this.ret_data['not_in_db'][idx][2]
            }
        )
      }

      console.log(this.table_data)
    }
  },
  data() {
    return {
      loading: false,
      columns: this.columns,
      table_data: this.table_data,
      fileList1: [
        {
          uid: '-1',
          name: '支持xls/xlsx',
          status: 'done',
        },
      ],
      fileList2: [
        {
          uid: '-1',
          name: '支持xls/xlsx',
          status: 'done',
        },
      ],
    };
  },
};

</script>