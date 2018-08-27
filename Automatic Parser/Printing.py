COLORED = 1

class colors:
    blue = "\033[93m"
    green = "\033[92m"
    red = "\033[91m"
    end = "\033[0m"

class effect: # Doesn't seem to work .-.
    bold = "\033[1m"
    end = "\033[21m"

def printER(er, nonTerminal = None):
    for rule in (nonTerminal if nonTerminal is not None else er):
        print("\t", rule, " = ", sep='', end='')
        for i, production in enumerate(er[rule]):
            if (i): print(" | ", end='')
            print(*production, end='')
        print()

def printLevel(leve):
    for i in range(len(level)):
        print("\tLevel %d: " % i, end='')
        for l in level[i]:
            print(l[1], end=' ')
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

def resetString():
    global string
    string = ""

global string
def prepateInterestingPrint(S, nonTerminal, graph, notFirst):
    global string
    if (S not in graph):
        # print(" "*4 + ((S[0]-1)*8)*" " + "|" + 1*"_" + "> " if notFirst else " ", tokenBox(S, nonTerminal), sep='')
        string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst else " -> ") + tokenBox(S, nonTerminal) + "\n"
        return
    # print(" "*4 + ((S[0]-1)*8)*" " + "|" + 1*"_" + "> " if notFirst and S[0] else (S[0]>0)*" ", tokenBox(S, nonTerminal), sep='', end='')
    string += (" "*9 + ((S[0]-1)*16)*" " + "|" + 4*"-" + "> " if notFirst and S[0] else (S[0]>0)*" -> ") + tokenBox(S, nonTerminal)
    for i, u in enumerate(graph[S]):
        prepateInterestingPrint(u, nonTerminal, graph, i)

def interestingPrint(S, nonTerminal, graph, notFirst):
    global string
    string = ""
    prepateInterestingPrint(S, nonTerminal, graph, notFirst)
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