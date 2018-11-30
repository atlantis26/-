import Vue from 'vue'
import Router from 'vue-router'
import monthdata from '@/components/monthdata'
import Index from '@/Index'
// import User from '@/components/user'
// import Visit from '@/components/visit'
Vue.use(Router);
export default new Router({
  routes: [
    {
      path: '/',
      name: '',
      component: Index,
      children: [
        {
          path: '',
          name: '',
          component: monthdata,
        },
      ]
    }
  ]
})
