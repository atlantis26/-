<template>
    <div>
      <div class="top">
        <div class="page">
          <font size="6">咪咕各组构建失败情况分析</font>
          <button type="button" style="width: 100px;height: 50px;float: right;margin-right: 100px" v-on:click="gotolog()">日志页面</button>
        </div>
        <div class="page1">
          <div class="p-left">
            <div style="height: 400px;width:1000px">
              <iframe id="showlog" v-bind:src="url" style="height: 390px;width:995px"></iframe>
            </div>
          </div>
        </div>
        <div class="end">
          <div class="list">
          <select style="width: 200px;height: 26px" v-model="logdata.ProblemClassify">
            <option v-for="problem in problems" v-bind:value="problem.value">
              {{problem.text}}
            </option>
          </select>
          <input type="text" v-model="logdata.ModuleName" placeholder="模块名称" style="width: 580px;height: 20px;"/>
          <input type="number" v-model="logdata.CaseNum" placeholder="失败case数量(个)" style="width: 200px;height: 20px;float: right"/>
          </div>
          <div class="list">
            <textarea rows="3" cols="20" v-model="logdata.FailureCause" placeholder="失败原因描述..." style="width: 994px;height: 48px;">
            </textarea>
          </div>
          <div class="list">
          <select v-model="logdata.ProblemStatus" style="width: 200px;height: 26px">
            <option value="待闭环">待闭环</option>
            <option value="已闭环">已闭环</option>
          </select>
          <input type="test" v-model="logdata.LoopMeasures" placeholder="闭环措施" style="width: 680px;height: 20px"/>
          <button type="button" style="width: 100px;height: 60px;float: right" v-on:click="postdata()">提交</button>
          <input type="text" v-model="logdata.LoopResults" placeholder="闭环结果" style="width: 886px;height: 20px;margin-top: 5px"/>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
//    import logTop from "./components/logtop.vue"
    export default {
//      name:log,
      components: {
//        logTop
      },
      data() {
            return {
              logdata:{
                Time:'',
                ObjId:'',
                projectname:'',
                ProblemClassify:'失败原因分类',
                ModuleName:'',
                CaseNum:'',
                FailureCause:'',
                ProblemStatus:'待闭环',
                LoopMeasures:'',
                LoopResults:'',
              },
              buildlog:'',
              objid:'',
              url:'',
              data:{},
              project:'',
              buttonlock:false,
              problems: [{ text: '失败原因分类', value: '失败原因分类'},
                  { text: '脚本问题', value: 'Script'},
                  { text: '环境问题', value: 'Environment'},
                  { text: '需求变更', value: 'ChangeRequest'},
                  { text: '修改引入缺陷', value: 'Introduction'},
                  { text: '新需求缺陷', value: 'DemandDefect'}]}
          },
//      props:['project', 'row'],
      methods: {
        getlog(){
          let logUrl='http://'+window.location.host+'/static/log/'+this.project+'/'+this.buildlog+'/report.html';
          this.url= logUrl
        },
        gotolog(){
          let url = 'http://'+window.location.host+'/static/log/'+this.project+'/'+this.buildlog+'/report.html';
          window.open(url)
        },
        postdata() {
          if(this.buttonlock == false){
            this.buttonlock = true;
          }else{
            alert('网络延时，请稍后再试...');
            return
          }
          if(this.logdata.ProblemClassify == '失败原因分类'){
            alert('请对问题进行分类，数据记录不生效...');
            this.buttonlock=false;
            return
          }
          if(this.logdata.ModuleName == ''){
            alert('请模块名称...');
            this.buttonlock=false;
            return
          }
          if( this.logdata.CaseNum == 0){
            alert('请输入不为\'0\'的构建失败数量...');
            this.buttonlock=false;
            return
          }
          if(this.logdata.FailureCause == ''){
            alert('请填写失败原因描述...');
            this.buttonlock=false;
            return
          }
          if(this.logdata.LoopMeasures == ''){
            alert('请填写闭环措施...');
            this.buttonlock=false;
            return
          }
          if(this.logdata.ProblemStatus == '已闭环' && this.logdata.LoopResults == ''){
            alert('已经闭环问题，请填写问题单号...');
            this.buttonlock=false;
            return
          }
          this.logdata.ObjId = this.objid;
          this.logdata.Time = this.buildlog;
          this.logdata.projectname = this.project;
          this.$ajax({
            method: 'post',
            url: '/postdata',
            params: {
              data: this.logdata
            }
          }).then((res)=>{
            this.restlogdata();
            this.buttonlock=false;
          }).catch((err)=>{
            alert('提交失败，请查看网络失败原因或者重试...');
            this.buttonlock=false;
          });
        },
        restlogdata(){
          this.logdata.objid = '';
          this.logdata.Time ='';
          this.logdata.projectname = '';
          this.logdata.ProblemClassify = '失败原因分类';
          this.logdata.ModuleName = '';
          this.logdata.CaseNum = '';
          this.logdata.FailureCause = '';
          this.logdata.ProblemStatus = '待闭环';
          this.logdata.LoopMeasures = '';
          this.logdata.LoopResults = '';
        },
        draw() {
          let scriptdata=this.data;
          let myChart = this.$echarts.init(document.getElementById('main'));
          // 绘制图表
          let option = {
            title : {
              text: '问题TOP展示',
              x:'center'
            },
            tooltip : {
              trigger: 'item',
//              formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            series : [
              {
                name: '访问来源',
                type: 'pie',
                radius : '55%',
                center: ['50%', '60%'],
                data:[
                {value:Number(scriptdata.changerequest), name:'需求变更'},
                {value:Number(scriptdata.script), name:'脚本问题'},
                {value:Number(scriptdata.environment), name:'环境问题'},
                {value:Number(scriptdata.introduction), name:'修改引入缺陷'},
                {value:Number(scriptdata.demanddefect), name:'新需求缺陷'},
//                {value:Number(scriptdata.other), name:'其他'},
//                {value:unparsed, name:'未分析'},
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
          // 使用刚指定的配置项和数据显示图表。
          myChart.setOption(option);
        },
      },
      updated(){
      },
      created(){
        this.buildlog = this.$route.query.row;
        this.project = this.$route.query.project;
        this.objid = this.$route.query.objid;
        },
      mounted(){
        this.getlog()
      }
    }
</script>

<style scoped>
  .top {
    /*color: #f71ddd;*/
    background-color: #F6F6F6;
    height: 50px;
    border-bottom: 5px #4F81BD solid;
  }
  .list{
    /*height: 50px;*/
    float: left;
    width: 1000px;
    margin-top: 5px;
  }
  .page {
    width: 1100px;
    height: inherit;
    margin: 0 auto;
  }
  .page1 {
    width: 1100px;
    height: 400px;
    margin: 0 auto;
  }
  .p-left{
    float: left;
    border:1px #FFFFFF solid;
    width: 1000px;
    height:400px;
    /*margin: 0 auto;*/
    margin-top: 5px;
    background-color: #F7F6F2;
  }
  .p-right{
    float: right;
    border:1px #FFFFFF solid;
    width: 290px;
    height:400px;
    background-color: #F7F6F2;
    margin-top: 5px;
  }
  .end{
    margin: 0 auto;
    border:1px #FFFFFF solid;
    width: 1100px;
    height:200px;
    background-color: #F7F6F2;
    /*float: left;*/
  }
</style>
