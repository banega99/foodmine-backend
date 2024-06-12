from flask import Blueprint, request, jsonify
from models.order_model import Order, db, OrderItem, LatLng
from middlewares.auth import auth_middleware
from constants import HTTP_BAD_REQUEST, OrderStatus
from models.user_model import User
from datetime import datetime
from models.food_model import Food

order_routes = Blueprint('order_routes', __name__)


@order_routes.route('/orders/create', methods=['POST'])
@auth_middleware
def create_order():
    request_order = request.get_json()
    if len(request_order.get('items', [])) <= 0:
        return jsonify({"msg": "Cart is Empty!"}), 400

    user_id = request_order['userId']
    print(user_id)
    # Ensure address_latlng is created first
    address_latlng = LatLng(
        lat=request_order['addressLatLng']['lat'],
        lng=request_order['addressLatLng']['lng']
    )
    db.session.add(address_latlng)
    db.session.flush()  # Flush to get the id of address_latlng

    new_order = Order(
        name=request_order['name'],
        address=request_order['address'],
        address_latlng_id=address_latlng.id,
        total_price=request_order['total_price'],
        status=OrderStatus.NEW.value,
        user_id=user_id,
        user=User.query.filter_by(id=user_id).first(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_order)
    db.session.flush()  # Flush to get the id of new_order

    for item in request_order['items']:
        print(item)
        order_item = OrderItem(
            food_id=item['food']['id'],
            food=Food.query.filter_by(id=item['food']['id']).first(),
            price=item['price'],
            quantity=item['quantity'],
            order_id=new_order.id
        )
        print(order_item.as_dict())
        db.session.add(order_item)

    db.session.commit()

    return jsonify({'message': 'Successfully created order!'}), 200


@order_routes.route('/orders/newOrderForCurrentUser/<user_id>', methods=['GET'])
@auth_middleware
def new_order_for_current_user(user_id):
    order = get_new_order_for_current_user(user_id)
    if order:
        return jsonify(order.as_dict())
    else:
        return jsonify({}), HTTP_BAD_REQUEST


@order_routes.route('/orders/pay', methods=['POST'])
@auth_middleware
def pay_order():
    print(request.get_json())
    user_id = request.get_json()['user_id']
    payment_id = request.get_json()['payment_id']
    order = get_new_order_for_current_user(user_id)
    if not order:
        return jsonify({"msg": "Order Not Found!"}), HTTP_BAD_REQUEST

    order.payment_id = payment_id
    order.status = OrderStatus.PAYED.value
    db.session.commit()

    return jsonify({"id": order.id})


@order_routes.route('/orders/user/<int:id>', methods=['GET'])
@auth_middleware
def get_user_orders(id):
    orders = Order.query.filter_by(user_id=id, status="PAYED").all()
    return jsonify([order.as_dict() for order in orders])


@order_routes.route('/orders/track/<int:id>', methods=['GET'])
@auth_middleware
def track_order(id):
    order = Order.query.get(id)
    return jsonify(order.as_dict() if order else {})


def get_new_order_for_current_user(user_id):
    return Order.query.filter_by(user_id=user_id, status=OrderStatus.NEW.value).first()
