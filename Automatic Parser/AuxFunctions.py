from Printing import *

def classify(token, tokenMap):
    if (token in tokenMap):
        return(tokenMap[token])
    return(token)

def first(production, grammar, nonTerminals, visited):
    if (production == ['e']): return(['e'])
    if (tuple(production) in visited): return([])
    visited.add(tuple(production))
    firstSet, hasEpi = set(), 0
    for element in production:
        done = 1
        if (element not in nonTerminals):
            firstSet.add(element)
            break
        elif (['e'] in grammar[element]): hasEpi, done = hasEpi + 1, 0
        if (element in nonTerminals):
            insideEpi = False
            for p in grammar[element]:
                firstMinusEpi = first(p, grammar, nonTerminals, visited)
                firstSet.update(firstMinusEpi)
                if ('e' in firstMinusEpi):
                    insideEpi = True
                    firstSet.remove('e')
            if (not insideEpi): break
            else: hasEpi += done
    else:
        if (hasEpi >= len(production)): firstSet.add('e')
    return(firstSet)

def follow(X, S, grammar, nonTerminals, visited):
    followSet = set()
    if (X == S): followSet.add("EOF")
    for A in nonTerminals:
        for production in grammar[A]:
            if (X in production):
                isLast = False
                for position, p in enumerate(production):
                    if (p != X): continue
                    isLast = position == len(production) - 1
                    if (position < len(production) - 1):
                        firstMinusEpi = first(production[position+1:], grammar, nonTerminals, set())
                        prevSize = len(followSet)
                        followSet.update(firstMinusEpi)
                        # if (len(followSet) == prevSize): return(followSet)
                        if ('e' in firstMinusEpi): isLast = True
                if (isLast):
                    if (X == A): continue
                    if (A not in visited):
                        visited.add(A)
                        followSet.update(follow(A, S, grammar, nonTerminals, visited))
    if ('e' in followSet): followSet.remove('e')
    return(followSet)

# each productionBlock in productions will be a pair: (pointer, (X, =, production))
def closure(productions, grammar, nonTerminals, visited):
    clousureSet = set()
    if (tuple(productions) in visited): return(clousureSet)
    visited.add(tuple(productions))
    for p in productions:
        clousureSet.add(p)
    for productionBlock in productions:
        pointer, production = productionBlock
        production = production[2]
        if (pointer < len(production) and production[pointer] in nonTerminals):
            for internProduction in grammar[production[pointer]]:
                internProductionBlock = (0, (production[pointer], "=", tuple(internProduction)))
                if (internProductionBlock not in clousureSet):
                    clousureSet.update(closure([internProductionBlock], grammar, nonTerminals, visited))
    return(sorted(clousureSet))

def goto(state, symbol, grammar, nonTerminals):
    newState = []
    for production in state:
        pointer, prod = production
        if (pointer == len(prod[2]) or prod[2][pointer] != symbol): continue
        newProduction = ((pointer + 1), (prod))
        newState += closure([newProduction], grammar, nonTerminals, set())
    else: return(newState)

def getSymbols(closureSet):
    symbols = set()
    for cl in closureSet:
        pointer, prod = cl
        if (pointer < len(prod[2])): symbols.add(prod[2][pointer])
    return(symbols)

def buildC(S, grammar, nonTerminals):
    C = []
    # print("closure({S' = . %s}) = " % S, end='')
    C += [closure([(0, ("S'", "=", tuple([S])))], grammar, nonTerminals, set())]
    # printClosure(C[0])
    i = 0
    while (i < len(C)):
        print(end="\tI_%d = " % i)
        printClosure(C[i])
        symbols = getSymbols(C[i])
        for symbol in symbols:
            newState = goto(C[i], symbol, grammar, nonTerminals)
            if (newState not in C): C += [newState]
        i += 1
    return(C)