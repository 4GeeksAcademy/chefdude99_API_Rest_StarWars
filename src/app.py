"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if len(users) < 1:
        return jsonify({'msg': 'NOT FOUND'}), 404
    serialized_users = [x.serialize() for x in users]
    return serialized_users, 202

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    if len(characters) < 1: 
        return jsonify({'msg': 'NOT FOUND'}), 404
    serialized_characters = [x.serialize() for x in characters]
    return serialized_characters, 202

@app.route('/starships', methods=['GET'])
def get_all_starships():
    starships = Starships.query.all()
    if len(starships) < 1: 
        return jsonify({'msg': 'NOT FOUND'}), 404
    serialized_starships = [x.serialize() for x in starships]
    return serialized_starships, 202

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    if len(planets) < 1: 
        return jsonify({'msg': 'NOT FOUND'}), 404
    serialized_planets = [x.serialize() for x in planets]
    return serialized_planets, 202

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': 'User NOT FOUND'}), 404
    return jsonify(user.serialize()), 200

@app.route('/characters/<int:id>', methods=['GET'])
def get_character_by_id(id):
    character = Characters.query.get(id)
    if character is None:
        return jsonify({'msg': 'Character NOT FOUND'}), 404
    return jsonify(character.serialize()), 200

@app.route('/starships/<int:id>', methods=['GET'])
def get_starship_by_id(id):
    starship = Starships.query.get(id)
    if starship is None:
        return jsonify({'msg': 'Starship NOT FOUND'}), 404
    return jsonify(starship.serialize()), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_by_id(id):
    planet = Planets.query.get(id)
    if planet is None:
        return jsonify({'msg': 'Planet NOT FOUND'}), 404
    return jsonify(planet.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
