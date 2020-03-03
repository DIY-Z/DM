import csv
def loadFile(path):
    dataMat=[]
    Map = {}
    reMap = {}
    L = []
    with open(path,newline='',encoding='gbk') as file:
        reader = csv.reader(file)
        n = 0 ; cnt = 0 ; j = 1
        for i in reader:
            if(n == 0):
                n = 1
                continue
            itemA = int(i[0])
            itemB = str(i[1])
            if itemA != j:
                L2 = []
                for l in L:
                    L2.append(l)
                dataMat.append(L2)
                L.clear()
                j = j + 1
            if itemB not in Map:
                Map[itemB] = cnt
                reMap[cnt] = itemB
                cnt += 1
            L.append(Map[itemB])
    return dataMat,Map,reMap