import json, os, Levenshtein
MAXSIZE = 50 * 1024 * 1024 #50mb | set to what you want
TOOBAD = -10 #number of votes needed to delete a character
def getchardata(char:str) -> dict[str] | None:
    cl = getcharsjson() 
    for c in cl:
        if c['name'] == char:
            return c
    return None
def getcharsjson() -> dict[dict[str]]:
    with open('chars.json', 'r') as f:
        return json.load(f)
def addchar(charname:str, prompt:str, image:str) -> bool:
    findex = 0
    if getchardata(charname) != None:
        return False
    try:
        while os.path.getsize(f'./data/{findex}.json') > MAXSIZE:
            findex += 1
    except FileNotFoundError:
        with open(f'./data/{findex}.json', 'w') as f:
            f.write('{}')
    charfile = getcharsjson()
    with open(f'./chars.json', 'w') as f:
        charfile.append({
            'name': charname,
            'jsonindex': findex,
            })
        json.dump(charfile, f)
    with open(f'./data/{findex}.json', 'r') as f:
        findexfile = json.load(f)
    with open(f'./data/{findex}.json', 'w') as f:
        findexfile[charname] = {
            'prompt': prompt,
            'imageurl': image,
            'votes': 0,
            'totalvotes': 0
        }
        json.dump(findexfile, f)
    return True
def vote(charname: str, positive: bool) -> bool:
    chardata = getchardata(charname)
    if chardata == None:
        return False
    with open(f'./data/{chardata["jsonindex"]}.json', 'r') as f:
        charjson = json.load(f)
    charjson[charname]['votes'] += 1 if positive else -1
    charjson[charname]['totalvotes'] += 1 
    with open(f'./data/{chardata["jsonindex"]}.json', 'w') as f:
        json.dump(charjson, f)
    return True
def search(charname) -> dict[str] | None:
    chardata = getcharsjson()
    for c in chardata:
        if c['name'] == charname:
            return c
    for c in chardata:
        if charname.lower() in c['name'].lower():
            return c
    levenlist = []
    for c in chardata:
        lev = Levenshtein.distance(charname.lower(), c['name'].lower())
        if lev <= 2:
            levenlist.append((c, lev))
    if len(levenlist) == 0:
        return None
    levenlist.sort(key=lambda x: x[1])
    return levenlist[0][0]
def getReal(smallC: dict[str]) -> dict[str]:
    #open the jsonindex file for this character
    with open(f'./data/{smallC["jsonindex"]}.json', 'r') as f:
        charjson = json.load(f)
    return charjson[smallC['name']]
def searchForBad():
    chardata = getcharsjson()
    countDeleted = 0
    for c in chardata:
        with open(f'./data/{c["jsonindex"]}.json', 'r') as f:
            charjson = json.load(f)
        if charjson['votes'] <= TOOBAD:
            with open(f'./chars.json', 'w') as f:
                del charjson[c['name']]
                json.dump(charjson, f)
            countDeleted += 1
    return countDeleted