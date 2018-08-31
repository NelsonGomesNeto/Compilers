from AuxFunctions import *
VERBOSE = 1

class TabularPredictive:
    tokenMap = {}
    def __init__(self, tokenMap):
        self.tokenMap = tokenMap

    def findProductionOfTerminal(self, X, grammar, t, nonTerminals):
        for production in grammar[X]:
            if (t in first(production, grammar, nonTerminals, set())):
                return(production)

    def buildParsingTable(self, grammar, grammarFirst, grammarFollow, nonTerminals, terminals):
        M = {}
        for X in nonTerminals:
            M[X] = {}
            for t in terminals: M[X][t] = ["Error"]
            M[X]["EOF"] = ["Error"]
            for t in grammarFirst[X]:
                M[X][t] = self.findProductionOfTerminal(X, grammar, t, nonTerminals)
            if ('e' in grammarFirst[X]):
                for e in grammarFollow[X]:
                    M[X][e] = ['e']
        return(M)

    def transformTree(self, newTree, tree, i, depth):
        nowProduction = [depth, []]
        while (i < len(tree)):
            if (tree[i][0] > depth):
                i = self.transformTree(newTree, tree, i, depth + 1)
            elif (tree[i][0] < depth):
                newTree += [nowProduction]
                return(i - 1)
            else:
                nowProduction[1] += [tree[i][1] if len(tree[i]) == 2 else tuple(tree[i][1:])]
            i += 1
        if (depth): newTree += [nowProduction]
        return(i)

    def topDownTabularPredictive(self, parsingTable, S, code, nonTerminals, terminals, tree):
        stack, codePointer = [[0, S]], 0
        while (True):
            if (VERBOSE): print(stack, code[codePointer] if codePointer < len(code) else "")
            while (stack and stack[len(stack) - 1][1] == 'e'): tree += [stack.pop(len(stack) - 1)]
            X = stack[len(stack) - 1][1] if len(stack) else None
            a = code[codePointer] if codePointer < len(code) else "EOF"
            depth = stack[len(stack) - 1][0] if len(stack) else 0
            if (not stack): return(codePointer if codePointer >= len(code) else -1)
            elif (X in terminals):
                if (X == classify(a, self.tokenMap)):
                    tree += [stack.pop(len(stack) - 1) + [a]]
                    codePointer += 1
                else:
                    return(-1)
            elif (X in nonTerminals):
                if (parsingTable[X][classify(a, self.tokenMap)] != ["Error"]):
                    tree += [stack.pop(len(stack) - 1)]
                    for d in reversed(parsingTable[X][classify(a, self.tokenMap)]):
                        stack += [[depth + 1, d]]
                else:
                    return(-1)
