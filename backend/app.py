from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a secure key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Tokens expire in 1 hour
jwt = JWTManager(app)

CORS(app)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/autopick_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Token Blacklist (Temporary storage, use Redis or DB in production)
blacklisted_tokens = set()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create Tables
with app.app_context():
    db.create_all()

# Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'token': access_token, 'message': 'Login successful'})

# **Protected Home Route (Requires Token)**
@app.route('/home', methods=['GET'])
@jwt_required()
def protected_home():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Welcome {current_user}, you are logged in!'})

# **Logout Route (Blacklist Token)**
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get token's unique ID
    blacklisted_tokens.add(jti)  # Add to blacklist
    return jsonify({'message': 'Logout successful. Token invalidated.'})

# **Check if Token is Blacklisted**
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    return jwt_data["jti"] in blacklisted_tokens  # Reject if blacklisted

# **List API Routes (Debugging)**
@app.route('/routes', methods=['GET'])
def list_routes():
    return jsonify({rule.rule: rule.endpoint for rule in app.url_map.iter_rules()})

if __name__ == '__main__':
    app.run(debug=True)
