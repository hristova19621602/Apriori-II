
import copy as cp
import itertools


def cantidati(filename):
    f = open(filename, "r") #файлът, в който се дават данни за транзакцията
    c1 = {} #генериране на речник на отделни елементи със съответната честота
    l = 0 # общ брой транзакции
    for line in f.readlines():
        l += 1
        line = line.strip()
        line = line.replace('"', '')
        lst = line.split(',')
        for item in lst:
            count = c1.get(item, 0)
            c1[item] = count + 1
    return c1, l

'''cand = речник на набор от елементи със съответната честота като стойност
n = общ брой транзакции
support = минимална поддръжка за артикул, за да бъде често срещан
'''

def frequence(cand, n, support):
    l = [] # списък с елементи, които са чести
    for item in cand:
        x = cand[item] / n
        if x >= support:
            l.append(item)
    return l

'''s = списък с елементи
n = дължина на набора от комбинации
lst = списък с елементи, които дават подмножество с дължина n'''

def namiraneObecti(s, n): # за подмножествата (subsets)
    lst = []
    for i in itertools.combinations(s, n):
        lst.append(frozenset(i))
    return lst


"""
lk = лист от всички често срещани елементи с дължина k
ele = елемент с дължина k+1
return True, ако цялото подмножество на ele присъства в lk
"""

def namalqvane(lk, ele):
    k = len(ele) - 1
    subset = namiraneObecti(ele, k)
    for i in subset:
        if i not in lk:
            return False
    return True


"""
lk1 = често срещан набор от елементи с дължина k
lk2 = кандидати за дължина k=1
"""
def generirane_candidati(lk1):
    lk = cp.deepcopy(lk1)
    n = len(lk)
    lk2 = []
    k = len(lk[0])
    for i in range(n - 1):
        lkt1 = list(lk[i])
        for j in range(i + 1, n):
            lkt2 = list(lk[j])
            flag = True
            for l in range(k - 1):
                if lkt1[l] != lkt2[l]:
                    flag = False
            if flag:
                lst = cp.deepcopy(lkt1)
                lst.append(lkt2[k - 1])
                lst = frozenset(lst)
                if namalqvane(lk, lst):
                    lk2.append(lst)
    return lk2


'''lk1 = набор от кандидати с дължина k
c = Връща речник на честотата на всеки набор от кандидати в lk1
'''
def get_candidati(filename, lk1):
    lk = cp.deepcopy(lk1)
    f = open(filename, "r")
    c = {}
    l = 0
    k = len(lk[0])
    for line in f.readlines():
        l += 1
        line = line.strip()
        line = line.replace('"', '')
        lst = line.split(',')
        subset = namiraneObecti(lst, k)
        for i in lk:
            # i_t = tuple(i)
            if i in subset:
                count = c.get(i, 0)
                c[i] = count + 1
    return c


'''
support = минимална поддръжка, при която се разглеждат честите елементи
freq_set = често срещан набор от елементи, които имат честота, по-голяма от поддържаната
'''
def apriori(filename, support=0.35):
    freq_set = {}
    cand1, n = cantidati('myDataSet.csv')
    l1 = frequence(cand1, n, support)
    for i in l1:
        freq_set[frozenset({i})] = cand1[i]
    c2 = namiraneObecti(l1, 2)
    while len(c2) != 0:
        cand = get_candidati(filename, c2)
        l2 = frequence(cand, n, support)
        if len(l2) == 0:
            break
        for i in l2:
            freq_set[i] = cand[i]
        c2 = generirane_candidati(l2)
    return freq_set


"""
freq_set : речник, съдържащ чести набори със съответните честоти
confidence : стойност на доверието
Rule: речник, даващ правила за асоцииране
"""

def pravila(freq_set, confidence=0.56):
    Rule = {}
    for key in freq_set.keys():
        if len(key) == 1:
            continue
        k = len(key)
        for i in range(1, k):
            subset = list(itertools.combinations(key, i))
            for j in subset:
                if freq_set[key] / freq_set[key - frozenset(j)] >= confidence:
                    Rule[key - frozenset(j)] = frozenset(j)
    return Rule


if __name__ == '__main__':
    frequence_set = apriori('myDataSet', support=0.2)
    rule = pravila(frequence_set, confidence=0.5)
    for i in rule:
        print(i, ' --->>> ', rule[i])
