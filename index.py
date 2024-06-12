from flask import Flask, Blueprint
from config import Config
from extensions.database import db
from routes.food_routes import food_routes
from routes.user_routes import user_routes
from routes.order_routes import order_routes
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from sqlalchemy import text


# Create a main blueprint to aggregate all route blueprints
main = Blueprint('main', __name__)

# Register all route blueprints under the main blueprint
main.register_blueprint(food_routes)
main.register_blueprint(user_routes)
main.register_blueprint(order_routes)

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
# db = MongoEngine(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

with app.app_context():
    # db.drop_all()
    db.create_all()

app.register_blueprint(main)


if __name__ == '__main__':
    app.run(debug=True)
