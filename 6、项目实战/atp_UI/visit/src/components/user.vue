<template>
    <div>
      <div id="usertop" style="height: 550px;width:390px;"></div>
    </div>
</template>

<script>
    export default {
      data() {
        return {
          uselist:[],
          userdata:'',
        }
      },
      methods: {
        usertop(){
          let UserChart = this.$echarts.init(document.getElementById('usertop'));
//          alert(this.userdata[0]);
          let option = {
              title : {
                text: '访问用户',
                subtext: '',
              },
            toolbox: {
              show: true,
              feature: {
                dataView: {readOnly:true},
                restore: {},
                saveAsImage: {}
              }
            },
              series : [
                {
                  name: '',
                  type: 'pie',
//                  radius : '55%',
//                  center: ['50%', '60%'],
//                  data:this.userdata[1]
                  data:this.userdata
                }
              ]
            };
          UserChart.setOption(option);
          }
        },
      mounted(){
        },
      created() {
        this.$ajax({
          method: 'get',
          url: '/getuser',
          params: {
          }
        }).then(res => {
          this.userdata = res.data;
          this.usertop()
        });
        }
    }
</script>

<style scoped>

</style>
