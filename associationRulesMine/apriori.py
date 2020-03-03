# -*- coding: utf-8 -*-
from associationRulesMine import LoadFile


def calCntForEveryComb(dataMat,reMap):
    cnt = {}
    for List in dataMat:
        n = len(List)
        for i in range(1,1<<n):
            comb = []
            for j in range(0,n):
                if((1<<j)&i):
                    comb.append(List[j])
            comb = sorted(comb)
            hashVal = hash(str(comb))
            if hashVal not in cnt:cnt[hashVal] = 1
            else:cnt[hashVal]+=1
    return cnt

def calL1(dataMat,cnt,support):
    L = []
    for itemList in dataMat:
        for item in itemList:
            if [item] not in L and cnt[hash(str([item]))] >= support:
                L.append([item])
    return L

def aprioriGen(preL):
    k = len(preL[0])
    L = []
    for i in range(0,len(preL)):
        for j in range(i+1,len(preL)):
            L1 = sorted(list(preL[i])[:k-1])
            L2 = sorted(list(preL[j])[:k-1])
            if L1 == L2:
                L.append(list(set(preL[i]).union(set(preL[j]))))
    return L

def createL(preL,cnt,support):
    L = []
    curC = aprioriGen(preL)
    for itemList in curC:
        itemList = sorted(itemList)
        if hash(str(itemList)) in cnt and cnt[hash(str(itemList))] >= support:
            L.append(itemList)
    return L

def Apriori(dataMat,cnt,support):
    Lk = calL1(dataMat,cnt,support)
    L = []
    while True:
        Lk = createL(Lk,cnt,support)
        if(len(Lk)==0):break
        L = L + Lk
    return L

def findRules(itemSet,H,cnt,conf,rules):
    prunedList = []
    for item in H:
        curConf = 1.0*cnt[hash(str(sorted(list(itemSet))))]/cnt[hash(str(sorted(list(itemSet-item))))]
        if(curConf>=conf):
            rules.append((itemSet-item,item,curConf))
            prunedList.append(item)
    return prunedList

def prunedRules(itemSet,H,cnt,conf,rules):
    k = len(H[0])
    if len(itemSet) > k:
        nextH = findRules(itemSet,H,cnt,conf,rules)
        if(len(nextH)==0): return
        nextH = [set(item) for item in aprioriGen(nextH)]
        if(len(nextH)>0) : prunedRules(itemSet,nextH,cnt,conf,rules)

def getRules(L,cnt,conf):
    rules = []
    for itemList in L:
        itemSet = set(itemList)
        H1 = [set([item]) for item in itemSet]
        if(len(itemSet)==2):findRules(itemSet,H1,cnt,conf,rules)
        else:prunedRules(itemSet,H1,cnt,conf,rules)
    return rules
def printRules(rules,reMap):
    for tul in rules:
        print("[",end="")
        n = 0
        for item in tul[0]:
            if n == 0 :
                print(reMap[item],end="")
                n = n + 1
            else:
                print(",",reMap[item],end="")
        print("] --> [",end="")
        n = 0
        for item in tul[1]:
            if n == 0:
                print(reMap[item],end="")
                n = n + 1
            else:
                print(",",reMap[item],end="")
        print("] , conf = ",tul[2])


support = 2
conf = 0.6
path = '/Users/seven7777777/QQDownload/Breakfast.csv'
dataMat,Map,reMap = LoadFile.loadFile(path)
cnt = calCntForEveryComb(dataMat,reMap)
res = Apriori(dataMat,cnt,support)
rules = getRules(res,cnt,0.6)
#printRules(rules,reMap)
print(len(res))


