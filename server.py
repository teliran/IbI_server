import sys
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idi.db'
db = SQLAlchemy(app)

class Analytics(db.Model):
   device_id = db.Column(db.Integer, primary_key = True)
   date = db.Column(db.DateTime, primary_key = True)
   text = db.Column(db.Text)


@app.route('/', methods=['GET'])
def printer():
    print("called")
    return json.dumps('Server is listening...')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')