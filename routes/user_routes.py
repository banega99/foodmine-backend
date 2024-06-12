from flask import Blueprint, jsonify, request
from models.user_model import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from extensions.database import db
from datetime import datetime

user_routes = Blueprint('user_routes', __name__)


@user_routes.route("/users/seed", methods=["GET"])
def seed_users():
    if User.query.count() > 1:
        return "Seed is already done!", 200
    sample_users = [
        {"name": "John Doe", "email": "john@example.com", "password": generate_password_hash("1234"),
         "address": "123 Main St", "isAdmin": False},
        {"name": "Jane Doe", "email": "jane@example.com", "password": generate_password_hash("5678"),
         "address": "456 Elm St", "isAdmin": True}
    ]
    for user in sample_users:
        new_user = User(
            name=user['name'],
            email=user['email'],
            password=user['password'],
            address=user['address'],
            isAdmin=user['isAdmin'],
            createdAt=datetime.utcnow()
        )
        db.session.add(new_user)
    db.session.commit()
    return "Seed is done!", 200


@user_routes.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter(User.email.like(email)).first_or_404()
    print(user)
    if user and check_password_hash(user.password, password):
        return generate_token_response(user)
    return jsonify({"error": "Email or password is not valid"}), 400


@user_routes.route("/users/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email').lower()
    password = data.get('password')
    address = data.get('address')

    if User.query.filter(User.email.like(email)).first():
        return jsonify({"error": "User already exists, please login!"}), 400

    encrypted_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=encrypted_password, address=address)
    db.session.add(new_user)
    db.session.commit()
    return generate_token_response(new_user)


@user_routes.route("/users/profile/<id>", methods=["GET"])
@jwt_required()
def get_profile(id):
    user = User.query.filter(User.id.like(id)).first_or_404()
    return jsonify(user.as_dict())


def generate_token_response(user):
    token = create_access_token(identity=str(user.id), expires_delta=False)
    return jsonify({
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "address": user.address,
        "isAdmin": user.isAdmin,
        "token": token
    })
