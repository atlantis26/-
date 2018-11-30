<template>
    <div class="rate">
      <el-form>
        <el-col :span="6">
          <el-date-picker
            type="month"
            placeholder="选择需要查询的日期"
            :editable="false"
            v-model="defaultStartDate"
            :default-value="defaultStartDate"
            format="yyyy-MM"
            :picker-options="pickerBeginDateAfter"
            @change="getStartTime">
          </el-date-picker>
        </el-col>
        <el-button type="info" v-on:click="sqlite()">查  询</el-button>
      </el-form>
      <div id="rate" style="width:900px;height: 400px;"></div>
      <div id="incrementrate" style="width:900px;height: 400px;"></div>
      <div id="increment" style="width:900px;height: 400px;"></div>
    </div>
</template>

<script>
    export default {
      data() {
        return {
          data:'',
          jobQueryForm: {
            beginDateBefore: '',
            beginDateAfter: '',
          },
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
          defaultStartDate:new Date(),
          defaultEndDate:new Date(),
          getEndTime:'',
        }
      },
      methods: {
        getStartTime(date){
          this.defaultStartDate=date
        },
        sqlite() {
          this.$ajax({
            method: 'get',
            url: '/getdata',
            params: {
              project: 'rate',
              month:this.defaultStartDate,
            }
          }).then(res => {
            this.data = res.data;
          })
        },
        passrate(){
          let rateChart = this.$echarts.init(document.getElementById('rate'));
          let option = {
            title: {
              text: '项目月度平均通过率',
              subtext: this.defaultStartDate,
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data:['通过率']
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
            xAxis:  {
              type: 'category',
//              boundaryGap: false,
              data:this.data[3],
//              data: ['attendance','bigdata','billing','campaigncenter','contentcenter','encapsulation','framework',
//                'migucredit','migustar', 'officedata','ordercenter','partnermanagement','pricecenter','productcenter',
//                'spms','subscribecenter'],
              axisLabel:{
                interval:0,//横轴信息全部显示
                rotate:-20,//-20度角倾斜显示
              },
            },
            yAxis: [{
              type: 'value',
              axisLabel: {
                formatter: '{value} %'
              }
            }],
            series: [
              {
                name:'通过率',
                type:'line',
                data:this.data[0],
                itemStyle:{
                  normal: {
                    color:'#f79f1f',
                  }},
                markPoint: {
                  data: [
                    {name: '周最低', value: -2, xAxis: 1, yAxis: -1.5}
                  ]
                },
                markLine: {
                  data: [
//                    {type: 'average', name: '平均值'},
                    [{
                      symbol: 'none',
                      x: '90%',
                      yAxis: 'max'
                    }, {
                      symbol: 'circle',
                      label: {
                        normal: {
                          position: 'start',
                          formatter: '最大值'
                        }
                      },
                      type: 'max',
                      name: '最高点'
                    }]
                  ]
                }
              }
            ]
          };
          rateChart.setOption(option);
        },
        incrementrate(){
          let incrementrate = this.$echarts.init(document.getElementById('incrementrate'));
          let option = {
            title: {
              text: '项目月度新增脚本幅度',
              subtext: this.defaultStartDate,
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data:['增长幅度']
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
            xAxis:  {
//              type:'log',
              type: 'category',
//              boundaryGap: false,
              data:this.data[3],
//              data: ['attendance','bigdata','billing','campaigncenter','contentcenter','encapsulation','framework',
//                'migucredit','migustar', 'officedata','ordercenter','partnermanagement','pricecenter','productcenter',
//                'spms','subscribecenter'],
              splitLine: {
                show: false
              },
              axisLabel:{
                interval:0,//横轴信息全部显示
                rotate:-20,//-20度角倾斜显示
              },
            },
            yAxis: [{
              type:'log',
//              type: 'value',
              axisLabel: {
                formatter: '{value} %'
              }
            }],
            series: [
              {
                name:'增长幅度',
                type:'bar',
                data:this.data[1],
                itemStyle:{
                  normal: {
                    color:'#f79f1f',
                  }},
                markPoint: {
                  data: [
                    {name: '周最低', value: -2, xAxis: 1, yAxis: -1.5}
                  ]
                },
//                markLine: {
//                  data: [
////                    {type: 'average', name: '平均值'},
//                    [{
//                      symbol: 'none',
//                      x: '90%',
//                      yAxis: 'max'
//                    },
//                      {
//                      symbol: 'circle',
//                      label: {
//                        normal: {
//                          position: 'start',
//                          formatter: '最大值'
//                        }
//                      },
//                      type: 'max',
//                      name: '最高点'
//                    }
//                    ]
//                  ]
//                }
              }
            ]
          };
          incrementrate.setOption(option);
        },
        increment(){
          let incrementChart = this.$echarts.init(document.getElementById('increment'));
          let option = {
            title: {
              text: '月度新增脚本数量',
              subtext: this.defaultStartDate,
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data:['月度增长量']
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
            xAxis:  {
              type: 'category',
//              boundaryGap: false,
              data:this.data[3],
//              data: ['attendance','bigdata','billing','campaigncenter','contentcenter','encapsulation','framework',
//                'migucredit','migustar', 'officedata','ordercenter','partnermanagement','pricecenter','productcenter',
//                'spms','subscribecenter'],
              axisLabel:{
                interval:0,//横轴信息全部显示
                rotate:-20,//-20度角倾斜显示
              },
            },
            yAxis: [{
              type: 'value',
              axisLabel: {
                formatter: '{value}'
              }
            }],
            series: [
              {
                name:'月度增长量',
                type:'bar',
                data:this.data[2],
                itemStyle:{
                  normal: {
                    color:'#f79f1f',
                  }},
                markPoint: {
                  data: [
                    {name: '周最低', value: -2, xAxis: 1, yAxis: -1.5}
                  ]
                },
                markLine: {
                  data: [
//                    {type: 'average', name: '平均值'},
                    [{
                      symbol: 'none',
                      x: '90%',
                      yAxis: 'max'
                    }, {
                      symbol: 'circle',
                      label: {
                        normal: {
                          position: 'start',
                          formatter: '最大值'
                        }
                      },
                      type: 'max',
                      name: '最高点'
                    }]
                  ]
                }
              }
            ]
          };
          incrementChart.setOption(option);
        },
        refresh(){
          this.passrate();
          this.incrementrate();
          this.increment();
        }
      },
      created() {
        this.$ajax({
          method: 'get',
          url: '/getdata',
          params: {
            project: 'rate',
          }
        }).then(res => {
          this.data = res.data;
//          alert(this.data)
        });
      },
      mounted() {
        this.refresh();
      },
      computed:{
//        newTime(){
//          const self = this;
//          return self.defaultStartDate;
//        }
      },
      watch:{
        'data':'refresh',
      }
    }
</script>

<style scoped>
  .rate{
    height:1500px;
  }
</style>
