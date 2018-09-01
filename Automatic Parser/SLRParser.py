from AuxFunctions import *
from Printing import *
VERBOSE = 0

class SLRParser:
    tokenMap = {}
    def __init__(self, tokenMap):
        self.tokenMap = tokenMap

    def initTable(self, states, eofTerminals, nonTerminals):
        table = {}
        for i in range(states):
            index = "I_%d" % i
            table[index] = {}
            for t in eofTerminals:
                table[index][t] = ["Error"]
            for n in nonTerminals:
                table[index][n] = ["Error"]
        return(table)

    def buildSLRTable(self, statesList, C, S, grammar, terminals, nonTerminals, grammarFollow):
        eofTerminals = terminals + ["EOF"]
        table = self.initTable(len(C), eofTerminals, nonTerminals)

        # S' = S . rule
        closureSet = closure(goto(C[0], S, grammar, nonTerminals), grammar, nonTerminals, set())
        table["I_%d" % C.index(closureSet)]["EOF"] = ["Accepted"]
        if (['e'] in grammar[S]): table["I_0"]["EOF"] = ["Accepted"]

        # goto(state, symbol) rule
        for state, symbol in sorted(statesList):
            index = "I_%d" % state
            table[index][symbol] = [("e" if symbol in terminals else "") + str(statesList[(state, symbol)])]

        # A = alpha . rule
        for i in range(len(C)):
            index = "I_%d" % i
            for dot, production in C[i]:
                n, production = production[0], production[2]
                if (n == "S'"): continue
                if (dot == len(production)):
                    for f in grammarFollow[n]:
                        table[index][f] = ["r%d" % grammar[n].index([*production]), n]

        return(table)

    def bottomUpSLRParser(self, slrTable, grammar, code):
        # stack has pair of [state, symbols]
        stack, history, codePointer = [[0, ""]], [], 0
        print("\tStack [State, Symbol]:")
        while (stack):
            printSLRStack(stack)
            history += [stack]
            state, symbol = stack[len(stack) - 1]
            if (VERBOSE): print("line", state, symbol, classify(code[codePointer], self.tokenMap) if codePointer < len(code) else "")
            action = slrTable["I_%d" % state][classify(code[codePointer], self.tokenMap) if codePointer < len(code) else "EOF"]
            if (action[0] == "Error"): return(codePointer if codePointer < len(code) else codePointer - 1)
            if (action[0] == "Accepted"): return(codePointer)
            if (action[0][0] == 'e'):
                stack += [[int(action[0][1:]), (classify(code[codePointer], self.tokenMap), code[codePointer])]]
                codePointer += 1
            elif (action[0][0] == 'r'):
                n, prevSymbol = action[1], symbol
                production = grammar[n][int(action[0][1:])]
                for i in range(len(production)):
                    stack.pop(len(stack) - 1)
                state, symbol = stack[len(stack) - 1]
                symbol = n
                transition = int(slrTable["I_%d" % state][n][0])
                # print("tosub", production, toSubstitute, production == toSubstitute, prevSymbol, rest)
                stack += [[transition, symbol]]
        # production.reverse()
        # toSubstitute, rest, done = [], [], False
        # for i in range(len(symbol) - 1, -1, -1):
        #     if (not done):
        #         toSubstitute += [symbol[i]]
        #         stack.pop(len(stack) - 1)
        #     else: rest += [symbol[i]]
        #     if (toSubstitute == production): done = True
        # rest.reverse()