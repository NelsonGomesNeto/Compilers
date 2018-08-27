COLORED = 1

class colors:
    yellow = "\033[93m"
    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[96m"
    end = "\033[0m"

class effect: # Doesn't seem to work .-.
    bold = "\033[1m"
    end = "\033[21m"

def printER(er, nonTerminals = None):
    for rule in (nonTerminals if nonTerminals is not None else er):
        print("\t", rule, " = ", sep='', end='')
        for i, production in enumerate(er[rule]):
            if (i): print(" | ", end='')
            print(*production, end='')
        print()

def printAuxFunction(name, grammarSet, nonTerminals):
    print(name)
    for n in nonTerminals:
        print("\t%s(%s) =" % (name, n), grammarSet[n])

def productionAsString(production):
    s = [colors.green, "", colors.end]
    if (production == ["Error"]): s[0] = colors.red
    if (production == ['e']): s[0] = colors.yellow
    for i, p in enumerate(production):
        if (i): s[1] += " "
        s[1] += str(p)
    return(tuple(s))

def printParsingTable(parsingTable, terminals):
    print("\nParsing Table:")
    print(end=" "*12)
    for t in terminals: print("|%10s|" % t, end='')
    print("|%10s|" % "EOF")
    for n in parsingTable:
        print("|%10s|" % n, end='')
        for t in terminals:
            print("|%s%10s%s|" % productionAsString(parsingTable[n][t]), end='')
        print("|%s%10s%s|" % productionAsString(parsingTable[n]["EOF"]))

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
    return("[%10s]" % ((colors.yellow*COLORED if S[3] == 'e' else "")+S[3]+(colors.end*COLORED if S[3] == 'e' else "") if (S[3] == 'e' or S[3] in nonTerminals) else (colors.green*COLORED+str(S[3][0])+", "+str(S[3][1])+colors.end*COLORED)))

def preOrderGraph(S, nonTerminals, graph):
    print(S[0]*13*" ", tokenBox(S, nonTerminals), sep='')
    if (S not in graph): return
    for u in graph[S]:
        preOrderGraph(u, nonTerminals, graph)

def resetString():
    global string
    string = ""

global string
def prepateInterestingPrint(S, nonTerminals, graph, notFirst):
    global string
    if (S not in graph):
        # print(" "*4 + ((S[0]-1)*8)*" " + "|" + 1*"_" + "> " if notFirst else " ", tokenBox(S, nonTerminals), sep='')
        string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst else " -> ") + tokenBox(S, nonTerminals) + "\n"
        return
    # print(" "*4 + ((S[0]-1)*8)*" " + "|" + 1*"_" + "> " if notFirst and S[0] else (S[0]>0)*" ", tokenBox(S, nonTerminals), sep='', end='')
    string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst and S[0] else (S[0]>0)*" -> ") + tokenBox(S, nonTerminals)
    for i, u in enumerate(graph[S]):
        prepateInterestingPrint(u, nonTerminals, graph, i)

def interestingPrint(S, nonTerminals, graph, notFirst):
    global string
    string = ""
    prepateInterestingPrint(S, nonTerminals, graph, notFirst)
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