import os
from json_data import load_data, save_data

def users_init():
    
    cwd = os.getcwd()
    target_path = os.path.join(cwd, 'data','users.json')
    data = load_data(target_path)
    if data == {}:
        save_data(target_path,[])