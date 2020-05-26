import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
r = redis.Redis(connection_pool=pool)


# STRING
# set(name,value)基本操作
# setex(name,value,time)经过time时长后value过期，单位秒
# psetex(name,value,time)经过time时长后value过期，单位毫秒
# set(name,value,nx=false,xx=false)nx只有name不存在时执行，xx只有name存在时执行
# 也可以用setnx(name,value)和setxx(name,value)
# 批量设置mset(name1=value1,name2=value2)或mset({name1=value1,name2=value2})
# 批量获取mget(*args)arg为name
# getset(name,value)设置name值为value并返回原value值
# setrange(name,offset,value)修改字符串指定位置开始的对应value长度的值
# 若添加后比原value长则往后继续添加剩余字符
# getrange(name,start,end)获取指定范围内的字符串
# setbit(name,offset,value)将value对应的ascii转换成二进制后的offset位进行修改，value只能是1和0
# getbit(name,offset)获取name的二进制中offset位置的值
# bitcount(name,start=?,end=?)获取start到end之间的字符的二进制个数
# strlen(name)字符串长度（汉字算三个长度）
# incr(self,name,amount=1),自增name对应值，不存在时自动创建，amount为每次自增的数值
# incrbyfloat(self,name,amount=0.1)同上，但自增数位浮点型
# decr(self,name,amount)自减
# append(name,value)在name的值后添加value
def setString(name,vlue):
    r.set(name,vlue)

def getString(dat):
    if r.get(dat):
        return r.get(dat)
    else:
        return ''


# HASH
# 可用来存储类似{'a':''，'b':''}形式数据
# hset(name,key,value)为设置某个key名下的某项属性的值
# hmset(name,mapping)可以理解为存储一个名为name的mapping
# mapping格式:{'a':'a1','b':'b1'}
# hget(name,key)获取name中键为key的value
# hgetall(name)获取所有键值对
# hmget(name,*args)获取多个key对应的value，arg代表key
# hlen(name)获取name的键值对个数
# hkeys(name)获取name的所有key值
# hvals(name)获取name的所有value值
# hexists(name,key)判断name中是否存在该key
# hdel(name,*keys)删除key对应键值对
# hincrby(name,key,amount=1)key自增，不存在时创建key=amount
# hincrbyfloat(name,key,amount=1.0)功能同上，数据类型为浮点型
def addNewLog(name,mapping):
    r.hmset(name,mapping)

def getLog(name):
    if r.hgetall(name):
        return r.hgetall(name)
    else:
        return ''


# LIST
# list -> lpush/rpush(name,values)，用以存储[1,2,3,4]类型数据
# 如果需要判定必须已经存在该名称才能进行存储则使用lpushx/rpushx
# 插入操作用linsert(name,where,refvalue,value)
# where参数有两种before和after，决定新插入的值是往refvalue（参考值）之前还是之后插入value
# 根据索引修改值用lset(name,index,value)
# 删除list中的指定数据用lrem（name,value,num）
# 因为list本身存储的值是可以重复的，所有num指的是删除是这个value数据的个数
# num=0，删除所有的；num=n,从前往后删除n个；num=-n，从后往前删除n个
# 移除第一个或者最后一个元素lpop/rpop(name)
# 获取名称为name索引为index的list的值lindex(name,index)
# 截取某几个数据lrange(name,start,end)end可以为负值，负值时反向截取
# 去除一个list的最后一个元素放进另一个list：rpoplpush(src,dst)src为被截取list，dst为被添加list
# brpoplpush(src,dst,timeout=0)功能同上，增加没元素后的阻塞时间，0代表一直阻塞
# blpop(*args,timeout)同时从左到右逐个删除多个列表内的元素，brpop为从右到左；keys->[list1,list2...]，arg为列表名


# SET
# set与list类似，但set中的存储的内容不可重复
# sadd(name,values)给name对应的集合中添加元素
# smembers(name)获取name的所有成员
# scard(name)获取name成员个数
# sdiff(*args)获取在第一个集合但不在其他集合中的元素的集合，arg为集合name
# sdiffstore(dest, *args)，相当于把sdiff获取的value存进dest中，dest为另一个集合，arg代表name
# sinter(*args)多个set中的相同value的集合
# sinterstore(dest,*args)将sinter获取到的value存进dest
# sismember(name, value)判断name中是否存在valuee
# smove(src, dest, value)将src集合中的value转移进dest
# spop(name)随机删除一个元素并返回该元素
# srem(name, values)删除指定value，可为多个
# srandmember(name, numbers)从name中随机获取numbers个value
# sunion(*args)获取多个set的并集
# sunionstore(dest,*args)将sunion获取的值存进dest
def addType(name,*dats):
    for dat in dats:
        r.sadd(name,dat)

def deleteType(name, value):
    r.srem(name, value)

def getAllType(name):
    if r.smembers(name):
        return r.smembers(name)
    else:
        return ''


# 有序集合
# 在集合的基础上，为每元素排序，元素的排序需要根据另外一个值来进行比较
# 所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序
# zadd(name, *args, **kwargs)在name对应的有序集合中添加元素,zadd(name1,v1,1,v2,2)或zadd(name1,v1=1,v2=2)
# zcard(name)获取元素的数量
# zcount(name, min, max)获取分数介于min和max之间的个数
# zincrby(name, value, amount)自增value
# zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)
# 按照索引获取从start到endname的元素
# desc为排序方式默认从小到大
# withscores是否获取score
# score_cast_func 分数的显示格式
# zrevrange(name, start, end, withscores=False, score_cast_func=float)
# 和zrange一样，但默认排序为从大到小
# zrank(name, value)获取value的排行位置，小->大，起始为0
# zrevrank(name, value)获取value的排行位置，大->小
# zscore(name, value)value对应score
# zrem(name, values)删除name中一个或多个value
# zremrangebyrank(name, min, max)删除排行值介于min和max之间的value
# zremrangebyscore(name, min, max)删除score介于min和max之间的value
# zinterstore(dest, keys, aggregate=None)取keys交集放入dest
# 有相同值但score不同时按aggregate操作，sun min max
# zunionstore(dest, keys, aggregate=None)并集


# 其他操作
# delete(*names)根据name删除redis中的任意数据类型
# exists(name)检测redis的name是否存在
# keys(pattern='*')根据* ？等通配符匹配获取redis的name
# expire(name ,time)为某个name设置超时时间
# rename(src, dst)重命名
# move(name, db))将redis的某个值移动到指定的db下
# randomkey()随机获取一个redis的name（不删除）
# type(name)获取name对应值的类型
# scan(cursor=0, match=None, count=None)查看所有元素
# scan_iter(match=None, count=None)查看所有元素--迭代器
# dbsize()当前redis包含多少条数据
# save()将数据写进磁盘
# flushdb()清空当前redis中的所有数据
def clearAll():
    r.flushdb()

def deleteData(name):
    r.delete(name)

def saveAll():
    r.save()