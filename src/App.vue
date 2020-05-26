<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  beforeCreate(){
    var ud = '';
    if(window.localStorage.updateTime){
      ud = window.localStorage.updateTime
    }

    this.axios.get('updateTime')
    .then(res => {
      if((res.data - ud) > 0){
        this.axios.get('restore')
        .then(storeres => {
          window.localStorage.logList = storeres.data.loglist
          window.localStorage.members = storeres.data.members
          window.localStorage.items = storeres.data.types
          window.localStorage.incomes = storeres.data.incomes
          window.localStorage.updateTime = storeres.data.updateTime
        })
      }else if((res.data - ud) < 0){
        this.axios.post('rewrite', {
          'updatetime': new Date().getTime(),
          'members': JSON.parse(this.loc.members),
          'types': JSON.parse(this.loc.items),
          'incomes': JSON.parse(this.loc.incomes),
          'loglist': JSON.parse(this.loc.logList),
        })
      }
    }).catch(res=>{
      alert('您正处于离线模式！')
    })
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
html {
  height: 100%;
}
body {
  margin: 0;
  padding: 0;
  height: 100%;
}
.colorRed {
  background-color: tomato;
}
.colorYellow {
  background-color: rgb(231, 197, 0);
}
p {
  padding: 0;
  margin: 0;
}
::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>
