from Printing import *
from Reading import *
from AuxFunctions import *
from TabularPredictive import TabularPredictive
from RecursiveParser import RecursiveParser
CODES = 1
LEVEL = 0
RAW = 0
TABULAR = 1
RECURSIVE = 0

def buildLevel(S, tree):
    level = [[[0, [S]]]]
    nowLevel = -1
    for i in range(len(tree)):
        if (tree[i][0] > nowLevel):
            nowLevel = tree[i][0]
            level[nowLevel - 1]
            level += [[]]
        level[nowLevel] += [tree[i]]
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

S = input().split()[1]
grammar, nonTerminals, terminals = readER()
printER(grammar, nonTerminals)
grammarFirst, grammarFollow = {}, {}
for n in nonTerminals:
    grammarFirst[n] = sorted(first([n], grammar, nonTerminals))
    grammarFollow[n] = sorted(follow(n, S, grammar, nonTerminals))
print()
printAuxFunction("First", grammarFirst, nonTerminals)
print()
printAuxFunction("Follow", grammarFollow, nonTerminals)

print()
tokenMap = readTokenMap()

tabularPredictive = TabularPredictive(tokenMap)
recursiveParser = RecursiveParser(tokenMap)
parsingTable = tabularPredictive.buildParsingTable(grammar, grammarFirst, grammarFollow, nonTerminals, terminals)
printParsingTable(parsingTable, terminals)

if (CODES):
    print()
    codes = readCodes()
    for code in codes:
        print("\nCode:", *code, "|", code)
        tabTree, recTree, cp = [], [], -1
        try:
            if (TABULAR): cp = tabularPredictive.topDownTabularPredictive(parsingTable, S, code, nonTerminals, terminals, tabTree)
            if (RECURSIVE): cp = recursiveParser.topDownRecursive(S, grammar, code, 0, recTree, 1)
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
            graph = buildGraph(grammar, level)
            # # printGraph(graph)
            # # print("Pre-Order:")
            # # preOrderGraph((0, 0, 0, S), nonTerminals, graph)
            print("Interesting-Print:")
            interestingPrint((0, 0, 0, S), nonTerminals, graph, 1)
