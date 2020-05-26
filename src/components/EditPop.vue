<template>
    <div class="masking" v-show=editLog.editShow>
    <div class="AddNewLog">
      <div class="clsBtn" @click="closePop"></div>
      <div class="titleBar">修改</div>
      <div>
        <p class="addTitle">您当前的类型为:<span class="colorRed">{{editLog.preMsg.type}}</span></p>
        <select class="typeSelect" id="editSelect" :value="editLog.preMsg.type">
          <option :value="editLog.preMsg.type">{{editLog.preMsg.type}}</option>
          <option v-for="type in types" v-bind:key="type" :value="type" >
            {{type}}
          </option>
        </select>
      </div>
      <div>
        <p class="addTitle">所属成员:<span class="colorRed">{{editLog.preMsg.member}}</span></p>
        <select class="typeSelect" id="editMemberSelect" :value="editLog.preMsg.member">
          <option :value="editLog.preMsg.member">{{editLog.preMsg.member}}</option>
          <option v-for="member in Emembers" v-bind:key="member" :value="member" >
            {{member}}
          </option>
        </select>
      </div>
      <div>
        <p class="addTitle">请输入修改金额:</p>
        <input type="number" class="addInput" id="editInput" min="0" :value="editLog.preMsg.mny" />
      </div>
      <div>
        <p class="addTitle">备注:</p>
        <textarea class="addTxt" id="editTxt" cols="25" rows="5" v-model="editLog.preMsg.stm"></textarea>
      </div>
      <div>
        <p class="addTitle">修改支出时间:</p>
        <input class="addDate" id="editDate" type="date" :value="editLog.preMsg.time">
      </div>
      <button class="closeBtn" @click = "savaEdit()">确定修改</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditPop',
  data(){
    return {

    }
  },
  props:['editLog'],
  computed: {
    types: function(){
      var types = []
      if(this.editLog.preMsg.ioe == '支出'){
        types = JSON.parse(this.loc.items)
      }else if(this.editLog.preMsg.ioe == '收入'){
        types = JSON.parse(this.loc.incomes)
      }
      for(var i = 0; i < types.length; i++){
        if(types[i] == this.editLog.preMsg.type){
          types.splice(i,1)
        }
      }
      return types
    },
    Emembers(){
      var members = []
      if(this.loc.members && this.loc.members != '[]'){
        members = JSON.parse(this.loc.members)
        for(var i = 0; i < members.length; i++){
          if(members[i] == this.editLog.preMsg.member){
            members.splice(i,1)
          }
        }
      }
      return members
    }
  },
  methods: {
    closePop: function(){
			this.$emit('closeEditPop',false)
    },
    savaEdit: function(){
      var editSelect = document.getElementById('editSelect')
			var editInput = document.getElementById('editInput')
			var editDate = document.getElementById('editDate')
      var editTxt = document.getElementById('editTxt')
      var editMemberSelect = document.getElementById('editMemberSelect')
      var udp = this.createId()
      var tmpList = {
        'id': this.editLog.preMsg.id,
        'type':editSelect.value,
        'mny':editInput.value - 0,
        'stm':editTxt.value,
        'time':editDate.value,
        'clr':'#'+this.createColor(editSelect.value),
        'ioe':this.editLog.preMsg.ioe,
        'member': editMemberSelect.value
      }
      if(editInput.value == '0' || editInput.value == ''){
        alert('请输入正确金额！')
      }else if(editDate.value == ''){
        alert('请选择日期！')
      }else{
        var tmpArr = JSON.parse(this.loc.logList)
        for(var i = 0; i < tmpArr.length; i++){
          if(tmpArr[i].id == this.editLog.preMsg.id){
            tmpArr.splice(i,1,tmpList)
          }
        }
        this.loc.logList = JSON.stringify(tmpArr)
        this.loc.updateTime = udp
        this.$emit('changeDetail',this.createId())
        this.axios.post(
          'editLog',{
            'id': this.editLog.preMsg.id,
            'log': tmpList,
            'updateTime':upd
          }
        )
      }
    }
  }
}
</script>

<style>
  .titleBar {
    width: 100%;
    height: 40px;
    text-align: center;
    color: white;
    border-bottom: 2px solid white;
    background-color: transparent;
    margin-bottom: 10px;
    line-height: 40px;
    font-size: 14px;
  }
</style>