// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
// import $ from 'jquery'
// import element from 'element-ui'
import echarts from 'echarts'
import axios from 'axios'
// import Vuex from 'vuex'
let host = window.location.host;
Vue.prototype.$ajax=axios.create({
  baseURL:'http://'+host,
  // baseURL:'http://10.148.133.134:8080',
  // baseURL:'http://10.148.133.134:4396',
});
Vue.config.productionTip = false;
// Vue.prototype.$vuex=Vuex;
Vue.use(ElementUI);
Vue.prototype.$echarts=echarts;
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
});
