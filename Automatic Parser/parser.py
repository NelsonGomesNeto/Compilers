from Printing import *
from Reading import *
VERBOSE = 0
CODES = 1

def classify(token):
    if (token in tokenMap):
        return(tokenMap[token])
    return(token)

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

def topDownRecursive(S, grammar, code, codePointer, tree, depth):
    if (VERBOSE): print(S, codePointer)
    prev = codePointer
    for production in grammar[S]:
        codePointer = prev
        finalProduction = []
        for i, element in enumerate(production):
            if (element == 'e'): break
            if (element in grammar):
                found = topDownRecursive(element, grammar, code, codePointer, tree, depth + 1)
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
        if (['e'] in grammar[S]):
            tree += [[depth, ['e']]]
            return(prev)
    return(-1)

def first(production, grammar, nonTerminal):
    if (production == ['e']): return(['e'])
    firstSet, hasEpi = set(), 0
    for element in production:
        done = 1
        if (element not in nonTerminal):
            firstSet.add(element)
            break
        elif (['e'] in grammar[element]): hasEpi, done = hasEpi + 1, 0
        if (element in nonTerminal):
            insideEpi = False
            for p in grammar[element]:
                firstMinusEpi = first(p, grammar, nonTerminal)
                firstSet.update(firstMinusEpi)
                if ('e' in firstMinusEpi):
                    insideEpi = True
                    firstSet.remove('e')
            if (not insideEpi): break
            else: hasEpi += done
    else:
        if (hasEpi >= len(production)): firstSet.add('e')
    return(firstSet)

def follow(X, S, grammar, nonTerminal):
    followSet = set()
    if (X == S): followSet.add("EOF")
    for A in nonTerminal:
        for production in grammar[A]:
            if (X in production):
                position, isLast = production.index(X), False
                isLast = position == len(production) - 1
                if (position < len(production) - 1):
                    firstMinusEpi = first(production[position+1:], grammar, nonTerminal)
                    followSet.update(firstMinusEpi)
                    if ('e' in firstMinusEpi): isLast = True
                if (isLast):
                    if (X == A): continue
                    followSet.update(follow(A, S, grammar, nonTerminal))
    if ('e' in followSet): followSet.remove('e')
    return(followSet)

S = input().split()[1]
grammar, nonTerminal = readER()
printER(grammar, nonTerminal)
print("\nFirst")
for n in nonTerminal:
    print("\tfirst(%s) =" % n, sorted(first([n], grammar, nonTerminal)))
print("\nFollow:")
for n in nonTerminal:
    print("\tfollow(%s) =" % n, sorted(follow(n, S, grammar, nonTerminal)))

if (CODES):
    print()
    tokenMap = readTokenMap()

    print()
    codes = readCodes()
    for code in codes:
        print("\nCode:", *code) #, "|", code)
        tree, cp = [], -1
        try: cp = topDownRecursive(S, grammar, code, 0, tree, 1)
        except: pass
        print("\tVerdict: " + ((colors.green+"Accepted"+colors.end) if cp >= len(code) else (colors.red+"ERROR at token: %d" % (cp)+colors.end)))

        if (cp >= len(code)):
            tree.sort(key=lambda x:x[0])
            print("\trawTree:", tree)
            level = buildLevel(S, tree)
            # printLevel(level)
            graph = buildGraph(grammar, level)
            # printGraph(graph)
            # print("Pre-Order:")
            # preOrderGraph((0, 0, 0, S), nonTerminal, graph)
            print("Interesting-Print:")
            interestingPrint((0, 0, 0, S), nonTerminal, graph, 1)
