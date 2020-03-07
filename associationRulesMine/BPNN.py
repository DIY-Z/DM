import numpy as np
import random as rd
def loadData(): #读取数据集
    inputData = [[0,0.5,0.5]]
    ouputData = [[0]]
    data = []
    data.append(inputData)
    data.append(ouputData)
    return data,len(inputData)

def sigmoid(x):#激活函数
    return 1.0/(1+np.exp(-x))

def createNetwork(layer):#创建神经网络
    sum = 1
    w = {}
    b = {}
    for i in range(len(layer)-1):#对于每一层节点和它的下一层节点
        sum += layer[i] #向后一层前进
        for j in range(layer[i+1]):
            for k in range(layer[i]):
                w[(sum-layer[i]+k,sum+j)] = rd.uniform(-5,5)
                #sum-layer[i]+k是指左边层的节点
                #sum+j是指右边层的节点
                #相邻的两层之间连一条边
            b[sum+j] = rd.uniform(-5,5)
            #隐藏层和输出层节点的阀值

    return w,b



def forward(w,b,Out,layer):#前向传播
    In = {}
    sum = 1
    for i in range(len(layer)-1):
        sum += layer[i]
        for j in range(layer[i+1]):
            In[sum+j] = b[sum+j]
            for k in range(layer[i]):
                #节点输入
                In[sum+j] += w[(sum-layer[i]+k,sum+j)]*Out[sum-layer[i]+k]
            #节点输出
            Out[sum+j] = sigmoid(In[sum+j])



def backward(w,b,Out,target,layer,l):#后向传播

    Err = {}
    sum = 1

    for i in range(len(layer)-1):
        sum += layer[i]
    for i in range(layer[-1]):
        #计算输出层的误差
        Err[sum+i] = (target[i]-Out[sum+i])*Out[sum+i]*(1-Out[sum+i])
    for i in range(len(layer)-2,-1,-1):
        for j in range(layer[i+1]):
            for k in range(layer[i]):
                ln = sum-layer[i]+k
                rn = sum + j
                #计算隐藏层的误差，由于这里输出层就一个节点，可以这样简写
                Err[ln] = Err[rn]*w[(ln,rn)]*Out[ln]*(1-Out[ln])
                w[(ln,rn)] += l*Err[rn]*Out[ln]
            b[rn] += l*Err[rn]
        sum -= layer[i]

def solve(w,b,data,count,layer,l):#对数据的一次训练
    for i in range(count):
        Out = {}
        target = {}
        for j in range(layer[0]):
            Out[j+1] = data[0][i][j]
        for j in range(layer[-1]):
            target[j] = data[1][i][j]
        forward(w,b,Out,layer)
        backward(w,b,Out,target,layer,l)



l = 0.9
data,count=loadData()
layer = [3,4,1]
w,b=createNetwork(layer)
for i in range(1):
    solve(w,b,data,count,layer,l)

