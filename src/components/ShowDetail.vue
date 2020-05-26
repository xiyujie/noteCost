<template>
  <div id="showDetail">
    <h1>{{member + cgType.type + dtils.ioe}}共:{{money}}&nbsp;&nbsp;元</h1>
    <h2>结余：{{restMoney}}元</h2>
    <h3>
      <button class="btn" @click="popAdd">新增一项{{dtils.ioe}}</button>
      <select @change="cgYear($event)" class="btn" :style="{'background-color':'#'+this.createColor('绿')}">
        <option value="年">年</option>
        <option v-for="year in date.year" v-bind:key="year" >
          {{year}}
        </option>
      </select>
      <select @change="cgMonth($event)" class="btn" :style="{'background-color':'#'+this.createColor('红')}">
        <option value="月">月</option>
        <option v-for="month in date.month" v-bind:key="month" >
          {{month}}
        </option>
      </select>
      <select @change="cgDay($event)" class="btn" :style="{'background-color':'#'+this.createColor('蛋')}">
        <option value="日">日</option>
        <option v-for="day in date.day" v-bind:key="day" >
          {{day}}
        </option>
      </select>
    </h3>
    <div class="emptyMsg" v-if="dtils.emptyMsgShow">
      您当前还没有{{dtils.ioe}}记录,添加您的第一条记录吧!
    </div>
    <div class="listBox" v-if="dtils.listBoxShow">
      <div class="listBox-child" v-for="detail in dtils.tmpList" v-bind:key="detail.id">
        <div class="l-cType" :style="{'background-color':detail.clr}">{{detail.type[0]}}</div>
        <div class="l-cLineOne">
          <div class="mnyStl">{{detail.mny}}<span class="unit">&nbsp;元</span></div>
          <div class="timeStl">{{detail.time}}</div>
        </div>
        <div class="l-cLineTwo">
          <div class="memStl">{{detail.member[detail.member.length - 1]}}</div>
          <div class="stmStl">备注：{{detail.stm}}</div>
        </div>
        <button class="editBtn psleft10 colorRed" @click="deleteLog(detail.id)"></button>
        <button class="editBtn psright10 colorYellow" @click="editPopUp(detail)"></button>
      </div>
    </div>
    <AddNewLog :ifAddShow=sendToAdd @closeAddPop = "closeAddPop" @changeData = "changeData"></AddNewLog>
    <EditPop :editLog=sendToEdit @changeDetail="changeDetail" @closeEditPop="closeEditPop"></EditPop>
  </div>
</template>

<script>
import AddNewLog from '@/components/AddNewLog'
import EditPop from '@/components/EditPop'
export default {
    name: 'ShowDetail',
    components: {
      AddNewLog,
      EditPop
    },
    props:[
      'cgType'
    ],
    data() {
      return {
        cgd: '',
        category: '',
        choseYear: '年',
        choseMonth: '月',
        choseDay: '日',
        sendToEdit: {
          editShow: false,
          preMsg: {}
        },
        sendToAdd: {
          addShow: false,
          addType: this.cgType.type,
          addIoe: this.cgType.ioe,
          addMemb: this.cgType.mb
        },
      }
    },
    computed: {
      member(){
        var dat = this.cgType
        var member = ''
        if(dat.mb != '总计'){
          member = '“' + this.cgType.mb + '”'
        }
        return member
      },
      dtils: function(){
        var changeData = this.cgd
        var category= this.category
        var sIoe = this.cgType.ioe
        var tmpType = this.cgType.type
        var member= this.cgType.mb
        var detils = {tmpList:[],listBoxShow:false,emptyMsgShow:true,ioe:sIoe}
        var orgLogList = []
        var abwArr = []
        var  mbs = []
        if(this.loc.members && this.loc.members != '[]'){
          mbs = JSON.parse(this.loc.members)
        }
        if(this.loc.logList && this.loc.logList != '[]'){
          orgLogList = JSON.parse(this.loc.logList);
          for(var i = 0; i < orgLogList.length; i++){
            if(orgLogList[i].ioe == this.cgType.ioe){
              abwArr.push(orgLogList[i])
            }
          }
          if(member != '总计'){
            var mList = []
            for(var i = 0; i < abwArr.length; i++){
              if(abwArr[i].member == member){
                mList.push(abwArr[i])
              }
            }
            abwArr = mList
          }
          if(tmpType == '总计'){
            detils.listBoxShow = true
            detils.emptyMsgShow = false
            if(this.choseYear == '年' && this.choseMonth == '月' && this.choseDay == '日'){
              detils.tmpList = abwArr
            }else{
              if(this.choseYear != '年'){
                abwArr = this.screeningData(abwArr,this.choseYear,0)
              }
              if(this.choseMonth != '月'){
                abwArr = this.screeningData(abwArr,this.choseMonth,1)
              }
              if(this.choseDay != '日'){
                abwArr = this.screeningData(abwArr,this.choseDay,2)
              }
              detils.tmpList = abwArr
              if(detils.tmpList.length == 0){
                detils.listBoxShow = false
                detils.emptyMsgShow = true
              }
            }
          }else{
            for(var i = 0; i < abwArr.length; i++){
              if(abwArr[i].type == tmpType){
                detils.tmpList.push(abwArr[i])
              }
            }
            if(detils.tmpList.length > 0){
              detils.listBoxShow = true
              detils.emptyMsgShow = false
            }
          }
        }else{
          detils.listBoxShow = false
          detils.emptyMsgShow = true
        }
        detils.tmpList.sort(this.$compare('id')).reverse()
        return detils
      },
      date: function(){
        var changeData = this.cgd
        var dateTArr = {year:[],month:[],day:[]}
        if(this.loc.logList && this.loc.logList != '[]'){
          var tmpArr = JSON.parse(this.loc.logList)
          for (var i = 0; i < tmpArr.length; i++){
            if(!dateTArr.year.includes(tmpArr[i].time.split('-')[0])){
              dateTArr.year.push(tmpArr[i].time.split('-')[0])
            }
            if(!dateTArr.month.includes(tmpArr[i].time.split('-')[1])){
              dateTArr.month.push(tmpArr[i].time.split('-')[1])
            }
            if(!dateTArr.day.includes(tmpArr[i].time.split('-')[2])){
              dateTArr.day.push(tmpArr[i].time.split('-')[2])
            }
          }
          dateTArr.year.sort().reverse()
          dateTArr.month.sort()
          dateTArr.day.sort()
        }
        return dateTArr
      },
      money: function(){
        var mny = 0
        if(this.dtils.tmpList.length != 0){
          for(var i = 0; i < this.dtils.tmpList.length; i++){
            mny += this.dtils.tmpList[i].mny - 0
          }
        }
        return mny.toFixed(2)
      },
      restMoney: function(){
        var change = this.cgd
        var tp = this.cgType.type
        var restMoney = 0
        var allData = []
        if(this.loc.logList && this.loc.logList != '[]'){
          allData = JSON.parse(this.loc.logList)
        }
        var icm = 0
        var epd = 0
        if(allData.length != 0 && allData.length){
          var tma = []
          if(this.cgType.mb != '总计'){
            for(let i = 0; i < allData.length; i++){
              if(allData[i].member == this.cgType.mb){
                tma.push(allData[i])
              }
            }
            allData = tma
          }
          for(let i = 0; i < allData.length; i++){
            if(allData[i].ioe == '支出'){
              epd += allData[i].mny - 0
            }else if(allData[i].ioe == '收入'){
              icm += allData[i].mny - 0
            }
          }
          restMoney = ( icm - epd ).toFixed(2)
        }
        return restMoney
      }
    },
    methods: {
      cgYear(evt){
        this.choseYear = evt.target.value
      },
      cgMonth(evt){
        this.choseMonth = evt.target.value
      },
      cgDay(evt){
        this.choseDay = evt.target.value
      },
      btnShow:function(){
        this.btnState = true
      },
      btnHide:function(){
        this.btnState = false
      },
      popAdd: function(){
        this.sendToAdd = {
          addShow: true,
          addType: this.cgType.type,
          addIoe: this.cgType.ioe,
          addMemb: this.cgType.mb
        }
      },
      closeAddPop: function(msg){
        this.sendToAdd.addShow = false
      },
      editPopUp: function(dat){
        this.sendToEdit = {
          editShow: true,
          preMsg: dat
        }
      },
      closeEditPop: function(bl){
        this.sendToEdit.editShow = bl
      },
      changeData: function(dat){
        this.listBoxShow = true
        this.emptyMsgShow = false
        this.cgd = dat
      },
      changeDetail: function(dat){
        this.sendToEdit.editShow = false
        this.cgd = dat
      },
      deleteLog: function(delId){
        var upd = this.createId()
        if(confirm('您确定要删除这条记录吗?')){
          var tmpArr = JSON.parse(this.loc.logList)
          for(var i = 0; i < tmpArr.length; i++){
            if(tmpArr[i].id == delId){
              tmpArr.splice(i,1)
            }
          }
          this.loc.updateTime = upd
          this.loc.logList = JSON.stringify(tmpArr)
          this.cgd = new Date().getTime()
          this.axios.post(
            'deleteLog',
            {
              'updateTime': upd,
              'id': delId
            }
          ).then(
            res=>{
              console.log(res)
            }
          )
        }
      },
    }
}
</script>

<style scoped>
  #showDetail {
    width: 100%;
    height: calc(100% - 100px);
    background-color: rgb(227, 228, 227);
    padding: 0.1px;
    overflow-y: auto;
  }
  .btn {
    background-color: tomato;
    border: 0;
    outline: 0;
    border-radius: 5px;
    color:  rgb(94, 6, 6) ;
    margin: 0 5px;
    padding: 5px 10px;
    box-shadow: 0 5px 5px 0 darkslategray;
  }
  .listBox {
    width: calc(100% - 40px);
    margin: auto;
  }
  .listBox-child {
    width: 100%;
    padding: 3px 65px 8px 50px;
    box-sizing: border-box;
    margin-bottom: 10px;
    border: slategrey solid 1px;
    border-radius: 5px;
    color: rgb(69, 82, 71) ;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    position: relative;
    box-shadow: 0 5px 5px 0 darkslategray;
    text-align: left;
    background-color: rgb(218, 213, 147);
  }
  .l-cType {
    position: absolute;
    width: 30px;
    height: 30px;
    background-color: turquoise;
    border-radius: 15px;
    overflow: hidden;
    left: 10px;
    text-align: center;
    line-height: 30px;
    top: calc(50% - 15px);
    color: white;
  }
  .l-cLineOne {
    width: 100%;
    position: relative;
  }
  .l-cLineTwo {
    font-size: 14px;
    line-height: 18px;
    width: 100%;
    word-wrap: break-word;
    word-break: break-all;
    position: relative;
  }
  .mnyStl {
    font-size: 30px;
    margin: 5px 0;
  }
  .unit {
    font-size: 25px;
  }
  .timeStl {
    font-size: 20px;
    position: absolute;
    top: 3px;
    right: 5px;
  }
  .stmStl {
    padding-right: 50px;
  }
  .memStl {
    position: absolute;
    right: 5px;
    width: 30px;
    text-align: center;
    background-color: rgba(151, 167, 120, 0.7);
    color: white;
    border-radius: 5px;
  }
  .psleft10 {
    right: 40px
  }
  .psright10 {
    right: 10px;
  }
  .editBtn {
    position: absolute;
    width: 18px;
    height: 18px;
    color: white;
    top: calc(50% - 9px);
    border: 0;
    border-radius: 10px;
    outline: 0;
    box-shadow: 0 3px 3px 0 darkslategray;
  }
  .emptyMsg {
    width: 100%;
    padding: 15px 0;
    color: darkslategrey;
    font-size: 18px;
  }
</style>