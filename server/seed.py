#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

# Create an application context to work with the database
with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    # Create restaurants
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='123 Pizza Street')
    bistro = Restaurant(name="Sanjay's Pizza Bistro", address='456 Pizza Avenue')
    palace = Restaurant(name="Kiki's Pizza Palace", address='789 Pizza Boulevard')
    restaurants = [shack, bistro, palace]

    # Add restaurants to session
    db.session.add_all(restaurants)

    # Create pizzas
    print("Creating pizzas...")
    cheese = Pizza(name="Cheese Pizza", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Pepperoni Pizza", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="California Pizza", ingredients="Dough, Sauce, Ricotta, Red Peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    # Add pizzas to session
    db.session.add_all(pizzas)

    # Create restaurant-pizza relationships
    print("Creating RestaurantPizza...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=10)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=12)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=15)
    restaurant_pizzas = [pr1, pr2, pr3]

    # Add restaurant-pizzas to session
    db.session.add_all(restaurant_pizzas)

    # Commit everything to the database
    db.session.commit()

    print("Seeding done!")
