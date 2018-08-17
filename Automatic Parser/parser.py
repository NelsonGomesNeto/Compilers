VERBOSE = 0
separator = "()+-*"

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

def postOrderGraph(S, graph):
    print(S[0]*8*" ", "[%5s]" % S[3], sep='')
    if (S not in graph): return
    for u in graph[S]:
        postOrderGraph(u, graph)

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
        for i, element in enumerate(production):
            if (element == 'e'): break
            if (element in er):
                found = parseCode(element, er, code, codePointer, tree, depth + 1)
                if (found == -1): break
                else: codePointer = found
            elif (codePointer < len(code) and element == code[codePointer]):
                codePointer += 1
            else:
                break
        else:
            tree += [[depth, production]]
            return(codePointer)
    else:
        if (['e'] in er[S]):
            tree += [[depth, ['e']]]
            return(prev)
    return(-1)

S = input()
er, nonTerminal = readER()
printER(er, nonTerminal)

codes = readCodes()
for code in codes:
    print()
    print("Code:", *code, "|", code)
    tree = []
    ac = parseCode(S, er, code, 0, tree, 1) >= len(code)
    print("\tAC" if ac else "ERROR at level: %d" % (ac))

    if (ac):
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
        print()
        postOrderGraph((0, 0, 0, S), graph)
