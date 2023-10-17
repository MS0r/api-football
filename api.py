from flask import (Blueprint,redirect, url_for, jsonify, request)
import os
from json_data import load_data
from queries import querieshandler
import jwt

bp = Blueprint('api',__name__,url_prefix='/api/v1')
cwd = os.getcwd()
source_path = os.path.join(cwd,'data', 'europe-champions-league-json')
users_path = os.path.join(cwd, 'data', 'users.json')
data = {}

for root, dirs, files in os.walk(source_path):
    for direc in dirs:
        data[direc] = load_data(os.path.join(source_path,direc,'cl.json'))
    break


@bp.before_request
def return_index():
    
    token = request.headers.get('Authorization')
    if data == {}: return redirect(url_for('index'))
    elif token is None: return jsonify({'message' : 'no token provided'}),400
    token = token.split(" ")[1]

    try:
        payload = jwt.decode(jwt=token, key='my_secret_key',algorithms=['HS256'])
    except:
        return jsonify({'message' : 'not valid token'}),400

@bp.route('/<temp>/teams')
def get_all_teams(temp):
    groups = data[temp]['Groups']
    num = 0
    response = {}
    for group in groups:
        for team in groups[group]:
            num += 1
            response.update({f'team{num}':groups[group][team]})

    return jsonify(response)

@bp.route('/<temp>/groups')
def get_groups(temp):
    response = data[temp]['Groups']
    return jsonify(response)

@bp.route('/<temp>/matchdays')
def get_matchdays(temp): 
    response = data[temp]['Matchday']
    return jsonify(response)


@bp.route('/<temp>/results')
def get_matchs_results(temp):

    '''API queries
        goals = minimum number of goals made in the game
        team = team who has played the match either local or away
        stadium = stadium where the game has been played
        day = either day of the week, month or specific day
    '''
    response = data[temp]['Matchs']

    matchgoals = request.args.get('goals')
    team = request.args.get('team')
    stadium = request.args.get('stadium')
    day = request.args.get('day')
    queries = [matchgoals, team, stadium, day]

    if queries.count(None) != 4:
        return jsonify(querieshandler(response,queries))
    else:
        return jsonify(response)
    
@bp.route('/<temp>/results/<matchday>')
def get_matchday_results(temp,matchday):
    matchs = data[temp]['Matchs']
    response = {}

    for group in matchs:
        response[group] = []
        for match in matchs[group]:
            if matchday in match:
                response[group].append(matchs[group][match])

    matchgoals = request.args.get('goals')
    team = request.args.get('team')
    stadium = request.args.get('stadium')
    day = request.args.get('day')
    queries = [matchgoals, team, stadium, day]
    
    if queries.count(None) != 4:
        return jsonify(querieshandler(response,queries))
    else:
        return jsonify(response)

@bp.route('/<temp>/<group>/group')
def get_group(temp,group):
    response = data[temp]['Groups'][f'Group {group.upper()}']
    return jsonify(response)

@bp.route('/<temp>/<group>/results')
def get_group_results(temp,group):
    response = data[temp]['Matchs'][f'Group {group.upper()}']
    return jsonify(response)


@bp.route('/users')
def get_all_users():
    users = load_data(users_path)
    return jsonify(users)

@bp.route('/users/<username>')
def get_user(username):
    users = load_data(users_path)
    morelikely = []
    for user in users:
        if username.lower() in user['username'].lower():
            morelikely.append(user)
    return jsonify(morelikely)

