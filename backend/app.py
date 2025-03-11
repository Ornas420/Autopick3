from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
import openai

app = Flask(__name__)
CORS(app)  # Leidžia frontend pasiekti backend
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/autopick_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def home():
    return jsonify({'message': 'Autopick API veikia!'})

if __name__ == '__main__':
    app.run(debug=True)