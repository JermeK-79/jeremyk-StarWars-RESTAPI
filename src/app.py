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
from models import db, User, Character, Planet, Favorite
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
    pass

@app.route('/planets/<int:planet_id>', methods=["GET"])
def get_single_planet():
    pass

@app.route('/users', methods=["GET"])
def get_all_users():
    pass

@app.route('/users/<int:user_id>/favorites', methods=["GET"])
def get_single_user_favorites(user_id):
    pass

@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_favorite_person(people_id):
    data = request.get_json()
    new_favorite_person = Favorite(user_id = data["user_id"], character_id = data[people_id])
    db.session.add(new_favorite_person)
    db.session.commit()

@app.route('/favorite/planets/<int:planet_id>', methods=["POST"])
def add_favorite_planet(planet_id):
    pass

@app.route('/favorite/people/<int:people_id>', methods=["DELETE"])
def remove_favorite_person(people_id):
    pass

@app.route('/favorite/planets/<int:planet_id>', methods=["DELETE"])
def remove_favorite_planet(planet_id):
    pass






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
