import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


# 标称属性，给出每个可能取值的频数
# 生成字典，统计出现的次数
def nominalHandle(data,attrname):
    tmp={}
    for i in data[attrname]:
        if pd.isnull(i):
            continue
        if i in tmp:
            tmp[i]+=1
        else:
            tmp[i]=1
    return tmp

# 标称属性， 使用直方图检查数据分布及离群点
def nominalPlay(dictData,attrname,threshold):
    #由于数据量庞大，只绘制超过阈值部分的数据
    keys=[]
    values=[]
    for k,v in dictData.items():
        if v>threshold:
            keys.append(k)
            values.append(v)
    plt.xlabel(attrname)
    plt.ylabel("number")
    plt.bar(keys,values, color='g')
    plt.show()

# 标称属性，给出每个可能取值的频数
# 打印字典
def dictPlay(dictData):
    for k,v in dictData.items():
        print(k,":",v)


# 数值属性，给出5数概括及缺失值的个数
def numericHandle(data,attrname,flag):
    tmp=[]
    for i in data[attrname]:
        if pd.isnull(i):
            flag+=1
            continue
        try:
            tmp.append(int(i))
        except ValueError:
            continue
    tmp.sort()
    lenth=len(tmp)
    minimum=min(tmp)
    q1=tmp[int(lenth/4)]
    mid=tmp[int(lenth/2)]
    q3=tmp[3*int(lenth/4)]
    maximum=max(tmp)
    print("这是",attrname,"的5数概括：")
    print("Min:",minimum)
    print("Q1:",q1)
    print("Mid:",mid)
    print("Q3:",q3)
    print("MaX:",maximum)
    print("--------")
    #print("缺失的个数：",flag)
    return tmp,flag

#  数值属性，使用盒图等检查数据分布及离群点
def boxPlay(data,attr):
    plt.title('BoxPlot of '+attr,fontsize=36,verticalalignment='bottom')
    plt.xlabel(attr)
    plt.ylabel("value")
    plt.boxplot(data,sym="",whis=(0,100))
    plt.show()

# 找到最高频率的值
def findHighest(data):
    ans={}
    for i in data:
        if i not in ans.keys():
            ans[i]=1
        else:
            ans[i]+=1
    num=0
    for k,v in ans.items():
        if v>num:
            num=v
            keys=k
    return keys

# 用最高频率值来填补缺失值
def fillWithHighest(data,attrname,num):
    tmp=[]
    for i in data[attrname]:
        if pd.isnull(i):
            tmp.append(num)
            continue
        try:
            tmp.append(int(i))
        except ValueError:
            continue
    #print(attrname,"出现次数最高频率的是：",num)
    return tmp

# 二分查找指定元素在有序数组中的位置
def rank(array,value):
    left = 0
    high = len(array) - 1
    while left <= high:
        mid = int((left + high) / 2)
        if array[mid] == value:
            return mid
        if array[mid] < value:
            left = mid + 1
        else:
            high = mid - 1
    return left

# 通过属性的相关关系来填补缺失值
def fillWithCorrelation(data,attrName1,attrName2):
    filled=[]   #filled不存在缺失部分
    missed=[]   #missed存在缺失部分
    res=[]
    for i in data[attrName1]:
        filled.append(i)
    for i in data[attrName2]:
        res.append(i)
        if not pd.isnull(i):
            missed.append(i)    
    filled.sort()
    missed.sort()
    res.sort()
    for i in range(len(res)):
        if pd.isnull(res[i]):
            # r是缺失的位置（在attrName1中所在位置的百分比）
            r = rank(filled,data.iloc[i][attrName1])/len(filled)
            res[i]=missed[int(r*len(missed))]
    return res

# 得到缺失和未缺失的数组
def partition(data,attrName1,attrName2):
    # filled是没有缺失部分的，missed是有缺失部分的
    filled = []
    missed = []
    for i in data[attrName1]:
        filled.append(i)
    for i in data[attrName2]:
        if not pd.isnull(i):
            missed.append(i)
    return filled, missed

# 通过数据对象之间的相似性来填补缺失值
def fillWithEuclidean_Distancetance(data,y, n, attrName):
    # n有缺失，但是不含空白;y，完整
    res=[] #res有缺失，含有空白
    for i in data[attrName]:
        if pd.isnull(i):
            i=0
        res.append(i)
    feature_1=np.array(y)
    feature_2=np.array(res)
    dist=np.linalg.norm(feature_1-feature_2)
    for i in range(len(res)):
        if res[i]==0:
            res[i]=res[(i+int(dist))%len(res)]
    #print("欧式距离为:",dist)
    return res

# 对比可视化 
def ViewAll(n1,n2,n3,n4,n,attr1,attr2,attr3,attr4,attr):
    data={attr1:n1,attr2:n2,attr3:n3,attr4:n4,attr:n}
    box1,box2,box3,box4,box=data[attr1],data[attr2],data[attr3],data[attr4],data[attr]
    #plt.subplot()
    labels = attr1,attr2,attr3,attr4,attr
    plt.boxplot([box1, box2,box3,box4,box],labels=labels,whis=(0,100))
    plt.show()

#标称属性：STREET NAME,STREET TYPE
#数值属性：PROPERTY GROUP，Community Areas，

data=pd.read_csv('E:/3rdDataMining/building-violations.csv')
dataName=['STREET NAME','STREET TYPE','PROPERTY GROUP','Community Areas']
# 3.1 数据可视化和摘要
# 标称属性，给出每个可能取值的频数，使用直方图检查数据分布及离群点
STREET_NAME=nominalHandle(data,'STREET NAME')
STREET_TYPE=nominalHandle(data,'STREET TYPE')

nominalPlay(STREET_NAME,'STREET NAME',8000)
nominalPlay(STREET_TYPE,'STREET TYPE',1000)

# 打印每个属性的各个值的频数。
# 因数据量太大。若需要显示，将下面六代码取消注释即可
# dictPlay(STREET_NAME)
# dictPlay(STREET_TYPE)


# 数值属性，给出5数概括及缺失值的个数，使用盒图等检查数据分布及离群点
PROPERTY_GROUP,PROPERTY_GROUPFlag=numericHandle(data,'PROPERTY GROUP',0)
Community_Areas,Community_AreasFlag=numericHandle(data,'Community Areas',0)
boxPlay(PROPERTY_GROUP,'PROPERTY GROUP')
boxPlay(Community_Areas,'Community Areas')


# 3.2 数据缺失的处理
# 经检验，PROPERTY_GROUP没有缺失，故对于数值属性，只对Community_Areas进行操作

# (1)将缺失部分剔除
# 在前面统计缺失个数的过程中，已经将缺失部分去除，上述的PROPERTY_GROUP和Community_Areas为经过删除缺失部分操作后的列表。
newCommunity_Areas1=Community_Areas

# (2)用最高频率值来填补缺失值
num=findHighest(Community_Areas)
newCommunity_Areas2=fillWithHighest(data,"Community Areas",num)

# (3)通过属性的相关关系来填补缺失值
arrayWith, arrayWithout = partition(data,'PROPERTY GROUP','Community Areas')
newCommunity_Areas3=fillWithEuclidean_Distancetance(data,arrayWith, arrayWithout,"Community Areas")

# (4)通过数据对象之间的相似性来填补缺失值
newCommunity_Areas4=fillWithCorrelation(data,'PROPERTY GROUP','Community Areas')

# 前后对比可视化
print("前后对比可视化，function1~4对应4种处理方法，第五个为原始数据，作为对比")
ViewAll(newCommunity_Areas1,newCommunity_Areas2,newCommunity_Areas3,newCommunity_Areas4,Community_Areas,"function1","function2","function3","function4","raw")

