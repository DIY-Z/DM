from associationRulesMine import LoadFile
import copy
class Node:
    def __init__(self,name,count,parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.child = {}
        self.nodeLink = None

def createInitDateSet(dataMat):
    dataDic = {}
    for itemList in dataMat:
        if frozenset(itemList) not in dataDic:
            dataDic[frozenset(itemList)] = 1
        else:
            dataDic[frozenset(itemList)] += 1
    return dataDic

def updateHead(headNode,treeNode):
    while(headNode.nodeLink != None):
        headNode = headNode.nodeLink
    headNode.nodeLink = treeNode


def insertIntoTree(itemList,tree,headTable,count):
    item = itemList[0]
    if item in tree.child:
        tree.child[item].count += count
    else:
        tree.child[item] = Node(item,count,tree)
        if headTable[item][1] == None:
            headTable[item][1] = tree.child[item]
        else:
            updateHead(headTable[item][1],tree.child[item])
    if len(itemList[1:])>0:
        insertIntoTree(itemList[1:],tree.child[item],headTable,count)

def createTree(dataSet,sup):
    headTable = {}
    for itemList in dataSet:
        for item in itemList:
            headTable[item] = headTable.get(item,0) + dataSet.get(frozenset(itemList))
    #print(len(headTable))
    validKeys = []
    for key in headTable.keys():
        if(headTable[key]<sup):
            validKeys.append(key)
    for key in validKeys:
        del headTable[key]
    #print(len(headTable))

    freqItemSet = set(headTable.keys())

    if(len(freqItemSet) == 0) : return None,None

    for key in headTable.keys():
        headTable[key] = [headTable[key],None]

    root = Node('root',0,None)
    for itemDic,count in dataSet.items():
        curItemDic = {}
        for item in itemDic:
            if item in freqItemSet:
                curItemDic[item] = headTable[item][0]
        if len(curItemDic) > 0:
            sortedItems = [v[0] for v in sorted(curItemDic.items(), key=lambda x: x[1], reverse=True)]
            insertIntoTree(sortedItems,root,headTable,count)
    return root,headTable

def findParent(curNode,preFix):
    if curNode.parent != None:
        preFix.append(curNode.name)
        findParent(curNode.parent,preFix)

def findPreFix(beginItem,LinkNode):
    condBasePath = {}
    while LinkNode != None:
        preFix = []
        findParent(LinkNode,preFix)
        if len(preFix)>1:
            condBasePath[frozenset(preFix[1:])] = LinkNode.count
        LinkNode = LinkNode.nodeLink
    return condBasePath


def createConTree(FPtree,headTable,sup,preFix,freqItemList):
    #print(headTable)
    itemList = [v[0] for v in sorted(headTable.items(), key=lambda x: x[1][0])]
    for beginItem in itemList:
        newFreqSet = copy.deepcopy(preFix)
        newFreqSet.add(beginItem)
        freqItemList.append(newFreqSet)
        condBasePath = findPreFix(beginItem,headTable[beginItem][1])
        #print(condBasePath)

        conTree,conHead = createTree(condBasePath,sup)
        if conTree != None:
            createConTree(conTree,conHead,sup,newFreqSet,freqItemList)

sup = 2
path = '/Users/seven7777777/QQDownload/Breakfast.csv'
dataMat,Map,reMap = LoadFile.loadFile(path)
dataDic = createInitDateSet(dataMat)
root,headTable = createTree(dataDic,sup)
freqItemList = []
createConTree(root,headTable,sup,set([]),freqItemList)
# for itemList in freqItemList:
#     itemList = list(itemList)
# for itemList in freqItemList:
#     itemList = list(itemList)
print(freqItemList)