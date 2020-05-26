// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:5000/'

Vue.config.productionTip = false
Vue.prototype.loc = window.localStorage
Vue.prototype.axios = axios
Vue.prototype.createColor = function (clr){
  var tmp = ""
  // 将获取到的字符串先转成unicode码再转成16位数字
  for(var i = 0; i < clr.length; i++){
    tmp += clr[i].charCodeAt().toString(16)
  }
  // 判断转化为16位后字符串长度
  if(tmp.length > 6){
    // 长度大于6时取后6位作为颜色值
    tmp = tmp.substr(0,6)
  }else if(tmp.length > 3){
    // 长度小于6大于3时取后3位作为颜色值
    tmp = tmp.substr(0,3)
  }else{
    // 若长度小于三则设置默认色
    tmp = 'aquamarine'
  }
  return tmp
}
Vue.prototype.createId = function(){
  var date = new Date()
  var id = date.getTime()
  return id
}
Vue.prototype.screeningData = function(list,choseType,idx){
  var tmp = []
  for(var i = 0; i < list.length; i++){
    if(list[i].time.split('-')[idx] == choseType){
      tmp.push(list[i])
    }
  }
  return tmp
}
Vue.prototype.deleteTypeWithData = function(type,dat,typelist){
  var upd = new Date().getTime()
  var deledList = []
  var idList = []
  if(this.loc.logList && this.loc.logList != '[]'){
    var allData = JSON.parse(this.loc.logList)
    for(let i = 0; i < allData.length; i++){
      if(allData[i][type] != dat){
        deledList.push(allData[i])
        idList.push(allData[i]['id'])
      }
    }
    axios.post(
      'deleteType',
      {
        'name': typelist,
        'value': dat,
        'updateTime': upd,
        'idList': idList
      }
    )
    allData = deledList
    this.types.mb = '总计'
    this.loc.logList = JSON.stringify(allData)
    this.loc.updateTime = upd
  }
}
Vue.prototype.$addTypeToDB = function(name, data, upd){
  axios.post(
    'addNewType',
    {
      'name':name,
      'data':data,
      'updatetime':upd
    }
  )
}
Vue.prototype.$compare = (property) => {
  return function(a,b){
      var value1 = a[property];
      var value2 = b[property];
      return value1 - value2;
   }
}


window.onbeforeunload = function(){
  axios.get('saveAll')
}


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})