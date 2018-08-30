from AuxFunctions import *
from Printing import *
VERBOSE = 0

class SLRParser:
    tokenMap = {}
    def __init__(self, tokenMap):
        self.tokenMap = tokenMap

    def buildSLRTable(self, C, S, grammar, terminals, nonTerminals, grammarFollow):
        table = {}
        eofTerminals = terminals + ["EOF"]
        for i in range(len(C)):
            index = "I_%d" % i
            table[index] = {}
            for t in eofTerminals:
                table[index][t] = ["Error"]
                closureSet = closure(goto(C[i], t, grammar, nonTerminals), grammar, nonTerminals, set())
                if (closureSet in C):
                    table[index][t] = ["e%d" % C.index(closureSet)]
            for n in nonTerminals:
                table[index][n] = ["Error"]
                closureSet = closure(goto(C[i], n, grammar, nonTerminals), grammar, nonTerminals, set())
                if (closureSet in C):
                    table[index][n] = ["%d" % C.index(closureSet)]
                for p, prod in enumerate(grammar[n]):
                    if ((len(prod), (n, "=", tuple(prod))) in C[i]):
                        for f in grammarFollow[n]:
                            table[index][f] = ["r%d" % p, n]
        closureSet = closure(goto(C[0], S, grammar, nonTerminals), grammar, nonTerminals, set())
        table["I_%d" % C.index(closureSet)]["EOF"] = ["Accepted"]
        return(table)

    def bottomUpSLRParser(self, slrTable, grammar, code):
        # stack has pair of [state, symbols]
        stack, codePointer = [[0, [""]]], 0
        while (stack):
            printSLRStack(stack)
            if (len(stack) > 6): return(True)
            state, symbol = stack[len(stack) - 1]
            # print("line", state, symbol, code[codePointer] if codePointer < len(code) else "")
            action = slrTable["I_%d" % state][code[codePointer] if codePointer < len(code) else "EOF"]
            # print("action", action[0], action[0][0])
            if (action[0] == "Error"): return(codePointer)
            if (action[0] == "Accepted"): return(codePointer)
            if (action[0][0] == 'e'):
                symbol += [code[codePointer]]
                stack += [[int(action[0][1:]), symbol]]
                codePointer += 1
            elif (action[0][0] == 'r'):
                n, prevSymbol = action[1], symbol
                production = grammar[n][int(action[0][1:])].copy()
                production.reverse()
                toSubstitute, rest, done = [], [], False
                for i in range(len(symbol) - 1, -1, -1):
                    if (not done):
                        toSubstitute += [symbol[i]]
                        stack.pop(len(stack) - 1)
                    else: rest += [symbol[i]]
                    if (toSubstitute == production): done = True
                rest.reverse()
                rest += [n]
                state, symbol = stack[len(stack) - 1]
                transition = int(slrTable["I_%d" % state][n][0])
                # print("tosub", production, toSubstitute, production == toSubstitute, prevSymbol, rest)
                stack += [[transition, rest]]
