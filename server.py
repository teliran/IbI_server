import sys
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
import json
from flask_restful import Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idi.db'
db = SQLAlchemy(app)

class Useres(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    datecreated = db.Column(db.DateTime)
    age = db.Column(db.Integer)
    sex = db.Column(db.Text)

class ImageRatings(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    imageid = db.Column(db.Text, primary_key = True)
    rating = db.Column(db.Integer)

class Actions(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    session_id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, primary_key = True)
    total_screens = db.Column(db.Integer)
    screen_order = db.Column(db.Integer)
    time_to_pass  = db.Column(db.Integer)
    success = db.Column(db.Boolean)
    selected_images = db.Column(db.ARRAY)
    shown_images = db.Column(db.ARRAY)
    top_rated_images = db.Column(db.ARRAY)




@app.route('/healthcheck', methods=['GET'])
def printer():
    print("called")
    return json.dumps('Server is listening...')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')