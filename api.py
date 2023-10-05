from flask import Blueprint
import os
from app import load_data

bp = Blueprint('api',__name__,url_prefix='/api/v1')
cwd = os.getcwd()
source_path = os.path.join(cwd, 'europe-champions-league-json')

@bp.route('/<temp>/teams')
def get_all_teams(temp):
    data = load_data(os.path.join(source_path,temp))
    if data == {}: return {}
    data = data['Groups']
    num = 0
    teams = {}
    for group in data:
        for team in group:
            num += 1
            teams.update({f'team{num}':group[team]})
    return teams

@bp.route('/<temp>/groups')
def get_groups(temp):
    data = load_data(os.path.join(source_path,temp))
    if data == {}: return {}
    return data['Groups']

    
