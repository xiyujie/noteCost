<template>
  <div class="masking" v-show="ifAddShow.addShow">
    <div class="AddNewLog">
      <div class="clsBtn" @click="closePop"></div>
      <div class="titleBar">添加</div>
      <div>
        <p class="addTitle">请选择要添加的类型:</p>
        <select class="typeSelect" id="typeSelect">
          <option v-if="theType.opShow" value=""></option>
          <option v-for="type in theType.types" v-bind:key="type" :value="type" >
            {{type}}
          </option>
        </select>
      </div>
      <div>
        <p class="addTitle">所属成员:</p>
        <select class="typeSelect" id="mbSelect">
          <option v-for="member in members" :key=member :value=member >
            {{member}}
          </option>
        </select>
      </div>
      <div>
        <p class="addTitle">请输入{{ifAddShow.addIoe}}金额:</p>
        <input type="number" class="addInput" id="addInput" min="0" value = 0 />
      </div>
      <div>
        <p class="addTitle">备注:</p>
        <textarea class="addTxt" id="addTxt" cols="25" rows="5">无</textarea>
      </div>
      <div>
        <p class="addTitle">{{ifAddShow.addIoe}}时间:</p>
        <input class="addDate" id="addDate" type="date">
      </div>
      <button class="closeBtn" @click = "addLog()">完成</button>
    </div>
  </div>
</template>

<script>
export default {
	name: 'AddNewLog',
	props:[
		'ifAddShow'
	],
	data() {
		return {

		}
	},
  computed: {
    theType: function(){
      var theType = {}
      if(this.ifAddShow.addType == '总计'){
        theType.opShow = true
        if(this.ifAddShow.addIoe == '支出'){
          theType.types = JSON.parse(this.loc.items)
        }else if(this.ifAddShow.addIoe == '收入'){
          theType.types = JSON.parse(this.loc.incomes)
        }
      }else{
        theType.opShow = false
        theType.types = [this.ifAddShow.addType]
      }
      return theType
    },
    members(){
      var dat = this.ifAddShow
      var members = []
      if(this.loc.members && this.loc.members != '[]'){
        members = JSON.parse(this.loc.members)
      }
      if(dat.addMemb != '总计'){
        for(let i = 0; i < members.length; i++){
          if(members[i] == dat.addMemb){
            members.splice(i,1)
            members.unshift(dat.addMemb)
          }
        }
      }
      return members
    }
  },
  mounted: function (){
		var date = new Date()
		var year = date.getFullYear()
		var month = date.getMonth() + 1
		var day = date.getDate()
		if(month < 10){
			month = '0'+ month.toString()
		}
		if(day < 10){
			day = '0'+ day.toString()
    }
    var preDate = year+'-'+month+'-'+day
    var addDate = document.getElementById('addDate')
    addDate.value = preDate
  },
	methods: {
		closePop: function(){
      document.getElementById('addInput').value = 0
      document.getElementById('addTxt').value = '无'
			this.$emit('closeAddPop',false)
    },
		addLog: function(){
      var typeSelect = document.getElementById('typeSelect')
      var mbSelect = document.getElementById('mbSelect')
			var addInput = document.getElementById('addInput')
			var addDate = document.getElementById('addDate')
			var addTxt = document.getElementById('addTxt')
			if(typeSelect.value == ''){
        alert('请先选择一种支出类型!')
      }else if(addInput.value == '' || addInput.value == 0){
        alert('请输入支出金额!')
      }else if(addDate.value == ''){
        alert('请选择支出时间!')
      }else if(mbSelect.value == ''){
        alert('请选择所属成员!')
      }else{
        var idt = this.createId()
        var tmpList = {
          'id': idt,
          'type':typeSelect.value,
          'mny':addInput.value - 0,
          'stm':addTxt.value,
          'time':addDate.value,
          'clr':'#'+this.createColor(typeSelect.value),
          'ioe':this.ifAddShow.addIoe,
          'member': mbSelect.value
          }
        var tmpArr = []
				if(this.loc.logList && this.loc.logList != '[]'){
          tmpArr = JSON.parse(this.loc.logList)
				}
				tmpArr.push(tmpList)
        this.loc.logList = JSON.stringify(tmpArr)
        this.loc.updateTime = idt
				this.$emit('changeData',idt)
				this.$emit('closeAddPop',false)
        addInput.value = 0
        addTxt.value = '无'
        this.axios.post('addNewLog',{
          'id': idt,
          'log': tmpList
        })
			}
		}
	}
}
</script>

<style>
  .masking {
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4);
    top: 0;
    left: 0;
    position: absolute;
    z-index: 998;
  }
  .AddNewLog {
    width: 250px;
    height: auto;
    position: absolute;
    left: calc(50% - 125px);
    top: calc(30% - 100px);
    background-color: rgba(49, 53, 56, 0.8);
    border-radius: 10px;
    padding-bottom: 55px;
    box-sizing: border-box;
    text-align: center;
    color: white;
    font-size: 18px;
  }
  .typeSelect {
    background-color: rgba(255, 255, 255, 0.7);
    border: 1px solid white;
    border-radius: 5px;
    outline: 0;
    margin: 10px;
    width: 100px;
    text-align: center;
  }
  .addTitle {
    margin-bottom: 5px;
  }
  .addInput {
    background-color: rgba(255, 255, 255, 0.7);
    outline: 0;
    border: 0;
    border-radius: 5px;
    width: 100px;
    margin: 5px;
    text-align: center;
    color: crimson;
  }
  .addTxt {
    padding: 10px 15px;
    box-sizing: border-box;
    border: 1px solid #333aaa;
    border-radius: 5px;
    outline: 0;
    background-color: rgba(255, 255, 255, 0.7);
  }
  .addDate {
    width: fit-content;
    background-color: rgba(255, 255, 255, 0.7);
    border: 0;
    outline: 0;
    border-radius: 5px;
    text-align: center;
    margin-top: 5px;
  }
</style>