from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)

# Set up the base directory and database path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact


# Define the User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')


# Create schema instances for serialization
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/")
def initial():
    return '<h1>Hello Welcome To Flask API Development</h1>'

# Add new user
@app.route("/user", methods=['POST'])
def add_user():
    name=request.json['name']
    contact =request.json['contact']
    new_user = User(name,contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

# show all user
@app.route("/user", methods=['GET'])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# show USer By ID
@app.route("/user/<id>", methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# update User by Id
@app.route('/user/<id>', methods=['PUT'])
def UpdateUser(id):
    user = User.query.get(id)
    name = request.json['name']
    contact = request.json['contact']
    user.name = name
    user.contact = contact
    db.session.commit()
    return user_schema.jsonify(user)

# delete the user By ID
@app.route('/user/<id>', methods=['DELETE'])
def deleteByUserId(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

# Run the app and create tables
if __name__ == '__main__':
    app.run()
