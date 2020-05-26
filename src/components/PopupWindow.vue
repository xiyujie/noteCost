<template>
  <div class="masking" v-if="ifShow.show">
    <div class="popupWindow">
      <div class="clsBtn" @click="closePop"></div>
      请在下方输入您想添加的{{ifShow.type}}名称
      <input id="typeInput" type="text">
      <button class="closeBtn" @click = "change()">完成</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'popupWindow',
  props: ['ifShow'],
  data (){
    return {

    }
  },
  methods: {
    closePop() {
      this.$emit('cgShow',false)
    },
    change() {
      var val = document.getElementById('typeInput').value
      var attr = []
      if(this.ifShow.type == '类型'){
        if(this.ifShow.ioe == '支出'){
          attr = JSON.parse(this.loc.items)
        }else if(this.ifShow.ioe == '收入'){
          attr = JSON.parse(this.loc.incomes)
        }
      }else if(this.ifShow.type == '成员'){
        if(this.loc.members && this.loc.members != '[]'){
          attr = JSON.parse(this.loc.members)
        }
      }

      if(val != ''){
        var ifAddType = true
        if(confirm('您确定要添加“'+ val +'”到您的帐本中吗？')){
          var upd = this.createId()
          for(var i = 0; i < attr.length; i++){
            if(attr[i] == val){
              alert('已存在该'+ this.ifShow.type +'名称，请重新添加！')
              ifAddType = false
              break;
            }
          }
          if(ifAddType == true){
            attr.push(val)
            if(this.ifShow.type == '类型'){
              if(this.ifShow.ioe == '支出'){
                this.loc.items = JSON.stringify(attr)
                this.$addTypeToDB('types', val, upd)
              }else if(this.ifShow.ioe == '收入'){
                this.loc.incomes = JSON.stringify(attr)
                this.$addTypeToDB('incomes', val, upd)
              }
            }else if (this.ifShow.type == '成员'){
              this.loc.members = JSON.stringify(attr)
                this.$addTypeToDB('members', val, upd)
            }
            this.$emit('cgShow',false)
            this.$emit('sendMsg',attr)
          } 
        }else{
          this.$emit('cgShow',true)
        }
      }
      this.$emit('cgShow',false)
    }
  }
}
</script>

<style>
  .popupWindow{
    width: 300px;
    height: 200px;
    position: absolute;
    left: calc(50% - 150px);
    top: calc(40% - 100px);
    background-color: rgba(49, 53, 56, 0.8);
    border-radius: 10px;
    padding-top: 40px;
    box-sizing: border-box;
    text-align: center;
    color: white;
    font-size: 14px;
    z-index: 999;
  }
  .clsBtn {
    position: absolute;
    top: 10px;
    right: 10px;
    height: 15px;
    width: 15px;
    border-radius: 10px;
    background: red;
    opacity: 0.8;
  }
  .closeBtn {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 40px;
    left: 0;
    background-color: transparent;
    border: 0;
    border-top: 2px solid white;
    outline: 0;
    color: white;
    font-size: 16px;
    letter-spacing: 5px;
  }
  #typeInput {
    width: 50%;
    margin-top: 20px;
    height: 25px;
    border: 2px solid whitesmoke;
    border-radius: 5px;
    outline: 0;
    background-color: transparent;
    text-align: center;
    color: white;
  }
</style>