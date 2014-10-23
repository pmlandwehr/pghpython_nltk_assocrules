from collections import Counter
from numpy import arange


def loadDataSet():
    return [[1, 2, 3, 4, 6], [2, 3, 4, 5, 6], [1, 2, 3, 5, 6], [1, 2, 4, 5, 6]]


def createC1(dataSet):
    c_1 = set()
    for transaction in dataSet:
        for item in transaction:
            c_1.add(item)
    c_1 = list(list(item) for item in c_1)
    c_1.sort()
    # use frozenset so we can use it as a key in the dict
    return [frozenset(x) for x in c_1]


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
    ret_list = []
    len_lk = len(Lk)
    for i in arange(len_lk):
        l_1 = list(Lk[i])[:k-2]
        l_1.sort()
        for j in arange(i+1, len_lk):
            l_2 = list(Lk[j])[:k-2]
            l_2.sort()
            # print("L1:", L1)
            # print("L2:", L2)
            # compare the first items to avoid duplicate
            # if first k-2 elements are equal, namely, besides the last item,
            # all the items of the two sets are the same!
            if l_1 == l_2:
                ret_list.append(Lk[i] | Lk[j])  # set union
    return ret_list


def apriori(dataSet, minSupport=0.5):
    c_1 = createC1(dataSet)
    d = [set(x) for x in dataSet]
    l_1, support_data = scanD(d, c_1, minSupport)
    l = [l_1]
    k = 2
    while len(l[k-2]) > 0:
        c_k = aprioriGen(l[k-2], k)
        l_k, sup_k = scanD(d, c_k, minSupport)  # scan DB to get Lk
        support_data.update(sup_k)
        l.append(l_k)
        k += 1
    return l, support_data


def generateRules(L, supportData, minConf=0.7):  # supportData is a dict coming from scanD
    big_rule_list = []
    for freq_set in L[1]:
        calcConf(freq_set, [frozenset([item]) for item in freq_set],
                 supportData, big_rule_list, minConf)

    for i in arange(2, len(L)):  # only get the sets with two or more items
        for freq_set in L[i]:
            rulesFromConseq(freq_set, [frozenset([item]) for item in freq_set],
                            supportData, big_rule_list, minConf)
    return big_rule_list


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    pruned_h = []  # create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]  # calc confidence
        if conf >= minConf:
            brl.append((freqSet - conseq, conseq, conf))
            print('{} --> {} conf: {}'.
                  format(brl[-1][0], brl[-1][1], brl[-1][2]))
            pruned_h.append(conseq)
    return pruned_h


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    print("freqSet:", freqSet)
    
    hm_plus_1 = calcConf(freqSet, H, supportData, brl, minConf)

    m = len(hm_plus_1[0])
    print("m:", m, "Hmp1 now:", hm_plus_1)

    if len(freqSet) > (m + 1):  # try further merging
        hm_plus_1 = aprioriGen(hm_plus_1, m+1)  # create Hm+1 new candidates
    print('Hmp1:', hm_plus_1)

    hm_plus_1 = calcConf(freqSet, hm_plus_1, supportData, brl, minConf)
    print('Hmp1 after calculate:', hm_plus_1)

    if len(hm_plus_1) > 1:  # need at least two sets to merge
        rulesFromConseq(freqSet, hm_plus_1, supportData, brl, minConf)


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