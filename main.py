from flask import Flask, request, jsonify
from app import main

app = Flask(__name__)

@app.route('/')
def index():
    return 'Home'

from api import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    main()
    app.run(debug=True)