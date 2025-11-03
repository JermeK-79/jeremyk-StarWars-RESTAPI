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
from models import db, User, Character, Planet, Vehicle, Favorite

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=["GET"])
def get_all_people():
    response_body = Character.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=["GET"])
def get_single_person(people_id):
    single_person = Character.query.get(people_id)
    if single_person is None:
        raise APIException(f'Person ID {people_id} not found.', status_code=404)
    return jsonify(single_person.serialize()), 200

@app.route('/planets', methods=["GET"])
def get_all_planets():
    response_body = Planet.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=["GET"])
def get_single_planet(planet_id):
    single_planet = Planet.query.get(planet_id)
    if single_planet is None:
        raise APIException(f'Planet ID {planet_id} not found.', status_code=404)
    return jsonify(single_planet.serialize()), 200

@app.route('/vehicles', methods=["GET"])
def get_all_vehicles():
    response_body = Vehicle.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@app.route('/vehicles/<int:vehicle_id>', methods=["GET"])
def get_single_vehicle(vehicle_id):
    single_vehicle = Vehicle.query.get(vehicle_id)
    if single_vehicle is None:
        raise APIException(f'Vehicle ID {vehicle_id} not found.', status_code=404)
    return jsonify(single_vehicle.serialize()), 200

@app.route('/users', methods=["GET"])
def get_all_users():
    response_body = User.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/favorites', methods=["GET"])
def get_single_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException(f'User ID {user_id} not found.', status_code=404)
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorites_list = list(map(lambda x: x.serialize(), favorites))
    return jsonify(favorites_list), 200

@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_favorite_person(people_id):
    data = request.get_json()
    
    if not data or "user_id" not in data:
        raise APIException('user_id is required in request body.', status_code=400)
    
    user_id = data["user_id"]

    user = User.query.get(user_id)
    if user is None:
        raise APIException(f'User ID {user_id} not found.', status_code=404)

    character = Character.query.get(people_id)
    if character is None:
        raise APIException(f'Person ID {people_id} not found.', status_code=404)

    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, 
        character_id=people_id
    ).first()
    
    if existing_favorite:
        raise APIException('This person is already in favorites.', status_code=400)

    new_favorite_person = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite_person)
    db.session.commit()
    
    return jsonify(new_favorite_person.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def remove_favorite_person(people_id):
    data = request.get_json()
    
    if not data or "user_id" not in data:
        raise APIException('user_id is required in request body.', status_code=400)
    
    user_id = data["user_id"]

    favorite = Favorite.query.filter_by(
        user_id=user_id, 
        character_id=people_id
    ).first()
    
    if favorite is None:
        raise APIException('Favorite person not found.', status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite person removed successfully"}), 200

@app.route('/favorite/planets/<int:planet_id>', methods=["POST"])
def add_favorite_planet(planet_id):
    data = request.get_json()
    
    if not data or "user_id" not in data:
        raise APIException('user_id is required in request body.', status_code=400)
    
    user_id = data["user_id"]

    user = User.query.get(user_id)
    if user is None:
        raise APIException(f'User ID {user_id} not found.', status_code=404)

    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException(f'Planet ID {planet_id} not found.', status_code=404)
    
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, 
        planet_id=planet_id
    ).first()
    
    if existing_favorite:
        raise APIException('This planet is already in favorites.', status_code=400)
    
    new_favorite_planet = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite_planet)
    db.session.commit()
    
    return jsonify(new_favorite_planet.serialize()), 201

@app.route('/favorite/planets/<int:planet_id>', methods=["DELETE"])
def remove_favorite_planet(planet_id):
    data = request.get_json()
    
    if not data or "user_id" not in data:
        raise APIException('user_id is required in request body.', status_code=400)
    
    user_id = data["user_id"]
    
    favorite = Favorite.query.filter_by(
        user_id=user_id, 
        planet_id=planet_id
    ).first()
    
    if favorite is None:
        raise APIException('Favorite planet not found.', status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite planet removed successfully"}), 200

@app.route('/favorite/vehicles/<int:vehicle_id>', methods=["POST"])
def add_favorite_vehicle(vehicle_id):
    data = request.get_json()
    
    if not data or "user_id" not in data:
        raise APIException('user_id is required in request body.', status_code=400)
    
    user_id = data["user_id"]

    user = User.query.get(user_id)
    if user is None:
        raise APIException(f'User ID {user_id} not found.', status_code=404)

    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        raise APIException(f'Vehicle ID {vehicle_id} not found.', status_code=404)

    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, 
        vehicle_id=vehicle_id
    ).first()
    
    if existing_favorite:
        raise APIException('This vehicle is already in favorites.', status_code=400)

    new_favorite_vehicle = Favorite(user_id=user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite_vehicle)
    db.session.commit()
    
    return jsonify(new_favorite_vehicle.serialize()), 201

@app.route('/favorite/vehicles/<int:vehicle_id>', methods=["DELETE"])
def remove_favorite_vehicle(vehicle_id):
    data = request.get_json()
    
    if not data or "user_id" not in data:
        raise APIException('user_id is required in request body.', status_code=400)
    
    user_id = data["user_id"]
    
    favorite = Favorite.query.filter_by(
        user_id=user_id, 
        vehicle_id=vehicle_id
    ).first()
    
    if favorite is None:
        raise APIException('Favorite vehicle not found.', status_code=404)
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"message": "Favorite vehicle removed successfully"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)