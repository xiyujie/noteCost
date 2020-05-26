<template>
  <div id="Account">
    <ul>
      <li id="memberSelect" @mouseover="showMemberChild()" @mouseout="hideMemberChild()">
        <div class="memberChild" @click="changeMemb('总计')">总计</div>
        <div id="memberBox">
          <div class="memberChild" v-for="member in members" :key="member" @click="changeMemb(member)" @dblclick="deleteThis(member)" :title=member :value=member>{{member}}</div>
          <div class="memberChild" @click="addNewMember">+</div>
        </div>
      </li>
      <li v-for="item in typeList" v-bind:key="item" @click="cgAType(item)" @dblclick="dbDelete(item)">
       {{item}}
      </li>
      <li @click="addNewType">
       +
      </li>
    </ul>
    <PopupWindow :ifShow=popMsg @cgShow="changeShow" @sendMsg="sendMsg"></PopupWindow>
    <ShowDetail :cgType=types></ShowDetail>
    <IncomeOrExpenditure @changeIoe=changeIoe></IncomeOrExpenditure>
  </div>
</template>

<script>
import PopupWindow from '@/components/PopupWindow'
import ShowDetail from '@/components/ShowDetail'
import IncomeOrExpenditure from '@/components/IncomeOrExpenditure'
export default {
  name: 'Account',
  components:{
    PopupWindow,
    ShowDetail,
    IncomeOrExpenditure
  },
  data () {
    return {
      cg: '',
      popMsg: {
        show: false,
        ioe: '支出',
        type: '类型',
      },
      actNum: 0,
      types:{
        type:'总计',
        ioe: '支出',
        mb: '总计'
      },
    }
  },
  computed: {
    typeList: function (){
      var change = this.cg
      var ioe = this.types.ioe
      var typeList = []
      var storage = this.loc;
      var upd = this.createId()
      if(ioe == '支出'){
        if(storage.items && storage.items != ''){
        typeList = JSON.parse(storage.items)
        }else{
          var tmp = ['餐饮','交通','医疗','服饰','通讯','学习','洗护','人情','电器','厨具']
          typeList = tmp
          storage.items = JSON.stringify(tmp)
          this.$addTypeToDB('types', tmp, upd)
        }
      }else if(ioe == '收入'){
        if(storage.incomes && storage.incomes != ''){
          typeList = JSON.parse(storage.incomes)
        }else{
          var tmp2 = ['工资','理财','副业']
          typeList = tmp2
          storage.incomes = JSON.stringify(tmp2)
          this.$addTypeToDB('incomes', tmp2, upd)
        }
      }
      storage.updateTime = upd
      return typeList
    },
    members: function(){
      var change = this.cg
      var members = []
      if(this.loc.members && this.loc.members != '[]'){
        members = JSON.parse(this.loc.members)
      }
      return members
    }
  },
  methods: {
    addNewType: function(){
      this.popMsg.show = true
      this.popMsg.type = '类型'
    },
    changeMemb(dt){
      this.types.type = '总计'
      this.types.mb = dt
    },
    addNewMember(){
      this.popMsg.show = true
      this.popMsg.type = '成员'
    },
    changeShow: function(pShow){
      this.popMsg.show = pShow
    },
    sendMsg: function (data){
      this.cg = this.createId()
    },
    deleteThis(mem){
      var mbrs = JSON.parse(this.loc.members)
      for(var i = 0; i < mbrs.length; i++){
        if(mem == mbrs[i]){
          document.getElementById('memberBox').style.position = 'relative'
          if(confirm('您确定要删除成员“'+ mem +'”吗？\n删除后会一并删除其对应数据！')){
            mbrs.splice(i,1)
            this.deleteTypeWithData('member', mem, 'members')
            this.loc.members = JSON.stringify(mbrs)
            this.cg = this.createId()
          }else{
            return
          }
          break
        }
      }
    },
    changeIoe(dat){
      this.types = {
        type:'总计',
        ioe: dat,
        mb: '总计'
      }
      this.popMsg.ioe = dat
    },
    dbDelete: function(typeName){
      var tmpItems = this.typeList
      var tps = ''
      if(confirm('您确定要删除"'+typeName+'"这个记账类型吗?\n删除后会将该类型所有数据进行清空！！')){
        for(var i = 0; i < tmpItems.length; i++){
          if(tmpItems[i] == typeName){
            tmpItems.splice( i, 1)
            break
          }
        }
        if(this.types.ioe == '支出'){
          this.loc.items = JSON.stringify(tmpItems)
          tps = 'types'
        }else if(this.types.ioe == '收入'){
          this.loc.incomes = JSON.stringify(tmpItems)
          tps = 'incomes'
        }
        this.deleteTypeWithData('type', typeName, tps)
        this.cg = this.createId()
      }
    },
    cgAType: function(itm){
      this.types.type = itm
    },
    showMemberChild: function(){
      document.getElementById('memberBox').style.position = 'absolute'
    },
    hideMemberChild: function(){
      document.getElementById('memberBox').style.position = 'relative'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    height: 50px;
    line-height: 50px;
    background-color: rgb(49, 53, 56);
    color: white;
    font-size: 13px;
    max-height: 50px;
    white-space: nowrap;
    overflow-x: scroll;
  }
  li {
    display: inline-block;
    vertical-align: top;
    margin: 0;
    text-align: center;
    width: 70px;
    height: 50px;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  li:hover  {
    background-color: rgb(8, 158, 133);
  }
  #Account {
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  #memberSelect {
    outline: 0;
    border: 0;
    background-color: transparent;
    color: rgb(101, 209, 177);
    overflow: hidden;
    background: radial-gradient(white 30%,transparent 70%);
  }
  #memberBox {
    position: relative;
    width: 70px;
    text-align: center;
    z-index: 1;
    max-height: 230px;
    overflow-y: auto;
  }
  .memberChild {
    background-color: rgba(49, 53, 56, 0.8);
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
