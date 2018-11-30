<template xmlns="http://www.w3.org/1999/html">
  <div>
    <!--<form v-on:submit="loadXMLDoc">-->
      <!--<button>展开日志</button>-->
    <!--</form>-->
  </div>
</template>

<script>

  export default {
    name:"logtop",
    props:['datadata'],
    data() {
      return{
        data:''
      }
    },
    methods: {
      draw() {
        let self = this;
        let myChart = self.$echarts.init(document.getElementById('main'));
        // 绘制图表
        let option = {
          title : {
            text: '问题TOP展示',
            x:'center'
          },
          tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          series : [
            {
              name: '访问来源',
              type: 'pie',
              radius : '55%',
              center: ['50%', '60%'],
              data:[
                {value:Number(2), name:'产品问题'},
                {value:Number(2), name:'脚本问题'},
                {value:Number(2), name:'环境问题'},
                {value:Number(2), name:'其他'},
                {value:Number(4), name:'未分析'},
              ],
              itemStyle: {
                emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        };
        myChart.setOption(option);
      },

    },
    created() {
      this.data=this.datadata
    },
    mounted() {
      setTimeout(this.draw(), 1)
    }
  }
</script>

<style scoped>

</style>
