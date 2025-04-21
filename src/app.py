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
from models import db, User, Characters, Planets, Starships, Fav_planet, Fav_character, Fav_starship
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

@app.route('/users/favorites', methods=['GET'])
def get_favorites_user():
    users = User.query.all()
    if not users:
        return jsonify({'msg': 'Users NOT FOUND'}), 404

    favorites = []
    for user in users:
        user_favorites = {
            'user_id': user.id,
            'characters_favorites': [fav.character.serialize() for fav in user.characters_favorites],
            'starships_favorites': [fav.starship.serialize() for fav in user.starships_favorites],
            'planets_favorites': [fav.planet.serialize() for fav in user.planets_favorites]
        }
        favorites.append(user_favorites)

    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
     planet = Planets.query.get(planet_id)
     if planet is None:
          return jsonify({'msg' : 'Planeta no existe'}), 400
     user = User.query.get(user_id)
     if user is None:
          return jsonify({'msg' : 'Usuario no encontrado'}), 400
     favorite = Fav_planet.query.filter_by(planet_id = planet_id, user_id = user_id).first()
     if favorite != None:
          return jsonify({'msg' : 'Favorito ya existe'}), 400
     new_favorite = Fav_planet()
     new_favorite.user_id = user_id
     new_favorite.planet_id= planet_id
     db.session.add(new_favorite)
     db.session.commit()
     return jsonify({'msg' : 'OK', 'data' : new_favorite.serialize()})

@app.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id, user_id):
     character = Characters.query.get(character_id)
     if character is None:
          return jsonify({'msg' : 'Personaje no existe'}), 400
     user = User.query.get(user_id)
     if user is None:
          return jsonify({'msg' : 'Usuario no encontrado'}), 400
     favorite = Fav_character.query.filter_by(character_id = character_id, user_id = user_id).first()
     if favorite != None:
          return jsonify({'msg' : 'Favorito ya existe'}), 400
     new_favorite = Fav_character()
     new_favorite.user_id = user_id
     new_favorite.character_id= character_id
     db.session.add(new_favorite)
     db.session.commit()
     return jsonify({'msg' : 'OK', 'data' : new_favorite.serialize()})

@app.route('/favorite/starship/<int:user_id>/<int:starship_id>', methods=['POST'])
def add_favorite_starship(starship_id, user_id):
     starship = Starships.query.get(starship_id)
     if starship is None:
          return jsonify({'msg' : 'Nave no existe'}), 400
     user = User.query.get(user_id)
     if user is None:
          return jsonify({'msg' : 'Usuario no encontrado'}), 400
     favorite = Fav_starship.query.filter_by(starship_id = starship_id, user_id = user_id).first()
     if favorite != None:
          return jsonify({'msg' : 'Favorito ya existe'}), 400
     new_favorite = Fav_starship()
     new_favorite.user_id = user_id
     new_favorite.starship_id= starship_id
     db.session.add(new_favorite)
     db.session.commit()
     return jsonify({'msg' : 'OK', 'data' : new_favorite.serialize()})

@app.route('/favorite/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_planet(user_id, planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
          return jsonify({'msg' : 'Planeta no existe'}), 404
    user = User.query.get(user_id)
    if user is None:
          return jsonify({'msg' : 'Usuario no encontrado'}), 404
    favorite = Fav_planet.query.filter_by(planet_id = planet_id, user_id = user_id).first()
    if favorite is None:
          return jsonify({'msg' : 'Favorito no existe'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg' : 'OK'}), 200

@app.route('/favorite/character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_character(user_id, character_id):
    character = Characters.query.get(character_id)
    if character is None:
          return jsonify({'msg' : 'Personaje no existe'}), 404
    user = User.query.get(user_id)
    if user is None:
          return jsonify({'msg' : 'Usuario no encontrado'}), 404
    favorite = Fav_character.query.filter_by(character_id = character_id, user_id = user_id).first()
    if favorite is None:
          return jsonify({'msg' : 'Favorito no existe'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg' : 'OK'}), 200

@app.route('/favorite/starship/<int:user_id>/<int:starship_id>', methods=['DELETE'])
def delete_starship(user_id, starship_id):
    starship = Starships.query.get(starship_id)
    if starship is None:
          return jsonify({'msg' : 'Nave no existe'}), 404
    user = User.query.get(user_id)
    if user is None:
          return jsonify({'msg' : 'Usuario no encontrado'}), 404
    favorite = Fav_starship.query.filter_by(starship_id = starship_id, user_id = user_id).first()
    if favorite is None:
          return jsonify({'msg' : 'Favorito no existe'}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg' : 'OK'}), 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
