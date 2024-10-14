#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

# Base directory and database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Flask app initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Print the database URI to verify
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Migrate setup
migrate = Migrate(app, db)

# Initialize database with Flask app
db.init_app(app)

# Initialize Flask-RESTful Api
api = Api(app)


@app.route('/')
def index():
    return '<h1>Code Challenge</h1>'


# RESTful resource for managing Restaurants
class RestaurantsResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict() for restaurant in restaurants], 200

    def post(self):
        data = request.get_json()
        try:
            new_restaurant = Restaurant(
                name=data.get('name'),
                address=data.get('address')
            )
            db.session.add(new_restaurant)
            db.session.commit()
            return new_restaurant.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


# RESTful resource for managing individual Restaurant
class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get_or_404(id)
        return restaurant.to_dict(), 200

    def delete(self, id):
        restaurant = Restaurant.query.get_or_404(id)
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204


# RESTful resource for managing Pizzas
class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict() for pizza in pizzas], 200

    def post(self):
        data = request.get_json()
        try:
            new_pizza = Pizza(
                name=data.get('name'),
                ingredients=data.get('ingredients')
            )
            db.session.add(new_pizza)
            db.session.commit()
            return new_pizza.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


# RESTful resource for managing RestaurantPizza (join table)
class RestaurantPizzasResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_restaurant_pizza = RestaurantPizza(
                restaurant_id=data.get('restaurant_id'),
                pizza_id=data.get('pizza_id'),
                price=data.get('price')
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return new_restaurant_pizza.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


# RESTful resource for individual RestaurantPizza
class RestaurantPizzaResource(Resource):
    def get(self, id):
        restaurant_pizza = RestaurantPizza.query.get_or_404(id)
        return restaurant_pizza.to_dict(), 200


# Registering resources to the API
api.add_resource(RestaurantsResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzasResource, '/pizzas')
api.add_resource(RestaurantPizzasResource, '/restaurant_pizzas')
api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
