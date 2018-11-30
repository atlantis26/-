<template>
    <div>
      <div id="top" class="top">
        <div style="float: left;margin-top:0px;margin-left: 15%;width: 85%;height: 50px;margin-right: 100%"><font size="6">ATP用户访问统计</font></div>
      </div>
      <div class="top" style="margin-left: 15%;height: 200px;width: 900px">
        <Visit></Visit>
      </div>
      <div class="top" style="margin-left: 15%;width: 900px">
        <div style="width: 900px">
          <router-view></router-view>
        </div>
        <div style="width: 350px;margin-left: 750px">
          <User></User>
        </div>
      </div>
    </div>
</template>

<script>
  import User from './components/user'
  import Visit from './components/visit'
    export default {
        data() {
            return {
              activeName:'',
              jobQueryForm: {
                beginDateBefore: '',
                beginDateAfter: '',
              },
              defaultStartDate:new Date(),
              pickerBeginDateAfter:'',
            }
        },
        methods: {
          getStartTime(){
          },
        },
        created() {
        },
      components:{
        User,
        Visit,
      }
    }
</script>

<style scoped>
  .p {
    color: black;
  }
  .ul {
    color: black;
  }
  .li {
    color: black;
  }
  div {
    height: 32px;
    color: #424b52;
  }
  .top {
    /*color: #f71ddd;*/
    background-color: #F6F6F6;
    width: 100%;
    border: 0px;
  }
  #top{
    height: 50px;
    border: 0;
    border-bottom: 5px #4F81BD solid;
  }
  /*.top page{*/
    /*height: 50px;*/
    /*border-bottom: 5px #4F81BD solid;*/
  /*}*/
  .page {
    width: 100%;
    /*margin-left: 15%;*/
    /*width: 1100px;*/
    /*height: inherit;*/
    /*margin: 0 auto;*/
  }
</style>
