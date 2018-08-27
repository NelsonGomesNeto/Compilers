separator = "{}()+-*/,"
tokenMap = {}

def readER():
    print("Reading:", input())
    er, nonTerminals, terminals = {}, [], []
    while (True):
        line = input()
        if (line == "END"): break
        left, right = line.split('=')
        left = left.strip(' ')
        er[left] = []
        nonTerminals += [left]
        for production in right.split('|'):
            production = production.split()
            er[left] += [production]
    for e in er:
        for j, p in enumerate(er[e]):
            for i in range(len(p)):
                if (p[i] not in er and p[i] != 'e'):
                    er[e][j][i] = p[i][1:len(p[i])-1]
                    terminals += [er[e][j][i]]
    return(er, nonTerminals, terminals)

def readCodes():
    print("Reading:", input())
    codes = []
    while (True):
        line = input()
        if (line == "END"): break
        for s in separator:
            line = line.replace(s, " " + s + " ")
        codes += [line.split()]
    return(codes)

def readTokenMap():
    print("Reading:", input())
    tokenMap = {}
    while (True):
        line = input()
        if (line == "END"): break
        print("\t", line, sep='')
        left, right = line.split('#=')
        left, right = left.split(' '), right.strip(' ')
        for t in left:
            t = t.strip(' ')
            if (not t): continue
            if t[0] == '\'':
                tokenMap[t[1:len(t)-1]] = right
            else:
                for tt in t:
                    tokenMap[tt] = right
    return(tokenMap)