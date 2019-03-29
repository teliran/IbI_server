import sys
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
import json

app = Flask(__name__)
app.config.from_pyfile('server.cfg', silent=True)
db = SQLAlchemy(app)

class Users(db.Model):
    user_id = db.Column(db.String, primary_key = True)
    date_created = db.Column(db.String)
    age = db.Column(db.Integer)
    sex = db.Column(db.Text)

class ImageRatings(db.Model):
    user_id = db.Column(db.String, primary_key = True)
    image_id = db.Column(db.Text, primary_key = True)
    rating = db.Column(db.Integer)

class Actions(db.Model):
    user_id = db.Column(db.String, primary_key = True)
    session_id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, primary_key = True)
    total_screens = db.Column(db.Integer)
    screen_order = db.Column(db.Integer)
    time_to_pass  = db.Column(db.Integer)
    success = db.Column(db.Boolean)
    selected_images = db.Column(db.String)
    shown_images = db.Column(db.String)
    top_rated_images = db.Column(db.String)

@app.route('/healthcheck', methods=['GET'])
def printer():
    print("called")
    return json.dumps('Server is listening...')

@app.route('/ratings', methods=['POST'])
def add_ratings():
    print("add_ratings")
    print("json:", request.json)
    data = ImageRatings(user_id=request.get_json(force=True)["userId"], image_id=request.get_json(force=True)["imageId"], rating=request.get_json(force=True)["rating"])
    db.session.add(data)
    db.session.commit()
    return json.dumps('Rating Added')

@app.route('/users', methods=['POST'])
def add_users():
    print("add_users")
    print("json:", request.json)
    data = Users(user_id=request.get_json(force=True)["userId"], date_created=request.get_json(force=True)["date"], age=request.get_json(force=True)["age"], sex=request.get_json(force=True)["sex"])
    db.session.add(data)
    db.session.commit()
    return json.dumps('User Added')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port='3002')