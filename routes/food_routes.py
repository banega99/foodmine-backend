from flask import Blueprint, request, jsonify
from data import sample_foods, sample_tags
from models.food_model import Food
from extensions.database import db
import sys
print(sys.path)

food_routes = Blueprint('food_routes', __name__)


@food_routes.route("/seed", methods=["GET"])
def seed():
    foods_count = Food.query.count()
    if foods_count > 0:
        return "Seed is already done!", 200
    for food in sample_foods:
        new_food = Food(
            name=food["name"],
            price=food["price"],
            tags=food["tags"],
            favorite=food["favorite"],
            stars=food["stars"],
            imageUrl=food["imageUrl"],
            origins=food["origins"],
            cookTime=food["cookTime"]
        )
        db.session.add(new_food)
    db.session.commit()
    return "Seed is done!", 200


@food_routes.route("/food", methods=["GET"])
def get_all_food():
    all_food = db.session.execute(db.select(Food).order_by(Food.id)).scalars().all()
    return jsonify([food.as_dict() for food in all_food])


@food_routes.route("/food/<food_name>", methods=["GET"])
def get_food_by_name(food_name):
    if food_name == '':
        return jsonify([])
    else:
        name_regex = f'%{food_name}%'
        foods = Food.query.filter(Food.name.like(name_regex)).all()
        return jsonify([food.as_dict() for food in foods])


@food_routes.route("/search/<search_term>", methods=["GET"])
def get_food_by_search_term(search_term):
    name_regex = f'%{search_term}%'
    foods = Food.query.filter(Food.name.like(name_regex)).all()
    return jsonify([food.as_dict() for food in foods])


@food_routes.route('/tags', methods=['GET'])
def get_tags():
    tags = db.session.query(Food.tags, db.func.count(Food.id)).group_by(Food.tags).all()
    tags = [{"name": tag, "count": count} for tag, count in tags]
    all_tags = {"name": "All", "count": Food.query.count()}
    tags.insert(0, all_tags)
    return jsonify(sample_tags)


@food_routes.route('/tags/<tag_name>', methods=['GET'])
def get_foods_by_tag(tag_name):
    print(tag_name)

    # Fetch all Food records
    foods = Food.query.all()

    # Filter foods in Python to match the tag
    filtered_foods = [food for food in foods if tag_name in food.tags]

    # Print the filtered foods for debugging
    print(filtered_foods)

    # Convert filtered foods to dictionary format for JSON response
    return jsonify([food.as_dict() for food in filtered_foods])


@food_routes.route('/food/<int:food_id>', methods=['GET'])
def get_food_by_id(food_id):
    food = Food.query.get_or_404(food_id)
    return jsonify(food.as_dict())
