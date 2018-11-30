<template>
    <div>
      <div class="top">
        <div class="page"><font size="6">咪咕各组自动化建设数据</font></div>
      </div>
      <div class="page">
        <nav>
          <ul>
            <li class="project" style="height: auto"><h3 style="width: 160px;text-align: center;">构建项目</h3></li>
            <li class="project">
              <span class="Darrow"></span>
              <a>大 数 据</a>
              <dl>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bigdata'}}">数据分析云</router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bd_func'}}"><p>功能场景</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bvreport'}}"><p>红海行动</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bas'}}"><p>红海系统APP</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bigdata_musiclabel'}}"><p>差异化运营</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bigdata_eagle'}}"><p>咪咕天眼</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bigdata_eagle2'}}"><p>天眼二期</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'migucredit'}}"><p>咪咕信用</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bigdata_labelview'}}"><p>标签可视化</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bigdata_monitor'}}"><p>业务监控</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'bigdata_recommand'}}"><p>个性化推荐</p></router-link></dd>
              </dl>
            </li><br/>
            <li class="project">
              <span class="Darrow"></span>
              <a>能 力 中 心</a>
              <dl>
                <dd><router-link :to="{path: 'project',query: {projectname: 'campaigncenter'}}"><p>营销中心</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'contentcenter'}}"><p>内容中心</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'framework'}}"><p>框架</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'ordercenter'}}"><p>订单中心</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'partnermanagement'}}"><p>合作伙伴管理</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'pricecenter'}}"><p>批价中心</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'productcenter'}}"><p>产品中心</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'subscribecenter'}}"><p>订购中心</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'encapsulation'}}"><p>封装层</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'usercenter'}}"><p>二级用户中心</p></router-link></dd>
              </dl>
            </li><br/>
            <li class="project">
              <span class="Darrow"></span>
              <a>服 务 云</a>
              <dl>
                <dd><router-link :to="{path: 'project',query: {projectname: 'faq_jiekou'}}">知识库</router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'im_jiekou'}}"><p>IM接续</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'web'}}"><p>坐席平台</p></router-link></dd>
              </dl>
            </li><br/>
            <li class="project">
              <span class="Darrow"></span>
              <a>统 一 搜 索</a>
              <dl>
                <dd><router-link :to="{path: 'project',query: {projectname: 'spyy'}}">视频影院</router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'music'}}"><p>音乐</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'read'}}"><p>阅读</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'cartoon'}}"><p>动漫</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'tongyimenhu'}}"><p>统一门户</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'opmanager'}}"><p>运营管理平台</p></router-link></dd>
              </dl>
            </li><br/>
            <li class="project">
              <span class="Darrow"></span>
              <a>统一网页计费安全</a>
              <dl>
                <dd><router-link :to="{path: 'project',query: {projectname: 'forapi'}}">forAPI</router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'forui'}}"><p>forUI</p></router-link></dd>
              </dl>
            </li><br/>
            <li class="project">
              <span class="Darrow"></span>
              <a>统一结算</a>
              <dl>
                <dd><router-link :to="{path: 'project',query: {projectname: 'migu_comic'}}">动漫子系统</router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'migu_game'}}"><p>互娱子系统</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'migu_book'}}"><p>数媒子系统</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'migu_music'}}"><p>音乐子系统</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'migu_video'}}"><p>视讯子系统</p></router-link></dd>
                <dd><router-link :to="{path: 'project',query: {projectname: 'migu_plus'}}"><p>咪咕+</p></router-link></dd>
              </dl>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'unifiedusercenter'}}"><p>统一用户中心系统</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'onion_data'}}"><p>统一CPA稽核系统</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'APPSDK'}}"><p>统一APP计费安全SDK</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'unifiedusercenterrisk'}}"><p>统一用户中心风控系统</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'umsauto'}}"><p>统一运维系统</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'credit'}}"><p>合作伙伴信用系统</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'billing'}}"><p>计费</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'attendance'}}"><p>考勤</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'solution'}}"><p>解决方案项目</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'officedata'}}"><p>局数据</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'spms'}}"><p>spms</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'miguplus'}}"><p>咪咕+</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'cmam'}}"><p>中央媒资</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'AI'}}"><p>人工智能</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'tuna'}}"><p>风险管控审计系统</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'embeded'}}"><p>廉洁风险防控系统</p></router-link>
            </li><br/>
            <!--<li class="project">-->
            <!--<router-link :to="{path: 'project',query: {projectname: 'unifiedsearch'}}"><p>统一搜索</p></router-link>-->
            <!--</li><br/>-->
            <!--<li class="project">-->
            <!--<router-link :to="{path: 'project',query: {projectname: 'jiesuan'}}"><p>统一结算</p></router-link>-->
            <!--</li><br/>-->
            <!--<li class="project">-->
              <!--<router-link :to="{path: 'project',query: {projectname: 'UWSPS'}}"><p>统一网页计费安全SDK</p></router-link>-->
            <!--</li><br/>-->
            <!--<li class="project">-->
              <!--<router-link :to="{path: 'project',query: {projectname: 'wxServiceCloud'}}"><p>服务云</p></router-link>-->
            <!--</li><br/>-->
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'ucpmcs'}}"><p>安管</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'ngoc'}}"><p>NGOC</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'aiplatform'}}"><p>AI平台</p></router-link>
            </li><br/>
            <li class="project">
              <router-link :to="{path: 'project',query: {projectname: 'migutoutou'}}"><p>智能投递柜</p></router-link>
            </li><br/>
            <li class="project" style="padding-bottom: 0px;">
              <router-link :to="{path:'rate'}"><p>通过率</p></router-link>
            </li><br/>
          </ul>
        </nav>
        <div class="p-right">
            <router-view></router-view>
        </div>
      </div>
    </div>
</template>

<script>
        export default {
            data() {
                return {
                  title:'hello world'
                }
            },
            methods: {
              handleOpen(key, keyPath) {
                console.log(key, keyPath);
              },
              handleClose(key, keyPath) {
                console.log(key, keyPath);
              }
            },
            created() {

            }
        }
</script>

<style scoped>
  .top {
    color: #f71ddd;
    background-color: #F6F6F6;
    height: 50px;
    border-bottom: 5px #4F81BD solid;
  }
  div {
    height: 32px;
    color: #424b52;
  }
  .page {
    width: 1100px;
    height: inherit;
    margin: 0 auto;
  }
  .p-left{
    float: left;
    border:1px #FFFFFF solid;
    width:15%;
    height:850px;
    background-color: #F7F6F2;
  }
  .p-right{
    float: right;
    border:1px #FFFFFF solid;
    border-bottom: none;
    width:84%;
    height:850px;
  }
</style>

