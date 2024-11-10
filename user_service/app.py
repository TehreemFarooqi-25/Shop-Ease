from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise RuntimeError("DATABASE_URL is not set in the environment")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'username': self.username}

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint to register a new user
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Endpoint to list all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
