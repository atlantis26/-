<template>
    <div>
      <div>
        <font size="6">今日流量</font>
        <table>
        <tr style="width:800px;">
          <th style="width: 200px"></th>
          <th style="width: 300px"><font size="5">浏览量(PV)</font></th>
          <th style="width: 300px"><font size="5">访客数(UV)</font></th>
        </tr>
        <tr style="width: 800px">
          <th style="width: 200px"><font size="5">今日</font></th>
          <th><font size="5">{{visitdata[0].pv}}</font></th>
          <th><font size="5">{{visitdata[0].uv}}</font></th>
        </tr>
        <tr style="width: 800px">
          <th style="width: 200px"><font size="5">本周</font></th>
          <th><font size="5">{{visitdata[1].pv}}</font></th>
          <th><font size="5">{{visitdata[1].uv}}</font></th>
        </tr>
        <tr style="width: 800px">
          <th style="width: 200px"><font size="5">总计</font></th>
          <th><font size="5">{{visitdata[2].pv}}</font></th>
          <th><font size="5">{{visitdata[2].uv}}</font></th>
        </tr>
        </table>
      </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
              visitdata:'',
            }
        },
        methods: {},
        created() {
          this.$ajax({
            method: 'get',
            url: '/getvisit',
            params: {}
          }).then(res => {
//            console.log(res);
            this.visitdata = res.data;
          });
        }
    }
</script>

<style scoped>

</style>
