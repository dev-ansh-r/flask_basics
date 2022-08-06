from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#init db
db = SQLAlchemy(app)


#init ma
ma= Marshmallow(app)


#user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    cringe = db.Column(db.String(120), unique=True)

    def __init__(self, username, email, cringe):
        self.username = username
        self.email = email
        self.cringe = cringe #cringe is the cringe


#userschema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email', 'cringe', 'id')


#init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#server route
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    cringe = request.json['cringe']

    new_user = User(username, email, cringe)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


#run server on port 5000
if __name__ == "__main__":
    app.run(debug=True)