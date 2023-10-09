import re

def booleanaffect(stringlist, boolean1, boolean2,q):
    for qu in q:
        if qu != None:
                boolean1 = boolean1 and qu.capitalize() in stringlist[0]
                boolean2 = boolean2 and qu.capitalize() in stringlist[1]
    return boolean1, boolean2

def querieshandler(data, queries):

    responseif = {}
    to_int = lambda x : int(x)
    searchre = lambda x : re.search('[0-9]{1,2}-[0-9]{1,2}',x)[0]
    checkmatchgoals = lambda x : sum(map(to_int,x.split('-'))) > int(queries[0])
    for group in data:
        responseif[group] = []
        for match in data[group]:
            booleanmatch1 = booleanmatch2 = True
            matchday = data[group][match]
            listmatchs = [matchday['match1'],matchday['match2']]

            if queries[0] != None:
                result1, result2 =  map(searchre,listmatchs)
                booleanmatch1, booleanmatch2 = map(checkmatchgoals,[result1, result2])

            booleanmatch1, booleanmatch2 = booleanaffect(listmatchs,booleanmatch1,booleanmatch2,[queries[1],queries[2]])

            if queries[3] != None:
                cap = queries[3] if queries[3][0].isnumeric() else queries[3].capitalize()
                if cap not in matchday['date']:
                    continue

            if booleanmatch1: responseif[group].append({'date' : matchday['date'], 'match' : matchday['match1'], 'goalscorers' : 'No info' if 'goalscorers1' not in matchday else matchday.get('goalscorers1')})
            if booleanmatch2: responseif[group].append({'date' : matchday['date'], 'match' : matchday['match2'], 'goalscorers' : 'No info' if 'goalscorers2' not in matchday else matchday.get('goalscorers2')})
        if len(responseif[group]) < 1:
            responseif.pop(group)
    return responseif