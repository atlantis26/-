<template>
  <div id="app">
    <!--<router-link to="/Index">index</router-link>-->
    <!--<router-link to="/log">log</router-link>-->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      user: null,
    }
  },
  created() {
//    this.fetchData()
  },
  watch: {
//    '$route': 'fetchData'
    '$route': '',
    '$addRoutes':''
  },
  methods: {
  }
}



</script>

<style>
</style>
