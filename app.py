import json
import os
import re
import time

def load_txt_data(filepath):
    try: 
        with open(filepath,'r', encoding="utf-8") as cl:
            return cl.read().split('\n')[2:]
    except FileNotFoundError:
        return None
    
def create_dir(target):
    if not os.path.exists(target):
        os.mkdir(target)

def load_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f,ensure_ascii=False)
    except:
        return {}

def save_data(filepath, data):
    with open(filepath, 'w',encoding='utf-8') as f:
        json.dumps(data)
        json.dump(data, f, indent=6,ensure_ascii=False)    

def get_groups(gro):
    groupsJSON = {}
    for i in gro:
        splited = [t for t in i.replace('|', '').split('  ') if t != '']
        groupsJSON[splited[0]] = {f'team{enum}' : j.strip() for enum,j in enumerate(splited) if enum != 0}
    return groupsJSON

def get_matchdays(mt):
    days = []
    for i in mt:
        matchday = [item for item in i.split() if not re.match('(Matchday|[|#-]+)',item)]
        days.append(matchday)
    return {f'{day[0]}' : f'{day[1]} {day[2]}' for day in days}

def get_match_results(data):
    groupmatch = {}
    num = 1
    matchs = []
    matchs.append(data[0])
    matchs.append({})
    numMatchday = iter(range(1,7))
    while num < len(data):
        number = iter(range(1,3))
        goalscorer = iter(range(1,3))
        if data[num].startswith('Group'):
            groupmatch[matchs[0]] = matchs[1]
            matchs.clear()
            matchs.extend([data[num],{}])
            num += 1
            numMatchday = iter(range(1,7))
        else:
            partidos = {}
            for i in data[num:num+6]:
                if "'" in i:
                    partidos.update({f'goalscorers{next(goalscorer)}' : i})
                elif re.match('^\[(Wed|Tue) [a-zA-Z/]{3}/[0-9]{1,2}\]$',i) != None:
                    if 'goalscorers1' in list(partidos.keys()) and len(partidos) == 3:
                        partidos.update({'date2':i})
                    elif len(partidos) >= 3:
                        break
                    else:
                        partidos.update({'date' : i})
                elif i.startswith('Group'):
                    break
                else:
                    partidos.update({f'match{next(number)}' : i})

            aux = {f'Matchday {next(numMatchday)}' : partidos}
            matchs[1].update(aux) 
            num += len(partidos)

    groupmatch[matchs[0]] = matchs[1]
    return groupmatch

if __name__ == '__main__':
    cwd = os.getcwd()
    source_path = os.path.join(cwd, 'europe-champions-league') # ..\api-python\data\europe-champions-league
    target_path = os.path.join(cwd, 'europe-champions-league-json') #  ..\api-python\data\europe-champions-league-json
    create_dir(target_path)

    for root, dirs, files in os.walk(source_path):
        for direc in dirs:
            if re.match('^201[0-9]{,1}-[0-9]{,2}',direc):

                datatxt = load_txt_data(os.path.join(source_path,direc,'cl.txt'))
                if datatxt != None:

                    '''leaving the list without empty items, comments and useless spaces between substrings
                    creating or getting the target json from the data folder which dict is saved in jsn'''

                    datatxt = list(filter(lambda x : not x.startswith('#') and x != '', map(lambda x : re.sub('[ ]{2,}','  ',x.strip()),datatxt)))
                    tar_path = os.path.join(target_path,direc)
                    create_dir(tar_path)
                    save_path = os.path.join(tar_path,'cl.json')
                    jsn = load_data(save_path)

                    '''filtering the list to get both groups and matchdays to get this information in json format'''

                    groups_filtered = list(filter(lambda x : x.startswith('Group'), datatxt[:8]))
                    matchdays_filtered = list(filter(lambda x : x.startswith('Matchday'), datatxt[8:15]))
                    groups = get_groups(groups_filtered)
                    days = get_matchdays(matchdays_filtered)
                    
                    ''''now doing the same but with the rest of the information inside txt to get matchs results'''
                    datatxt = datatxt[len(groups_filtered)+len(days):]
                    groupmatch = get_match_results(datatxt)
                
                    '''now with all the information we add that to the jsn dict and save it in the save path'''                
                    jsn['Groups'] = groups
                    jsn['Matchday'] = days
                    jsn['Matchs'] = groupmatch

                    save_data(save_path,jsn)
        break