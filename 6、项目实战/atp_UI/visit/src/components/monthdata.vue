<template>
  <div class="rate">
    <el-form>
      <el-col :span="6">
        <el-date-picker
          type="date"
          placeholder="选择需要查询的日期"
          :editable="false"
          v-model="defaultStartDate"
          value-format="yyyy-MM-dd"
          :picker-options="pickerBeginDateAfter"
          @change="getStartTime">
        </el-date-picker>
      </el-col>
      <el-col :span="6">
        <el-date-picker
          type="date"
          placeholder="选择需要查询的日期"
          :editable="false"
          v-model="defaultEndDate"
          value-format="yyyy-MM-dd"
          :picker-options="pickerBeginDateBefore"
          @change="getEndTime">
        </el-date-picker>
      </el-col>
      <el-button type="primary" v-on:click="sqlite()">查  询</el-button>
    </el-form>
    <div id="visit" style="width:710px;height: 400px;"></div>
    <!--<div id="userlog" style="width:900px;height: 400px;"></div>-->
  </div>
</template>

<script>
export default {
//  name: 'HelloWorld',
  data () {
    return {
      data:[],
      msg: 'Welcome to Your Vue.js App',
      activeName:'',
      jobQueryForm: {
        beginDateBefore: '',
        beginDateAfter: '',
      },
      defaultEndDate:new Date(),
      defaultStartDate:new Date(),
      pickerBeginDateBefore:{
        disabledDate:(time)=>{
          return time.getTime() > Date.now();
        }
      },
      pickerBeginDateAfter:{
        disabledDate:(time)=>{
          return time.getTime() > Date.now();
        }
      },
//      endtime:'',
//      starttime:'',
      visitdata:[],
    }
  },
  methods: {
    getStartTime(val){
      this.starttime = val;
    },
    getEndTime(data){
      this.endtime = data;
    },
    sqlite(){
      if (typeof (this.starttime) == 'undefined'){
        alert('请选择查询开始时间');
        return
      }
      if (typeof (this.endtime) == 'undefined'){
        this.$ajax({
          method: 'get',
          url: '/getmonth',
          params: {
            starttime:this.starttime,
          }
        }).then(res => {
          this.visitdata = res.data;
        });
        return
      }
      this.$ajax({
        method: 'get',
        url: '/getmonth',
        params: {
          starttime:this.starttime,
          endtime:this.endtime,
        }
      }).then(res => {
        this.visitdata = res.data;
      });
    },
    visitnum(){
      let rateChart = this.$echarts.init(document.getElementById('visit'));
      let option = {
        title : {
          text: '访问统计',
          subtext: '',
        },
        color: ['#3398DB'],
        legend: {
          data:['数据反馈','ATP主页','知识库']
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            dataView: {readOnly:true},
            magicType: {type: ['line', 'bar']},
            restore: {},
            saveAsImage: {}
          }
        },
        tooltip : {
          trigger: 'axis',
          axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '6%',
          bottom: '5%',
          containLabel: true
        },
        xAxis : {
            type : 'category',
            boundaryGap: false,
            data : this.visitdata[0],
            axisLabel :{
              interval:0
            }
          },
        yAxis : [
          {
            type : 'value'
          }
        ],
        series : [
          {
            name:'数据反馈',
            type:'line',
            barWidth: '60%',
            data:this.visitdata[1],
          },
          {
            name:'ATP主页',
            type:'line',
            barWidth: '60%',
            itemStyle:{
              normal: {
                color:'#f79f1f',
              }},
            data:this.visitdata[2]
          },
          {
            name:'知识库',
            type:'line',
            barWidth: '60%',
            itemStyle:{
              normal: {
                color:'#d9f71b',
              }},
            data:this.visitdata[3]
          }
        ]
      };
      rateChart.setOption(option);
    },
  },
  created(){
    this.$ajax({
      method: 'get',
      url: '/getmonth',
      params: {
      }
    }).then(res => {
      this.visitdata = res.data;
    });
    },
  mounted(){
  },
  watch:{
      'visitdata':'visitnum',
  }
}
</script>
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.rate{
  height:250px;
}
</style>
