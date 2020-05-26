from flask import Flask, jsonify, request, json
from flask_cors import CORS

import redisDB

app = Flask(__name__)
# 解决跨域问题
CORS(app,resources=r'/*') 


# 添加类型
@app.route('/addNewType', methods=['GET', 'POST'])
def addType():
    data = json.loads(request.get_data().decode('utf-8'))
    redisDB.setString('updateTime',data.get('updatetime'))
    redisDB.addType(data.get('name'),*data.get('data'))
    return data.get('name')+'添加成功'

# 删除某一记录
@app.route('/deleteLog', methods=['GET', 'POST'])
def deleteLog():
    data = json.loads(request.get_data().decode('utf-8'))
    redisDB.setString('updateTime',data.get('updateTime'))
    redisDB.deleteData(data.get('id'))
    redisDB.deleteType('idList',data.get('id'))
    return '删除成功'

# 删除类型及其对应的记录
@app.route('/deleteType', methods=['GET', 'POST'])
def deleteType():
    data = json.loads(request.get_data().decode('utf-8'))
    idList = data.get('idList')
    redisDB.deleteType(data.get('name'), data.get('value'))
    redisDB.setString('updateTime',data.get('updateTime'))
    for item in idList:
        redisDB.deleteData(item)
        redisDB.deleteType('idList',item)
    return '删除结束'

# 添加新记录
@app.route('/addNewLog', methods=['GET', 'POST'])
def addNewLog():
    data = json.loads(request.get_data().decode('utf-8'))
    redisDB.setString('updateTime',data.get('id'))
    redisDB.addType('idList',data.get('id'))
    redisDB.addNewLog(data.get('id'),data.get('log'))
    return '新纪录添加成功'

# 修改记录
@app.route('/editLog', methods=['GET', 'POST'])
def editLog():
    data = json.loads(request.get_data().decode('utf-8'))
    redisDB.setString('updateTime',data.get('updateTime'))
    redisDB.addNewLog(data.get('id'),data.get('log'))
    return '编辑完成'

# 获取对应类型
@app.route('/getAllType', methods=['GET', 'POST'])
def getAllType():
    data = request.get_data().decode('utf-8')
    tmp = []
    for item in redisDB.getAllType(data):
        tmp.append(item)
    return jsonify(tmp)

# 重写数据库
@app.route('/rewrite', methods=['GET', 'POST'])
def rewrite():
    redisDB.clearAll()
    data = json.loads(request.get_data().decode('utf-8'))
    updateTime = data.get('updatetime')
    members = data.get('members')
    types = data.get('types')
    incomes = data.get('incomes')
    loglist = data.get('loglist')
    redisDB.setString('updateTime',updateTime)
    redisDB.addType('members',*members)
    redisDB.addType('types',*types)
    redisDB.addType('incomes',*incomes)
    for item in loglist:
        redisDB.addType('idList',item['id'])
        redisDB.addNewLog(item['id'],item)
    return ''

# 前端重写
@app.route('/restore', methods=['GET', 'POST'])
def restore():
    loglist = []
    for item in redisDB.getAllType('idList'):
        loglist.append(redisDB.getLog(item))
    tmp = {
        'members': redisDB.getAllType('members'),
        'incomes': redisDB.getAllType('incomes'),
        'types': redisDB.getAllType('types'),
        'updateTime': redisDB.getString('updateTime'),
        'loglist': loglist
    }
    return tmp

# 保存数据
@app.route('/saveAll', methods=['GET', 'POST'])
def saveAll():
    redisDB.saveAll()



if __name__ == '__main__':
    app.run()