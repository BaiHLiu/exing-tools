import Vue from 'vue'
import router from "@/router/index";
import Antd from 'ant-design-vue'
import App from './App'
import 'ant-design-vue/dist/antd.css'

Vue.config.productionTip = false

Vue.use(Antd)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
