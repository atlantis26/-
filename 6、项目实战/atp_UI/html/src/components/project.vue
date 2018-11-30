<template>
  <div>
    <div>
      <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
        <el-tab-pane label="自动化数据展示" name="first">
          <el-form>
            <el-col :span="6">
              <el-date-picker
                type="date"
                placeholder="开始日期"
                :editable="false"
                v-model="jobQueryForm.beginDateAfter"
                :default-value="defaultStartDate"
                format="yyyy-MM-dd"
                :picker-options="pickerBeginDateAfter"
                @change="getStartTime">
              </el-date-picker>
            </el-col>
            <el-col :span="6">
              <el-date-picker
                type="date"
                placeholder="结束日期"
                :editable="false"
                v-model="defaultEndDate"
                format="yyyy-MM-dd"
                :picker-options="pickerBeginDateBefore"
                @change="getEndTime">
              </el-date-picker>
            </el-col>
            <el-button type="info" v-on:click="onSubmit()">搜  索</el-button>
          </el-form>
          <div id="main" style="width:750px;height: 400px;margin-top: 20px;margin-bottom:0px"></div>
          <div id="main1" style="width:900px;height: 500px;margin-top: 20px;margin-bottom:0px">
            <el-table :data="data[4]" style="width: 140%" height="500">
              <el-table-column prop="objid" label="构建ID" width="80%"></el-table-column>
              <el-table-column prop="buildtime" label="执行时间" width="150%"></el-table-column>
              <!--<el-table-column prop="coverage" label="覆盖率(line)" width="110%"></el-table-column>-->
              <el-table-column prop="version" label="构建版本" width="80%"></el-table-column>
              <el-table-column prop="all" label="用例总量"></el-table-column>
              <el-table-column prop="pass" label="通过量"></el-table-column>
              <el-table-column prop="fail" label="失败量" width="90%"></el-table-column>
              <el-table-column prop="Feedback" label="已反馈" width="90%"></el-table-column>
              <el-table-column label="未反馈" inline-template>
                <!--<template slot-scope="scope">-->
                  <el-button type="primary" @click="toLog(row)">反馈</el-button>
                <!--</template>-->
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        <el-tab-pane label="问题分布" name="second">
          <div>
            <el-table :data="problem.slice((currpage-1) * pagesize,currpage * pagesize)">
              <el-table-column prop="ObjId" label="构建ID"></el-table-column>
              <el-table-column prop="Time" label="执行时间" width="200%"></el-table-column>
              <el-table-column prop="Script" label="脚本问题"></el-table-column>
              <el-table-column prop="Environment" label="环境问题"></el-table-column>
              <el-table-column prop="ChangeRequest" label="需求变更"></el-table-column>
              <el-table-column prop="Introduction" label="修改引入缺陷"></el-table-column>
              <el-table-column prop="DemandDefect" label="新需求缺陷"></el-table-column>
              <el-table-column label="下载" inline-template>
                <!--<template slot-scope="scope">-->
                    <el-button type="info" v-on:click="download(row)">下载</el-button>
                <!--</template>-->
              </el-table-column>
            </el-table>
            <el-pagination background
                           layout="prev, pager, next, sizes, total, jumper"
                           :page-sizes="[10,15,20,50]"
                           :page-size=pagesize
                           :total=problem.length
                           @current-change="handleCurrentChange" @size-change="handleSizeChange">
            </el-pagination>
          </div>
        </el-tab-pane>
        <el-tab-pane label="覆盖率" name="third">
          <!--<div id="coverage" style="width:750px;height: 400px;margin-top: 20px;margin-bottom:0px"></div>-->
          <div>
            <el-table :data="coverage.slice((currpage-1) * pagesize,currpage * pagesize)">
              <el-table-column prop="Time" label="执行时间" width="200%"></el-table-column>
              <el-table-column prop="class" label="class"></el-table-column>
              <el-table-column prop="method" label="method"></el-table-column>
              <el-table-column prop="line" label="line"></el-table-column>
              <el-table-column prop="branch" label="branch"></el-table-column>
              <el-table-column prop="instruction" label="instruction"></el-table-column>
            </el-table>
            <el-pagination background
                           layout="prev, pager, next, sizes, total, jumper"
                           :page-sizes="[10,15,20,50]"
                           :page-size=pagesize
                           :total=coverage.length
                           @current-change="handleCurrentChange" @size-change="handleSizeChange">
            </el-pagination>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
    export default {
      data() {
        return {
          data:[],
          problem:[],
          coverage:[],
          projectname:'',
          activeName:'first',
          defaultEndDate:new Date(),
          defaultStartDate:new Date(),
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
          myChart:null,
          currpage:1,
          pagesize:15,
        }
      },
      methods: {
        handleCurrentChange(cpage) {
          this.currpage = cpage;
        },
        handleSizeChange(psize) {
          this.pagesize = psize;
        },
        toLog(row) {
          this.$router.push({
            path:'log',
            query:{
              project:this.$route.query.projectname,
              row:row.buildtime,
              objid:row.objid,
            },
          })
        },
        handleClick(){},
        getEndTime(date){
          this.endtime = date;
        },
        getStartTime(date){
          this.starttime = date;
        },
        onSubmit(){
          if (typeof (this.starttime) != 'undefined'){
            if(typeof (this.endtime) == 'undefined'){
              this.$ajax({
                method: 'get',
                url: '/getdata',
                params: {
                  project: this.$route.query.projectname,
                  starttime:this.starttime,
                }
              }).then(res => {
                this.data=res.data
              })
            }
            else {
              if (this.starttime > this.endtime){
                alert('开始时间小于结束时间，请重新输入时间范围。')
                return
              }
              else{
                this.$ajax({
                  method: 'get',
                  url: '/getdata',
                  params: {
                    project: this.$route.query.projectname,
                    starttime:this.starttime,
                    endtime:this.endtime,
                  }
                }).then(res => {
                  this.data=res.data
                })
              }
            }
          }
          else {
            alert('请输入起始时间。')
            return
          }
        },
        download(row) {
          this.$ajax({
            method: 'get',
            url: '/download',
            params: {
              project: this.$route.query.projectname,
              time: row.Time,
            }
          }).then(()=>{
            window.location='http://'+window.location.host+'/static/readout.xls';
          });
        },
        draw() {
          let self = this;
          // 绘制图表
          let option = {
            color: ['#4F81BD'],
            title: {
              text: '自动化执行数据',
              subtext:'构建项目：'+ this.$route.query.projectname,
            },
            tooltip: {},
            legend: {
              data: ['pass', 'fail', '通过率']
            },
            xAxis: {
              data:this.data[0],
              axisLabel:{
                interval:0,//横轴信息全部显示
                rotate:-20,//-20度角倾斜显示
              }
            },
            yAxis: [{
              type : 'value',
              name:'',
              position: 'left',
            },
              { type:'value',
                name:'通过率',
                min: 0,
                max: 100,
                interval: 10,
                axisLabel: {
                  formatter: '{value} %'
                }
              }],
            series: [{
              name: 'pass',
              type: 'bar',
              itemStyle:{
                normal: {
                  color:'#65C0EF',
                }},
              stack:'case',
              data:this.data[2]
            },
              {
                name: 'fail',
                type: 'bar',
                itemStyle:{normal: {
                  color:'#FFB104',
                }},
                stack:'case',
                data:this.data[1]
              },
              {
                name: '通过率',
                type: 'line',
                yAxisIndex:1,
                stack:'',
                data:this.data[3]
              }],
          };
          // 使用刚指定的配置项和数据显示图表。
          self.myChart.setOption(option);
        },
        getData(){
          this.$ajax({
            method: 'get',
//            url: 'http://10.148.133.134:8080/getdata',
            url: '/getdata',
            params: {
              project:this.newPath,
            }
          }).then(res => {
            this.data = res.data;
//            console.log(this.data);
            this.draw();
          });
          this.$ajax({
            method: 'get',
//            url: 'http://10.148.133.134:8080/getproblem',
            url: '/getproblem',
            params: {
              project:this.newPath,
            }
          }).then(res => {
            this.problem = res.data;
          });
          this.$ajax({
            method: 'get',
//            url: 'http://10.148.133.134:8080/getcoverage',
            url: '/getcoverage',
            params: {
              project:this.newPath,
            }
          }).then(res => {
            this.coverage = res.data;
          })
        },
      },
      updated(){
//        this.$nextTick(()=>{
//          this.myChart=this.$echarts.init(document.getElementById('main'),'walden');
//          this.getData();
//        });
//        this.myChart=this.$echarts.init(document.getElementById('main'),'walden');
       /* this.$nextTick(()=>{
          this.getData()
        });*/
      },
      created() {
      },
      mounted() {
        this.$nextTick(()=>{
          this.myChart=this.$echarts.init(document.getElementById('main'),'walden');
          this.getData();
        });
      },
      computed:{
        newPath(){
          const self = this;
          return self.$route.query.projectname || '';
        }
      },
      watch:{
        'newPath':'getData',
        'data':'draw',
      }
    }
</script>

<style scoped>

</style>
