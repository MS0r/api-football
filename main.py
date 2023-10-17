from flask import (Flask, request,jsonify)
from json_data import (main,load_data, save_data)
from users import users_init
import os
import jwt

app = Flask(__name__)
users_path = os.path.join(os.getcwd(), 'data', 'users.json')
users = load_data(users_path)

@app.route('/')
def index():
    return 'Home'

from api import bp
app.register_blueprint(bp)

@app.route('/auth/login',methods=['POST'])
def login():
    
    json = request.get_json(force=True)
    username = json.get('username')
    password = json.get('password')

    if username is None or password is None:
        return jsonify({'message' : 'Bad request'}), 400
    
    users = load_data(users_path)
    
    for user in users:
        if username == user['username']:
            if password == user['password']:
                user.pop('password')
                token = jwt.encode(payload=user, key='my_secret_key')
                return jsonify({'Success' : True, 'token' : token})
            else:
                break
    
    return jsonify({'message' : 'user or password were wrong'}), 404

@app.route('/auth/register', methods=['POST'])
def register():

    json = request.get_json(force=True)
    username = json.get('username')
    password = json.get('password')

    if username is None or password is None:
        return jsonify({'message' : 'Bad request'}), 400

    user = {'id' : len(users),'username' : username, 'password' : password}
    users.append(user)
    save_data(users_path, users)
    return user


if __name__ == '__main__':
    main()
    users_init()
    app.run(debug=True)