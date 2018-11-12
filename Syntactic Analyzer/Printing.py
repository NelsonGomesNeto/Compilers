COLORED = 1

class colors:
    yellow = "\033[93m"
    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[96m"
    end = "\033[0m"

class effect: # Doesn't seem to work .-.
    bold = "\033[1m"
    end = "\033[0m"

def printGrammar(grammar, terminals, nonTerminals = None):
    for n in (nonTerminals if nonTerminals is not None else grammar):
        print("\t", colors.blue, n, colors.end, " = ", sep='', end='')
        for i, production in enumerate(grammar[n]):
            if (i): print(" | ", end='')
            print(*[symbolString(s, terminals) for s in production], end='')
        print()

def stateString(i):
    return(colors.yellow+("I_%d" % i)+colors.end)

def symbolString(symbol, terminals):
    return((colors.green if symbol in terminals else colors.blue if (symbol != 'e' and symbol != "EOF") else colors.yellow) + symbol + colors.end)

def printAuxFunction(name, grammarSet, terminals, nonTerminals):
    print("\n"+colors.yellow+name+colors.end)
    for n in nonTerminals:
        print("\t%s(%s) = {" % (name, symbolString(n, terminals)), ', '.join([symbolString(s, terminals) for s in grammarSet[n]]), "}", sep='')

def productionAsString(production, terminals):
    s = [colors.blue, "", colors.end]
    if (production == ["Error"]): s[0] = colors.red
    if (production == ['e']): s[0] = colors.yellow
    if (production == ["Accepted"]): s[0] = colors.green
    for i, p in enumerate(production):
        if (i): s[1] += " "
        s[1] += str(p) if (p not in terminals) else '\''+str(p)+'\''
    return(tuple(s))

def printPredictiveParsingTable(parsingTable, terminals):
    print("\n"+colors.yellow+"Predictive Parsing Table:"+colors.end)
    print(end=" "*16)
    for t in sorted(terminals): print("|%14s|" % t, end='')
    print("|%14s|" % "EOF")
    for n in sorted(parsingTable):
        print("|%14s|" % n, end='')
        for t in sorted(terminals):
            print("|%s%14s%s|" % productionAsString(parsingTable[n][t], terminals), end='')
        print("|%s%14s%s|" % productionAsString(parsingTable[n]["EOF"], terminals))

def printSLRTable(SLRTable, terminals, nonTerminals):
    print("\n"+colors.yellow+"SLR Table:"+colors.end)
    print(end=" "*8)
    lol = sorted(terminals)
    # lol.reverse()
    column = lol + ["EOF"] + nonTerminals
    for c in column: print(("|%s%10s%s|" % (colors.yellow,c,colors.end)) if c == "EOF" else "|%10s|" % c, end='')
    print()
    for I in sorted(SLRTable, key=lambda x:int(x[2:])):
        print("|%s%6s%s|" % (colors.yellow,I,colors.end), end='')
        for t in column:
            print("|%s%10s%s|" % productionAsString(SLRTable[I][t], terminals), end='')
        print()

def stackItem(item):
    if (isinstance(item, str)): return(colors.blue+str(item)+colors.end)
    return(colors.green+"("+str(item[0])+", \'"+str(item[1])+'\''+")"+colors.end)

def printSLRStack(stack):
    states, symbols, all = "", "", ""
    for i, s in enumerate(stack):
        if (i):
            states += " "
            symbols += " "
            all += " "
        states += str(s[0])
        symbols += str(s[1])
        st, sy = colors.yellow + str(s[0]) + colors.end, stackItem(s[1])
        all += "[" + sy + ", " + st + "]"
    # print("\t%-30s | %-30s" % (states, symbols))
    print("\t", all, sep='')

def printClosureBox(closureBox, nonTerminals):
    print(colors.blue, closureBox[1][0], " ", colors.yellow, closureBox[1][1], colors.end, sep='', end='')
    for i, c in enumerate(closureBox[1][2]):
        if (i == closureBox[0]): print(end=colors.red+' .'+colors.end)
        print(end=' ' + (colors.blue+c if c in nonTerminals else colors.green+c) + colors.end)
    if (closureBox[0] == len(closureBox[1][2])): print(end=colors.red+' .'+colors.end)

def printClosure(closureSet, nonTerminals):
    print(end='{')
    for i, cl in enumerate(closureSet):
        if (i): print(end=', ')
        printClosureBox(cl, nonTerminals)
    print(end='}\n')

def printLevel(level):
    for i in range(len(level)):
        print("\tLevel %d: " % i, end='')
        for l in level[i]:
            print(l[1], end=' ')
        print()

def lolPrint(tree):
    for l in tree:
        print(" "*5*l[0], l[1] if len(l) == 2 else l[2])

def printGraph(graph):
    print(graph)
    for l, node in enumerate(sorted(graph, key=lambda x:(x[0], x[1], x[2]))):
        print(node[0]*"    ", node, " -> ", sep='', end='')
        for u in graph[node]:
            print(u, end=' ')
        print()

def tokenBox(S, nonTerminals):
    return("[%10s]" % ((colors.yellow*COLORED if S[3] == 'e' else "")+S[3]+(colors.end*COLORED if S[3] == 'e' else "") if (S[3] == 'e' or S[3] in nonTerminals) else (colors.green*COLORED+str(S[3][0])+", \'"+str(S[3][1])+'\''+colors.end*COLORED)))

def preOrderGraph(S, nonTerminals, graph):
    print(S[0]*13*" ", tokenBox(S, nonTerminals), sep='')
    if (S not in graph): return
    for u in graph[S]:
        preOrderGraph(u, nonTerminals, graph)

def resetString():
    global string
    string = ""

def printAST(AST, depth = 0):
    if (type(AST) is tuple):
        print(" "*(depth - len(str(AST)) + 2) + tokenBox([0, 0, 0, AST], []))
        return
    spacing = 0
    for u in AST:
        if (type(u) is tuple):
            spacing = len(str(u)) - 2
    for u in AST:
        printAST(u, depth + spacing)

def newPrintAST(newAST, depth = 0):
    if (type(newAST) is not dict):
        print(" "*depth + str(newAST))
        return
    for u in newAST:
        if (type(u) is not int): print(" "*(depth) + str(u))
        newPrintAST(newAST[u], depth + 1)

global string
def prepareInterestingPrint(S, nonTerminals, graph, notFirst):
    global string
    if (S not in graph):
        string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst else " -> ") + tokenBox(S, nonTerminals) + "\n"
        return
    string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst and S[0] else (S[0]>0)*" -> ") + tokenBox(S, nonTerminals)
    for i, u in enumerate(graph[S]):
        prepareInterestingPrint(u, nonTerminals, graph, i)

def interestingPrint(S, nonTerminals, graph, notFirst):
    global string
    string = ""
    prepareInterestingPrint(S, nonTerminals, graph, notFirst)
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
