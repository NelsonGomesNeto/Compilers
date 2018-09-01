from Printing import colors
separator = "{}()[]+-*/,^;"

def reading():
    print("Reading: ", colors.yellow+input()+colors.end, sep='')

def readER():
    reading()
    grammar, nonTerminals, terminals = {}, [], []
    while (True):
        line = input()
        if (line == "END"): break
        left, right = line.split('=')
        left = left.strip(' ')
        grammar[left] = []
        nonTerminals += [left]
        for production in right.split('|'):
            production = production.split()
            grammar[left] += [production]
    for e in grammar:
        for j, p in enumerate(grammar[e]):
            for i in range(len(p)):
                if (p[i] not in grammar and p[i] != 'e'):
                    grammar[e][j][i] = p[i][1:len(p[i])-1]
                    if (grammar[e][j][i] not in terminals): terminals += [grammar[e][j][i]]
    return(grammar, nonTerminals, terminals)

def readCodes():
    reading()
    codes = []
    while (True):
        line = input()
        if (line == "END"): break
        for s in separator:
            line = line.replace(s, " " + s + " ")
        codes += [line.split()]
    return(codes)

def readTokenMap():
    reading()
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
