import Vue from 'vue'
import Router from 'vue-router'
import project from '@/components/project'
import Rate from '@/components/rate'
import Index from '@/Index'
import Log from '@/log'

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
          component: Rate,
        },
        {
          path: '/project',
          name: 'Project',
          component: project,
        },
        {
          path: '/rate',
          name: 'Rate',
          component: Rate,
        },
      ]
    },
    {
      path: '/log',
      name: '',
      component: Log,
    }
  ],
})
