from AuxFunctions import *
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
                for prod in grammar[n]:
                    if ((len(prod), (n, "=", tuple(prod))) in C[i]):
                        for f in grammarFollow[n]:
                            table[index][f] = n # prod
        closureSet = closure(goto(C[0], S, grammar, nonTerminals), grammar, nonTerminals, set())
        table["I_%d" % C.index(closureSet)]["EOF"] = ["Accepted"]
        return(table)

    def bottomUpSLRParser():
        pass