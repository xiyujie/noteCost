<template>
<div id="IncomeOrExpenditure">
  <button style="color:white" class="ioeChose" @click="changeIoe('支出')">
    支出
  </button>
  <button class="ioeChose" @click="changeIoe('收入')">
    收入
  </button>
</div>
</template>

<script>
export default {
  name: 'IncomeOrExpenditure',
  data(){
    return {
      ioe: '支出'
    }
  },
  methods: {
    changeIoe(dat){
      this.ioe = dat
      var ioef = document.getElementById('IncomeOrExpenditure')
      if(dat == '支出'){
        ioef.children[0].style.color = 'white'
        ioef.children[1].style.color = 'rgb(173, 173, 173)'
      }else{
        ioef.children[0].style.color = 'rgb(173, 173, 173)'
        ioef.children[1].style.color = 'white'
      }
      this.$emit('changeIoe',dat)
    }
  }
}
</script>

<style>
  #IncomeOrExpenditure {
    width: 100%;
    height: 50px;
    background-color: rgb(49, 53, 56);
    display: flex;
  }
  .ioeChose {
    width: 50%;
    height: 100%;
    color: rgb(173, 173, 173);
    text-align: center;
    line-height: 50px;
    border: 0;
    outline: 0;
    background: radial-gradient(rgb(83, 87, 88), transparent);
  }
</style>