from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
import logging



app = Flask(__name__)
app.config.from_pyfile('server.cfg', silent=True)
db = SQLAlchemy(app)
#Configure logging
handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
handler.setLevel(app.config['LOGGING_LEVEL'])
app.logger.addHandler(handler)

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
    session_id = db.Column(db.String, primary_key = True)
    timestamp = db.Column(db.String, primary_key = True)
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
    previous_rating = ImageRatings.query.filter_by(user_id=request.get_json(force=True)["userId"], image_id=request.get_json(force=True)["imageId"]).first()
    print("previous:", previous_rating)
    if previous_rating is not None:
        previous_rating.rating = request.get_json(force=True)["rating"]
        db.session.commit()
    else:
        data = ImageRatings(user_id=request.get_json(force=True)["userId"], image_id=request.get_json(force=True)["imageId"], rating=request.get_json(force=True)["rating"])
        try:
            db.session.add(data)
            db.session.commit()
            app.logger.info('Rating added successfully: %s', (data))
        except exc.SQLAlchemyError:
            return jsonify({"ERROR": "rating did not written to DB, try again"}), 400
    return json.dumps('Rating Added')

@app.route('/users', methods=['POST'])
def add_users():
    print("add_users")
    print("json:", request.json)
    data = Users(user_id=request.get_json(force=True)["userId"], date_created=request.get_json(force=True)["date"], age=request.get_json(force=True)["age"], sex=request.get_json(force=True)["sex"])
    try:
        db.session.add(data)
        db.session.commit()
        app.logger.info('User added successfully: %s', (data))
    except exc.SQLAlchemyError as e:
        app.logger.error('Unhandled Exception: %s', (e))
        return jsonify({"ERROR": "user already in DB"}), 400
    return json.dumps('User Added')

@app.route('/actions', methods=['POST'])
def add_actions():
    print("add_action")
    print("json:", request.json)
    data = Actions(user_id=request.get_json(force=True)["userId"], session_id=request.get_json(force=True)["sessionId"], timestamp=request.get_json(force=True)["timestamp"], total_screens=request.get_json(force=True)["total_screens"], screen_order=request.get_json(force=True)["screen_order"], time_to_pass=request.get_json(force=True)["time_to_pass"], success=request.get_json(force=True)["success"], selected_images=request.get_json(force=True)["selected_images"], shown_images=request.get_json(force=True)["shown_images"], top_rated_images=request.get_json(force=True)["top_rated_images"])
    try:
        db.session.add(data)
        db.session.commit()
        app.logger.info('Action added successfully: %s', (data))
    except exc.SQLAlchemyError as e:
        app.logger.error('Unhandled Exception: %s', (e))
        return jsonify({"ERROR": "Action has not registered, try again"}), 400
    return json.dumps('Action registered')


def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port='3002')