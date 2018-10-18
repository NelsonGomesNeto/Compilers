from AuxFunctions import *
from Printing import *
VERBOSE = 1

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

    def buildSLRTable(self, statesList, canonical, S, grammar, terminals, nonTerminals, grammarFollow):
        eofTerminals = terminals + ["EOF"]
        table = self.initTable(len(canonical), eofTerminals, nonTerminals)

        # RULE: S' = S .
        closureSet = canonical[statesList[(0, S)]]
        table["I_%d" % canonical.index(closureSet)]["EOF"] = ["Accepted"]
        if (['e'] in grammar[S]): table["I_0"]["EOF"] = ["Accepted"]

        # RULE: goto(state, symbol) [symbol = terminals U nonTerminals]
        for state, symbol in sorted(statesList):
            index = "I_%d" % state
            table[index][symbol] = [("e" if symbol in terminals else "") + str(statesList[(state, symbol)])]

        # RULE: A = alpha .
        for i in range(len(canonical)):
            index = "I_%d" % i
            for dot, production in canonical[i]:
                n, production = production[0], production[2]
                if (n == "S'"): continue
                if (dot == len(production)):
                    for f in grammarFollow[n]:
                        table[index][f] = ["r%d" % grammar[n].index([*production]), n]

        return(table)

    def bottomUpSLRParser(self, slrTable, grammar, code, tree):
        # stack has pair of [state, symbols]
        stack, history, codePointer = [[0, ""]], [], 0
        print("\tStack [State, Symbol]:")
        while (stack):
            if (VERBOSE): printSLRStack(stack)
            history += [stack]

            state, symbol = stack[len(stack) - 1]
            action = slrTable["I_%d" % state][classify(code[codePointer], self.tokenMap) if codePointer < len(code) else "EOF"]

            if (action[0] == "Error"): return(codePointer if codePointer < len(code) else codePointer - 1)
            if (action[0] == "Accepted"): return(codePointer)

            if (action[0][0] == 'e'): # stacks
                stack += [[int(action[0][1:]), (classify(code[codePointer], self.tokenMap), code[codePointer])]]
                codePointer += 1
            elif (action[0][0] == 'r'): # reducts
                n = action[1] # getting nonTerminal
                production = grammar[n][int(action[0][1:])]
                now = []
                for i in range(len(production)):
                    state, symbol = stack.pop(len(stack) - 1)
                    now += [symbol]
                tree += [now]
                state, symbol = stack[len(stack) - 1]
                transition = int(slrTable["I_%d" % state][n][0])
                stack += [[transition, n]]

    def fillNewTree(self, tree, newTree, nonTerminals, depth, i):
        newTree += [[depth, tree[i[0]]]]
        for element in tree[i[0]]:
            if (element in nonTerminals):
                i[0] += 1
                self.fillNewTree(tree, newTree, nonTerminals, depth + 1, i)

    def transformTree(self, tree, S, nonTerminals):
        if (not tree): return([[1, ['e']]])
        tree.reverse()
        newTree, i = [], [0]
        self.fillNewTree(tree, newTree, nonTerminals, 1, i)
        return(newTree)
