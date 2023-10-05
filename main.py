from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Home'

from . import api
app.register_blueprint(api.bp)

if __name__ == '__main__':
    app.debug()