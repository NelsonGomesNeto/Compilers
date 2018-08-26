VERBOSE = 0
COLORED = 1
separator = "{}()+-*/,"
tokenMap = {}
class colors:
    blue = "\033[93m"
    green = "\033[92m"
    end = "\033[0m"

def classify(token):
    if (token in tokenMap):
        return(tokenMap[token])
    return(token)

def printER(er, nonTerminal = None):
    for rule in (nonTerminal if nonTerminal is not None else er):
        print("\t", rule, " = ", sep='', end='')
        for i, production in enumerate(er[rule]):
            if (i): print(" | ", end='')
            print(*production, end='')
        print()

def printGraph(graph):
    print(graph)
    for l, node in enumerate(sorted(graph, key=lambda x:(x[0], x[1], x[2]))):
        print(node[0]*"    ", node, " -> ", sep='', end='')
        for u in graph[node]:
            print(u, end=' ')
        print()

def tokenBox(S, nonTerminal):
    return("[%10s]" % ((colors.blue*COLORED if S[3] == 'e' else "")+S[3]+(colors.end*COLORED if S[3] == 'e' else "") if (S[3] == 'e' or S[3] in nonTerminal) else (colors.green*COLORED+str(S[3][0])+", "+str(S[3][1])+colors.end*COLORED)))

def preOrderGraph(S, nonTerminal, graph):
    print(S[0]*13*" ", tokenBox(S, nonTerminal), sep='')
    if (S not in graph): return
    for u in graph[S]:
        preOrderGraph(u, nonTerminal, graph)

global string
def interestingPrint(S, nonTerminal, graph, notFirst):
    global string
    if (S not in graph):
        # print(" "*4 + ((S[0]-1)*8)*" " + "|" + 1*"_" + "> " if notFirst else " ", tokenBox(S, nonTerminal), sep='')
        string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst else " -> ") + tokenBox(S, nonTerminal) + "\n"
        return
    # print(" "*4 + ((S[0]-1)*8)*" " + "|" + 1*"_" + "> " if notFirst and S[0] else (S[0]>0)*" ", tokenBox(S, nonTerminal), sep='', end='')
    string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst and S[0] else (S[0]>0)*" -> ") + tokenBox(S, nonTerminal)
    for i, u in enumerate(graph[S]):
        interestingPrint(u, nonTerminal, graph, i)

def fillSpacing(S, nonTerminal, graph, spacing, now):
    spacing[S] = [now, now + len(tokenBox(S, nonTerminal))]
    if (S not in graph): return(len(tokenBox(S, nonTerminal)))
    now += len(tokenBox(S, nonTerminal))
    for u in graph[S]:
        now += fillSpacing(u, nonTerminal, graph, spacing, 0)
    spacing[S][1] = now
    return(now)

def readER():
    print("Reading:", input())
    er, nonTerminal = {}, []
    while (True):
        line = input()
        if (line == "END"): break
        left, right = line.split('=')
        left = left.strip(' ')
        er[left] = []
        nonTerminal += [left]
        for production in right.split('|'):
            production = production.split()
            er[left] += [production]
    for e in er:
        for j, p in enumerate(er[e]):
            for i in range(len(p)):
                if (p[i] not in er and p[i] != 'e'):
                    er[e][j][i] = p[i][1:len(p[i])-1]
    return(er, nonTerminal)

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

def buildLevel(S, tree):
    level = [[[0, [S]]]]
    nowLevel = 0
    for i in range(len(tree)):
        if (tree[i][0] > nowLevel):
            nowLevel = tree[i][0]
            level[nowLevel - 1]
            level += [[]]
        level[nowLevel] += [tree[i]]
    return(level)

def buildGraph(er, level):
    graph = {}
    for i in range(len(level)):
        di, dj = 0, 0
        for jj, j in enumerate(level[i]):
            if (i):
                while (level[i - 1][di][1][dj] not in er):
                    dj += 1
                    if (dj >= len(level[i - 1][di][1])):
                        dj = 0
                        di += 1
                prev = level[i - 1][di][1][dj]
                kkk = []
                for kk, k in enumerate(j[1]):
                    kkk += [(i, jj, kk, k)]
                graph[(i-1, di, dj, prev)] = kkk + graph[(i-1, di, dj, prev)]
                dj += 1
                if (dj >= len(level[i - 1][di][1])):
                    dj = 0
                    di += 1
            for kk, k in enumerate(j[1]):
                if (k not in er): continue
                graph[(i, jj, kk, k)] = []
    return(graph)

def parseCode(S, er, code, codePointer, tree, depth):
    if (VERBOSE): print(S, codePointer)
    prev = codePointer
    for production in er[S]:
        codePointer = prev
        finalProduction = []
        for i, element in enumerate(production):
            if (element == 'e'): break
            if (element in er):
                found = parseCode(element, er, code, codePointer, tree, depth + 1)
                if (found == -1): break
                else:
                    finalProduction += [element]
                    codePointer = found
            elif (codePointer < len(code) and element == classify(code[codePointer])):
                finalProduction += [(element, code[codePointer])]
                codePointer += 1
            else:
                break
        else:
            tree += [[depth, finalProduction]]#[[depth, production]]
            return(codePointer)
    else:
        if (['e'] in er[S]):
            tree += [[depth, ['e']]]
            return(prev)
    return(-1)

S = input().split()[1]
er, nonTerminal = readER()
printER(er, nonTerminal)

tokenMap = readTokenMap()

print()
codes = readCodes()
for code in codes:
    print()
    print("Code:", *code, "|", code)
    tree, ac = [], -1
    try:
        ac = parseCode(S, er, code, 0, tree, 1)
    except:
        pass
    print("\tAC" if ac >= len(code) else "ERROR at token: %d" % (ac))

    if (ac >= len(code)):
        tree.sort(key=lambda x:x[0])
        print("\trawTree:", tree)
        level = buildLevel(S, tree)
        for i in range(len(level)):
            print("\tLevel %d: " % i, end='')
            for l in level[i]:
                print(l[1], end=' ')
            print()

        graph = buildGraph(er, level)
        # printGraph(graph)
        print("Pre-Order:")
        preOrderGraph((0, 0, 0, S), nonTerminal, graph)
        print("Interesting-Print:")
        string = ""
        interestingPrint((0, 0, 0, S), nonTerminal, graph, 1)
        lines = string.splitlines()
        for l in range(len(lines)):
            for i in range(len(lines[l])):
                if (lines[l][i] == '|'):
                    for j in range(l - 1, -1, -1):
                        if (lines[j][i + 2] == ']'):
                            break
                        lines[j] = lines[j][:i] + '|' + lines[j][i+1:]
        for line in lines:
            print(line)

