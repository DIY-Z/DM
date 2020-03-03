class Node:
    def __init__(self,a,b,support,conf):
        self.a = a
        self.b = b
        self.support = support
        self.conf = conf
def getRelationRule(cnt,L,conf):
    rules = []
    for itemList in L:
        n = len(itemList)
        itemList.sort()
        for i in range(1,1<<n):
            a = []
            b = []
            for j in range(0,n):
                if((1<<j)&i):a.append(itemList[j])
                else:b.append(itemList[j])
            if(len(b)==0):continue
            a.sort()
            b.sort()
            abSup = cnt[hash(str(itemList))]
            aSup = cnt[hash(str(a))]
            if 1.0*abSup/aSup>= conf:
                rules.append(Node(a,b,abSup,1.0*abSup/aSup))
    return rules