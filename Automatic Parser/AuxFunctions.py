def classify(token, tokenMap):
    if (token in tokenMap):
        return(tokenMap[token])
    return(token)

def first(production, grammar, nonTerminals):
    if (production == ['e']): return(['e'])
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
                firstMinusEpi = first(p, grammar, nonTerminals)
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
                        firstMinusEpi = first(production[position+1:], grammar, nonTerminals)
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
