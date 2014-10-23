from collections import Counter
from numpy import arange


def loadDataSet():
    return [[1, 2, 3, 4, 6], [2, 3, 4, 5, 6], [1, 2, 3, 5, 6], [1, 2, 4, 5, 6]]


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if [item] not in C1:
                C1.append([item])            
    C1.sort()
    # use frozenset so we can use it as a key in the dict
    return [frozenset(x) for x in C1]


def scanD(D, Ck, minSupport):
    ss_counter = Counter()
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                ss_counter[can] += 1
    num_items = len(D)

    support_data = {key: ss_counter[key]/num_items for key in ss_counter}
    ret_list = [key for key in ss_counter if ss_counter[key]/num_items >= minSupport][::-1]

    return ret_list, support_data


def aprioriGen(Lk, k):  # creates Ck
    retList = []
    lenLk = len(Lk)
    for i in arange(lenLk):
        l_1 = list(Lk[i])[:k-2]
        l_1.sort()
        for j in arange(i+1, lenLk):
            l_2 = list(Lk[j])[:k-2]
            l_2.sort()
            # print("L1:", L1)
            # print("L2:", L2)
            # compare the first items to avoid duplicate
            # if first k-2 elements are equal, namely, besides the last item,
            # all the items of the two sets are the same!
            if l_1 == l_2:
                retList.append(Lk[i] | Lk[j])  # set union
    return retList


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = [set(x) for x in dataSet]
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)  # scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.7):  # supportData is a dict coming from scanD
    bigRuleList = []
    for i in arange(1, len(L)):  # only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList         


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []  # create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]  # calc confidence
        if conf >= minConf: 
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    print("freqSet:", freqSet)
    
    Hmp1 = calcConf(freqSet, H, supportData, brl, minConf)
    
    m = len(Hmp1[0])
    print("m:", m, "Hmp1 now:", Hmp1)
    if len(freqSet) > (m + 1):  # try further merging
        Hmp1 = aprioriGen(Hmp1, m+1)  # create Hm+1 new candidates
    print('Hmp1:', Hmp1)
    Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
    print('Hmp1 after calculate:', Hmp1)
    if len(Hmp1) > 1:  # need at least two sets to merge
        rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


def main():
    """
    dataset = loadDataSet()
    C1 = createC1(dataset)
    retList,supportData=scanD(dataset, C1,0.5)
    print('C1:', C1)
    print('retList:', retList)
    print('supportData:', supportData)
    """
    dataSet = loadDataSet()
    L, supportData = apriori(dataSet, 0.7)
    brl = generateRules(L, supportData, 0.7)
    print('brl:', brl)


if __name__ == "__main__":
    main()