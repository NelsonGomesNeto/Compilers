from AuxFunctions import *
VERBOSE = 0

class RecursiveParser:
    tokenMap = {}
    def __init__(self, tokenMap):
        self.tokenMap = tokenMap

    def topDownRecursive(self, S, grammar, code, codePointer, tree, depth):
        if (VERBOSE): print(S, codePointer)
        prev = codePointer
        for production in grammar[S]:
            codePointer = prev
            finalProduction = []
            for i, element in enumerate(production):
                if (element == 'e'): break
                if (element in grammar):
                    found = self.topDownRecursive(element, grammar, code, codePointer, tree, depth + 1)
                    if (found == -1): break
                    else:
                        finalProduction += [element]
                        codePointer = found
                elif (codePointer < len(code) and element == classify(code[codePointer], self.tokenMap)):
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