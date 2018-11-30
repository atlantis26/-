// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import echarts from 'echarts'
import axios from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
let host = window.location.host;
// Vue.prototype.$ajax=axios;
Vue.prototype.$ajax=axios.create({
  baseURL:'http://'+host,
});
Vue.config.productionTip = false;
Vue.use(ElementUI);
Vue.prototype.$echarts=echarts;

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
