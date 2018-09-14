from Printing import *
from Reading import *
from AuxFunctions import *
from TabularPredictive import TabularPredictive
from RecursiveParser import RecursiveParser
from SLRParser import SLRParser
CODES = 1
LEVEL = 0
RAW = 0
AUX = 1
TABULAR = 0
RECURSIVE = 0
SLR = 1
REVERSED = 1

def buildLevel(S, tree):
    level = [[[0, [S]]]]
    nowLevel = -1
    for i in range(len(tree)):
        if (tree[i][0] > nowLevel):
            nowLevel = tree[i][0]
            level += [[]]
        if (REVERSED): tree[i][1].reverse()
        level[nowLevel] += [tree[i]]
    if (REVERSED):
        for l in range(len(level)):
            level[l].reverse()
    return(level)

def buildGraph(grammar, level):
    graph = {}
    for i in range(len(level)):
        di, dj = 0, 0
        for jj, j in enumerate(level[i]):
            if (i):
                while (level[i - 1][di][1][dj] not in grammar):
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
                if (k not in grammar): continue
                graph[(i, jj, kk, k)] = []
    return(graph)

def spacing(S, graph, grammar, nonTerminals, space):
    if (S not in graph): return(0, len(tokenBox(S, nonTerminals)))
    mini, maxi = 0, 0
    each = {}
    for u in graph[S]:
        mi, ma = spacing(u, graph, grammar, nonTerminals, 0)
        each[u] = [mi, ma]
        mini, maxi = min(mini, mi), max(maxi, ma)
    print(S[3], each)
    return(mini, maxi)

S = input().split()[1]
grammar, nonTerminals, terminals = readER()
printGrammar(grammar, terminals, nonTerminals)
if (AUX):
    grammarFirst, grammarFollow = {}, {}
    for n in nonTerminals:
        grammarFirst[n] = sorted(first([n], grammar, nonTerminals, set()))
        grammarFollow[n] = sorted(follow(n, S, grammar, nonTerminals, set(), grammarFollow))
    printAuxFunction("First", grammarFirst, terminals, nonTerminals)
    printAuxFunction("Follow", grammarFollow, terminals, nonTerminals)

if (SLR):
    print("\n"+colors.yellow+"Closure:"+colors.end)
    statesList, C = buildC(S, grammar, terminals, nonTerminals)

print()
tokenMap = readTokenMap()

if (TABULAR):
    tabularPredictive = TabularPredictive(tokenMap)
    parsingTable = tabularPredictive.buildParsingTable(grammar, grammarFirst, grammarFollow, nonTerminals, terminals)
    printPredictiveParsingTable(parsingTable, terminals)

if (RECURSIVE): recursiveParser = RecursiveParser(tokenMap)

if (SLR):
    slrParser = SLRParser(tokenMap)
    slrTable = slrParser.buildSLRTable(statesList, C, S, grammar, terminals, nonTerminals, grammarFollow)
    printSLRTable(slrTable, terminals, nonTerminals)

if (CODES):
    print()
    codes = readCodes()
    for code in codes:
        print("\n"+colors.yellow+"Code: ",colors.blue, *code, colors.end, " | tokens: ", code, sep='')
        tabTree, recTree, slrTree, cp = [], [], [], -1
        try:
            if (TABULAR): cp = tabularPredictive.topDownTabularPredictive(parsingTable, S, code, nonTerminals, terminals, tabTree)
            if (RECURSIVE): cp = recursiveParser.topDownRecursive(S, grammar, code, 0, recTree, 1)
            if (SLR): cp = slrParser.bottomUpSLRParser(slrTable, grammar, code, slrTree)
        except Exception as e:
            print("BUG on parsers", e)
        print("\tVerdict: " + ((colors.green+"Accepted"+colors.end) if cp >= len(code) else (colors.red+"ERROR at token: %d" % (cp)+colors.end)))

        if (cp >= len(code)):
            level = []
            if (TABULAR):
                auxTree = []
                tabularPredictive.transformTree(auxTree, tabTree, 0, 0)
                tabTree = auxTree
                tabTree.sort(key=lambda x:x[0])
                if (RAW): print("\ttabRawTree:", tabTree)
                tabLevel = buildLevel(S, tabTree)
                level = tabLevel
                if (LEVEL): printLevel(tabLevel)
            if (RECURSIVE):
                recTree.sort(key=lambda x:x[0])
                if (RAW): print("\trecRawTree:", recTree)
                recLevel = buildLevel(S, recTree)
                level = recLevel
                if (LEVEL): printLevel(recLevel)
            if (SLR):
                slrTree = slrParser.transformTree(slrTree, S, nonTerminals)
                slrTree.sort(key=lambda x:x[0])
                if (RAW): print("\tslrRawTree:", slrTree)
                slrLevel = buildLevel(S, slrTree)
                level = slrLevel
                if (LEVEL): printLevel(slrLevel)
            if (TABULAR and RECURSIVE): print("\tTree Equality: " + ((colors.green+"True") if tabTree == recTree else (colors.red+"False")) + colors.end)
            graph = buildGraph(grammar, level)
            # print("Pre-Order:")
            # preOrderGraph((0, 0, 0, S), nonTerminals, graph)
            print("Interesting-Print:")
            interestingPrint((0, 0, 0, S), nonTerminals, graph, 1)
